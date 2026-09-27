# MSL-KCDB

[![Tests Status](https://github.com/MSLNZ/msl-kcdb/actions/workflows/ci.yml/badge.svg)](https://github.com/MSLNZ/msl-kcdb/actions/workflows/ci.yml)
[![Docs Status](https://github.com/MSLNZ/msl-kcdb/actions/workflows/docs.yml/badge.svg)](https://github.com/MSLNZ/msl-kcdb/actions/workflows/docs.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/msl-kcdb?logo=pypi&logoColor=gold&label=PyPI&color=blue)](https://pypi.org/project/msl-kcdb/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/msl-kcdb.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/msl-kcdb/)

## Overview
Search the key comparison database, [KCDB](https://www.bipm.org/kcdb/), that is provided by the International Bureau of Weights and Measures, [BIPM](https://www.bipm.org/en/).

## Install
`msl-kcdb` is available at the [Python Package Index](https://pypi.org/project/msl-kcdb/) and can be installed with `pip`

```console
pip install msl-kcdb
```

## User Guide
The following classes are available to (synchronously) search the three metrology domains

* [ChemistryBiology] &mdash; Search the Chemistry and Biology database
* [Physics] &mdash; Search the General Physics database
* [Radiation] &mdash; Search the Ionizing Radiation database

and there are asynchronous (use of `async`/`await`) alternatives

* [AsyncChemistryBiology]
* [AsyncPhysics]
* [AsyncRadiation]

See the [examples](https://mslnz.github.io/msl-kcdb/latest/examples/) on how to use each of these classes to extract information from the KCDB. Example scripts are also available in the `msl-kcdb` [repository](https://github.com/MSLNZ/msl-kcdb/tree/main/examples).

## Documentation
The documentation for `msl-kcdb` is available [here](https://mslnz.github.io/msl-kcdb/).

[ChemistryBiology]: https://mslnz.github.io/msl-kcdb/latest/api/chemistry_biology/#msl.kcdb.chemistry_biology.ChemistryBiology
[Physics]: https://mslnz.github.io/msl-kcdb/dev/api/general_physics/#msl.kcdb.general_physics.Physics
[Radiation]: https://mslnz.github.io/msl-kcdb/latest/api/ionizing_radiation/#msl.kcdb.ionizing_radiation.Radiation
[AsyncChemistryBiology]: https://mslnz.github.io/msl-kcdb/latest/api/chemistry_biology/#msl.kcdb.chemistry_biology.AsyncChemistryBiology
[AsyncPhysics]: https://mslnz.github.io/msl-kcdb/latest/api/general_physics/#msl.kcdb.general_physics.AsyncPhysics
[AsyncRadiation]: https://mslnz.github.io/msl-kcdb/latest/api/ionizing_radiation/#msl.kcdb.ionizing_radiation.AsyncRadiation
