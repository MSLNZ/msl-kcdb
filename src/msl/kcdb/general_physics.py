"""Search the General Physics database."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .kcdb import KCDB, check_page_info, to_countries, to_label, to_physics_code
from .types import Branch, Domain, IndividualService, ResultsPhysics, Service, Status, SubService

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date

    from .types import Country, MetrologyArea


class Physics(KCDB):
    """General Physics class."""

    DOMAIN: Domain = Domain(code="PHYSICS", name="General physics")
    """The General Physics domain."""

    def branches(self, metrology_area: MetrologyArea) -> list[Branch]:
        """Return all General Physics branches for the specified metrology area.

        Args:
            metrology_area: The metrology area to return the branches for.

        Returns:
            A list of [Branch][msl.kcdb.types.Branch]es.
        """
        if metrology_area.label in ["QM", "RI"]:
            # ignore CHEM-BIO and RADIATION
            return []

        response = self.get(
            f"{KCDB.BASE_URL}/referenceData/branch",
            params={"areaId": metrology_area.id},
        )
        response.raise_for_status()
        return [Branch(metrology_area=metrology_area, **data) for data in response.json()["referenceData"]]

    def individual_services(self, sub_service: SubService) -> list[IndividualService]:
        """Return all General Physics individual services for the specified sub service.

        Args:
            sub_service: The sub service to return the individual services for.

        Returns:
            A list of [IndividualService][msl.kcdb.types.IndividualService]s.
        """
        response = self.get(
            f"{KCDB.BASE_URL}/referenceData/individualService",
            params={"subServiceId": sub_service.id},
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

    def search(  # noqa: C901, PLR0913
        self,
        metrology_area: str | MetrologyArea,
        *,
        branch: str | Branch | None = None,
        countries: str | Country | Iterable[str | Country] | None = None,
        individual_service: str | IndividualService | None = None,
        keywords: str | None = None,
        page: int = 0,
        page_size: int = 100,
        physics_code: str | Service | SubService | IndividualService | None = None,
        public_date_from: str | date | None = None,
        public_date_to: str | date | None = None,
        service: str | Service | None = None,
        show_table: bool = False,
        status: str | Status | None = None,
        sub_service: str | SubService | None = None,
    ) -> ResultsPhysics:
        """Perform a General Physics search.

        Args:
            metrology_area: Metrology area label. _Example:_ `"EM"`
            branch: Branch label. _Example:_ `"EM/RF"`
            countries: Country label(s). _Example:_ `["CH", "FR", "JP"]`
            individual_service: KCDB individual service label. _Example:_ `"1"`
            keywords: Search keywords in elasticsearch format. _Example:_ `"phase OR multichannel OR water"`
            page: Page number requested (0 means first page).
            page_size: Maximum number of elements in a page (maximum value is 10000).
            physics_code: Physics code is composed of `Service.label`, `SubService.label` (if requested)
                and `IndividualService.label` (if requested) separated by dots. _Example:_ `"11.3.3"`
            public_date_from: Minimal publication date. _Example:_ `"2005-01-31"`
            public_date_to: Maximal publication date. _Example:_ `"2020-06-30"`
            service: KCDB service label. _Example:_ `"3"`
            show_table: Set to `True` to return table data.
            status: CMC status.
            sub_service: KCDB sub-service label. _Example:_ `"1"`

        Returns:
            The CMC results for General Physics.
        """
        check_page_info(page, page_size)

        request: dict[str, bool | int | str | list[str]] = {
            "page": page,
            "pageSize": page_size,
            "showTable": show_table,
        }

        request["metrologyAreaLabel"] = to_label(metrology_area)

        if branch:
            request["branchLabel"] = to_label(branch)

        if countries:
            request["countries"] = to_countries(countries)

        if individual_service:
            request["individualServiceLabel"] = to_label(individual_service)

        if keywords:
            request["keywords"] = keywords

        if physics_code:
            request["physicsCode"] = to_physics_code(physics_code)

        if public_date_from:
            request["publicDateFrom"] = str(public_date_from)

        if public_date_to:
            request["publicDateTo"] = str(public_date_to)

        if service:
            request["serviceLabel"] = to_label(service)

        if status:
            request["status"] = status.value if isinstance(status, Status) else status

        if sub_service:
            request["subServiceLabel"] = to_label(sub_service)

        response = self.post(
            f"{KCDB.BASE_URL}/cmc/searchData/physics",
            json=request,
        )
        response.raise_for_status()
        return ResultsPhysics(response.json())

    def services(self, branch: Branch) -> list[Service]:
        """Return all General Physics services for the specified branch.

        Args:
            branch: The branch to return the services for.

        Returns:
            A list of [Service][msl.kcdb.types.Service]s.
        """
        if branch.id in [32, 33, 34]:
            # Dosimetry(id=32), Radioactivity(id=33) and Neutron Measurements(id=34) do not have Services
            return []

        response = self.get(
            f"{KCDB.BASE_URL}/referenceData/service",
            params={"branchId": branch.id},
        )
        response.raise_for_status()
        return [Service(branch=branch, physics_code=data["label"], **data) for data in response.json()["referenceData"]]

    def sub_services(self, service: Service) -> list[SubService]:
        """Return all General Physics sub services for the specified service.

        Args:
            service: The service to return the sub services for.

        Returns:
            A list of [SubService][msl.kcdb.types.SubService]s.
        """
        response = self.get(
            f"{KCDB.BASE_URL}/referenceData/subService",
            params={"serviceId": service.id},
        )
        response.raise_for_status()
        return [
            SubService(service=service, physics_code=f"{service.physics_code}.{data['label']}", **data)
            for data in response.json()["referenceData"]
        ]
