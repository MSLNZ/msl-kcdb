from kcdb import CMCSearchData


def test_physics() -> None:
    physics = CMCSearchData.physics(
        "EM",
        branch_label="EM/RF",
        physics_code="11.3.3",
        keywords="phase OR multichannel OR water",
        countries=["CH", "FR", "JP"],
        public_date_from="2005-01-31",
        public_date_to="2024-06-30",
    )

    assert physics["totalElements"] == 1
    assert physics["data"][0]["nmiCode"] == "METAS"
    assert physics["data"][0]["nmiServiceCode"] == "217.01.04"


def test_chemistry_and_biology() -> None:
    chem_bio = CMCSearchData.chemistry_and_biology(
        analyte_label="antimony",
        category_label="5",
        keywords="phase OR multichannel OR water",
        countries=["CH", "FR", "JP"],
        public_date_from="2005-01-31",
        public_date_to="2024-06-30",
    )

    assert chem_bio["totalElements"] == 1
    assert chem_bio["data"][0]["nmiCode"] == "NMIJ AIST"
    assert chem_bio["data"][0]["nmiServiceCode"] == "5-01-02"


def test_radiation() -> None:
    radiation = CMCSearchData.radiation(
        branch_label="RAD",
        quantity_label="1",
        medium_label="3",
        source_label="2",
        nuclide_label="Co-60",
        keywords="phase OR multichannel OR water",
        countries=["CH", "FR", "JP"],
        public_date_from="2005-01-31",
        public_date_to="2020-06-30",
    )

    assert radiation["totalElements"] == 1
    assert radiation["data"][0]["nmiCode"] == "NMIJ AIST"
    assert radiation["data"][0]["nmiServiceCode"] == "APM-RAD-NMIJ/AIST-2144"


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

    assert quick["totalElements"] > 10
