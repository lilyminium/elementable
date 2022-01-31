.. elementable documentation master file, created by
   sphinx-quickstart on Thu Mar 15 13:55:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to elementable's documentation!
=========================================================

Elementable is *another* elements package defined in Python.
It is written to be usable with a number of different unit systems and classes.
At its most minimal, it has no dependencies outside the main Python library.
However, Elementable can be combined with units packages such as OpenFF-Units,
and fun subclasses such as Pydantic.

Elementable was written because many, many, many other elements packages
and distributions already exist. Most downstream packages are looking
for different things out of an elements package; some value being lightweight,
some value complete data, some require *specific data*,
some require a units system, some might need elements to be serializable, etc.
Elementable aims to provide a single solution by enabling packages
to ship their own required datasets, base classes, units, and so on,
using Elementable's general API.

I mostly envision Elementable being used in a separate ``elements.py``
module in a library. For example, the below class creates a Pydantic BaseModel
subclass with OpenForceField units.

.. ipython::

   import elementable as elm
   from pydantic import BaseModel
   from openff.units import unit

   elements = elm.Elementable(
      units=dict(
         mass=unit.amu,
         covalent_radius=unit.angstrom,
      ),
      element_cls=BaseModel
   )

   print(elements.H)
   print(elements.H.json())
   

------------
Installation
------------

Elementable can be installed via pip.

.. code-block:: bash

   pip install elementable


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   customizing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
