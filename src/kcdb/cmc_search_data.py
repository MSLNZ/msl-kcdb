"""Wrapper around the KCDB API for CMC search queries."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests

from .classes import Country, ResultsChemistryAndBiology, ResultsPhysics, ResultsQuickSearch, ResultsRadiation
from .reference_data import KCDB_BASE_URL

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date

    from .classes import (
        Analyte,
        Branch,
        Category,
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


class CMCSearchData:
    """Helper class that contains `staticmethod`s to perform a CMC search."""

    MAX_PAGE_SIZE: int = 10_000
    """The maximum number of pages that may be requested."""

    TIMEOUT: float = 30.0
    """The maximum number of seconds to wait for a response from the KCDB server."""

    @staticmethod
    def chemistry_and_biology(  # noqa: PLR0913
        *,
        analyte_label: str | Analyte | None = None,
        category_label: str | Category | None = None,
        countries: str | Country | Iterable[str | Country] | None = None,
        keywords: str | None = None,
        metrology_area_label: str | MetrologyArea = "QM",
        page: int = 0,
        page_size: int = 100,
        public_date_from: str | date | None = None,
        public_date_to: str | date | None = None,
        show_table: bool = False,
    ) -> ResultsChemistryAndBiology:
        """Chemistry and biology search criteria.

        Args:
            analyte_label: Search for analyte containing this value (example: `"antimony"`).
            category_label: Category label (example: `"5"`).
            countries: Country code(s) (example: `["CH", "FR", "JP"]`).
            keywords: Search keywords in elasticsearch format (example: `"phase OR multichannel OR water"`).
            metrology_area_label: Metrology-area label to search (example: `"QM"`).
            page: Page number requested (0 means first page).
            page_size: Maximum number of elements in one page (maximum value is 10000).
            public_date_from: Minimal publication date (example: `"2005-01-31"`).
            public_date_to: Maximal publication date (example: `"2020-06-30"`).
            show_table: Set to `True` to return table data.

        Returns:
            The CMC results.
        """
        if page_size > CMCSearchData.MAX_PAGE_SIZE:
            msg = f"Page size, {page_size}, too big. Must be <= {CMCSearchData.MAX_PAGE_SIZE}"
            raise ValueError(msg)

        request: dict[str, bool | str | int | list[str]] = {
            "page": page,
            "pageSize": page_size,
            "showTable": show_table,
        }

        request["metrologyAreaLabel"] = _label(metrology_area_label)

        if analyte_label:
            request["analyteLabel"] = _label(analyte_label)

        if category_label:
            request["categoryLabel"] = _label(category_label)

        if countries:
            request["countries"] = _countries(countries)

        if keywords:
            request["keywords"] = keywords

        if public_date_from:
            request["publicDateFrom"] = str(public_date_from)

        if public_date_to:
            request["publicDateTo"] = str(public_date_to)

        response = requests.post(
            f"{KCDB_BASE_URL}/cmc/searchData/chemistryAndBiology",
            json=request,
            timeout=CMCSearchData.TIMEOUT,
        )
        response.raise_for_status()
        return ResultsChemistryAndBiology(response.json())

    @staticmethod
    def physics(  # noqa: PLR0913
        metrology_area_label: str | MetrologyArea,
        *,
        branch_label: str | Branch | None = None,
        countries: str | Country | Iterable[str | Country] | None = None,
        keywords: str | None = None,
        page: int = 0,
        page_size: int = 100,
        physics_code: str | Service | SubService | IndividualService | None = None,
        public_date_from: str | date | None = None,
        public_date_to: str | date | None = None,
        show_table: bool = False,
    ) -> ResultsPhysics:
        """Physics search criteria.

        Args:
            metrology_area_label: Metrology-area label to search (example: `"EM"`).
            branch_label: Branch label (example: `"EM/RF"`).
            countries: Country code(s) (example: `["CH", "FR", "JP"]`).
            keywords: Search keywords in elasticsearch format (example: `"phase OR multichannel OR water"`).
            page: Page number requested (0 means first page).
            page_size: Maximum number of elements in one page (maximum value is 10000).
            physics_code: Physics code is composed of "service-label", "subService-label" if
                requested and "individualService-label" if requested, separated using dot (example: `"11.3.3"`).
            public_date_from: Minimal publication date (example: `"2005-01-31"`).
            public_date_to: Maximal publication date (example: `"2020-06-30"`).
            show_table: Set to `True` to return table data.

        Returns:
            The CMC results.
        """
        if page_size > CMCSearchData.MAX_PAGE_SIZE:
            msg = f"Page size, {page_size}, too big. Must be <= {CMCSearchData.MAX_PAGE_SIZE}"
            raise ValueError(msg)

        request: dict[str, bool | str | int | list[str]] = {
            "page": page,
            "pageSize": page_size,
            "showTable": show_table,
        }

        request["metrologyAreaLabel"] = _label(metrology_area_label)

        if branch_label:
            request["branchLabel"] = _label(branch_label)

        if countries:
            request["countries"] = _countries(countries)

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
            f"{KCDB_BASE_URL}/cmc/searchData/physics",
            json=request,
            timeout=CMCSearchData.TIMEOUT,
        )
        response.raise_for_status()
        return ResultsPhysics(response.json())

    @staticmethod
    def quick_search(  # noqa: PLR0913
        *,
        excluded_filters: list[str] | None = None,
        included_filters: list[str] | None = None,
        keywords: str | None = None,
        page: int = 0,
        page_size: int = 100,
        show_table: bool = False,
    ) -> ResultsQuickSearch:
        """Quick search criteria.

        Args:
            excluded_filters: Excluded filters (example: `["cmcServices.AC current", "cmcServices.AC power"]`).
            included_filters: Included filters (example: `["cmcDomain.CHEM-BIO", "cmcBranches.Dimensional metrology"]`).
            keywords: Search keywords in elasticsearch format (example: `"phase OR test"`).
            page: Page number requested (0 means first page).
            page_size: Maximum number of elements in one page (maximum value is 10000).
            show_table: Set to `True` to return table data.

        Returns:
            The CMC results.
        """
        if page_size > CMCSearchData.MAX_PAGE_SIZE:
            msg = f"Page size, {page_size}, too big. Must be <= {CMCSearchData.MAX_PAGE_SIZE}"
            raise ValueError(msg)

        request: dict[str, bool | str | int | list[str]] = {
            "page": page,
            "pageSize": page_size,
            "showTable": show_table,
        }

        if excluded_filters:
            request["excludedFilters"] = excluded_filters

        if included_filters:
            request["includedFilters"] = included_filters

        if keywords:
            request["keywords"] = keywords

        response = requests.post(
            f"{KCDB_BASE_URL}/cmc/searchData/quickSearch",
            json=request,
            timeout=CMCSearchData.TIMEOUT,
        )
        response.raise_for_status()
        return ResultsQuickSearch(response.json())

    @staticmethod
    def radiation(  # noqa: C901, PLR0913
        *,
        branch_label: str | Branch | None = None,
        countries: str | Country | Iterable[str | Country] | None = None,
        keywords: str | None = None,
        medium_label: str | Medium | None = None,
        metrology_area_label: str | MetrologyArea = "RI",
        nuclide_label: str | Nuclide | None = None,
        page: int = 0,
        page_size: int = 100,
        public_date_from: str | date | None = None,
        public_date_to: str | date | None = None,
        quantity_label: str | Quantity | None = None,
        show_table: bool = False,
        source_label: str | Source | None = None,
    ) -> ResultsRadiation:
        """Radiation search criteria.

        Args:
            branch_label: Branch label (example: `"RAD"`).
            countries: Country code(s) (example: `["CH", "FR", "JP"]`).
            keywords: Search keywords in elasticsearch format (example: `"phase OR multichannel OR water"`).
            medium_label: Medium radiation service label (example: `"3"`).
            metrology_area_label: Metrology-area label to search (example: `"RI"`).
            nuclide_label: Nuclide label (example: `"Co-60"`).
            page: Page number requested (0 means first page).
            page_size: Maximum number of elements in one page (maximum value is 10000).
            public_date_from: Minimal publication date (example: `"2005-01-31"`).
            public_date_to: Maximal publication date (example: `"2020-06-30"`).
            quantity_label: Quantity radiation service label (example: `"1"`).
            show_table: Set to `True` to return table data.
            source_label: Source radiation service label (example: `"2"`).

        Returns:
            The CMC results.
        """
        if page_size > CMCSearchData.MAX_PAGE_SIZE:
            msg = f"Page size, {page_size}, too big. Must be <= {CMCSearchData.MAX_PAGE_SIZE}"
            raise ValueError(msg)

        request: dict[str, bool | str | int | list[str]] = {
            "page": page,
            "pageSize": page_size,
            "showTable": show_table,
        }

        request["metrologyAreaLabel"] = _label(metrology_area_label)

        if branch_label:
            request["branchLabel"] = _label(branch_label)

        if countries:
            request["countries"] = _countries(countries)

        if keywords:
            request["keywords"] = keywords

        if medium_label:
            request["mediumLabel"] = _label(medium_label)

        if nuclide_label:
            request["nuclideLabel"] = _label(nuclide_label)

        if public_date_from:
            request["publicDateFrom"] = str(public_date_from)

        if public_date_to:
            request["publicDateTo"] = str(public_date_to)

        if quantity_label:
            request["quantityLabel"] = _label(quantity_label)

        if source_label:
            request["sourceLabel"] = _label(source_label)

        response = requests.post(
            f"{KCDB_BASE_URL}/cmc/searchData/radiation",
            json=request,
            timeout=CMCSearchData.TIMEOUT,
        )
        response.raise_for_status()
        return ResultsRadiation(response.json())


def _label(obj: str | RefData) -> str:
    if isinstance(obj, str):
        return obj
    return obj.label


def _countries(countries: str | Country | Iterable[str | Country]) -> list[str]:
    if isinstance(countries, str):
        return [countries]
    if isinstance(countries, Country):
        return [countries.label]
    return [c if isinstance(c, str) else c.label for c in countries]
