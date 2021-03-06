elementable
==============================
Yet another elements package

[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/lilyminium/elementable/workflows/CI/badge.svg)](https://github.com/lilyminium/elementable/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/lilyminium/elementable/branch/master/graph/badge.svg)](https://codecov.io/gh/lilyminium/elementable/branch/main)
[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/elementable)](https://anaconda.org/conda-forge/elementable)
[![PyPI version](https://badge.fury.io/py/elementable.svg)](https://pypi.org/project/elementable/)
[![Documentation Status](https://readthedocs.org/projects/elementable/badge/?version=latest)](https://elementable.readthedocs.io/en/latest/?badge=latest)

[![Last release tag](https://img.shields.io/github/release-pre/lilyminium/elementable.svg)](https://github.com/lilyminium/elementable/releases) ![GitHub commits since latest release (by date) for a branch](https://img.shields.io/github/commits-since/lilyminium/elementable/latest)


Elementable is *another* elements package defined in Python.
It is written to be usable with a number of different unit systems and classes.
At its most minimal, it has no dependencies outside the main Python library.
However, the real point of the package is to automagically work with a number of units, base classes, custom data, and be generally flexible.

### Usage

Elementable can be installed via pip or conda:

```
pip install elementable
# or
conda install -c conda-forge elementable
```

Alternatively, you can download this repository and build from source:

```
git clone https://github.com/lilyminium/elementable.git
cd elementable
python setup.py install
```

#### Standard

You can use Elementable immediately by importing the standard `Elements` class. Please see the [documentation for information about customization](https://elementable.readthedocs.io/en/latest/customizing.html). Each element is defined uniquely to allow for `is` comparisons.

```python

In [1]: import elementable as elm

In [2]: h = elm.Elements(atomic_number=1)

In [3]: h is elm.Elements(name="hydrogen")
Out[3]: True

In [4]: h is elm.Elements.H
Out[4]: True

In [5]: h.mass
Out[5]: 1.00782503223

```

Supported attributes include:

* atomic_number
* symbol
* name
* mass (in atomic mass units)
* period
* group
* covalent_radius (in angstrom)

Each attribute can be used to obtain an Element or list of Elements. Floats are rounded to the nearest 4 decimals when using `Elements()`.

```python
In [5]: elm.Elements(mass=1.0078)
Out[5]: Element(name='hydrogen', symbol='H', atomic_number=1, mass=1.00782503223, period=1, group=1, covalent_radius=0.31)
```

Using `Elements()` to retrieve an element can be quite slow, as a number of different cases are checked. If your search is more defined, you can access registries for each attribute directly at `Elements.registry`. Keys for all floats are rounded to 4 decimal places.

```python
In [6]: elm.Elements.registry.mass[1.0078]
Out[6]: Element(name='hydrogen', symbol='H', atomic_number=1, mass=1.00782503223, period=1, group=1, covalent_radius=0.31)
```

For attributes where multiple elements have the same value, a sorted tuple of elements is returned.

```python
In [8]: elm.Elements(period=5)
Out[8]:
(Element(name='rubidium', symbol='Rb', atomic_number=37, mass=84.9117897379, period=5, group=1, covalent_radius=2.2),
 Element(name='strontium', symbol='Sr', atomic_number=38, mass=87.9056125, period=5, group=2, covalent_radius=1.95),
 Element(name='yttrium', symbol='Y', atomic_number=39, mass=88.9058403, period=5, group=3, covalent_radius=1.9),
 Element(name='zirconium', symbol='Zr', atomic_number=40, mass=89.9046977, period=5, group=4, covalent_radius=1.75),
 Element(name='niobium', symbol='Nb', atomic_number=41, mass=92.906373, period=5, group=5, covalent_radius=1.64),
 Element(name='molybdenum', symbol='Mo', atomic_number=42, mass=97.90540482, period=5, group=6, covalent_radius=1.54),
 Element(name='technetium', symbol='Tc', atomic_number=43, mass=97.9072124, period=5, group=7, covalent_radius=1.47),
 Element(name='ruthenium', symbol='Ru', atomic_number=44, mass=101.9043441, period=5, group=8, covalent_radius=1.46),
 Element(name='rhodium', symbol='Rh', atomic_number=45, mass=102.905498, period=5, group=9, covalent_radius=1.42),
 Element(name='palladium', symbol='Pd', atomic_number=46, mass=105.9034804, period=5, group=10, covalent_radius=1.39),
 Element(name='silver', symbol='Ag', atomic_number=47, mass=106.9050916, period=5, group=11, covalent_radius=1.45),
 Element(name='cadmium', symbol='Cd', atomic_number=48, mass=113.90336509, period=5, group=12, covalent_radius=1.44),
 Element(name='indium', symbol='In', atomic_number=49, mass=114.903878776, period=5, group=13, covalent_radius=1.42),
 Element(name='tin', symbol='Sn', atomic_number=50, mass=119.90220163, period=5, group=14, covalent_radius=1.39),
 Element(name='antimony', symbol='Sb', atomic_number=51, mass=120.903812, period=5, group=15, covalent_radius=1.39),
 Element(name='tellurium', symbol='Te', atomic_number=52, mass=129.906222748, period=5, group=16, covalent_radius=1.38),
 Element(name='iodine', symbol='I', atomic_number=53, mass=126.9044719, period=5, group=17, covalent_radius=1.39),
 Element(name='xenon', symbol='Xe', atomic_number=54, mass=131.9041550856, period=5, group=18, covalent_radius=1.4))
```

These can be narrowed down with multiple keyword arguments.

```python
In [9]: elm.Elements(period=5, group=17)
Out[9]: (Element(name='iodine', symbol='I', atomic_number=53, mass=126.9044719, period=5, group=17, covalent_radius=1.39),)
```


### Units

The default units in the standard elements library are:

* mass: atomic mass units
* length: angstrom


### Sources


The data in the standard package are sourced, with much gratitude, from [qcelemental](https://github.com/MolSSI/QCElemental) version 0.23.0.
Please see the documentation for [qcelemental](https://docs.qcarchive.molssi.org/projects/QCElemental/en/stable/) for full details.
The covalent radii are obtained from Alvarez 2008.


### Copyright

Copyright (c) 2022, Lily Wang


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.6.
