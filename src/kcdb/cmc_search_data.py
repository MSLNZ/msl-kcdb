"""Wrapper around the API for CMC search queries."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import requests

from .reference_data import KCDB_BASE_URL, Country

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date

    from .reference_data import (
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
    """Perform a CMC search."""

    MAX_PAGE_SIZE: int = 10_000
    TIMEOUT: float = 10.0

    @staticmethod
    def chemistry_and_biology(  # noqa: PLR0913
        *,
        analyte_label: str | Analyte | None = None,
        category_label: str | Category | None = None,
        countries: str | Country | Iterable[str | Country] | None = None,
        keywords: str | None = None,
        metrology_area_label: str | MetrologyArea = "QM",
        page: int = 0,
        page_size: int = 10000,
        public_date_from: str | date | None = None,
        public_date_to: str | date | None = None,
        show_table: bool = False,
    ) -> dict[str, Any]:
        """Chemistry and biology search criteria.

        :param analyte_label: Search for analyte containing this value.
            Example: "antimony"
        :param category_label: Category label.
            Example: "5"
        :param countries: Country code list.
            Example: ["CH", "FR", "JP"]
        :param keywords: Search keywords in elasticsearch format.
            Example: "phase OR multichannel OR water"
        :param metrology_area_label: Metrology-area label to search.
            Example: "QM"
        :param page: Page number requested (0 means first page).
        :param page_size: Maximum number of elements in one page (maximum value is 10000).
        :param public_date_from: Minimal publication date (YYYY-MM-DD).
            Example: "2005-01-31"
        :param public_date_to: Maximal publication date (YYYY-MM-DD).
            Example: "2020-06-30"
        :param show_table: Set to true to return table data.

        :return: The CMC results.
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
        json: dict[str, Any] = response.json()
        return json

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
    ) -> dict[str, Any]:
        """Physics search criteria.

        :param metrology_area_label: Metrology-area label to search.
            Example: "EM"
        :param branch_label: Branch label.
            Example: "EM/RF"
        :param countries: Country code list.
            Example: ["CH", "FR", "JP"]
        :param keywords: Search keywords in elasticsearch format.
            Example: "phase OR multichannel OR water"
        :param page: Page number requested (0 means first page).
        :param page_size: Maximum number of elements in one page (maximum value is 10000).
        :param physics_code: Physics code is composed of "service identifier", "subService identifier" if
            requested and "individualService identifier" if requested, separated using dot.
            Example: "11.3.3"
        :param public_date_from: Minimal publication date (YYYY-MM-DD).
            Example: "2005-01-31"
        :param public_date_to: Maximal publication date (YYYY-MM-DD).
            Example: "2020-06-30"
        :param show_table: Set to true to return table data.

        :return: The CMC results.
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
        json: dict[str, Any] = response.json()
        return json

    @staticmethod
    def quick_search(  # noqa: PLR0913
        *,
        excluded_filters: list[str] | None = None,
        included_filters: list[str] | None = None,
        keywords: str | None = None,
        page: int = 0,
        page_size: int = 100,
        show_table: bool = False,
    ) -> dict[str, Any]:
        """Quick search criteria.

        :param excluded_filters: Excluded filter list.
            Example: ["cmcServices.AC current", "cmcServices.AC power"]
        :param included_filters: Included filter list.
            Example: ["cmcDomain.CHEM-BIO", "cmcBranches.Dimensional metrology"]
        :param keywords: Search keywords in elasticsearch format.
            Example: "phase OR test"
        :param page: Page number requested (0 means first page).
        :param page_size: Maximum number of elements in one page (maximum value is 10000).
        :param show_table: Set to true to return table data.

        :return: The CMC results.
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
        json: dict[str, Any] = response.json()
        return json

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
    ) -> dict[str, Any]:
        """Radiation search criteria.

        :param branch_label: Branch label.
            Example: "RAD"
        :param countries: Country code list.
            Example: ["CH", "FR", "JP"]
        :param keywords: Search keywords in elasticsearch format.
            Example: "phase OR multichannel OR water"
        :param medium_label: Medium radiation service label.
            Example: "3"
        :param metrology_area_label: Metrology-area label to search.
            Example: "RI"
        :param nuclide_label: Nuclide label.
            Example: "Co-60"
        :param page: Page number requested (0 means first page).
        :param page_size: Maximum number of elements in one page (maximum value is 10000).
        :param public_date_from: Minimal publication date (YYYY-MM-DD).
            Example: "2005-01-31"
        :param public_date_to: Maximal publication date (YYYY-MM-DD).
            Example: "2020-06-30"
        :param quantity_label: Quantity radiation service label.
            Example: "1"
        :param show_table: Set to true to return table data.
        :param source_label: Source radiation service label.
            Example: "2"

        :return: The CMC results.
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
        json: dict[str, Any] = response.json()
        return json


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
