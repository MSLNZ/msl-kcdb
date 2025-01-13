from datetime import date

import pytest

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
            countries=["CH", Country(id=29, label="FR", value="France"), "JP", "AR"],
            public_date_from=date(2005, 1, 31),
            public_date_to="2024-06-30",
            show_table=True,
        )

        assert str(physics) == (
            "ResultsGeneralPhysics(number_of_elements=1, page_number=0, page_size=100, "
            "total_elements=1, total_pages=1, version_api_kcdb='1.0.8')"
        )

        assert physics.version_api_kcdb == "1.0.8"
        assert physics.page_number == 0
        assert physics.page_size == 100
        assert physics.number_of_elements == 1
        assert physics.total_elements == 1
        assert physics.total_pages == 1
        assert len(physics.data) == 1
        data = physics.data[0]
        assert str(data) == "ResultGeneralPhysics(id=26707, nmi_code='INTI', rmo='SIM')"
        assert data.id == 26707
        assert data.status == "Published"
        assert data.status_date == "2025-01-09"
        assert data.kcdb_code == "SIM-EM-AR-00000K2C-1"
        assert data.domain_code == "PHYSICS"
        assert data.metrology_area_label == "EM"
        assert data.rmo == "SIM"
        assert data.country_value == "Argentina"
        assert data.nmi_code == "INTI"
        assert data.nmi_name == "Instituto Nacional de Tecnologia Industrial"
        assert data.nmi_service_code == ""
        assert data.nmi_service_link == ""
        assert data.quantity_value == "Scattering parameters: transmission coefficient (Sij) in coaxial line, phase"
        assert data.cmc is not None
        assert str(data.cmc) == "ResultUnit(lower_limit=-180.0, unit='°', upper_limit=180.0)"
        assert data.cmc.lower_limit == -180.0
        assert data.cmc.upper_limit == 180.0
        assert data.cmc.unit == "°"
        assert data.cmc_uncertainty is not None
        assert str(data.cmc_uncertainty) == "ResultUnit(lower_limit=0.2, unit='°', upper_limit=8.9)"
        assert data.cmc_uncertainty.lower_limit == 0.2
        assert data.cmc_uncertainty.upper_limit == 8.9
        assert data.cmc_uncertainty.unit == "°"
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
            == "ResultUnit(lower_limit=0.0034906585039886605, unit='rad', upper_limit=0.15533430342749538)"
        )
        assert data.cmc_uncertainty_base_unit.lower_limit == 0.0034906585039886605
        assert data.cmc_uncertainty_base_unit.upper_limit == 0.15533430342749538
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
            == "ResultTable(table_rows=21, table_cols=7, table_name='Matrix 5', table_comment='')"
        )
        assert data.uncertainty_table.table_name == "Matrix 5"
        assert data.uncertainty_table.table_rows == 21
        assert data.uncertainty_table.table_cols == 7
        assert data.uncertainty_table.table_comment == ""
        assert data.uncertainty_table.table_contents.startswith(
            '{"row_1": {"col_1":"<div Style=\\"FONT-FAMILY: Calibri;FONT-SIZE:'
        )
        assert data.uncertainty_mode is not None
        assert data.uncertainty_mode.name == "ABSOLUTE"
        assert data.uncertainty_mode.value == "Absolute"
        assert data.traceability_source == "INTI"
        assert data.comments == ""
        assert data.group_identifier == ""
        assert data.publication_date == "2020-04-16"
        assert data.approval_date == "2019-10-15"
        assert data.international_standard == ""
        assert data.branch_value == "Radio frequency measurements"
        assert data.service_value == "Radio frequency measurements"
        assert data.sub_service_value == "Scattering parameters (vectors)"
        assert data.individual_service_value == "Transmission coefficient in coaxial line (real and imaginary)"
        assert data.instrument == "Passive devices"
        assert data.instrument_method == "Vector Network Analyzer"
        assert len(data.parameters) == 2
        assert str(data.parameters[0]) == "ResultParam(parameter_name='Frequency', parameter_value='1 MHz to 32 GHz')"
        assert data.parameters[1].parameter_name == "Connector"
        assert data.parameters[1].parameter_value == "Type-N, PC3.5mm"

    def test_services(self) -> None:
        """Test GeneralPhysics.services()."""
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

    def test_services_radiation_branches(self) -> None:
        """Test GeneralPhysics.services() for Ionizing Radiation branches."""
        radiation = IonizingRadiation()
        for area in radiation.metrology_areas():
            for branch in radiation.branches(area):
                assert not self.physics.services(branch)

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

    def test_timeout(self) -> None:
        """Test timeout error message."""
        original = self.physics.timeout

        # Making the timeout value be around 1 second causes a TimeoutError
        # instead of a urllib.error.URLError if it is too small
        self.physics.timeout = 0.9
        with pytest.raises(TimeoutError, match=r"No reply from KCDB server after 0.9 seconds"):
            self.physics.search("M")

        self.physics.timeout = original
