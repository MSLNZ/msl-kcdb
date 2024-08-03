"""Search the General Physics database."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from .classes import KCDB, Branch, Domain, IndividualService, ResultsGeneralPhysics, Service, SubService

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date

    from .classes import Country, MetrologyArea


class GeneralPhysics(KCDB):
    """General Physics class."""

    DOMAIN = Domain(code="PHYSICS", name="General physics")
    """The General Physics domain."""

    def branches(self, metrology_area: MetrologyArea) -> list[Branch]:
        """Return all General Physics branches for the specified metrology area.

        Args:
            metrology_area: The metrology area to return the branches for.

        Returns:
            A list of [Branch][msl.kcdb.classes.Branch]es.
        """
        if metrology_area.label in ["QM", "RI"]:
            # ignore CHEM-BIO and RADIATION
            return []

        response = requests.get(
            f"{KCDB.BASE_URL}/referenceData/branch",
            params={"areaId": metrology_area.id},
            timeout=self._timeout,
        )
        response.raise_for_status()
        return [Branch(metrology_area=metrology_area, **data) for data in response.json()["referenceData"]]

    def individual_services(self, sub_service: SubService) -> list[IndividualService]:
        """Return all General Physics individual services for the specified subservice.

        Args:
            sub_service: The subservice to return the individual services for.

        Returns:
            A list of [IndividualService][msl.kcdb.classes.IndividualService]s.
        """
        response = requests.get(
            f"{KCDB.BASE_URL}/referenceData/individualService",
            params={"subServiceId": sub_service.id},
            timeout=self._timeout,
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

        # When this method was written, "Not attributed 1" and "Fibre Polarization mode dispersion (inactive)"
        # did not have Individual Services and HTTP error 404 was returned from the API
        assert sub_service.id in [104, 151]  # noqa: S101
        return []

    def search(  # noqa: PLR0913
        self,
        metrology_area: str | MetrologyArea,
        *,
        branch: str | Branch | None = None,
        countries: str | Country | Iterable[str | Country] | None = None,
        keywords: str | None = None,
        page: int = 0,
        page_size: int = 100,
        physics_code: str | Service | SubService | IndividualService | None = None,
        public_date_from: str | date | None = None,
        public_date_to: str | date | None = None,
        show_table: bool = False,
    ) -> ResultsGeneralPhysics:
        """Perform a General Physics search.

        Args:
            metrology_area: Metrology Area label (example: `"EM"`).
            branch: Branch label (example: `"EM/RF"`).
            countries: Country label(s) (example: `["CH", "FR", "JP"]`).
            keywords: Search keywords in elasticsearch format (example: `"phase OR multichannel OR water"`).
            page: Page number requested (0 means first page).
            page_size: Maximum number of elements in a page (maximum value is 10000).
            physics_code: Physics code is composed of `Service.label`, `SubService.label` (if requested)
                and `IndividualService.label` (if requested) separated by dots (example: `"11.3.3"`).
            public_date_from: Minimal publication date (example: `"2005-01-31"`).
            public_date_to: Maximal publication date (example: `"2020-06-30"`).
            show_table: Set to `True` to return table data.

        Returns:
            The CMC results for General Physics.
        """
        self._check_page_info(page, page_size)

        request: dict[str, bool | int | str | list[str]] = {
            "page": page,
            "pageSize": page_size,
            "showTable": show_table,
        }

        request["metrologyAreaLabel"] = self._to_label(metrology_area)

        if branch:
            request["branchLabel"] = self._to_label(branch)

        if countries:
            request["countries"] = self._to_countries(countries)

        if keywords:
            request["keywords"] = keywords

        if physics_code:
            if isinstance(physics_code, str):
                request["physicsCode"] = physics_code
            else:
                request["physicsCode"] = physics_code.physics_code

        if public_date_from:
            request["publicDateFrom"] = str(public_date_from)

        if public_date_to:
            request["publicDateTo"] = str(public_date_to)

        response = requests.post(
            f"{KCDB.BASE_URL}/cmc/searchData/physics",
            json=request,
            timeout=self._timeout,
        )
        response.raise_for_status()
        return ResultsGeneralPhysics(response.json())

    def services(self, branch: Branch) -> list[Service]:
        """Return all General Physics services for the specified branch.

        Args:
            branch: The branch to return the services for.

        Returns:
            A list of [Service][msl.kcdb.classes.Service]s.
        """
        if branch.id in [32, 33, 34]:
            # Dosimetry(id=32), Radioactivity(id=33) and Neutron Measurements(id=34) do not have Services
            return []

        response = requests.get(
            f"{KCDB.BASE_URL}/referenceData/service",
            params={"branchId": branch.id},
            timeout=self._timeout,
        )
        response.raise_for_status()
        return [Service(branch=branch, physics_code=data["label"], **data) for data in response.json()["referenceData"]]

    def sub_services(self, service: Service) -> list[SubService]:
        """Return all General Physics subservices for the specified service.

        Args:
            service: The service to return the subservices for.

        Returns:
            A list of [SubService][msl.kcdb.classes.SubService]s.
        """
        response = requests.get(
            f"{KCDB.BASE_URL}/referenceData/subService",
            params={"serviceId": service.id},
            timeout=self._timeout,
        )
        response.raise_for_status()
        return [
            SubService(service=service, physics_code=f"{service.physics_code}.{data['label']}", **data)
            for data in response.json()["referenceData"]
        ]