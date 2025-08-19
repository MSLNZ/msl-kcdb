# Overview
Search the key comparison database, [KCDB](https://www.bipm.org/kcdb/cmc/advanced-search){:target="_blank"}, that is provided by the International Bureau of Weights and Measures, [BIPM](https://www.bipm.org/en/){:target="_blank"}.

## Install
`msl-kcdb` is available for installation via the [Python Package Index](https://pypi.org/){:target="_blank"} and may be installed with [pip](https://pip.pypa.io/en/stable/){:target="_blank"}

```console
pip install msl-kcdb
```

## User Guide
Three classes are available to search the three metrology domains

* [`ChemistryBiology`][msl.kcdb.chemistry_biology.ChemistryBiology] &mdash; Search the Chemistry and Biology database
* [`IonizingRadiation`][msl.kcdb.ionizing_radiation.IonizingRadiation] &mdash; Search the Ionizing Radiation database
* [`Physics`][msl.kcdb.general_physics.Physics] &mdash; Search the General Physics database

See the [examples][] on how to use each of these classes to extract information from the KCDB. The example scripts are also available in the `msl-kcdb` [repository](https://github.com/MSLNZ/msl-kcdb/tree/main/examples){:target="_blank"}.

The classes as based on version `1.0.9` of the [KCDB XSD Schema](https://www.bipm.org/api/kcdb/cmc/searchData/xsdSchema){:target="_blank"}. Should the KCDB API change, please open an [issue](https://github.com/MSLNZ/msl-kcdb/issues){:target="_blank"}.