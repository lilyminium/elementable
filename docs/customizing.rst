.. _customizing-ref:

Customizing elements
====================

Element generation can be customized a number of ways by creating a new class with :class:`Elementable()`.
You can change:

* whether attributes have units attached
* the base class used for each Element (default: namedtuple)
* the number of decimal places to round each floating point value to
* the JSON file from which the elements are created

-----
Units
-----

It is relatively easy to use a number of different units packages.
These include OpenFF Units, OpenMM Units, Pint Units, and Unyt.
All that's needed is to define ``units`` as a dictionary, where
the expected unit of each attribute is given. These units
get multiplied with the bare integers or floating point numbers in
the JSON file used.

.. ipython:: python

    import elementable as elm
    from openff.units import unit as offunit

    OpenFFElements = elm.Elementable(
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

.. ipython:: python

    OpenFFElements(mass=1.673532838315319e-24 * offunit.g)


----------
Base class
----------

NamedTuples were chosen as the Element base class as they are natively JSON-serializable.

.. ipython:: python

    import json
    h = elm.Element.registry.atomic_number[1]
    json.dumps(h)


However, this representation may not be fantastic.
You can create a custom representation with another class, such as a Pydantic BaseModel.

.. ipython:: python

    from pydantic import BaseModel

    PydElements = elm.Elementable(
        element_cls=BaseModel
    )
    h = PydElements(atomic_number=1)
    h.json()


-----------------------
Decimal place precision
-----------------------

The number of places to round floating point attributes is a user-chosen value.
You can make it more or less precise.


.. ipython:: python

    LessPreciseElement = elm.Elementable(
        decimals=0
    )
    LessPreciseElement(mass=1)


-----------
JSON source
-----------

By default, Elementable creates elements from a file packaged in the library.
This may not contain the best values for you.
You can pass in ``json_file`` to create Elements from a different source.
These can have *arbitrary* attributes.
For a silly example:

.. ipython:: python

    from elementable.tests.datafiles import VEGETABLES_JSON
    Vegetables = elm.Elementable(json_file=VEGETABLES_JSON)
    print(Vegetables(name="carrot"))
    print(Vegetables.registry.name)



