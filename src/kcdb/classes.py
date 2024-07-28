"""Classes defined in the KCDB API schema."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class AbsoluteRelative(Enum):
    """CRM uncertainty mode."""

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class UncertaintyConvention(Enum):
    """Chemistry and Biology uncertainty convention."""

    ONE = "One"
    TWO = "Two"


@dataclass(frozen=True, order=True)
class Domain:
    """One of General Physics, Chemistry and Biology or Ionizing Radition."""

    code: str
    """Domain code (example: "PHYSICS")."""

    name: str
    """Domain code (example: "General physics")."""


@dataclass(frozen=True, order=True)
class RefData:
    """Base class for reference data."""

    id: int
    """Reference data identity."""

    label: str
    """Reference data label (example: "QM")."""

    value: str
    """Reference data value (example: "Chemistry and Biology")."""


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


@dataclass(frozen=True, order=True)
class MetrologyArea(RefData):
    """A Metrology Area of a :class:`.Domain`."""

    domain: Domain
    """The Domain that the Metrology Area belongs to."""


@dataclass(frozen=True, order=True)
class Branch(RefData):
    """A Branch of a :class:`.MetrologyArea`."""

    metrology_area: MetrologyArea
    """The Metrology Area that the Branch belongs to."""


@dataclass(frozen=True, order=True)
class Service(RefData):
    """A Service for a :class:`.Branch`."""

    branch: Branch
    """The Branch that the Service belongs to."""

    physics_code: str
    """The physics code for this Service."""


@dataclass(frozen=True, order=True)
class SubService(RefData):
    """A Sub-Service of a :class:`.Service`."""

    physics_code: str
    """The physics code for this Sub Service."""

    service: Service
    """The Service that the Sub Service belongs to."""


@dataclass(frozen=True, order=True)
class IndividualService(RefData):
    """An Individual Service of a :class:`.SubService`."""

    physics_code: str
    """The physics code for this Individual Service."""

    sub_service: SubService
    """The Sub Service that the Individual Service belongs to."""


class ResultAggregation:
    """Aggregation representation."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Representation of an aggregation."""
        self.name: str = kwargs.get("name", "")
        """Aggregation name (example: "cmcCountries")."""

        self.values: list[str] = kwargs.get("values", [])
        """Aggreation values (example: ["Kazakhstan", "Portugal", "Greece"])."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultAggregation(name={self.name!r}, len(values)={len(self.values)})"


class ResultEquation:
    """Equation representation."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Representation of an equation."""
        self.equation: str = kwargs.get("equation", "")
        """Equation name."""

        self.equation_comment: str = kwargs.get("equationComment", "")
        """Equation comment."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultEquation(equation={self.equation!r}, equation_comment={self.equation_comment!r})"


class ResultFilter:
    """Filter representation."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Representation of a filter."""
        self.children: list[ResultFilter] = [ResultFilter(c) for c in kwargs.get("children", [])]
        """Filter children."""

        self.code: str = kwargs.get("code", "")
        """Filter code (example: "cmcMaterial")."""

        self.count: int = kwargs["count"]
        """Filter count."""

        self.name: str = kwargs.get("name", "")
        """Filter name (example: "cmcMaterial")."""

        self.order: int = kwargs["order"]
        """Filter order."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return (
            f"ResultFilter(code={self.code!r}, count={self.count}, "
            f"name={self.name!r}, order={self.order}, len(children)={len(self.children)})"
        )


class ResultParam:
    """Parameter representation."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Representation of a parameter."""
        self.parameter_name: str = kwargs.get("parameterName", "")
        """Parameter name (example: "S21 and S12")."""

        self.parameter_value: str = kwargs.get("parameterValue", "")
        """Parameter value (example: "-80 dB to 0 dB")."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultParam(parameter_name={self.parameter_name!r}, parameter_value={self.parameter_value!r})"


class ResultTable:
    """Table representation."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Representation of a table."""
        self.table_rows: int = kwargs["tableRows"]
        """Number of rows in table."""

        self.table_cols: int = kwargs["tableCols"]
        """Number of columns in table."""

        self.table_name: str = kwargs.get("tableName", "")
        """Table name (example: "CH_Scatt-Atten_Mag")."""

        self.table_comment: str = kwargs.get("tableComment", "")
        """Table comment."""

        self.table_contents: str = kwargs.get("tableContents", "")
        """Table contents (example: "{"row_1":{"col_1":"val_1","col_2":"val_2"}}")."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return (
            f"ResultTable(table_rows={self.table_rows}, table_cols={self.table_cols}, "
            f"table_name={self.table_name!r}, table_comment={self.table_comment!r})"
        )


class ResultUnit:
    """Units object definition."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Units object definition."""
        self.lower_limit: float | None = kwargs.get("lowerLimit")
        """Lower limit value."""

        self.unit: str = kwargs.get("unit", "")
        """Unit symbol (example: "%")."""

        self.upper_limit: float | None = kwargs.get("upperLimit")
        """Upper limit value."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultUnit(lower_limit={self.lower_limit}, unit={self.unit!r}, upper_limit={self.upper_limit})"


class Results:
    """Attributes for advanced search results."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Attributes for advanced search results."""
        self.number_of_elements: int = kwargs["numberOfElements"]
        """Number of elements on this page."""

        self.page_number: int = kwargs["pageNumber"]
        """Page number, 0 as first page."""

        self.page_size: int = kwargs["pageSize"]
        """Number of elements in the page."""

        self.total_elements: int = kwargs["totalElements"]
        """Total number of elements available."""

        self.total_pages: int = kwargs["totalPages"]
        """Total number of pages."""

        self.version_api_kcdb: str = kwargs.get("versionApiKcdb", "")
        """API KCDB version (example: "1.0.7")."""

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
    """Common attributes for advanced search results."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401, PLR0915
        """Attributes for advanced search results that are common."""
        self.id: int = kwargs["id"]
        """Document database id."""

        self.approval_date: str = kwargs.get("approvalDate", "")
        """Approval date (YYYY-MM-DD)."""

        k = kwargs.get("cmc")
        self.cmc: ResultUnit | None = ResultUnit(k) if k else None
        """CMC result unit."""

        k = kwargs.get("cmcBaseUnit")
        self.cmc_base_unit: ResultUnit | None = ResultUnit(k) if k else None
        """CMC base unit."""

        k = kwargs.get("cmcUncertainty")
        self.cmc_uncertainty: ResultUnit | None = ResultUnit(k) if k else None
        """CMC uncertainty."""

        k = kwargs.get("cmcUncertaintyBaseUnit")
        self.cmc_uncertainty_base_unit: ResultUnit | None = ResultUnit(k) if k else None
        """CMC uncertainty base unit."""

        self.comments: str = kwargs.get("comments", "")
        """Comments."""

        self.confidence_level: float | None = kwargs.get("confidenceLevel")
        """Confidence level."""

        self.country_value: str = kwargs.get("countryValue", "")
        """Country full name (example: "China")."""

        self.coverage_factor: float | None = kwargs.get("coverageFactor")
        """Coverage factor."""

        self.domain_code: str = kwargs.get("domainCode", "")
        """Domain code (example: "CHEM-BIO")."""

        self.group_identifier: str = kwargs.get("groupIdentifier", "")
        """Group identifier."""

        self.kcdb_code: str = kwargs.get("kcdbCode", "")
        """Document kcdb code (example: "APMP-QM-CN-00000JZR-1")."""

        self.metrology_area_label: str = kwargs.get("metrologyAreaLabel", "")
        """Metrology area label (example: "QM")."""

        self.nmi_code: str = kwargs.get("nmiCode", "")
        """NMI code (example: "NIM")."""

        self.nmi_name: str = kwargs.get("nmiName", "")
        """NMI name (example: "National Institute of Metrology")."""

        self.nmi_service_code: str = kwargs.get("nmiServiceCode", "")
        """NMI service code (example: "Other-11")."""

        self.nmi_service_link: str = kwargs.get("nmiServiceLink", "")
        """NMI service link."""

        self.publication_date: str = kwargs.get("publicationDate", "")
        """Publication date (YYYY-MM-DD)."""

        self.quantity_value: str = kwargs.get("quantityValue", "")
        """Quantity value (example: "Absorbed dose/rate")."""

        self.rmo: str = kwargs.get("rmo", "")
        """RMO acronym (example: "EURAMET")."""

        self.status: str = kwargs.get("status", "")
        """CMC status (example: "Published")."""

        self.status_date: str = kwargs.get("statusDate", "")
        """Last status date (YYYY-MM-DD)."""

        self.traceability_source: str = kwargs.get("traceabilitySource", "")
        """Traceability source (example: "VSL")."""

        k = kwargs.get("uncertaintyEquation")
        self.uncertainty_equation: ResultEquation | None = ResultEquation(k) if k else None
        """Uncertainty equation."""

        k = kwargs.get("uncertaintyMode")
        self.uncertainty_mode: AbsoluteRelative | None = AbsoluteRelative(k) if k else None
        """Uncertainty mode."""

        k = kwargs.get("uncertaintyTable")
        self.uncertainty_table: ResultTable | None = ResultTable(k) if k else None
        """Uncertainty table."""


class ResultChemistryAndBiology(ResultCommon):
    """Chemistry and Biology result."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Chemistry and Biology result."""
        super().__init__(kwargs)

        self.analyte_matrix: str = kwargs.get("analyteMatrix", "")
        """Analyte matrix (example: "high purity antimony")."""

        self.analyte_value: str = kwargs.get("analyteValue", "")
        """Analyte value (example: "antimony")."""

        self.category_value: str = kwargs.get("categoryValue", "")
        """Category value (example: "High purity chemicals")."""

        k = kwargs.get("crm")
        self.crm: ResultUnit | None = ResultUnit(k) if k else None
        """CRM unit."""

        self.crm_confidence_level: float | None = kwargs.get("crmConfidenceLevel")
        """CRM confidence level."""

        self.crm_coverage_factor: float | None = kwargs.get("crmCoverageFactor")
        """CRM coverage factor."""

        k = kwargs.get("crmUncertainty")
        self.crm_uncertainty: ResultUnit | None = ResultUnit(k) if k else None
        """CRM uncertainty."""

        k = kwargs.get("crmUncertaintyEquation")
        self.crm_uncertainty_equation: ResultEquation | None = ResultEquation(k) if k else None
        """CRM uncertainty equation."""

        k = kwargs.get("crmUncertaintyMode")
        self.crm_uncertainty_mode: AbsoluteRelative | None = AbsoluteRelative(k) if k else None
        """CRM uncertainty mode."""

        k = kwargs.get("crmUncertaintyTable")
        self.crm_uncertainty_table: ResultTable | None = ResultTable(k) if k else None
        """CRM uncertainty table."""

        self.measurment_technique: str = kwargs.get("measurmentTechnique", "")
        """Measurment technique (example: "Liquid-solid extraction with SPE cleanup and bracketing LC-IDMS/MS")."""

        self.mechanism: str = kwargs.get("mechanism", "")
        """Mechanism (example: "Customer service; GD-MS-200; delivery only to other NMIs")."""

        self.sub_category_value: str = kwargs.get("subCategoryValue", "")
        """Sub category value (example: "Metals")."""

        k = kwargs.get("uncertaintyConvention")
        self.uncertainty_convention: UncertaintyConvention | None = UncertaintyConvention(k) if k else None
        """Uncertainty convention."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultChemistryAndBiology(id={self.id}, nmi_code={self.nmi_code!r}, rmo={self.rmo!r})"


class ResultPhysics(ResultCommon):
    """Physics result."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Physics result."""
        super().__init__(kwargs)

        self.branch_value: str = kwargs.get("branchValue", "")
        """Branch value (example: "Radio frequency measurements")."""

        self.individual_service_value: str = kwargs.get("individualServiceValue", "")
        """Individual service value (example: "Transmission coefficient in coaxial line (real and imaginary)")."""

        self.instrument: str = kwargs.get("instrument", "")
        """Instrument (example: "Passive device")."""

        self.instrument_method: str = kwargs.get("instrumentMethod", "")
        """Instrument method (example: "Vector network analyser")."""

        self.international_standard: str = kwargs.get("internationalStandard", "")
        """International standard (example: "EURAMET Cg19, ISO 8655-6")."""

        self.parameters: list[ResultParam] = [ResultParam(p) for p in kwargs.get("parameters", [])]
        """Parameters list with name and value."""

        self.service_value: str = kwargs.get("serviceValue", "")
        """Service value (example: "Radio frequency measurements")."""

        self.sub_service_value: str = kwargs.get("subServiceValue", "")
        """Sub service value (example: "Scattering parameters (vectors)")."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultPhysics(id={self.id}, nmi_code={self.nmi_code!r}, rmo={self.rmo!r})"


class ResultRadiation(ResultCommon):
    """Radiation result."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Radiation result."""
        super().__init__(kwargs)

        self.branch_value: str = kwargs.get("branchValue", "")
        """Branch value (example: "Radio frequency measurements")."""

        self.instrument: str = kwargs.get("instrument", "")
        """Instrument (example: "Passive device")."""

        self.instrument_method: str = kwargs.get("instrumentMethod", "")
        """Instrument method (example: "Vector network analyser")."""

        self.international_standard: str = kwargs.get("internationalStandard", "")
        """International standard (example: "EURAMET Cg19, ISO 8655-6")."""

        self.medium_value: str = kwargs.get("mediumValue", "")
        """Medium value (example: "Liquid")."""

        self.nuclide_value: str = kwargs.get("nuclideValue", "")
        """Nuclide value (example: "Cr-51")."""

        self.radiation_code: str = kwargs.get("radiationCode", "")
        """Radiation code separated by a dot for branch, quantity, source, medium (example: "2.1.3.2")."""

        self.radiation_specification: str = kwargs.get("radiationSpecification", "")
        """Radiation specification name (example: "10 ml to 500 ml NMIJ/AIST standard cylindrical plastic bottle")."""

        self.reference_standard: str = kwargs.get("referenceStandard", "")
        """Reference standard (example: "Comparison with the NMIJ/AIST standard source")."""

        self.source_value: str = kwargs.get("sourceValue", "")
        """Source value (example: "Multi-radionuclide source")."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultRadiation(id={self.id}, nmi_code={self.nmi_code!r}, rmo={self.rmo!r})"


class ResultsChemistryAndBiology(Results):
    """Chemistry and Biology search results."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Chemistry and Biology search results."""
        super().__init__(kwargs)

        self.data: list[ResultChemistryAndBiology] = [ResultChemistryAndBiology(d) for d in kwargs.get("data", [])]
        """The chemistry and biology result data."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultsChemistryAndBiology({super().__repr__()})"


class ResultsPhysics(Results):
    """Physics search results."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Physics search results."""
        super().__init__(kwargs)

        self.data: list[ResultPhysics] = [ResultPhysics(d) for d in kwargs.get("data", [])]
        """The physics result data."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultsPhysics({super().__repr__()})"


class ResultsQuickSearch(Results):
    """Quick search results."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Quick search results."""
        super().__init__(kwargs)

        self.aggregations: list[ResultAggregation] = [ResultAggregation(d) for d in kwargs.get("aggregations", [])]
        """The aggregations list."""

        self.data: list[Any] = kwargs.get("data", [])
        """The quick search results data."""

        self.filters_list: list[ResultFilter] = [ResultFilter(d) for d in kwargs.get("filtersList", [])]
        """The filters list."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return (
            f"ResultsQuickSearch({super().__repr__()}, "
            f"len(aggregations)={len(self.aggregations)}, "
            f"len(filters_list)={len(self.filters_list)})"
        )


class ResultsRadiation(Results):
    """Radiation search results."""

    def __init__(self, kwargs: Any) -> None:  # noqa: ANN401
        """Radiation search results."""
        super().__init__(kwargs)

        self.data: list[ResultRadiation] = [ResultRadiation(d) for d in kwargs.get("data", [])]
        """The radiation results data."""

    def __repr__(self) -> str:
        """Return the object representation."""
        return f"ResultsRadiation({super().__repr__()})"
