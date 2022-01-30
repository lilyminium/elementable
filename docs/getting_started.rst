Getting started
===============

Elementary comes with standard elements defined, but there are a number of ways to customize the Elements class.
Please see :ref:`customizing-ref` for more.


For immediate usage, import :class:`Element`. Elements can be retrieved with :func:`Element()`:

.. ipython:: python

    import pyelementary as elm
    h = elm.Element(atomic_number=1)
    print(h)


:func:`Element()` accepts all attributes defined on an :class:`Element`, including floating point numbers.
In the standard formulation, these get rounded to 4 decimal places.

.. ipython:: python

    elm.Element(mass=1.0078)



------
Source
------

The data in the standard package are sourced, with much gratitude, from `qcelemental`_ version 0.23.0.
Please see the documentation for `qcelemental`_ for full details.
The covalent radii are obtained from Alvarez 2008.

.. _qcelemental: https://docs.qcarchive.molssi.org/projects/QCElemental/en/stable/