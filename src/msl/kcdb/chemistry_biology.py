"""Search the Chemistry and Biology database."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from .classes import KCDB, Analyte, Category, Domain, ResultsChemistryBiology

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date

    from .classes import Country, MetrologyArea


class ChemistryBiology(KCDB):
    """Chemistry and Biology class."""

    DOMAIN = Domain(code="CHEM-BIO", name="Chemistry and Biology")
    """The Chemistry and Biology domain."""

    def analytes(self) -> list[Analyte]:
        """Return all Chemistry and Biology analytes.

        Returns:
            A list of [Analyte][msl.kcdb.classes.Analyte]s
        """
        response = requests.get(f"{KCDB.BASE_URL}/referenceData/analyte", timeout=self._timeout)
        response.raise_for_status()
        return [Analyte(**data) for data in response.json()["referenceData"]]

    def categories(self) -> list[Category]:
        """Return all Chemistry and Biology categories.

        Returns:
            A list of [Category][msl.kcdb.classes.Category]'s
        """
        response = requests.get(f"{KCDB.BASE_URL}/referenceData/category", timeout=self._timeout)
        response.raise_for_status()
        return [Category(**data) for data in response.json()["referenceData"]]

    def search(  # noqa: PLR0913
        self,
        *,
        analyte: str | Analyte | None = None,
        category: str | Category | None = None,
        countries: str | Country | Iterable[str | Country] | None = None,
        keywords: str | None = None,
        metrology_area: str | MetrologyArea = "QM",
        page: int = 0,
        page_size: int = 100,
        public_date_from: str | date | None = None,
        public_date_to: str | date | None = None,
        show_table: bool = False,
    ) -> ResultsChemistryBiology:
        """Perform a Chemistry and Biology search.

        Args:
            analyte: Analyte label. _Example:_ `"antimony"`
            category: Category label. _Example:_ `"5"`
            countries: Country label(s). _Example:_ `["CH", "FR", "JP"]`
            keywords: Search keywords in elasticsearch format. _Example:_ `"phase OR multichannel OR water"`
            metrology_area: Metrology area label. _Example:_ `"QM"`
            page: Page number requested (0 means first page).
            page_size: Maximum number of elements in a page (maximum value is 10000).
            public_date_from: Minimal publication date. _Example:_ `"2005-01-31"`
            public_date_to: Maximal publication date. _Example:_ `"2020-06-30"`
            show_table: Set to `True` to return table data.

        Returns:
            The CMC results for Chemistry and Biology.
        """
        self._check_page_info(page, page_size)

        request: dict[str, bool | int | str | list[str]] = {
            "page": page,
            "pageSize": page_size,
            "showTable": show_table,
        }

        request["metrologyAreaLabel"] = self._to_label(metrology_area)

        if analyte is not None:
            request["analyteLabel"] = self._to_label(analyte)

        if category:
            request["categoryLabel"] = self._to_label(category)

        if countries:
            request["countries"] = self._to_countries(countries)

        if keywords:
            request["keywords"] = keywords

        if public_date_from:
            request["publicDateFrom"] = str(public_date_from)

        if public_date_to:
            request["publicDateTo"] = str(public_date_to)

        response = requests.post(
            f"{KCDB.BASE_URL}/cmc/searchData/chemistryAndBiology",
            json=request,
            timeout=self._timeout,
        )
        response.raise_for_status()
        return ResultsChemistryBiology(response.json())
