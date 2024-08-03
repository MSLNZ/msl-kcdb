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

    def test_search(self) -> None:
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

        assert physics.total_elements == 1
        assert physics.data[0].nmi_code == "METAS"
        assert physics.data[0].nmi_service_code == "217.01.04"

        assert str(physics) == (
            f"ResultsGeneralPhysics(number_of_elements=1, page_number=0, page_size=100, "
            f"total_elements=1, total_pages=1, version_api_kcdb={physics.version_api_kcdb!r})"
        )

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
