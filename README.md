[![Tests Status](https://github.com/MSLNZ/msl-kcdb/actions/workflows/tests.yml/badge.svg)](https://github.com/MSLNZ/msl-kcdb/actions/workflows/tests.yml)
[![Docs](https://github.com/MSLNZ/msl-kcdb/actions/workflows/docs.yml/badge.svg)](https://github.com/MSLNZ/msl-kcdb/actions/workflows/docs.yml)

## Overview
Search the key comparison database, [KCDB](https://www.bipm.org/kcdb/), that is provided by the International Bureau of Weights and Measures, [BIPM](https://www.bipm.org/en/).

## Install
`msl-kcdb` is available for installation via the [Python Package Index](https://pypi.org/) and may be installed with [pip](https://pip.pypa.io/en/stable/)

```console
pip install msl-kcdb
```

## User Guide
Three classes are available to search the three metrology domains

* [`ChemistryBiology`](https://mslnz.github.io/msl-kcdb/api/chemistry_biology/) &ndash; Search the Chemistry and Biology database
* [`GeneralPhysics`](https://mslnz.github.io/msl-kcdb/api/general_physics/) &ndash; Search the General Physics database
* [`IonizingRadiation`](https://mslnz.github.io/msl-kcdb/api/ionizing_radiation/) &ndash; Search the Ionizing Radiation database

Examples on how to use the classes are available in the `msl-kcdb` [repository](https://github.com/MSLNZ/msl-kcdb/tree/main/src/msl/examples/kcdb) and these examples are also included with the `msl-kcdb` installation in the `../site-packages/msl/examples/kcdb` directory of your Python interpreter.

The examples are provided as [Jupyter](https://jupyter.org/) notebooks. Follow [these instructions](https://jupyter.org/install) to learn how to install and launch a Jupyter notebook.

## Documentation
The documentation for `msl-kcdb` is available [here](https://mslnz.github.io/msl-kcdb/).
