from datetime import date

from msl.kcdb import ChemistryBiology, GeneralPhysics, IonizingRadiation
from msl.kcdb.classes import Country


class TestIonizingRadiation:
    """Test the IonizingRadiation class."""

    def setup_class(self) -> None:
        """Create IonizingRadiation instance."""
        self.radiation = IonizingRadiation()
        self.metrology_areas = self.radiation.metrology_areas()
        assert len(self.metrology_areas) == 1
        self.branches = self.radiation.branches(self.metrology_areas[0])

        p = GeneralPhysics()
        self.physics_branches = [b for a in p.metrology_areas() for b in p.branches(a)]
        assert len(self.physics_branches) == 32

    def test_branches(self) -> None:
        """Test IonizingRadiation.branches()."""
        assert len(self.branches) == 3

        neu, *rest = self.radiation.filter(self.branches, "NEU")
        assert not rest
        assert neu.id == 34
        assert neu.label == "NEU"
        assert neu.value == "Neutron Measurements"
        assert neu.metrology_area.id == 9
        assert neu.metrology_area.label == "RI"
        assert neu.metrology_area.value == "Ionizing Radiation"

    def test_branches_chem_bio_areas(self) -> None:
        """Test IonizingRadiation.branches() for Chemistry and Biology areas."""
        chem_bio = ChemistryBiology()
        for area in chem_bio.metrology_areas():
            branches = self.radiation.branches(area)
            assert not branches

    def test_branches_physics_areas(self) -> None:
        """Test IonizingRadiation.branches() for General Physics areas."""
        physics = GeneralPhysics()
        for area in physics.metrology_areas():
            branches = self.radiation.branches(area)
            assert not branches

    def test_domain(self) -> None:
        """Test IonizingRadiation.DOMAIN class attribute."""
        chem_bio, phys, rad = sorted(self.radiation.domains())
        assert rad == self.radiation.DOMAIN
        assert rad.code == "RADIATION"
        assert rad.name == "Ionizing radiation"

    def test_mediums_dosimetry(self) -> None:
        """Test IonizingRadiation.mediums() for Dosimetry branch."""
        branches = self.radiation.filter(self.branches, "Dosimetry")
        assert len(branches) == 1
        mediums = self.radiation.mediums(branches[0])
        assert len(mediums) == 7

        medium, *rest = self.radiation.filter(mediums, "Graphite")
        assert not rest
        assert medium.id == 21
        assert medium.label == "4"
        assert medium.value == "Graphite"

    def test_mediums_neutron(self) -> None:
        """Test IonizingRadiation.mediums() for Neutron Measurement branch."""
        branches = self.radiation.filter(self.branches, "Neutron")
        assert len(branches) == 1
        mediums = self.radiation.mediums(branches[0])
        assert len(mediums) == 4

        medium, *rest = self.radiation.filter(mediums, "Tissue")
        assert not rest
        assert medium.id == 26
        assert medium.label == "3"
        assert medium.value == "Tissue"

    def test_mediums_radioactivity(self) -> None:
        """Test IonizingRadiation.mediums() for Radioactivity branch."""
        branches = self.radiation.filter(self.branches, "Radioactivity")
        assert len(branches) == 1
        mediums = self.radiation.mediums(branches[0])
        assert len(mediums) == 14

        medium, *rest = self.radiation.filter(mediums, "Aerosol")
        assert not rest
        assert medium.id == 5
        assert medium.label == "5"
        assert medium.value == "Aerosol"

    def test_mediums_physics_branches(self) -> None:
        """Test IonizingRadiation.mediums() for General Physics branches."""
        for branch in self.physics_branches:
            mediums = self.radiation.mediums(branch)
            assert not mediums

    def test_metrology_area(self) -> None:
        """Test IonizingRadiation.metrology_areas()."""
        assert len(self.metrology_areas) == 1
        radiation = self.metrology_areas[0]
        assert radiation.id == 9
        assert radiation.label == "RI"
        assert radiation.value == "Ionizing Radiation"
        assert radiation.domain.code == "RADIATION"
        assert radiation.domain.name == "Ionizing radiation"

    def test_nuclides(self) -> None:
        """Test IonizingRadiation.nuclides()."""
        nuclides = self.radiation.nuclides()
        assert len(nuclides) > 100

        nuclide, *rest = self.radiation.filter(nuclides, "^Ce-144$")
        assert not rest
        assert nuclide.id == 3
        assert nuclide.label == "Ce-144"
        assert nuclide.value == "Ce-144"

    def test_repr(self) -> None:
        """Test string representation."""
        assert str(self.radiation) == "IonizingRadiation(code='RADIATION', name='Ionizing radiation')"

    def test_search(self) -> None:
        """Test IonizingRadiation.search()."""
        radiation = self.radiation.search(
            branch="RAD",
            quantity="1",
            medium="3",
            source="2",
            nuclide="Co-60",
            keywords="phase OR multichannel OR water",
            countries=Country(id=1, label="JP", value="Japan"),
            public_date_from=date(2005, 1, 31),
            public_date_to="2020-06-30",
        )

        assert radiation.total_elements == 1
        assert radiation.data[0].nmi_code == "NMIJ AIST"
        assert radiation.data[0].nmi_service_code == "APM-RAD-NMIJ/AIST-2144"

        assert str(radiation) == (
            f"ResultsRadiation(number_of_elements=1, page_number=0, page_size=100, "
            f"total_elements=1, total_pages=1, version_api_kcdb={radiation.version_api_kcdb!r})"
        )

    def test_sources_dosimetry(self) -> None:
        """Test IonizingRadiation.sources() for Dosimetry branch."""
        branches = self.radiation.filter(self.branches, "Dosimetry")
        assert len(branches) == 1
        sources = self.radiation.sources(branches[0])
        assert len(sources) == 17

        source, *rest = self.radiation.filter(sources, "Photons")
        assert not rest
        assert source.id == 6
        assert source.label == "6"
        assert source.value == "Photons, high energy"

    def test_sources_neutron(self) -> None:
        """Test IonizingRadiation.sources() for Neutron Measurement branch."""
        branches = self.radiation.filter(self.branches, "Neutron")
        assert len(branches) == 1
        sources = self.radiation.sources(branches[0])
        assert len(sources) > 10

        source, *rest = self.radiation.filter(sources, "Mono")
        assert not rest
        assert source.id == 36
        assert source.label == "2"
        assert source.value == "Mono-energetic neutrons"

    def test_sources_radioactivity(self) -> None:
        """Test IonizingRadiation.sources() for Radioactivity branch."""
        branches = self.radiation.filter(self.branches, "Radioactivity")
        assert len(branches) == 1
        sources = self.radiation.sources(branches[0])
        assert len(sources) == 3

        source, *rest = self.radiation.filter(sources, "x-rays")
        assert not rest
        assert source.id == 34
        assert source.label == "3"
        assert source.value == "K x-rays"

    def test_sources_physics_branches(self) -> None:
        """Test IonizingRadiation.sources() for General Physics branches."""
        for branch in self.physics_branches:
            sources = self.radiation.sources(branch)
            assert not sources

    def test_quantities_dosimetry(self) -> None:
        """Test IonizingRadiation.quantities() for Dosimetry branch."""
        branches = self.radiation.filter(self.branches, "Dosimetry")
        assert len(branches) == 1
        quantities = self.radiation.quantities(branches[0])
        assert len(quantities) == 16

        quantity, *rest = self.radiation.filter(quantities, "X-ray")
        assert not rest
        assert quantity.id == 14
        assert quantity.label == "14"
        assert quantity.value == "X-ray tube voltage"

    def test_quantities_neutron(self) -> None:
        """Test IonizingRadiation.quantities() for Neutron Measurement branch."""
        branches = self.radiation.filter(self.branches, "Neutron")
        assert len(branches) == 1
        quantities = self.radiation.quantities(branches[0])
        assert len(quantities) == 17

        quantity, *rest = self.radiation.filter(quantities, "^Fluence$")
        assert not rest
        assert quantity.id == 49
        assert quantity.label == "3"
        assert quantity.value == "Fluence"

    def test_quantities_radioactivity(self) -> None:
        """Test IonizingRadiation.quantities() for Radioactivity branch."""
        branches = self.radiation.filter(self.branches, "Radioactivity")
        assert len(branches) == 1
        quantities = self.radiation.quantities(branches[0])
        assert len(quantities) == 12

        quantity, *rest = self.radiation.filter(quantities, "Activity per unit area")
        assert not rest
        assert quantity.id == 34
        assert quantity.label == "3"
        assert quantity.value == "Activity per unit area"

    def test_quantities_physics_branches(self) -> None:
        """Test IonizingRadiation.quantities() for General Physics branches."""
        for branch in self.physics_branches:
            quantities = self.radiation.quantities(branch)
            assert not quantities
