import pytest

from msl.kcdb.classes import KCDB


class TestKCDB:
    """Test the KCDB base class."""

    def setup_class(self) -> None:
        """Create KCDB instance."""
        self.kcdb = KCDB()

    def test_countries(self) -> None:
        """Test KCDB.countries()."""
        countries = self.kcdb.countries()
        assert len(countries) > 100

        country, *rest = self.kcdb.filter(countries, "NZ")
        assert not rest
        assert country.id == 58
        assert country.label == "NZ"
        assert country.value == "New Zealand"

    def test_domains(self) -> None:
        """Test KCDB.domains()."""
        chem, phys, rad = sorted(self.kcdb.domains())
        assert chem.code == "CHEM-BIO"
        assert chem.name == "Chemistry and Biology"
        assert phys.code == "PHYSICS"
        assert phys.name == "General physics"
        assert rad.code == "RADIATION"
        assert rad.name == "Ionizing radiation"

    def test_invalid_page_value(self) -> None:
        """Test page value invalid."""
        with pytest.raises(ValueError, match=r"Must be >= 0"):
            self.kcdb.quick_search(page=-1)

    def test_invalid_page_size_value(self) -> None:
        """Test page_size value invalid."""
        with pytest.raises(ValueError, match=r"Invalid page size"):
            self.kcdb.quick_search(page_size=0)

    def test_non_ionizing_quantities(self) -> None:
        """Test KCDB.non_ionizing_quantities()."""
        quantities = self.kcdb.non_ionizing_quantities()
        assert len(quantities) > 1000

        quantity, *rest = self.kcdb.filter(quantities, "Sound pressure response")
        assert not rest
        assert quantity is not None
        assert quantity.id == 78
        assert quantity.value == "Sound pressure response level"

    def test_quick_search(self) -> None:
        """Test KCDB.quick_search()."""
        quick = self.kcdb.quick_search(
            keywords="phase OR test",
            included_filters=[
                "cmcDomain.CHEM-BIO",
                "cmcBranches.Dimensional metrology",
            ],
            excluded_filters=[
                "cmcServices.AC current",
                "cmcServices.AC power",
            ],
        )

        assert quick.total_elements > 10
        assert str(quick).startswith("ResultsQuickSearch(")

    def test_timeout(self) -> None:
        """Test timeout setter/getter."""
        self.kcdb.timeout = 100
        assert isinstance(self.kcdb.timeout, float)
        assert self.kcdb.timeout == 100.0

        self.kcdb.timeout = None
        assert self.kcdb.timeout is None

        # make sure that requests.get(url, timeout=None) is okay
        assert len(self.kcdb.domains()) == 3

        self.kcdb.timeout = -1
        assert self.kcdb.timeout is None

    def test_to_label_raises(self) -> None:
        """Test KCDB._to_label() for an invalid object."""
        with pytest.raises(AttributeError):
            KCDB._to_label(None)  # type: ignore[arg-type] # noqa: SLF001
