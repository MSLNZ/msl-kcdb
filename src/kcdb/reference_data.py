"""Wrapper around the API to recover reference data for CMC queries."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

import requests

if TYPE_CHECKING:
    from collections.abc import Iterable

KCDB_BASE_URL = "https://www.bipm.org/api/kcdb"


@dataclass(frozen=True, kw_only=True)
class Domain:
    """One of General Physics, Chemistry and Biology or Ionizing Radition."""

    code: str
    name: str


@dataclass(frozen=True, kw_only=True)
class RefData:
    """Base class for reference data."""

    id: int
    label: str
    value: str


class Analyte(RefData):
    """An Analyte for the CHEM-BIO :class:`.Domain`."""


class Category(RefData):
    """A Category for the CHEM-BIO :class:`.Domain`."""


class Country(RefData):
    """Information about a country."""


class Nuclide(RefData):
    """A Nuclide for the RADIATION :class:`.Domain`."""


class Medium(RefData):
    """A Medium for the RADIATION :class:`.Domain`."""


class Quantity(RefData):
    """A Quantity for the RADIATION :class:`.Domain`."""


class Source(RefData):
    """A Source for the RADIATION :class:`.Domain`."""


@dataclass(frozen=True, kw_only=True)
class MetrologyArea(RefData):
    """A Metrology Area of a :class:`.Domain`."""

    domain: Domain


@dataclass(frozen=True, kw_only=True)
class Branch(RefData):
    """A Branch of a :class:`.MetrologyArea`."""

    metrology_area: MetrologyArea


@dataclass(frozen=True, kw_only=True)
class Service(RefData):
    """A Service for a :class:`.Branch`."""

    branch: Branch
    physics_code: str


@dataclass(frozen=True, kw_only=True)
class SubService(RefData):
    """A Sub-Service of a :class:`.Service`."""

    physics_code: str
    service: Service


@dataclass(frozen=True, kw_only=True)
class IndividualService(RefData):
    """An Individual Service of a :class:`.SubService`."""

    physics_code: str
    sub_service: SubService


T = TypeVar("T", bound=RefData)


class ReferenceData:
    """Static Reference-Data API functions to perform CMC search queries."""

    TIMEOUT: float = 10.0

    @staticmethod
    def analytes() -> list[Analyte]:
        """Return a list of all analytes."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/analyte", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Analyte(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def branches(metrology_area: MetrologyArea) -> list[Branch]:
        """Return all branches for the specified :class:`.MetrologyArea`."""
        response = requests.get(
            f"{KCDB_BASE_URL}/referenceData/branch",
            params={"areaId": metrology_area.id},
            timeout=ReferenceData.TIMEOUT,
        )
        if response.ok:
            return [Branch(metrology_area=metrology_area, **data) for data in response.json()["referenceData"]]

        # "Chemistry and Biology" does not have branches
        # HTTP error 404 is returned from the API
        assert metrology_area.id in [8]  # noqa: S101
        return []

    @staticmethod
    def categories() -> list[Category]:
        """Return all categories for the CHEM-BIO :class:`.Domain`."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/category", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Category(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def countries() -> list[Country]:
        """Return all countries."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/country", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Country(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def domains() -> list[Domain]:
        """Return all domains."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/domain", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Domain(**data) for data in response.json()["domains"]]

    @staticmethod
    def filter(ref_data: Iterable[T], pattern: str, *, flags: int = 0) -> list[T]:
        """Filter the reference data based on a string search.

        :param ref_data: An iterable of reference data.
        :param pattern: A regular-expression pattern to use to filter results.
            Uses the `label` and `value` attributes of each item in `ref_data` to perform the filtering.
        :param flags: Pattern flags passed to :func:`re.compile` [default: 0].

        :return: The filtered reference data.
        """
        regex = re.compile(pattern, flags=flags)
        return [item for item in ref_data if regex.search(item.value) or regex.search(item.label)]

    @staticmethod
    def find(ref_data: Iterable[T], id: int) -> T:  # noqa: A002
        """Find the item in the reference data based on an id search.

        :param ref_data: An iterable of reference data.
        :param id: The id in `ref_data` to find.

        :raises ValueError: If the `id` cannot be found.

        :return: The item with the specified `id`.
        """
        for item in ref_data:
            if item.id == id:
                return item

        msg = f"ID {id} cannot be found"
        raise ValueError(msg)

    @staticmethod
    def individual_services(sub_service: SubService) -> list[IndividualService]:
        """Return all Individual Services for the specified :class:`.SubService`."""
        response = requests.get(
            f"{KCDB_BASE_URL}/referenceData/individualService",
            params={"subServiceId": sub_service.id},
            timeout=ReferenceData.TIMEOUT,
        )
        if response.ok:
            return [
                IndividualService(
                    sub_service=sub_service,
                    physics_code=f"{sub_service.physics_code}.{data['id']}",
                    **data,
                )
                for data in response.json()["referenceData"]
            ]

        # "Not attributed 1" and "Fibre Polarization mode dispersion (inactive)" do not have Individual Services
        # HTTP error 404 is returned from the API
        assert sub_service.id in [104, 151]  # noqa: S101
        return []

    @staticmethod
    def metrology_areas(domain: Domain) -> list[MetrologyArea]:
        """Return all metrology areas for the specified domain."""
        response = requests.get(
            f"{KCDB_BASE_URL}/referenceData/metrologyArea",
            params={"domainCode": domain.code},
            timeout=ReferenceData.TIMEOUT,
        )
        response.raise_for_status()
        return [MetrologyArea(domain=domain, **data) for data in response.json()["referenceData"]]

    @staticmethod
    def nuclides() -> list[Nuclide]:
        """Return a list of all nuclides for the RADIATION :class:`.Domain`."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/nuclide", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Nuclide(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def quantities() -> list[Quantity]:
        """Return a list of all quantities for the RADIATION :class:`.Domain`."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/quantity", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        out = []
        for data in response.json()["referenceData"]:
            if data["label"] is None:
                data["label"] = ""
            out.append(Quantity(**data))
        return out

    @staticmethod
    def radiation_mediums() -> list[Medium]:
        """Return a list of all radiation mediums for the RADIATION :class:`.Domain`."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/radiationMedium", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Medium(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def radiation_sources() -> list[Source]:
        """Return a list of all Radiation Sources for the RADIATION :class:`.Domain`."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/radiationSource", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Source(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def services(branch: Branch) -> list[Service]:
        """Return all Services for the specified :class:`.Branch`."""
        response = requests.get(
            f"{KCDB_BASE_URL}/referenceData/service",
            params={"branchId": branch.id},
            timeout=ReferenceData.TIMEOUT,
        )
        if response.ok:
            return [
                Service(branch=branch, physics_code=f"{data['id']}", **data)
                for data in response.json()["referenceData"]
            ]

        # Dosimetry(id=32), Radioactivity(id=33) and Neutron Measurements(id=34) do not have Services
        # HTTP error 404 is returned from the API
        assert branch.id in [32, 33, 34]  # noqa: S101
        return []

    @staticmethod
    def sub_services(service: Service) -> list[SubService]:
        """Return all Sub Services for the specified :class:`.Service`."""
        response = requests.get(
            f"{KCDB_BASE_URL}/referenceData/subService",
            params={"serviceId": service.id},
            timeout=ReferenceData.TIMEOUT,
        )
        response.raise_for_status()
        return [
            SubService(service=service, physics_code=f"{service.physics_code}.{data['id']}", **data)
            for data in response.json()["referenceData"]
        ]
