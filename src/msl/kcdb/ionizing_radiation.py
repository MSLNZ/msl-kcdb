"""Search the Ionizing Radiation database."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from .classes import KCDB, Branch, Domain, Medium, Nuclide, Quantity, ResultsIonizingRadiation, Source

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date

    from .classes import Country, MetrologyArea


class IonizingRadiation(KCDB):
    """Ionizing Radiation class."""

    DOMAIN = Domain(code="RADIATION", name="Ionizing radiation")
    """The Ionizing Radiation domain."""

    def branches(self, metrology_area: MetrologyArea) -> list[Branch]:
        """Return all Ionizing Radiation branches for the specified metrology area.

        Args:
            metrology_area: The metrology area to return the branches for.

        Returns:
            A list of [Branch][msl.kcdb.classes.Branch]es.
        """
        if metrology_area.id < 9:  # noqa: PLR2004
            # ignore PHYSICS and CHEM-BIO
            return []

        response = requests.get(
            f"{KCDB.BASE_URL}/referenceData/branch",
            params={"areaId": metrology_area.id},
            timeout=self._timeout,
        )
        response.raise_for_status()
        return [Branch(metrology_area=metrology_area, **data) for data in response.json()["referenceData"]]

    def mediums(self, branch: Branch) -> list[Medium]:
        """Return all Ionizing Radiation mediums for the specified branch.

        Args:
            branch: The branch to return the mediums for.

        Returns:
            A list of [Medium][msl.kcdb.classes.Medium]s.
        """
        # The /radiationMedium endpoint does not accept parameters, so we need to filter the mediums
        # based on the Branch that is specified
        if branch.label not in ["RAD", "DOS", "NEU"]:
            return []

        response = requests.get(f"{KCDB.BASE_URL}/referenceData/radiationMedium", timeout=self._timeout)
        response.raise_for_status()
        data = response.json()["referenceData"]

        if branch.label == "RAD":
            return [Medium(branch=branch, **d) for d in data if d["id"] < 17]  # noqa: PLR2004
        if branch.label == "DOS":
            return [Medium(branch=branch, **d) for d in data if 17 <= d["id"] < 24]  # noqa: PLR2004
        return [Medium(branch=branch, **d) for d in data if d["id"] >= 24]  # noqa: PLR2004

    def nuclides(self) -> list[Nuclide]:
        """Return all Ionizing Radiation nuclides.

        Returns:
            A list of [Nuclide][msl.kcdb.classes.Nuclide]s.
        """
        response = requests.get(f"{KCDB.BASE_URL}/referenceData/nuclide", timeout=self._timeout)
        response.raise_for_status()
        return [Nuclide(**data) for data in response.json()["referenceData"]]

    def quantities(self, branch: Branch) -> list[Quantity]:
        """Return all Ionizing Radiation quantities for the specified branch.

        Args:
            branch: The branch to return the quantities for.

        Returns:
            A list of [Quantity][msl.kcdb.classes.Quantity]'s.
        """
        # The /quantity endpoint does not accept parameters, so we need to filter the quantities
        # based on the Branch that is specified. There are many more quantities after id=78, but
        # these all have "label": null, so we ignore these additional quantities here and
        # provide them in KCDB.non_ionizing_quantities()
        if branch.label not in ["RAD", "DOS", "NEU"]:
            return []

        response = requests.get(f"{KCDB.BASE_URL}/referenceData/quantity", timeout=self._timeout)
        response.raise_for_status()
        data = response.json()["referenceData"]

        if branch.label == "DOS":
            return [Quantity(branch=branch, **d) for d in data if d["id"] < 32]  # noqa: PLR2004
        if branch.label == "RAD":
            return [Quantity(branch=branch, **d) for d in data if 32 <= d["id"] < 47]  # noqa: PLR2004
        return [Quantity(branch=branch, **d) for d in data if 47 <= d["id"] < 78]  # noqa: PLR2004

    def search(  # noqa: PLR0913
        self,
        *,
        branch: str | Branch | None = None,
        countries: str | Country | Iterable[str | Country] | None = None,
        keywords: str | None = None,
        medium: str | Medium | None = None,
        metrology_area: str | MetrologyArea = "RI",
        nuclide: str | Nuclide | None = None,
        page: int = 0,
        page_size: int = 100,
        public_date_from: str | date | None = None,
        public_date_to: str | date | None = None,
        quantity: str | Quantity | None = None,
        show_table: bool = False,
        source: str | Source | None = None,
    ) -> ResultsIonizingRadiation:
        """Perform an Ionizing Radiation search.

        Args:
            branch: Branch label. _Example:_ `"RAD"`
            countries: Country label(s). _Example:_ `["CH", "FR", "JP"]`
            keywords: Search keywords in elasticsearch format. _Example:_ `"phase OR multichannel OR water"`
            medium: Medium label. _Example:_ `"3"`
            metrology_area: Metrology area label. _Example:_ `"RI"`
            nuclide: Nuclide label. _Example:_ `"Co-60"`
            page: Page number requested (0 means first page).
            page_size: Maximum number of elements in a page (maximum value is 10000).
            public_date_from: Minimal publication date. _Example:_ `"2005-01-31"`
            public_date_to: Maximal publication date. _Example:_ `"2020-06-30"`
            quantity: Quantity label. _Example:_ `"1"`
            show_table: Set to `True` to return table data.
            source: Source label. _Example:_ `"2"`

        Returns:
            The CMC results for Ionizing Radiation.
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

        if medium:
            request["mediumLabel"] = self._to_label(medium)

        if nuclide:
            request["nuclideLabel"] = self._to_label(nuclide)

        if public_date_from:
            request["publicDateFrom"] = str(public_date_from)

        if public_date_to:
            request["publicDateTo"] = str(public_date_to)

        if quantity:
            request["quantityLabel"] = self._to_label(quantity)

        if source:
            request["sourceLabel"] = self._to_label(source)

        response = requests.post(
            f"{KCDB.BASE_URL}/cmc/searchData/radiation",
            json=request,
            timeout=self._timeout,
        )
        response.raise_for_status()
        return ResultsIonizingRadiation(response.json())

    def sources(self, branch: Branch) -> list[Source]:
        """Return all Ionizing Radiation sources for the specified branch.

        Args:
            branch: The branch to return the mediums for.

        Returns:
            A list of [Source][msl.kcdb.classes.Source]s.
        """
        # The /radiationSource endpoint does not accept parameters, so we need to filter the sources
        # based on the Branch that is specified
        if branch.label not in ["RAD", "DOS", "NEU"]:
            return []

        response = requests.get(f"{KCDB.BASE_URL}/referenceData/radiationSource", timeout=self._timeout)
        response.raise_for_status()
        data = response.json()["referenceData"]

        if branch.label == "DOS":
            return [Source(branch=branch, **d) for d in data if d["id"] < 32]  # noqa: PLR2004
        if branch.label == "RAD":
            return [Source(branch=branch, **d) for d in data if 32 <= d["id"] < 35]  # noqa: PLR2004
        return [Source(branch=branch, **d) for d in data if d["id"] >= 35]  # noqa: PLR2004
