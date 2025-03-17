"""Common classes for the KCDB API."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, TypeVar

from . import https

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any


class AbsoluteRelative(Enum):
    """CRM uncertainty mode.

    Attributes:
        ABSOLUTE (str): `"Absolute"`
        RELATIVE (str): `"Relative"`
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class UncertaintyConvention(Enum):
    """Chemistry and Biology uncertainty convention.

    Attributes:
        ONE (str): `"One"`
        TWO (str): `"Two"`
    """

    ONE = "One"
    TWO = "Two"


@dataclass(frozen=True, order=True)
class Domain:
    """The domain of either General Physics, Chemistry and Biology or Ionizing Radiation.

    Attributes:
        code: Domain code. _Example:_ `"PHYSICS"`
        name: Domain name. _Example:_ `"General physics"`
    """

    code: str
    name: str


@dataclass(frozen=True, order=True)
class ReferenceData:
    """Base class for reference data.

    Attributes:
        id: Reference data identity. _Example:_ 8
        label: Reference data label. _Example:_ `"QM"`
        value: Reference data value. _Example:_ `"Chemistry and Biology"`
    """

    id: int
    label: str
    value: str


class Analyte(ReferenceData):
    """An analyte of Chemistry and Biology.

    Attributes:
        id: Analyte identity. _Example:_ 1
        label: Analyte label. _Example:_ `"nitrogen"`
        value: Analyte value. _Example:_ `"nitrogen"`
    """


class Category(ReferenceData):
    """A category of Chemistry and Biology.

    Attributes:
        id: Category identity. _Example:_ 8
        label: Category label. _Example:_ `"2"`
        value: Category value. _Example:_ `"Inorganic solutions"`
    """


class Country(ReferenceData):
    """Information about a country.

    Attributes:
        id: Country identity. _Example:_ 58
        label: Country label. _Example:_ `"NZ"`
        value: Country value. _Example:_ `"New Zealand"`
    """


class Nuclide(ReferenceData):
    """A nuclide of Ionizing Radiation.

    Attributes:
        id: Nuclide identity. _Example:_ 1
        label: Nuclide label. _Example:_ `"C-14"`
        value: Nuclide value. _Example:_ `"C-14"`
    """


class NonIonizingQuantity(ReferenceData):
    """A quantity that is not Ionizing Radiation.

    Attributes:
        id: Non-ionizing identity. _Example:_ 109
        label: Always an empty string. _Example:_ `""`
        value: Non-ionizing value. _Example:_ `"Absorbance, regular, spectral"`
    """


@dataclass(frozen=True, order=True)
class MetrologyArea(ReferenceData):
    """A metrology area of a domain.

    Attributes:
        domain: The domain that the metrology area belongs to.
        id: Metrology area identity. _Example:_ 2
        label: Metrology area label. _Example:_ `"EM"`
        value: Metrology area value. _Example:_ `"Electricity and Magnetism"`
    """

    domain: Domain


@dataclass(frozen=True, order=True)
class Branch(ReferenceData):
    """A branch of General Physics or Ionizing Radiation.

    Attributes:
        id: Branch identity. _Example:_ 21
        label: Branch label. _Example:_ `"PR/Fibre"`
        metrology_area: The metrology area that the branch belongs to.
        value: Branch value. _Example:_ `"Fibre optics"`
    """

    metrology_area: MetrologyArea


@dataclass(frozen=True, order=True)
class Service(ReferenceData):
    """A service of General Physics.

    Attributes:
        branch: The branch that the service belongs to.
        id: Service identity. _Example:_ 16
        label: Service label. _Example:_ `"6"`
        physics_code: The physics code for this service. _Example:_ `"6"`
        value: Service value. _Example:_ `"AC current"`
    """

    branch: Branch
    physics_code: str


@dataclass(frozen=True, order=True)
class SubService(ReferenceData):
    """A sub service of General Physics.

    Attributes:
        id: Sub service identity. _Example:_ 33
        label: Sub service label. _Example:_ `"1"`
        physics_code: The physics code for this sub service. _Example:_ `"6.1"`
        service: The service that the sub service belongs to.
        value: Sub service value. _Example:_ `"AC-DC current transfer"`
    """

    physics_code: str
    service: Service


@dataclass(frozen=True, order=True)
class IndividualService(ReferenceData):
    """An individual service of General Physics.

    Attributes:
        id: Individual service identity. _Example:_ 225
        label: Individual service label. _Example:_ `"1"`
        physics_code: The physics code for this individual service. _Example:_ `"11.1.1"`
        sub_service: The sub service that the individual service belongs to.
        value: Individual service value. _Example:_ `"Absolute power in coaxial line"`
    """

    physics_code: str
    sub_service: SubService


@dataclass(frozen=True, order=True)
class Quantity(ReferenceData):
    """A quantity of Ionizing Radiation.

    Attributes:
        branch: The branch that the quantity belongs to.
        id: Quantity identity. _Example:_ 1
        label: Quantity label. _Example:_ `"1"`
        value: Quantity value. _Example:_ `"Absorbed dose/rate to air"`
    """

    branch: Branch


@dataclass(frozen=True, order=True)
class Medium(ReferenceData):
    """A medium of Ionizing Radiation.

    Attributes:
        branch: The branch that the medium belongs to.
        id: Medium identity. _Example:_ 5
        label: Medium label. _Example:_ `"5"`
        value: Medium value. _Example:_ `"Aerosol"`
    """

    branch: Branch


@dataclass(frozen=True, order=True)
class Source(ReferenceData):
    """A source of Ionizing Radiation.

    Attributes:
        branch: The branch that the source belongs to.
        id: Source identity. _Example:_ 3
        label: Source label. _Example:_ `"3"`
        value: Source value. _Example:_ `"Beta radiation"`
    """

    branch: Branch


class ResultAggregation:
    """Aggregation representation.

    Attributes:
        name: Aggregation name. _Example:_ `"cmcCountries"`
        values: Aggregation values. _Example:_ `["Kazakhstan", "Portugal", "Greece"]`
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of an aggregation."""
        self.name: str = kwargs.get("name") or ""
        self.values: list[str] = kwargs.get("values", [])

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultAggregation(name={self.name!r}, len(values)={len(self.values)})"


class ResultEquation:
    """Equation representation.

    Attributes:
        equation: Equation name.
        equation_comment: Equation comment.
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of an equation."""
        self.equation: str = kwargs.get("equation") or ""
        self.equation_comment: str = kwargs.get("equationComment") or ""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultEquation(equation={self.equation!r}, equation_comment={self.equation_comment!r})"


class ResultFilter:
    """Filter representation.

    Attributes:
        children: Filter children.
        code: Filter code. _Example:_ `"cmcMaterial"`
        count: Filter count.
        name: Filter name. _Example:_ `"cmcMaterial"`
        order: Filter order.
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of a filter."""
        self.children: list[ResultFilter] = [ResultFilter(c) for c in kwargs.get("children", [])]
        self.code: str = kwargs.get("code") or ""
        self.count: int = kwargs["count"]
        self.name: str = kwargs.get("name") or ""
        self.order: int = kwargs["order"]

    def __repr__(self) -> str:
        """Return the object representation."""
        return (
            f"ResultFilter(code={self.code!r}, count={self.count}, "
            f"name={self.name!r}, order={self.order}, len(children)={len(self.children)})"
        )


class ResultParam:
    """Parameter representation.

    Attributes:
        parameter_name: Parameter name. _Example:_ `"S21 and S12"`
        parameter_value: Parameter value. _Example:_ `"-80 dB to 0 dB"`
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of a parameter."""
        self.parameter_name: str = kwargs.get("parameterName") or ""
        self.parameter_value: str = kwargs.get("parameterValue") or ""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultParam(parameter_name={self.parameter_name!r}, parameter_value={self.parameter_value!r})"


class ResultTable:
    """Table representation.

    Attributes:
        table_rows: Number of rows in table.
        table_cols: Number of columns in table.
        table_name: Table name. _Example:_ `"CH_Scatt-Atten_Mag"`
        table_comment: Table comment.
        table_contents: Table contents. _Example:_ `"{"row_1":{"col_1":"val1","col_2":"val2"}}"`
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of a table."""
        self.table_rows: int = kwargs["tableRows"]
        self.table_cols: int = kwargs["tableCols"]
        self.table_name: str = kwargs.get("tableName") or ""
        self.table_comment: str = kwargs.get("tableComment") or ""
        self.table_contents: str = kwargs.get("tableContents") or ""

    def __repr__(self) -> str:
        """Return the object representation."""
        return (
            f"ResultTable(table_rows={self.table_rows}, table_cols={self.table_cols}, "
            f"table_name={self.table_name!r}, table_comment={self.table_comment!r})"
        )


class ResultUnit:
    """Units object definition.

    Attributes:
        lower_limit: Lower limit value.
        unit: Unit symbol. _Example:_ `"%"`
        upper_limit: Upper limit value.
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Units object definition."""
        self.lower_limit: float | None = kwargs.get("lowerLimit")
        self.unit: str = kwargs.get("unit") or ""
        self.upper_limit: float | None = kwargs.get("upperLimit")

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultUnit(lower_limit={self.lower_limit}, unit={self.unit!r}, upper_limit={self.upper_limit})"


class Results:
    """Attributes for advanced search results.

    Attributes:
        number_of_elements: Number of elements on this page.
        page_number: The page number (first page is 0) of the request.
        page_size: The page size that was requested.
        total_elements: Total number of elements available (in all pages).
        total_pages: Total number of pages.
        version_api_kcdb: KCDB API version. _Example:_ `"1.0.7"`
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Attributes for advanced search results."""
        self.number_of_elements: int = kwargs["numberOfElements"]
        self.page_number: int = kwargs["pageNumber"]
        self.page_size: int = kwargs["pageSize"]
        self.total_elements: int = kwargs["totalElements"]
        self.total_pages: int = kwargs["totalPages"]
        self.version_api_kcdb: str = kwargs.get("versionApiKcdb") or ""

    def __repr__(self) -> str:
        """Return the object representation."""
        return (
            f"number_of_elements={self.number_of_elements}, "
            f"page_number={self.page_number}, "
            f"page_size={self.page_size}, "
            f"total_elements={self.total_elements}, "
            f"total_pages={self.total_pages}, "
            f"version_api_kcdb={self.version_api_kcdb!r}"
        )


class ResultCommon:
    """Common attributes for advanced search results.

    Attributes:
        id: Document database id.
        approval_date: Approval date (YYYY-MM-DD).
        cmc: CMC result unit.
        cmc_base_unit: CMC base unit.
        cmc_uncertainty: CMC uncertainty.
        cmc_uncertainty_base_unit: CMC uncertainty base unit.
        comments: Comments.
        confidence_level: Confidence level.
        country_value: Country full name. _Example:_ `"China"`
        coverage_factor:Coverage factor.
        domain_code: Domain code. _Example:_ `"CHEM-BIO"`
        group_identifier: Group identifier.
        kcdb_code: Document KCDB code. _Example:_ `"APMP-QM-CN-00000JZR-1"`
        metrology_area_label: Metrology area label. _Example:_ `"QM"`
        nmi_code: NMI code. _Example:_ `"NIM"`
        nmi_name: NMI name. _Example:_ `"National Institute of Metrology"`
        nmi_service_code: NMI service code. _Example:_ `"NIM/11.1.4a"`
        nmi_service_link: NMI service link.
        publication_date: Publication date (YYYY-MM-DD).
        quantity_value: Quantity value. _Example:_ `"Absorbed dose/rate"`
        rmo: RMO acronym. _Example:_ `"EURAMET"`
        status: CMC status. _Example:_ `"Published"`
        status_date: Last status date (YYYY-MM-DD).
        traceability_source: Traceability source. _Example:_ `"VSL"`
        uncertainty_equation: Uncertainty equation.
        uncertainty_mode: Uncertainty mode.
        uncertainty_table: Uncertainty table.
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Attributes for advanced search results that are common."""
        self.id: int = kwargs["id"]
        self.approval_date: str = kwargs.get("approvalDate") or ""

        k = kwargs.get("cmc")
        self.cmc: ResultUnit | None = ResultUnit(k) if k else None

        k = kwargs.get("cmcBaseUnit")
        self.cmc_base_unit: ResultUnit | None = ResultUnit(k) if k else None

        k = kwargs.get("cmcUncertainty")
        self.cmc_uncertainty: ResultUnit | None = ResultUnit(k) if k else None

        k = kwargs.get("cmcUncertaintyBaseUnit")
        self.cmc_uncertainty_base_unit: ResultUnit | None = ResultUnit(k) if k else None

        self.comments: str = kwargs.get("comments") or ""
        self.confidence_level: float | None = kwargs.get("confidenceLevel")
        self.country_value: str = kwargs.get("countryValue") or ""
        self.coverage_factor: float | None = kwargs.get("coverageFactor")
        self.domain_code: str = kwargs.get("domainCode") or ""
        self.group_identifier: str = kwargs.get("groupIdentifier") or ""
        self.kcdb_code: str = kwargs.get("kcdbCode") or ""
        self.metrology_area_label: str = kwargs.get("metrologyAreaLabel") or ""
        self.nmi_code: str = kwargs.get("nmiCode") or ""
        self.nmi_name: str = kwargs.get("nmiName") or ""
        self.nmi_service_code: str = kwargs.get("nmiServiceCode") or ""
        self.nmi_service_link: str = kwargs.get("nmiServiceLink") or ""
        self.publication_date: str = kwargs.get("publicationDate") or ""
        self.quantity_value: str = kwargs.get("quantityValue") or ""
        self.rmo: str = kwargs.get("rmo") or ""
        self.status: str = kwargs.get("status") or ""
        self.status_date: str = kwargs.get("statusDate") or ""
        self.traceability_source: str = kwargs.get("traceabilitySource") or ""

        k = kwargs.get("uncertaintyEquation")
        self.uncertainty_equation: ResultEquation | None = ResultEquation(k) if k else None

        k = kwargs.get("uncertaintyMode")
        self.uncertainty_mode: AbsoluteRelative | None = AbsoluteRelative(k) if k else None

        k = kwargs.get("uncertaintyTable")
        self.uncertainty_table: ResultTable | None = ResultTable(k) if k else None


class ResultChemistryBiology(ResultCommon):
    """Chemistry and Biology result.

    Attributes:
        analyte_matrix: Analyte matrix. _Example:_ `"high purity antimony"`
        analyte_value: Analyte value. _Example:_ `"antimony"`
        category_value: Category value. _Example:_ `"High purity chemicals"`
        crm: CRM unit.
        crm_confidence_level: CRM confidence level.
        crm_coverage_factor: CRM coverage factor.
        crm_uncertainty: CRM uncertainty.
        crm_uncertainty_equation: CRM uncertainty equation.
        crm_uncertainty_mode: CRM uncertainty mode.
        crm_uncertainty_table: CRM uncertainty table.
        measurement_technique: Measurement technique.
            _Example:_ `"Liquid-solid extraction with SPE cleanup and bracketing LC-IDMS/MS"`
        mechanism: Mechanism. _Example:_ `"Customer service; GD-MS-200; delivery only to other NMIs"`
        sub_category_value: Sub category value. _Example:_ `"Metals"`
        uncertainty_convention: Uncertainty convention.
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Chemistry and Biology result."""
        super().__init__(kwargs)

        self.analyte_matrix: str = kwargs.get("analyteMatrix") or ""
        self.analyte_value: str = kwargs.get("analyteValue") or ""
        self.category_value: str = kwargs.get("categoryValue") or ""

        k = kwargs.get("crm")
        self.crm: ResultUnit | None = ResultUnit(k) if k else None

        self.crm_confidence_level: float | None = kwargs.get("crmConfidenceLevel")
        self.crm_coverage_factor: float | None = kwargs.get("crmCoverageFactor")

        k = kwargs.get("crmUncertainty")
        self.crm_uncertainty: ResultUnit | None = ResultUnit(k) if k else None

        k = kwargs.get("crmUncertaintyEquation")
        self.crm_uncertainty_equation: ResultEquation | None = ResultEquation(k) if k else None

        k = kwargs.get("crmUncertaintyMode")
        self.crm_uncertainty_mode: AbsoluteRelative | None = AbsoluteRelative(k) if k else None

        k = kwargs.get("crmUncertaintyTable")
        self.crm_uncertainty_table: ResultTable | None = ResultTable(k) if k else None

        # Note spelling mistake in "measurmentTechnique" is what the KCDB API returns cSpell:disable-line
        self.measurement_technique: str = kwargs.get("measurmentTechnique") or ""  # cSpell:disable-line
        self.mechanism: str = kwargs.get("mechanism") or ""
        self.sub_category_value: str = kwargs.get("subCategoryValue") or ""

        k = kwargs.get("uncertaintyConvention")
        self.uncertainty_convention: UncertaintyConvention | None = UncertaintyConvention(k) if k else None

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultChemistryBiology(id={self.id}, nmi_code={self.nmi_code!r}, rmo={self.rmo!r})"


class ResultGeneralPhysics(ResultCommon):
    """General Physics result.

    Attributes:
        branch_value: Branch value. _Example:_ `"Radio frequency measurements"`
        individual_service_value: Individual service value.
            _Example:_ `"Transmission coefficient in coaxial line (real and imaginary)"`
        instrument: Instrument. _Example:_ `"Passive device"`
        instrument_method: Instrument method. _Example:_ `"Vector network analyser"`
        international_standard: International standard. _Example:_ `"EURAMET Cg19, ISO 8655-6"`
        parameters: Parameters list with name and value.
        service_value: Service value. _Example:_ `"Radio frequency measurements"`
        sub_service_value: Sub service value. _Example:_ `"Scattering parameters (vectors)"`
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """General Physics result."""
        super().__init__(kwargs)
        self.branch_value: str = kwargs.get("branchValue") or ""
        self.individual_service_value: str = kwargs.get("individualServiceValue") or ""
        self.instrument: str = kwargs.get("instrument") or ""
        self.instrument_method: str = kwargs.get("instrumentMethod") or ""
        self.international_standard: str = kwargs.get("internationalStandard") or ""
        self.parameters: list[ResultParam] = [ResultParam(p) for p in kwargs.get("parameters", [])]
        self.service_value: str = kwargs.get("serviceValue") or ""
        self.sub_service_value: str = kwargs.get("subServiceValue") or ""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultGeneralPhysics(id={self.id}, nmi_code={self.nmi_code!r}, rmo={self.rmo!r})"


class ResultIonizingRadiation(ResultCommon):
    """Ionizing Radiation result.

    Attributes:
        branch_value: Branch value. _Example:_ `"Radioactivity"`
        instrument: Instrument. _Example:_ `"Multiple nuclide source, solution"`
        instrument_method: Instrument method. _Example:_ `"Ge detector, multichannel analyzer"`
        international_standard: International standard. _Example:_ `"EURAMET Cg19, ISO 8655-6"`
        medium_value: Medium value. _Example:_ `"Liquid"`
        nuclide_value: Nuclide value. _Example:_ `"Cr-51"`
        radiation_code: Radiation code separated by a dot for branch, quantity, source, medium. _Example:_ `"2.1.3.2"`
        radiation_specification: Radiation specification name.
            _Example:_ `"10 ml to 500 ml NMIJ/AIST standard cylindrical plastic bottle"`
        reference_standard: Reference standard. _Example:_ `"Comparison with the NMIJ/AIST standard source"`
        source_value: Source value. _Example:_ `"Multi-radionuclide source"`
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Ionizing Radiation result."""
        super().__init__(kwargs)
        self.branch_value: str = kwargs.get("branchValue") or ""
        self.instrument: str = kwargs.get("instrument") or ""
        self.instrument_method: str = kwargs.get("instrumentMethod") or ""
        self.international_standard: str = kwargs.get("internationalStandard") or ""
        self.medium_value: str = kwargs.get("mediumValue") or ""
        self.nuclide_value: str = kwargs.get("nuclideValue") or ""
        self.radiation_code: str = kwargs.get("radiationCode") or ""
        self.radiation_specification: str = kwargs.get("radiationSpecification") or ""
        self.reference_standard: str = kwargs.get("referenceStandard") or ""
        self.source_value: str = kwargs.get("sourceValue") or ""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultIonizingRadiation(id={self.id}, nmi_code={self.nmi_code!r}, rmo={self.rmo!r})"


class ResultsChemistryBiology(Results):
    """Chemistry and Biology search results.

    Attributes:
        data: Chemistry and Biology result data.
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Chemistry and Biology search results."""
        super().__init__(kwargs)
        self.data: list[ResultChemistryBiology] = [ResultChemistryBiology(d) for d in kwargs.get("data", [])]

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultsChemistryBiology({super().__repr__()})"


class ResultsGeneralPhysics(Results):
    """General Physics search results.

    Attributes:
        data: General Physics result data.
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """General Physics search results."""
        super().__init__(kwargs)
        self.data: list[ResultGeneralPhysics] = [ResultGeneralPhysics(d) for d in kwargs.get("data", [])]

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultsGeneralPhysics({super().__repr__()})"


class ResultsQuickSearch(Results):
    """Quick search results.

    Attributes:
        aggregations: The aggregations list.
        data: The quick search result data.
        filters_list: The filters list.
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Quick search results."""
        super().__init__(kwargs)
        self.aggregations: list[ResultAggregation] = [ResultAggregation(d) for d in kwargs.get("aggregations", [])]
        self.data: list[Any] = kwargs.get("data", [])
        self.filters_list: list[ResultFilter] = [ResultFilter(d) for d in kwargs.get("filtersList", [])]

    def __repr__(self) -> str:
        """Return the object representation."""
        return (
            f"ResultsQuickSearch({super().__repr__()}, "
            f"len(aggregations)={len(self.aggregations)}, "
            f"len(filters_list)={len(self.filters_list)})"
        )


class ResultsIonizingRadiation(Results):
    """Ionizing Radiation search results.

    Attributes:
        data: Ionizing Radiation result data.
    """

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Ionizing Radiation search results."""
        super().__init__(kwargs)
        self.data: list[ResultIonizingRadiation] = [ResultIonizingRadiation(d) for d in kwargs.get("data", [])]

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultsIonizingRadiation({super().__repr__()})"


T = TypeVar("T", bound=ReferenceData)


class KCDB:
    """KCDB base class."""

    BASE_URL: str = "https://www.bipm.org/api/kcdb"
    """The base url to the KCDB API."""

    MAX_PAGE_SIZE: int = 10_000
    """The maximum number of elements that can be returned in a single KCDB request."""

    DOMAIN: Domain

    def __init__(self, timeout: float | None = 30) -> None:
        """Initialise the KCDB base class.

        Args:
            timeout: The maximum number of seconds to wait for a response from the KCDB server.
        """
        self.timeout = timeout

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"{self.__class__.__name__}(code={self.DOMAIN.code!r}, name={self.DOMAIN.name!r})"

    @staticmethod
    def _check_page_info(page: int, page_size: int) -> None:
        if page < 0:
            msg = f"Invalid page value, {page}. Must be >= 0"
            raise ValueError(msg)

        if page_size < 1 or page_size > KCDB.MAX_PAGE_SIZE:
            msg = f"Invalid page size, {page_size}. Must be in the range [1, {KCDB.MAX_PAGE_SIZE}]"
            raise ValueError(msg)

    @staticmethod
    def _to_countries(countries: str | Country | Iterable[str | Country]) -> list[str]:
        if isinstance(countries, str):
            return [countries]
        if isinstance(countries, Country):
            return [countries.label]
        return [c if isinstance(c, str) else c.label for c in countries]

    @staticmethod
    def _to_label(obj: str | ReferenceData) -> str:
        if isinstance(obj, str):
            return obj
        return obj.label

    @staticmethod
    def _to_physics_code(obj: str | Service | SubService | IndividualService) -> str:
        if isinstance(obj, str):
            return obj
        return obj.physics_code

    def countries(self) -> list[Country]:
        """Return all countries.

        Returns:
            A list of [Country][msl.kcdb.classes.Country]'s.
        """
        response = https.get(f"{KCDB.BASE_URL}/referenceData/country", timeout=self._timeout)
        response.raise_for_status()
        return [Country(**data) for data in response.json()["referenceData"]]

    def domains(self) -> list[Domain]:
        """Return all KCDB domains.

        Returns:
            A list of [Domain][msl.kcdb.classes.Domain]s.
        """
        response = https.get(f"{KCDB.BASE_URL}/referenceData/domain", timeout=self._timeout)
        response.raise_for_status()
        return [Domain(**data) for data in response.json()["domains"]]

    @staticmethod
    def filter(data: Iterable[T], pattern: str, *, flags: int = 0) -> list[T]:
        """Filter the reference data based on a pattern search.

        Args:
            data: An iterable of a [ReferenceData][msl.kcdb.classes.ReferenceData] subclass.
            pattern: A [regular-expression](https://regexone.com/) pattern to use to filter results.
                Uses the `label` and `value` attributes of each item in `data` to perform the filtering.
            flags: Pattern flags passed to [re.compile][].

        Returns:
            The filtered reference data.
        """
        regex = re.compile(pattern, flags=flags)
        return [item for item in data if regex.search(item.value) or regex.search(item.label)]

    def metrology_areas(self) -> list[MetrologyArea]:
        """Return all metrology areas for this domain.

        Returns:
            A list of [MetrologyArea][msl.kcdb.classes.MetrologyArea]s.
        """
        response = https.get(
            f"{KCDB.BASE_URL}/referenceData/metrologyArea",
            params={"domainCode": self.DOMAIN.code},
            timeout=self._timeout,
        )
        response.raise_for_status()
        return [MetrologyArea(domain=self.DOMAIN, **data) for data in response.json()["referenceData"]]

    def non_ionizing_quantities(self) -> list[NonIonizingQuantity]:
        """Return all non-Ionizing Radiation quantities.

        Returns:
            A list of [NonIonizingQuantity][msl.kcdb.classes.NonIonizingQuantity]'s.
        """
        response = https.get(f"{KCDB.BASE_URL}/referenceData/quantity", timeout=self._timeout)
        response.raise_for_status()
        return [
            NonIonizingQuantity(id=d["id"], label="", value=d["value"])
            for d in response.json()["referenceData"]
            if d["label"] is None
        ]

    def quick_search(
        self,
        *,
        excluded_filters: Iterable[str] | None = None,
        included_filters: Iterable[str] | None = None,
        keywords: str | None = None,
        page: int = 0,
        page_size: int = 100,
        show_table: bool = False,
    ) -> ResultsQuickSearch:
        """Perform a quick search.

        Args:
            excluded_filters: Excluded filters. _Example:_ `["cmcServices.AC current", "cmcServices.AC power"]`
            included_filters: Included filters. _Example:_ `["cmcDomain.CHEM-BIO", "cmcBranches.Dimensional metrology"]`
            keywords: Search keywords in elasticsearch format. _Example:_ `"phase OR test"`
            page: Page number requested (0 means first page).
            page_size: Maximum number of elements in a page (maximum value is 10000).
            show_table: Set to `True` to return table data.

        Returns:
            The CMC quick-search results.
        """
        self._check_page_info(page, page_size)

        request: dict[str, bool | str | int | list[str]] = {
            "page": page,
            "pageSize": page_size,
            "showTable": show_table,
        }

        if excluded_filters:
            request["excludedFilters"] = list(excluded_filters)

        if included_filters:
            request["includedFilters"] = list(included_filters)

        if keywords:
            request["keywords"] = keywords

        response = https.post(
            f"{KCDB.BASE_URL}/cmc/searchData/quickSearch",
            json=request,
            timeout=self._timeout,
        )
        response.raise_for_status()
        return ResultsQuickSearch(response.json())

    @property
    def timeout(self) -> float | None:
        """The timeout value, in seconds, to use for a KCDB request.

        Returns:
            The maximum number of seconds to wait for a response from the KCDB server. If `None`, there is no timeout.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value: float | None) -> None:
        if value is None or value < 0:
            self._timeout = None
        else:
            self._timeout = float(value)
