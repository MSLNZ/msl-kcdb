"""Reference data and Results classes for the KCDB API.

These classes represent the `xs:complexType` and `xs:simpleType` definitions in the
[KCDB XSD Schema](https://www.bipm.org/api/kcdb/cmc/searchData/xsdSchema){:target="_blank"}.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


class AbsoluteRelative(Enum):
    """CRM uncertainty mode.

    Attributes:
        ABSOLUTE (str): `"Absolute"`
        RELATIVE (str): `"Relative"`
    """

    ABSOLUTE = "Absolute"
    RELATIVE = "Relative"


class Status(Enum):
    """CMC Status.

    Attributes:
        PUBLISHED (str): `"Published"`
        ARCHIVED (str): `"Archived"`
        DELETED (str): `"Deleted"`
        GREYED_OUT (str): `"Greyed out"`
    """

    PUBLISHED = "Published"
    ARCHIVED = "Archived"
    DELETED = "Deleted"
    GREYED_OUT = "Greyed out"


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

    name: str
    values: list[str]

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of an aggregation."""
        self.name = kwargs.get("name") or ""
        self.values = kwargs.get("values", [])

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        """Return the object representation."""
        return f"ResultAggregation(name={self.name!r}, len(values)={len(self.values)})"


class ResultEquation:
    """Equation representation.

    Attributes:
        equation: Equation name.
        equation_comment: Equation comment.
    """

    equation: str
    equation_comment: str

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of an equation."""
        self.equation = kwargs.get("equation") or ""
        self.equation_comment = kwargs.get("equationComment") or ""

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
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

    children: list[ResultFilter]
    code: str
    count: int
    name: str
    order: int

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of a filter."""
        self.children = [ResultFilter(c) for c in kwargs.get("children", [])]
        self.code = kwargs.get("code") or ""
        self.count = kwargs["count"]
        self.name = kwargs.get("name") or ""
        self.order = kwargs["order"]

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
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

    parameter_name: str
    parameter_value: str

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of a parameter."""
        self.parameter_name = kwargs.get("parameterName") or ""
        self.parameter_value = kwargs.get("parameterValue") or ""

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
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

    table_rows: int
    table_cols: int
    table_name: str
    table_comment: str
    table_contents: str

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Representation of a table."""
        self.table_rows = kwargs["tableRows"]
        self.table_cols = kwargs["tableCols"]
        self.table_name = kwargs.get("tableName") or ""
        self.table_comment = kwargs.get("tableComment") or ""
        self.table_contents = kwargs.get("tableContents") or ""

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
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

    lower_limit: float | None
    unit: str
    upper_limit: float | None

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Units object definition."""
        self.lower_limit = kwargs.get("lowerLimit")
        self.unit = kwargs.get("unit") or ""
        self.upper_limit = kwargs.get("upperLimit")

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
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
        version_api_kcdb: KCDB API version. _Example:_ `"1.0.13"`
    """

    number_of_elements: int
    page_number: int
    page_size: int
    total_elements: int
    total_pages: int
    version_api_kcdb: str

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Attributes for advanced search results."""
        self.number_of_elements = kwargs["numberOfElements"]
        self.page_number = kwargs["pageNumber"]
        self.page_size = kwargs["pageSize"]
        self.total_elements = kwargs["totalElements"]
        self.total_pages = kwargs["totalPages"]
        self.version_api_kcdb = kwargs.get("versionApiKcdb") or ""

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
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
        nmi_identifier: KCDB NMI identifier. _Example:_ `24`
        nmi_name: NMI name. _Example:_ `"National Institute of Metrology"`
        nmi_ror_identifier: NMI ROR identifier. _Example:_ `"02m5haa59"`
        nmi_service_code: NMI service code. _Example:_ `"NIM/11.1.4a"`
        nmi_service_link: NMI service link.
        nmi_wiki_data_identifier: NMI wiki data identifier. _Example:_ `"Q11293816"`
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

    id: int
    approval_date: str
    cmc: ResultUnit | None
    cmc_base_unit: ResultUnit | None
    cmc_uncertainty: ResultUnit | None
    cmc_uncertainty_base_unit: ResultUnit | None
    comments: str
    confidence_level: float | None
    country_value: str
    coverage_factor: float | None
    domain_code: str
    group_identifier: str
    kcdb_code: str
    metrology_area_label: str
    nmi_code: str
    nmi_identifier: int
    nmi_name: str
    nmi_ror_identifier: str
    nmi_service_code: str
    nmi_service_link: str
    nmi_wiki_data_identifier: str
    publication_date: str
    quantity_value: str
    rmo: str
    status: str
    status_date: str
    traceability_source: str
    uncertainty_equation: ResultEquation | None
    uncertainty_mode: AbsoluteRelative | None
    uncertainty_table: ResultTable | None

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Attributes for advanced search results that are common."""
        self.id = kwargs["id"]
        self.approval_date = kwargs.get("approvalDate") or ""

        k = kwargs.get("cmc")
        self.cmc = ResultUnit(k) if k else None

        k = kwargs.get("cmcBaseUnit")
        self.cmc_base_unit = ResultUnit(k) if k else None

        k = kwargs.get("cmcUncertainty")
        self.cmc_uncertainty = ResultUnit(k) if k else None

        k = kwargs.get("cmcUncertaintyBaseUnit")
        self.cmc_uncertainty_base_unit = ResultUnit(k) if k else None

        self.comments = kwargs.get("comments") or ""
        self.confidence_level = kwargs.get("confidenceLevel")
        self.country_value = kwargs.get("countryValue") or ""
        self.coverage_factor = kwargs.get("coverageFactor")
        self.domain_code = kwargs.get("domainCode") or ""
        self.group_identifier = kwargs.get("groupIdentifier") or ""
        self.kcdb_code = kwargs.get("kcdbCode") or ""
        self.metrology_area_label = kwargs.get("metrologyAreaLabel") or ""
        self.nmi_code = kwargs.get("nmiCode") or ""
        self.nmi_identifier = kwargs.get("nmiIdentifier", -1)
        self.nmi_name = kwargs.get("nmiName") or ""
        self.nmi_ror_identifier = kwargs.get("nmiRorIdentifier") or ""
        self.nmi_service_code = kwargs.get("nmiServiceCode") or ""
        self.nmi_service_link = kwargs.get("nmiServiceLink") or ""
        self.nmi_wiki_data_identifier = kwargs.get("nmiWikiDataIdentifier") or ""
        self.publication_date = kwargs.get("publicationDate") or ""
        self.quantity_value = kwargs.get("quantityValue") or ""
        self.rmo = kwargs.get("rmo") or ""
        self.status = kwargs.get("status") or ""
        self.status_date = kwargs.get("statusDate") or ""
        self.traceability_source = kwargs.get("traceabilitySource") or ""

        k = kwargs.get("uncertaintyEquation")
        self.uncertainty_equation = ResultEquation(k) if k else None

        k = kwargs.get("uncertaintyMode")
        self.uncertainty_mode = AbsoluteRelative(k) if k else None

        k = kwargs.get("uncertaintyTable")
        self.uncertainty_table = ResultTable(k) if k else None


class ResultChemistryBiology(ResultCommon):
    """Chemistry and Biology result.

    Attributes:
        analyte_matrix: Analyte matrix. _Example:_ `"high purity antimony"`
        analyte_value: Analyte value. _Example:_ `"antimony"`
        category_label: Category identifier. _Example:_ `1`
        category_value: Category value. _Example:_ `"High purity chemicals"`
        crm: CRM unit.
        crm_confidence_level: CRM confidence level.
        crm_coverage_factor: CRM coverage factor.
        crm_uncertainty: CRM uncertainty.
        crm_uncertainty_equation: CRM uncertainty equation.
        crm_uncertainty_mode: CRM uncertainty mode.
        crm_uncertainty_table: CRM uncertainty table.
        kcdb_service_category: KCDB service category. _Example:_ `"QM-5.1"`
        measurement_technique: Measurement technique.
            _Example:_ `"Liquid-solid extraction with SPE cleanup and bracketing LC-IDMS/MS"`
        mechanism: Mechanism. _Example:_ `"Customer service; GD-MS-200; delivery only to other NMIs"`
        sub_category_label: Sub category identifier. _Example:_ `1`
        sub_category_value: Sub category value. _Example:_ `"Fresh water"`
        uncertainty_convention: Uncertainty convention.
    """

    analyte_matrix: str
    analyte_value: str
    category_label: int
    category_value: str
    crm: ResultUnit | None
    crm_confidence_level: float | None
    crm_coverage_factor: float | None
    crm_uncertainty: ResultUnit | None
    crm_uncertainty_equation: ResultEquation | None
    crm_uncertainty_mode: AbsoluteRelative | None
    crm_uncertainty_table: ResultTable | None
    kcdb_service_category: str
    measurement_technique: str
    mechanism: str
    sub_category_label: int
    sub_category_value: str
    uncertainty_convention: UncertaintyConvention | None

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Chemistry and Biology result."""
        super().__init__(kwargs)

        self.analyte_matrix = kwargs.get("analyteMatrix") or ""
        self.analyte_value = kwargs.get("analyteValue") or ""
        self.category_label = kwargs.get("categoryLabel", -1)
        self.category_value = kwargs.get("categoryValue") or ""

        k = kwargs.get("crm")
        self.crm = ResultUnit(k) if k else None

        self.crm_confidence_level = kwargs.get("crmConfidenceLevel")
        self.crm_coverage_factor = kwargs.get("crmCoverageFactor")

        k = kwargs.get("crmUncertainty")
        self.crm_uncertainty = ResultUnit(k) if k else None

        k = kwargs.get("crmUncertaintyEquation")
        self.crm_uncertainty_equation = ResultEquation(k) if k else None

        k = kwargs.get("crmUncertaintyMode")
        self.crm_uncertainty_mode = AbsoluteRelative(k) if k else None

        k = kwargs.get("crmUncertaintyTable")
        self.crm_uncertainty_table = ResultTable(k) if k else None

        self.kcdb_service_category = kwargs.get("kcdbServiceCategory") or ""

        # Note spelling mistake in "measurmentTechnique" is what the KCDB API returns cSpell:disable-line
        self.measurement_technique = kwargs.get("measurmentTechnique") or ""  # cSpell:disable-line
        self.mechanism = kwargs.get("mechanism") or ""
        self.sub_category_label = kwargs.get("subCategoryLabel", -1)
        self.sub_category_value = kwargs.get("subCategoryValue") or ""

        k = kwargs.get("uncertaintyConvention")
        self.uncertainty_convention = UncertaintyConvention(k) if k else None

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        """Return the object representation."""
        return f"ResultChemistryBiology(id={self.id}, nmi_code={self.nmi_code!r}, rmo={self.rmo!r})"


class ResultPhysics(ResultCommon):
    """General Physics result.

    Attributes:
        branch_label: Branch label. _Example:_ `"PR/Photo"`
        branch_value: Branch value. _Example:_ `"Photometry"`
        individual_service_value: Individual service value. _Example:_ `"Tungsten source"`
        instrument: Instrument. _Example:_ `"Illuminance meter"`
        instrument_method: Instrument method. _Example:_ `"Standard lamp"`
        international_standard: International standard. _Example:_ `"EURAMET Cg19, ISO 8655-6"`
        kcdb_service_category: KCDB service category. _Example:_ `"PR/Photo-1.2.1"`
        parameters: Parameters list with name and value.
        physics_code: Physics code. _Example:_ `"1.2.1"`
        service_value: Service value. _Example:_ `"Photometry"`
        sub_service_value: Sub service value. _Example:_ `"Illuminance responsivity"`
    """

    branch_label: str
    branch_value: str
    individual_service_value: str
    instrument: str
    instrument_method: str
    international_standard: str
    kcdb_service_category: str
    parameters: list[ResultParam]
    physics_code: str
    service_value: str
    sub_service_value: str

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """General Physics result."""
        super().__init__(kwargs)
        self.branch_label = kwargs.get("branchLabel") or ""
        self.branch_value = kwargs.get("branchValue") or ""
        self.individual_service_value = kwargs.get("individualServiceValue") or ""
        self.instrument = kwargs.get("instrument") or ""
        self.instrument_method = kwargs.get("instrumentMethod") or ""
        self.international_standard = kwargs.get("internationalStandard") or ""
        self.kcdb_service_category = kwargs.get("kcdbServiceCategory") or ""
        self.parameters = [ResultParam(p) for p in kwargs.get("parameters", [])]
        self.physics_code = kwargs.get("physicsCode") or ""
        self.service_value = kwargs.get("serviceValue") or ""
        self.sub_service_value = kwargs.get("subServiceValue") or ""

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        """Return the object representation."""
        return f"ResultPhysics(id={self.id}, nmi_code={self.nmi_code!r}, rmo={self.rmo!r})"


class ResultRadiation(ResultCommon):
    """Ionizing Radiation result.

    Attributes:
        branch_label: Branch label. _Example:_ `"RAD"`
        branch_value: Branch value. _Example:_ `"Radioactivity"`
        instrument: Instrument. _Example:_ `"Multiple nuclide source, solution"`
        instrument_method: Instrument method. _Example:_ `"Ge detector, multichannel analyzer"`
        international_standard: International standard. _Example:_ `"EURAMET Cg19, ISO 8655-6"`
        kcdb_service_category: KCDB service category. _Example:_ `"RI/RAD-1.3.2"`
        medium_value: Medium value. _Example:_ `"Liquid"`
        nuclide_value: Nuclide value. _Example:_ `"Cr-51"`
        radiation_code: Radiation code separated by a dot for branch, quantity, source, medium. _Example:_ `"2.1.3.2"`
        radiation_specification: Radiation specification name.
            _Example:_ `"10 ml to 500 ml NMIJ/AIST standard cylindrical plastic bottle"`
        reference_standard: Reference standard. _Example:_ `"Comparison with the NMIJ/AIST standard source"`
        source_value: Source value. _Example:_ `"Multi-radionuclide source"`
    """

    branch_label: str
    branch_value: str
    instrument: str
    instrument_method: str
    international_standard: str
    kcdb_service_category: str
    medium_value: str
    nuclide_value: str
    radiation_code: str
    radiation_specification: str
    reference_standard: str
    source_value: str

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Ionizing Radiation result."""
        super().__init__(kwargs)
        self.branch_label = kwargs.get("branchLabel") or ""
        self.branch_value = kwargs.get("branchValue") or ""
        self.instrument = kwargs.get("instrument") or ""
        self.instrument_method = kwargs.get("instrumentMethod") or ""
        self.international_standard = kwargs.get("internationalStandard") or ""
        self.kcdb_service_category = kwargs.get("kcdbServiceCategory") or ""
        self.medium_value = kwargs.get("mediumValue") or ""
        self.nuclide_value = kwargs.get("nuclideValue") or ""
        self.radiation_code = kwargs.get("radiationCode") or ""
        self.radiation_specification = kwargs.get("radiationSpecification") or ""
        self.reference_standard = kwargs.get("referenceStandard") or ""
        self.source_value = kwargs.get("sourceValue") or ""

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        """Return the object representation."""
        return f"ResultRadiation(id={self.id}, nmi_code={self.nmi_code!r}, rmo={self.rmo!r})"


class ResultsChemistryBiology(Results):
    """Chemistry and Biology search results.

    Attributes:
        data: Chemistry and Biology result data.
    """

    data: list[ResultChemistryBiology]

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Chemistry and Biology search results."""
        super().__init__(kwargs)
        self.data = [ResultChemistryBiology(d) for d in kwargs.get("data", [])]

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        """Return the object representation."""
        return f"ResultsChemistryBiology({super().__repr__()})"


class ResultsPhysics(Results):
    """General Physics search results.

    Attributes:
        data: General Physics result data.
    """

    data: list[ResultPhysics]

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """General Physics search results."""
        super().__init__(kwargs)
        self.data = [ResultPhysics(d) for d in kwargs.get("data", [])]

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        """Return the object representation."""
        return f"ResultsPhysics({super().__repr__()})"


class ResultsQuickSearch(Results):
    """Quick search results.

    Attributes:
        aggregations: The aggregations list.
        data: The quick search result data.
        filters_list: The filters list.
    """

    aggregations: list[ResultAggregation]
    data: list[dict[str, Any]]
    filters_list: list[ResultFilter]

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Quick search results."""
        super().__init__(kwargs)
        self.aggregations = [ResultAggregation(d) for d in kwargs.get("aggregations", [])]
        self.data = kwargs.get("data", [])
        self.filters_list = [ResultFilter(d) for d in kwargs.get("filtersList", [])]

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        """Return the object representation."""
        return (
            f"ResultsQuickSearch({super().__repr__()}, "
            f"len(aggregations)={len(self.aggregations)}, "
            f"len(filters_list)={len(self.filters_list)})"
        )


class ResultsRadiation(Results):
    """Ionizing Radiation search results.

    Attributes:
        data: Ionizing Radiation result data.
    """

    data: list[ResultRadiation]

    def __init__(self, kwargs: dict[str, Any]) -> None:
        """Ionizing Radiation search results."""
        super().__init__(kwargs)
        self.data = [ResultRadiation(d) for d in kwargs.get("data", [])]

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        """Return the object representation."""
        return f"ResultsRadiation({super().__repr__()})"
