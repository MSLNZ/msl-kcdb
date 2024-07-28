from kcdb import ReferenceData
from kcdb.classes import Branch, Domain, MetrologyArea, Service, SubService


def test_analytes() -> None:
    analytes = ReferenceData.analytes()
    assert len(analytes) > 100

    analyte, *rest = ReferenceData.filter(analytes, "^nitrogen$")
    assert not rest
    assert analyte.id == 1
    assert analyte.label == "nitrogen"
    assert analyte.value == "nitrogen"


def test_categories() -> None:
    categories = ReferenceData.categories()
    assert len(categories) > 10

    category, *rest = ReferenceData.filter(categories, "^Biological fluids")
    assert not rest
    assert category.id == 2
    assert category.label == "10"
    assert category.value == "Biological fluids and materials"


def test_nuclides() -> None:
    nuclides = ReferenceData.nuclides()
    assert len(nuclides) > 100

    nuclide, *rest = ReferenceData.filter(nuclides, "^Ce-144$")
    assert not rest
    assert nuclide.id == 3
    assert nuclide.label == "Ce-144"
    assert nuclide.value == "Ce-144"


def test_quantities() -> None:
    quantities = ReferenceData.quantities()
    assert len(quantities) > 100

    quantity, *rest = ReferenceData.filter(quantities, "Luminance coefficient")
    assert not rest
    assert quantity.id == 116
    assert quantity.label == ""
    assert quantity.value == "Luminance coefficient"


def test_radiation_mediums() -> None:
    radiation_mediums = ReferenceData.radiation_mediums()
    assert len(radiation_mediums) > 10

    medium, *rest = ReferenceData.filter(radiation_mediums, "fauna")
    assert not rest
    assert medium.id == 13
    assert medium.label == "13"
    assert medium.value == "Reference material: fauna"


def test_radiation_sources() -> None:
    radiation_sources = ReferenceData.radiation_sources()
    assert len(radiation_sources) > 10

    source, *rest = ReferenceData.filter(radiation_sources, "Electrons")
    assert not rest
    assert source.id == 2
    assert source.label == "2"
    assert source.value == "Electrons"


def test_countries() -> None:
    countries = ReferenceData.countries()
    assert len(countries) > 100

    country, *rest = ReferenceData.filter(countries, "NZ")
    assert not rest
    assert country.id == 58
    assert country.label == "NZ"
    assert country.value == "New Zealand"


def test_domain() -> None:
    chem, phys, rad = sorted(ReferenceData.domains())
    assert chem.code == "CHEM-BIO"
    assert chem.name == "Chemistry and Biology"
    assert phys.code == "PHYSICS"
    assert phys.name == "General physics"
    assert rad.code == "RADIATION"
    assert rad.name == "Ionizing radiation"


def test_metrology_area_chem_bio() -> None:
    domain = Domain(code="CHEM-BIO", name="Chemistry and Biology")
    chem_bio, *rest = ReferenceData.metrology_areas(domain)
    assert not rest
    assert chem_bio.id == 8
    assert chem_bio.label == "QM"
    assert chem_bio.value == "Chemistry and Biology"
    assert chem_bio.domain.code == "CHEM-BIO"
    assert chem_bio.domain.name == "Chemistry and Biology"


def test_metrology_area_radiation() -> None:
    domain = Domain(code="RADIATION", name="Ionizing radiation")
    radiation, *rest = ReferenceData.metrology_areas(domain)
    assert not rest
    assert radiation.id == 9
    assert radiation.label == "RI"
    assert radiation.value == "Ionizing Radiation"
    assert radiation.domain.code == "RADIATION"
    assert radiation.domain.name == "Ionizing radiation"


def test_metrology_area_physics() -> None:
    area = ReferenceData.metrology_areas(Domain(code="PHYSICS", name="General physics"))
    tf = ReferenceData.find(area, 7)
    assert tf.id == 7
    assert tf.label == "TF"
    assert tf.value == "Time and Frequency"
    assert tf.domain.code == "PHYSICS"
    assert tf.domain.name == "General physics"


def test_branches_chem_bio() -> None:
    domain = Domain(code="CHEM-BIO", name="Chemistry and Biology")
    area = MetrologyArea(domain=domain, id=8, label="QM", value="Chemistry and Biology")
    branches = ReferenceData.branches(area)
    assert not branches


def test_branches_radiation() -> None:
    domain = Domain(code="RADIATION", name="Ionizing radiation")
    area = MetrologyArea(domain=domain, id=9, label="RI", value="Ionizing Radiation")
    branches = ReferenceData.branches(area)

    neu, *rest = ReferenceData.filter(branches, "NEU")
    assert not rest
    assert neu.id == 34
    assert neu.label == "NEU"
    assert neu.value == "Neutron Measurements"
    assert neu.metrology_area.id == 9
    assert neu.metrology_area.label == "RI"
    assert neu.metrology_area.value == "Ionizing Radiation"


def test_branches_physics() -> None:
    domain = Domain(code="PHYSICS", name="General physics")
    area = MetrologyArea(domain=domain, id=7, label="TF", value="Time and Frequency")
    branches = ReferenceData.branches(area)

    t, *rest = ReferenceData.filter(branches, "interval")
    assert not rest
    assert t.id == 28
    assert t.label == "TF/TI"
    assert t.value == "Time interval"
    assert t.metrology_area.id == 7
    assert t.metrology_area.label == "TF"
    assert t.metrology_area.value == "Time and Frequency"


def test_services_physics() -> None:
    domain = Domain(code="PHYSICS", name="General physics")
    area = MetrologyArea(domain=domain, id=7, label="TF", value="Time and Frequency")
    branch = Branch(metrology_area=area, id=27, label="TF/F", value="Frequency")
    services = ReferenceData.services(branch)
    service, *rest = services
    assert not rest
    assert service.id == 55
    assert service.label == "2"
    assert service.value == "Frequency"
    assert service.physics_code == "2"
    assert service.branch.id == 27
    assert service.branch.metrology_area.id == 7


def test_services_radiation() -> None:
    domain = Domain(code="RADIATION", name="Ionizing radiation")
    area = MetrologyArea(domain=domain, id=9, label="RI", value="Ionizing Radiation")
    branch = Branch(metrology_area=area, id=33, label="RAD", value="Radioactivity")
    services = ReferenceData.services(branch)
    assert not services


def test_sub_services_physics() -> None:
    domain = Domain(code="PHYSICS", name="General physics")
    area = MetrologyArea(domain=domain, id=7, label="TF", value="Time and Frequency")
    branch = Branch(metrology_area=area, id=27, label="TF/F", value="Frequency")
    service = Service(branch=branch, id=55, label="2", value="Frequency", physics_code="2")

    sub_services = ReferenceData.sub_services(service)
    meter, *rest = ReferenceData.filter(sub_services, "meter")
    assert not rest
    assert meter.id == 218
    assert meter.label == "3"
    assert meter.value == "Frequency meter"
    assert meter.physics_code == "2.3"
    assert meter.service.id == 55
    assert meter.service.physics_code == "2"
    assert meter.service.branch.id == 27
    assert meter.service.branch.metrology_area.id == 7


def test_individual_services_physics() -> None:
    domain = Domain(code="PHYSICS", name="General physics")
    area = MetrologyArea(domain=domain, id=7, label="TF", value="Time and Frequency")
    branch = Branch(metrology_area=area, id=27, label="TF/F", value="Frequency")
    service = Service(branch=branch, physics_code="2", id=55, label="2", value="Frequency")
    sub_service = SubService(service=service, physics_code="2.3", id=218, label="3", value="Frequency meter")

    individual_services = ReferenceData.individual_services(sub_service)
    counter, *rest = ReferenceData.filter(individual_services, "counter")
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


def test_individual_services_physics_http404() -> None:
    domain = Domain(code="PHYSICS", name="General physics")
    area = MetrologyArea(id=3, label="L", value="Length", domain=domain)
    branch = Branch(id=12, label="L/DimMet", value="Dimensional metrology", metrology_area=area)
    service = Service(id=31, label="6", value="Various dimensional", branch=branch, physics_code="6")
    sub_service = SubService(id=104, label="7", value="Not attributed 1", service=service, physics_code="6.7")

    individual_services = ReferenceData.individual_services(sub_service)
    assert not individual_services
