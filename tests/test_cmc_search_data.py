from datetime import date

from kcdb import CMCSearchData
from kcdb.reference_data import Country


def test_physics() -> None:
    physics = CMCSearchData.physics(
        "EM",
        branch_label="EM/RF",
        physics_code="11.3.3",
        keywords="phase OR multichannel OR water",
        countries=["CH", "FR", "JP"],
        public_date_from=date(2005, 1, 31),
        public_date_to="2024-06-30",
        show_table=True,
    )

    assert physics.total_elements == 1
    assert physics.data[0].nmi_code == "METAS"
    assert physics.data[0].nmi_service_code == "217.01.04"

    assert str(physics) == (
        f"ResultsPhysics(number_of_elements=1, page_number=0, page_size=100, "
        f"total_elements=1, total_pages=1, version_api_kcdb={physics.version_api_kcdb!r})"
    )


def test_chemistry_and_biology() -> None:
    chem_bio = CMCSearchData.chemistry_and_biology(
        analyte_label="antimony",
        category_label="5",
        keywords="phase OR multichannel OR water",
        countries="JP",
        public_date_from="2005-01-31",
        public_date_to=date(2024, 6, 30),
    )

    assert chem_bio.total_elements == 1
    assert chem_bio.data[0].nmi_code == "NMIJ AIST"
    assert chem_bio.data[0].nmi_service_code == "5-01-02"

    assert str(chem_bio) == (
        f"ResultsChemistryAndBiology(number_of_elements=1, page_number=0, page_size=100, "
        f"total_elements=1, total_pages=1, version_api_kcdb={chem_bio.version_api_kcdb!r})"
    )


def test_radiation() -> None:
    radiation = CMCSearchData.radiation(
        branch_label="RAD",
        quantity_label="1",
        medium_label="3",
        source_label="2",
        nuclide_label="Co-60",
        keywords="phase OR multichannel OR water",
        countries=["CH", Country(id=1, label="JP", value="Japan")],
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


def test_quick_search() -> None:
    quick = CMCSearchData.quick_search(
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
