from datetime import date

from msl.kcdb import ChemistryBiology, GeneralPhysics, IonizingRadiation
from msl.kcdb.classes import Country


class TestGeneralPhysics:
    """Test the GeneralPhysics class."""

    def setup_class(self) -> None:
        """Create GeneralPhysics instance."""
        self.physics = GeneralPhysics()
        self.metrology_areas = self.physics.metrology_areas()

    def test_branches(self) -> None:
        """Test GeneralPhysics.branches()."""
        areas = self.physics.filter(self.metrology_areas, "TF")
        assert len(areas) == 1
        branches = self.physics.branches(areas[0])
        assert len(branches) == 3

        t, *rest = self.physics.filter(branches, "interval")
        assert not rest
        assert t.id == 28
        assert t.label == "TF/TI"
        assert t.value == "Time interval"
        assert t.metrology_area.id == 7
        assert t.metrology_area.label == "TF"
        assert t.metrology_area.value == "Time and Frequency"

    def test_branches_chem_bio(self) -> None:
        """Test GeneralPhysics.branches() for Chemistry and Biology areas."""
        chem_bio = ChemistryBiology()
        for area in chem_bio.metrology_areas():
            branches = self.physics.branches(area)
            assert not branches

    def test_branches_radiation(self) -> None:
        """Test GeneralPhysics.branches() for Ionizing Radiation areas."""
        rad = IonizingRadiation()
        for area in rad.metrology_areas():
            branches = self.physics.branches(area)
            assert not branches

    def test_domain(self) -> None:
        """Test GeneralPhysics.DOMAIN class attribute."""
        chem_bio, phys, rad = sorted(self.physics.domains())
        assert phys == self.physics.DOMAIN
        assert phys.code == "PHYSICS"
        assert phys.name == "General physics"

    def test_individual_services(self) -> None:
        """Test GeneralPhysics.individual_services()."""
        areas = self.physics.filter(self.metrology_areas, "TF")
        assert len(areas) == 1
        branches = self.physics.filter(self.physics.branches(areas[0]), r"TF/F")
        assert len(branches) == 1
        services = self.physics.filter(self.physics.services(branches[0]), "Frequency")
        assert len(services) == 1
        sub_services = self.physics.filter(self.physics.sub_services(services[0]), "Frequency meter")
        assert len(sub_services) == 1
        individual_services = self.physics.individual_services(sub_services[0])
        assert len(individual_services) == 2

        counter, *rest = self.physics.filter(individual_services, "counter")
        assert not rest
        assert counter.id == 546
        assert counter.label == "1"
        assert counter.value == "Frequency counter"
        assert counter.physics_code == "2.3.1"
        assert counter.sub_service.id == 218
        assert counter.sub_service.physics_code == "2.3"
        assert counter.sub_service.service.id == 55
        assert counter.sub_service.service.physics_code == "2"
        assert counter.sub_service.service.branch.id == 27
        assert counter.sub_service.service.branch.metrology_area.id == 7

    def test_individual_services_no_http_404_error(self) -> None:
        """Test GeneralPhysics.individual_services() for HTTP 404 error."""
        areas = self.physics.filter(self.metrology_areas, "L")
        assert len(areas) == 1
        branches = self.physics.filter(self.physics.branches(areas[0]), r"L/DimMet")
        assert len(branches) == 1
        services = self.physics.filter(self.physics.services(branches[0]), "Various dimensional")
        assert len(services) == 1
        sub_services = self.physics.filter(self.physics.sub_services(services[0]), "7")
        assert len(sub_services) == 1

        individual_services = self.physics.individual_services(sub_services[0])
        assert not individual_services

    def test_metrology_area(self) -> None:
        """Test GeneralPhysics.metrology_areas()."""
        assert len(self.metrology_areas) == 7
        therm, *rest = self.physics.filter(self.metrology_areas, "Thermometry")
        assert not rest
        assert therm.id == 6
        assert therm.label == "T"
        assert therm.value == "Thermometry"
        assert therm.domain.code == "PHYSICS"
        assert therm.domain.name == "General physics"

    def test_repr(self) -> None:
        """Test string representation."""
        assert str(self.physics) == "GeneralPhysics(code='PHYSICS', name='General physics')"

    def test_search(self) -> None:  # noqa: PLR0915
        """Test GeneralPhysics.search()."""
        physics = self.physics.search(
            "EM",
            branch="EM/RF",
            physics_code="11.3.3",
            keywords="phase OR multichannel OR water",
            countries=["CH", Country(id=29, label="FR", value="France"), "JP"],
            public_date_from=date(2005, 1, 31),
            public_date_to="2024-06-30",
            show_table=True,
        )

        assert str(physics) == (
            "ResultsGeneralPhysics(number_of_elements=1, page_number=0, page_size=100, "
            "total_elements=1, total_pages=1, version_api_kcdb='1.0.7')"
        )

        assert physics.version_api_kcdb == "1.0.7"
        assert physics.page_number == 0
        assert physics.page_size == 100
        assert physics.number_of_elements == 1
        assert physics.total_elements == 1
        assert physics.total_pages == 1
        assert len(physics.data) == 1
        data = physics.data[0]
        assert str(data) == "ResultGeneralPhysics(id=35071, nmi_code='METAS', rmo='EURAMET')"
        assert data.id == 35071
        assert data.status == "Published"
        assert data.status_date == "2022-01-04"
        assert data.kcdb_code == "EURAMET-EM-CH-00000GFB-5"
        assert data.domain_code == "PHYSICS"
        assert data.metrology_area_label == "EM"
        assert data.rmo == "EURAMET"
        assert data.country_value == "Switzerland"
        assert data.nmi_code == "METAS"
        assert data.nmi_name == "Federal Institute of Metrology"
        assert data.nmi_service_code == "217.01.04"
        assert data.nmi_service_link == ""
        assert data.quantity_value == "Scattering parameters: transmission coefficient (Sij) in coaxial line, phase"
        assert data.cmc is not None
        assert str(data.cmc) == "ResultUnit(lower_limit=-180.0, unit='degree', upper_limit=180.0)"
        assert data.cmc.lower_limit == -180.0
        assert data.cmc.upper_limit == 180.0
        assert data.cmc.unit == "degree"
        assert data.cmc_uncertainty is not None
        assert str(data.cmc_uncertainty) == "ResultUnit(lower_limit=0.2, unit='degree', upper_limit=1.4)"
        assert data.cmc_uncertainty.lower_limit == 0.2
        assert data.cmc_uncertainty.upper_limit == 1.4
        assert data.cmc_uncertainty.unit == "degree"
        assert data.cmc_base_unit is not None
        assert (
            str(data.cmc_base_unit)
            == "ResultUnit(lower_limit=-3.141592653589794, unit='rad', upper_limit=3.141592653589794)"
        )
        assert data.cmc_base_unit.lower_limit == -3.141592653589794
        assert data.cmc_base_unit.upper_limit == 3.141592653589794
        assert data.cmc_base_unit.unit == "rad"
        assert data.cmc_uncertainty_base_unit is not None
        assert (
            str(data.cmc_uncertainty_base_unit)
            == "ResultUnit(lower_limit=0.0034906585039886605, unit='rad', upper_limit=0.024434609527920616)"
        )
        assert data.cmc_uncertainty_base_unit.lower_limit == 0.0034906585039886605
        assert data.cmc_uncertainty_base_unit.upper_limit == 0.024434609527920616
        assert data.cmc_uncertainty_base_unit.unit == "rad"
        assert data.confidence_level == 95
        assert data.coverage_factor == 2
        assert data.uncertainty_equation is not None
        assert str(data.uncertainty_equation) == "ResultEquation(equation='', equation_comment='')"
        assert data.uncertainty_equation.equation == ""
        assert data.uncertainty_equation.equation_comment == ""
        assert data.uncertainty_table is not None
        assert (
            str(data.uncertainty_table)
            == "ResultTable(table_rows=122, table_cols=13, table_name='Scat_coax_atten_phase', table_comment='')"
        )
        assert data.uncertainty_table.table_name == "Scat_coax_atten_phase"
        assert data.uncertainty_table.table_rows == 122
        assert data.uncertainty_table.table_cols == 13
        assert data.uncertainty_table.table_comment == ""
        assert data.uncertainty_table.table_contents.startswith('{"row_1":{"col_1":"Connector",')
        assert data.uncertainty_mode is not None
        assert data.uncertainty_mode.name == "ABSOLUTE"
        assert data.uncertainty_mode.value == "Absolute"
        assert data.traceability_source == "METAS"
        assert data.comments == ""
        assert data.group_identifier == "F"
        assert data.publication_date == "2022-01-04"
        assert data.approval_date == "2022-01-04"
        assert data.international_standard == ""
        assert data.branch_value == "Radio frequency measurements"
        assert data.service_value == "Radio frequency measurements"
        assert data.sub_service_value == "Scattering parameters (vectors)"
        assert data.individual_service_value == "Transmission coefficient in coaxial line (real and imaginary)"
        assert data.instrument == "Passive device"
        assert data.instrument_method == "Vector network analyser"
        assert len(data.parameters) == 4
        assert (
            str(data.parameters[0]) == "ResultParam(parameter_name='Frequency', parameter_value='9 kHz to 116.5 GHz')"
        )
        assert data.parameters[1].parameter_name == "Connector"
        assert data.parameters[1].parameter_value == (
            "BNC 50 ohm,<br />\r\nType-N 75 ohm,<br />\r\n4.3-10<br />\r\nType-N 50 ohm,<br />\r\n"
            "PC-7 mm,<br />\r\nNEX10,<br />\r\nPC-3.5 mm,<br />\r\nPC-2.92 mm,<br />\r\n"
            "PC-2.4 mm,<br />\r\nPC-1.85 mm,<br />\r\nPC-1.0 mm"
        )
        assert data.parameters[2].parameter_name == "S11 and S22"
        assert data.parameters[2].parameter_value == "&lt; 0.1"
        assert data.parameters[3].parameter_name == "S21 and S12"
        assert data.parameters[3].parameter_value == "-80 dB to 0 dB"

    def test_services(self) -> None:
        """Test GeneralPhysics.search()."""
        areas = self.physics.filter(self.metrology_areas, "TF")
        assert len(areas) == 1
        branches = self.physics.filter(self.physics.branches(areas[0]), r"TF/F")
        assert len(branches) == 1
        services = self.physics.services(branches[0])
        assert len(services) == 1

        service = services[0]
        assert service.id == 55
        assert service.label == "2"
        assert service.value == "Frequency"
        assert service.physics_code == "2"
        assert service.branch.id == 27
        assert service.branch.metrology_area.id == 7

    def test_sub_services(self) -> None:
        """Test GeneralPhysics.sub_services()."""
        areas = self.physics.filter(self.metrology_areas, "TF")
        assert len(areas) == 1
        branches = self.physics.filter(self.physics.branches(areas[0]), r"TF/F")
        assert len(branches) == 1
        services = self.physics.filter(self.physics.services(branches[0]), "Frequency")
        assert len(services) == 1
        sub_services = self.physics.sub_services(services[0])
        assert len(sub_services) == 3

        meter, *rest = self.physics.filter(sub_services, "meter")
        assert not rest
        assert meter.id == 218
        assert meter.label == "3"
        assert meter.value == "Frequency meter"
        assert meter.physics_code == "2.3"
        assert meter.service.id == 55
        assert meter.service.physics_code == "2"
        assert meter.service.branch.id == 27
        assert meter.service.branch.metrology_area.id == 7
