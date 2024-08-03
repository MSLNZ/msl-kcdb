from datetime import date

from msl.kcdb import ChemistryBiology


class TestChemBio:
    """Test the ChemistryBiology class."""

    def setup_class(self) -> None:
        """Create ChemistryBiology instance."""
        self.chem_bio = ChemistryBiology()

    def test_analytes(self) -> None:
        """Test ChemistryBiology.analytes()."""
        analytes = self.chem_bio.analytes()
        assert len(analytes) > 100

        analyte, *rest = self.chem_bio.filter(analytes, "^nitrogen$")
        assert not rest
        assert analyte.id == 1
        assert analyte.label == "nitrogen"
        assert analyte.value == "nitrogen"

    def test_categories(self) -> None:
        """Test ChemistryBiology.categories()."""
        categories = self.chem_bio.categories()
        assert len(categories) > 10

        category, *rest = self.chem_bio.filter(categories, "^Biological fluids")
        assert not rest
        assert category.id == 2
        assert category.label == "10"
        assert category.value == "Biological fluids and materials"

    def test_domain(self) -> None:
        """Test ChemistryBiology.DOMAIN class attribute."""
        chem_bio, phys, rad = sorted(self.chem_bio.domains())
        assert chem_bio == self.chem_bio.DOMAIN
        assert chem_bio.code == "CHEM-BIO"
        assert chem_bio.name == "Chemistry and Biology"

    def test_metrology_area(self) -> None:
        """Test ChemistryBiology.metrology_areas()."""
        chem_bio, *rest = self.chem_bio.metrology_areas()
        assert not rest
        assert chem_bio.id == 8
        assert chem_bio.label == "QM"
        assert chem_bio.value == "Chemistry and Biology"
        assert chem_bio.domain.code == "CHEM-BIO"
        assert chem_bio.domain.name == "Chemistry and Biology"

    def test_repr(self) -> None:
        """Test string representation."""
        assert str(self.chem_bio) == "ChemistryBiology(code='CHEM-BIO', name='Chemistry and Biology')"

    def test_search(self) -> None:
        """Test ChemistryBiology.search()."""
        chem_bio = self.chem_bio.search(
            analyte="antimony",
            category="5",
            keywords="phase OR multichannel OR water",
            countries="JP",
            public_date_from="2005-01-31",
            public_date_to=date(2024, 6, 30),
        )

        assert chem_bio.total_elements == 1
        assert chem_bio.data[0].nmi_code == "NMIJ AIST"
        assert chem_bio.data[0].nmi_service_code == "5-01-02"

        assert str(chem_bio) == (
            f"ResultsChemistryBiology(number_of_elements=1, page_number=0, page_size=100, "
            f"total_elements=1, total_pages=1, version_api_kcdb={chem_bio.version_api_kcdb!r})"
        )
