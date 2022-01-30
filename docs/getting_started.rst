Getting started
===============

Elementary comes with standard elements defined, but there are a number of ways to customize the Elements class.

--------
Standard
--------

For immediate usage, import :class:`Element`. Elements can be retrieved with :func:`Element()`:

.. ipython:: python

    import pyelementary as elm
    h = elm.Element(atomic_number=1)
    print(h)

:func:`Element()` accepts all attributes defined on an :class:`Element`, including floating point numbers.
In the standard formulation, these get rounded to 4 decimal places. For custom behavior, see below.

.. ipython:: python

    elm.Element(mass=1.0078)


Source
------

The data in the standard package are sourced, with much gratitude, from `qcelemental`_ version 0.23.0.
Please see the documentation for `qcelemental`_ for full details.
The covalent radii are obtained from Alvarez 2008.


------
Custom
------

Element generation can be customized a number of ways by creating a new class with :class:`Elementary()`.
You can change:

* whether attributes have units attached
* the base class used for each Element (default: namedtuple)
* the number of decimal places to round each floating point value to
* the JSON file from which the elements are created

Units
-----

It is relatively easy to use a number of different units packages.
These include OpenFF Units, OpenMM Units, Pint Units, and Unyt.
All that's needed is to define ``units`` as a dictionary, where
the expected unit of each attribute is given. These units
get multiplied with the bare integers or floating point numbers in
the JSON file used.

.. ipython:: python

    from openff.units import unit as offunit

    OpenFFElements = elm.Elementary(
        units=dict(
            mass=offunit.amu,
            covalent_radius=offunit.angstrom
        )
    )

Each element has now units defined on the object.

.. ipython:: python

    offh = OpenFFElements(atomic_number=1)

However, units are **not** included in searching as keys to the Element registry.
That's because many of the packages are not hashable.

.. ipython:: python

    OpenFFElements.registry.mass[1.0078]

Nonetheless, you can search for elements with unit-associated attributes.

.. ipython:: python

    OpenFFElements(mass=1.0078 * offunit.amu)
    
You can even search with *different*, but compatible, units.

    OpenFFElements(mass=1.673532838315319e-24 * offunit.g)


Base class
----------

NamedTuples were chosen as the Element base class as they are natively JSON-serializable.

.. ipython:: python

    import json
    json.dumps(h)

However, this representation may not be fantastic.
You can create a custom representation with another class, such as a Pydantic BaseModel.

.. ipython:: python

    from pydantic import BaseModel

    PydElements = elm.Elementary(
        element_cls=BaseModel
    )
    h = PydElements(atomic_number=1)
    h.json()


Decimal place precision
-----------------------

The number of places to round floating point attributes is a user-chosen value.
You can make it more or less precise.


.. ipython:: python

    LessPreciseElement = elm.Elmeentary(
        decimals=0
    )
    LessPreciseElement(mass=1)


JSON source
-----------

By default, Elementary creates elements from a file packaged in the library.
This may not contain the best values for you.
You can pass in ``json_file`` to create Elements from a different source.
These can have *arbitrary* attributes.
For a silly example:

.. ipython:: python

    from pyelementary.tests.datafiles import VEGETABLES_JSON
    Vegetables = elm.Elementary(json_file=VEGETABLES_JSON)
    print(Vegetables(name="carrot"))
    print(Vegetables.registry.name)
