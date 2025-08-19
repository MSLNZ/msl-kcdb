# MSL-KCDB

[![Tests Status](https://github.com/MSLNZ/msl-kcdb/actions/workflows/ci.yml/badge.svg)](https://github.com/MSLNZ/msl-kcdb/actions/workflows/ci.yml)
[![Docs Status](https://github.com/MSLNZ/msl-kcdb/actions/workflows/docs.yml/badge.svg)](https://github.com/MSLNZ/msl-kcdb/actions/workflows/docs.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/msl-kcdb?logo=pypi&logoColor=gold&label=PyPI&color=blue)](https://pypi.org/project/msl-kcdb/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/msl-kcdb.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/msl-kcdb/)

## Overview
Search the key comparison database, [KCDB](https://www.bipm.org/kcdb/), that is provided by the International Bureau of Weights and Measures, [BIPM](https://www.bipm.org/en/).

## Install
`msl-kcdb` is available for installation via the [Python Package Index](https://pypi.org/) and may be installed with [pip](https://pip.pypa.io/en/stable/)

```console
pip install msl-kcdb
```

## User Guide
Three classes are available to search the three metrology domains

* [`ChemistryBiology`](https://mslnz.github.io/msl-kcdb/latest/api/chemistry_biology/) &ndash; Search the Chemistry and Biology database
* [`IonizingRadiation`](https://mslnz.github.io/msl-kcdb/latest/api/ionizing_radiation/) &ndash; Search the Ionizing Radiation database
* [`Physics`](https://mslnz.github.io/msl-kcdb/latest/api/general_physics/) &ndash; Search the General Physics database

See the [examples](https://mslnz.github.io/msl-kcdb/latest/examples/) on how to use each of these classes to extract information from the KCDB. The example scripts are also available in the `msl-kcdb` [repository](https://github.com/MSLNZ/msl-kcdb/tree/main/examples).

## Documentation
The documentation for `msl-kcdb` is available [here](https://mslnz.github.io/msl-kcdb/).
