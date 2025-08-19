"""Search the "Ionizing Radiation" metrology area of the KCDB."""

from msl.kcdb import IonizingRadiation

ir = IonizingRadiation()

#
# Get all reference data for the "Ionizing Radiation" metrology area
#
print(f"Getting all reference data for {ir.DOMAIN.name}...")
metrology_areas = ir.metrology_areas()
print(f"  There are {len(metrology_areas)} metrology areas")
branches = [b for ma in metrology_areas for b in ir.branches(ma)]
print(f"  There are {len(branches)} branches")
nuclides = ir.nuclides()
print(f"  There are {len(nuclides)} nuclides")
quantities = [q for b in branches for q in ir.quantities(b)]
print(f"  There are {len(quantities)} quantities")
mediums = [m for b in branches for m in ir.mediums(b)]
print(f"  There are {len(mediums)} mediums")
sources = [s for b in branches for s in ir.sources(b)]
print(f"  There are {len(sources)} sources")

#
# Search the "Ionizing Radiation" database for NMIs that are capable of
# performing measurements with a source of "Beta radiation" and print
# some information about each NMI
#
print("The following NMIs have capabilities to perform measurements with Beta radiation...")
for source in ir.filter(sources, "Beta"):
    # Here, we request the maximum number of elements that can be returned
    # by the KCDB server within a single request
    results = ir.search(branch=source.branch, source=source, page_size=ir.MAX_PAGE_SIZE)
    for data in results.data:
        print(f"  {data.nmi_code} ({data.instrument}): {data.radiation_specification}")
