Getting started
===============

Elementable comes with standard elements defined, but there are a number of ways to customize the Elements class.
Please see :ref:`customizing-ref` for more.


For immediate usage, import :class:`Elements`. Elements can be retrieved with :func:`Elements()`:

.. ipython:: python

    import elementable as elm
    h = elm.Elements(atomic_number=1)
    print(h)


:func:`Elements()` accepts all attributes defined on an :class:`Element`, including floating point numbers.
In the standard formulation, these get rounded to 4 decimal places.

.. ipython:: python

    elm.Elements(mass=1.0078)


Each standard element is also available as an attribute.

.. ipython:: python

    elm.Elements.Na

Elements can also be directly retrieved from various registries of attributes.
These can return single elements, such as from the atomic number:

.. ipython:: python

    elm.Elements.registry.atomic_number[1]

Or multiple elements, such as from the period.

.. ipython:: python

    elm.Elements.registry.period[1]


------
Source
------

The data in the standard package are sourced, with much gratitude, from `qcelemental`_ version 0.23.0.
Please see the documentation for `qcelemental`_ for full details.
The covalent radii are obtained from Alvarez 2008.

.. _qcelemental: https://docs.qcarchive.molssi.org/projects/QCElemental/en/stable/