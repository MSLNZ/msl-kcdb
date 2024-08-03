# Overview
Interact with the key comparison database, [KCDB]{:target="_blank"}, that is provided by the International Bureau of Weights and Measures, [BIPM](https://www.bipm.org/en/){:target="_blank"}.

## Install
`msl-kcdb` is available for installation via the [Python Package Index](https://pypi.org/){:target="_blank"} and may be installed with [pip](https://pip.pypa.io/en/stable/){:target="_blank"}

```console
pip install msl-kcdb
```

## User Guide
Three classes are available to interact with the three metrology domains

* [`ChemistryBiology`][msl.kcdb.chemistry_biology.ChemistryBiology] &ndash; Search the Chemistry and Biology database
* [`GeneralPhysics`][msl.kcdb.general_physics.GeneralPhysics] &ndash; Search the General Physics database
* [`IonizingRadiation`][msl.kcdb.ionizing_radiation.IonizingRadiation] &ndash; Search the Ionizing Radiation database

Examples on how to use the classes to interact with the [KCDB]{:target="_blank"} are available in the `msl-kcdb` [repository](https://github.com/MSLNZ/msl-kcdb/tree/main/src/msl/examples/kcdb){:target="_blank"} and these examples are also included with the `msl-kcdb` installation in the `../site-packages/msl/examples/kcdb` directory of your Python interpreter.

The examples are provided as [Jupyter](https://jupyter.org/){:target="_blank"} notebooks. Follow [these instructions](https://jupyter.org/install){:target="_blank"} to learn how to install and start Jupyter notebooks.

[KCDB]: https://www.bipm.org/kcdb/