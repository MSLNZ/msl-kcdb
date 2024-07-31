"""Wrapper around the KCDB API to recover reference data for CMC queries."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, TypeVar

import requests

from .classes import (
    Analyte,
    Branch,
    Category,
    Country,
    Domain,
    IndividualService,
    Medium,
    MetrologyArea,
    Nuclide,
    Quantity,
    RefData,
    Service,
    Source,
    SubService,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

T = TypeVar("T", bound=RefData)

KCDB_BASE_URL = "https://www.bipm.org/api/kcdb"


class ReferenceData:
    """Helper class that contains `staticmethod`s to recover reference data for CMC queries."""

    TIMEOUT: float = 10.0
    """The maximum number of seconds to wait for a response from the KCDB server."""

    @staticmethod
    def analytes() -> list[Analyte]:
        """Return all analytes for the `CHEM-BIO` [Domain](/api/classes/#src.kcdb.classes.Domain)."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/analyte", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Analyte(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def branches(metrology_area: MetrologyArea) -> list[Branch]:
        """Return all branches for the specified [MetrologyArea](/api/classes/#src.kcdb.classes.MetrologyArea)."""
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
        """Return all categories for the `CHEM-BIO` [Domain](/api/classes/#src.kcdb.classes.Domain)."""
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

        Args:
            ref_data: An iterable of reference data.
            pattern: A regular-expression pattern to use to filter results.
                Uses the `label` and `value` attributes of each item in `ref_data` to perform the filtering.
            flags: Pattern flags passed to [re.compile]().

        Returns:
            The filtered reference data.
        """
        regex = re.compile(pattern, flags=flags)
        return [item for item in ref_data if regex.search(item.value) or regex.search(item.label)]

    @staticmethod
    def find(ref_data: Iterable[T], id: int) -> T:  # noqa: A002
        """Find the item in the reference data based on an id search.

        Args:
            ref_data: An iterable of reference data.
            id: The id in `ref_data` to find.

        Raises:
            ValueError: If the `id` cannot be found.

        Returns:
            The item with the specified `id`.
        """
        for item in ref_data:
            if item.id == id:
                return item

        msg = f"ID {id} cannot be found"
        raise ValueError(msg)

    @staticmethod
    def individual_services(sub_service: SubService) -> list[IndividualService]:
        """Return all individual-services for the specified [SubService](/api/classes/#src.kcdb.classes.SubService)."""
        response = requests.get(
            f"{KCDB_BASE_URL}/referenceData/individualService",
            params={"subServiceId": sub_service.id},
            timeout=ReferenceData.TIMEOUT,
        )
        if response.ok:
            return [
                IndividualService(
                    sub_service=sub_service,
                    physics_code=f"{sub_service.physics_code}.{data['label']}",
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
        """Return all metrology areas for the specified [Domain](/api/classes/#src.kcdb.classes.Domain)."""
        response = requests.get(
            f"{KCDB_BASE_URL}/referenceData/metrologyArea",
            params={"domainCode": domain.code},
            timeout=ReferenceData.TIMEOUT,
        )
        response.raise_for_status()
        return [MetrologyArea(domain=domain, **data) for data in response.json()["referenceData"]]

    @staticmethod
    def nuclides() -> list[Nuclide]:
        """Return all nuclides for the `RADIATION` [Domain](/api/classes/#src.kcdb.classes.Domain)."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/nuclide", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Nuclide(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def quantities(branch: Branch) -> list[Quantity]:
        """Return all quantities for the specified `RADIATION` [Branch](/api/classes/#src.kcdb.classes.Branch)."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/quantity", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        quantities = [data for data in response.json()["referenceData"] if data["label"]]
        if branch.label == "DOS":
            return [Quantity(**q) for q in quantities if q["id"] < 32]  # noqa: PLR2004
        if branch.label == "NEU":
            return [Quantity(**q) for q in quantities if q["id"] >= 47]  # noqa: PLR2004
        if branch.label == "RAD":
            return [Quantity(**q) for q in quantities if 32 <= q["id"] < 47]  # noqa: PLR2004
        return []

    @staticmethod
    def radiation_mediums() -> list[Medium]:
        """Return all radiation mediums for the `RADIATION` [Domain](/api/classes/#src.kcdb.classes.Domain)."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/radiationMedium", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Medium(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def radiation_sources() -> list[Source]:
        """Return all radiation sources for the `RADIATION` [Domain](/api/classes/#src.kcdb.classes.Domain)."""
        response = requests.get(f"{KCDB_BASE_URL}/referenceData/radiationSource", timeout=ReferenceData.TIMEOUT)
        response.raise_for_status()
        return [Source(**data) for data in response.json()["referenceData"]]

    @staticmethod
    def services(branch: Branch) -> list[Service]:
        """Return all services for the specified [Branch](/api/classes/#src.kcdb.classes.Branch)."""
        response = requests.get(
            f"{KCDB_BASE_URL}/referenceData/service",
            params={"branchId": branch.id},
            timeout=ReferenceData.TIMEOUT,
        )
        if response.ok:
            return [
                Service(branch=branch, physics_code=data["label"], **data) for data in response.json()["referenceData"]
            ]

        # Dosimetry(id=32), Radioactivity(id=33) and Neutron Measurements(id=34) do not have Services
        # HTTP error 404 is returned from the API
        assert branch.id in [32, 33, 34]  # noqa: S101
        return []

    @staticmethod
    def sub_services(service: Service) -> list[SubService]:
        """Return all sub-services for the specified [Service](/api/classes/#src.kcdb.classes.Service)."""
        response = requests.get(
            f"{KCDB_BASE_URL}/referenceData/subService",
            params={"serviceId": service.id},
            timeout=ReferenceData.TIMEOUT,
        )
        response.raise_for_status()
        return [
            SubService(service=service, physics_code=f"{service.physics_code}.{data['label']}", **data)
            for data in response.json()["referenceData"]
        ]
