from typing import Type, Dict, Any, NamedTuple, Optional, Callable
from types import MappingProxyType, new_class
from pkg_resources import resource_filename
from collections import namedtuple, defaultdict
import json

from .exceptions import InvalidElementError, ElementableError

__all__ = ["Elementable", "Elements"]


NoneType = type(None)


def _resolve_multiple_types(type1, type2):
    if type1 == type2:
        return type2

    if type1 == Optional[type2]:
        return type1
    if type2 == Optional[type1]:
        return type2
    not_none = (
        type1
        if type1 not in (None, NoneType)
        else type2
    )
    if {type1, type2} in ({NoneType, not_none}, {None, not_none}):
        return Optional[not_none]

    if {type1, type2} == {float, int}:
        return float


class Elementable(type):
    """Class factory for generating Elements in a container

    Parameters
    ----------
        units: Dict[str, Any]
            A dictionary of units multiplied with element data for the final value.
            A key is an attribute (e.g. "mass").
            A value should be a unit (e.g. unit.angstrom)
        converters: Dict[str, Callable]
            A dictionary of converters to transform element data.
            A key is an attribute (e.g. "name").
            A value is a function (e.g. ``lambda x: x.lower()``)
        element_cls: Type
            The base class that is subclassed to create an Element class.
        json_file: str
            The JSON file used to read in the data and create elements.
            This should be formatted as a list of dictionaries.
            Each key in the dictionary should be an attribute name.
            Each value in the dictionary should be the corresponding data value.
        decimals: int
            The number of decimals to round floating point data to.
            The rounding only occurs when registering elements in dictionaries,
            or when searching for an element. No rounding occurs for the
            attribute value on the ``Element``.
            If ``None``, no rounding will occur.
            If units are given, all values are converted into that unit
            prior to roundind.
        key_attr: str
            The returned elements container will include all elements
            as attributes for direct access. By default, key_attr="symbol",
            meaning that the attributes are created from the element symbol.
            The chosen key must correspond to string values on **each**
            element, and **each value must be unique**.
        key_transform: Callable
            A function to transform the key for key_attr. This is useful
            for values that are not valid Python identifiers.
            For example, in the default Elements, the empty Element
            (symbol="*") cannot be set as an attribute ``elements.*``.
            The default ``key_transform`` function converts * to X.

    Returns
    -------
        elements_container: namedtuple
            This object holds all the created elements and registries.

    Examples
    --------
        The most basic::

            elements = Elementable()
            assert elements.H is elements.registry.name["hydrogen"]
            assert elements.O is elements(atomic_number=8)

        Or with all bells and whistles::

            from openff.units import unit
            from pydantic import BaseModel

            class Element(BaseModel):
                class Config:
                    # necessary for openff.unit type
                    arbitrary_types_allowed = True

            elements = Elementable(
                units=dict(
                    mass=unit.amu,
                    covalent_radius=unit.angstrom
                ),
                element_cls=Element,
                json_file="my_fancy_json_file.json",
                decimals=10,
                key_attr="name"
            )

            assert elements.hydrogen is elements.registry.atomic_number[1]


    """
    def __new__(
        cls,
        units: Dict[str, Any] = {},
        converters: Dict[str, Callable] = {
            "name": lambda x: x.lower(),
            "symbol": lambda x: x.capitalize()
        },
        element_cls: Type = NamedTuple,
        json_file: Optional[str] = None,
        decimals: Optional[int] = 4,
        key_attr: str = "symbol",
        key_transform: Callable = lambda x: x if x != "*" else "X",
    ):

        # ===== load elements from json =====
        if json_file is None:
            json_file = resource_filename(__name__, "data/elements.json")

        with open(str(json_file), "r") as f:
            contents = json.load(f)

        # ===== gather attribute types and convert values =====
        attr_types = {}
        initial_attr_types = {}
        converted_element_dictionaries = []
        for element_dictionary in contents:
            new_item = {}
            for attr_name, attr_value in element_dictionary.items():
                initial_type = type(attr_value)
                if attr_name in converters:
                    attr_value = converters[attr_name](attr_value)
                if attr_name in units and attr_value is not None:
                    attr_value = attr_value * units[attr_name]
                attr_type = type(attr_value)
                if attr_name in attr_types:
                    existing = attr_types[attr_name]
                    attr_type = _resolve_multiple_types(attr_type, existing)
                    initial_existing = initial_attr_types[attr_name]
                    initial_type = _resolve_multiple_types(
                        initial_existing,
                        initial_type,
                    )

                attr_types[attr_name] = attr_type
                initial_attr_types[attr_name] = initial_type
                new_item[attr_name] = attr_value
            converted_element_dictionaries.append(new_item)

        initial_attr_types = {
            k: v if v != Optional[float] else float
            for k, v in initial_attr_types.items()
        }

        # ===== class definition =====

        def annotate(namespace):
            namespace["__annotations__"] = attr_types
            namespace["__module__"] = __name__

        Element = new_class("Element", (element_cls,), exec_body=annotate)

        # ===== define and register elements =====
        registries = {k: defaultdict(list) for k in attr_types}

        if issubclass(Element, tuple):
            def create(kwargs):
                return Element(*[kwargs.get(k) for k in attr_types])
        else:
            def create(kwargs):
                return Element(**kwargs)

        all_elements = []
        for element_dictionary in converted_element_dictionaries:
            el = create(element_dictionary)
            for attr_name, registry in registries.items():
                key = element_dictionary.get(attr_name)
                if key is not None:
                    initial_type = initial_attr_types[attr_name]
                    if attr_name in units:
                        key = initial_type(key / units[attr_name])
                    if initial_type == float and decimals is not None:
                        key = round(key, decimals)
                    registry[key].append(el)
            all_elements.append(el)

        clean_registries = {}
        for regname, regvalue in registries.items():
            if all(len(v) == 1 for v in regvalue.values()):
                regvalue = {k: v[0] for k, v in regvalue.items()}
            else:
                regvalue = {k: tuple(v) for k, v in regvalue.items()}

            clean_registries[regname] = regvalue

        # create container
        sorted_attrs = sorted(registries)
        Registry = namedtuple("Registry", sorted_attrs)
        proxies = [MappingProxyType(clean_registries[k]) for k in sorted_attrs]

        keys = [key_transform(getattr(el, key_attr)) for el in all_elements]
        Elements = namedtuple("Elements", keys)

        Elements.registry = Registry(*proxies)

        # ===== overwrite __new__ and __init__ =====

        def _get_key_and_value(key, value, getter):
            try:
                registry = getter(key)
            except (AttributeError, KeyError):
                raise ElementableError(
                    f"{key} attribute not supported. Available keys: "
                    ", ".join(sorted_attrs)
                )
            if key in converters:
                value = converters[key](value)

            if key in units:
                value = (0 * units[key]) + value
                value /= units[key]
                value = initial_attr_types[key](value)

            if (initial_attr_types[key] == float
                    and decimals is not None):
                value = round(value, decimals)

            try:
                return registry[value]
            except KeyError:
                raise InvalidElementError(f"{key}={value}")

        def _retrieve_element(cls, *args, **kwargs):
            if not kwargs and args:
                kwargs = {k: x for k, x in zip(attr_types, args)}
            if len(kwargs) == 1:
                key = list(kwargs)[0]
                return _get_key_and_value(
                    key, kwargs[key], Elements.registry.__getattribute__,
                )

            element_group = list(all_elements)
            for k, v in kwargs.items():
                if v is not None:
                    sub_group = _get_key_and_value(
                        k, v, registries.__getitem__,
                    )
                element_group = [x for x in element_group if x in sub_group]
            return tuple(element_group)

        initial_new = Element.__new__

        def _element_new(cls, *args, **kwargs):
            if not len(kwargs):
                return initial_new(cls, *args, **kwargs)
            possibilities = _retrieve_element(cls, *args, **kwargs)
            if isinstance(possibilities, Element):
                return possibilities
            n_possibilities = len(possibilities)
            if n_possibilities == 1:
                return possibilities[0]
            if not n_possibilities:
                return initial_new(cls, *args, **kwargs)
            return possibilities

        def dummy(self, **kwargs):
            pass  # pragma: no cover

        n_elements = len(all_elements)

        Element.__new__ = _element_new
        Element.__init__ = dummy
        Elements.__call__ = _retrieve_element
        Elements.n_elements = n_elements
        Elements.element_class = Element

        Elements = Elements(*all_elements)

        return Elements

    def __init__(
        self,
        units: Dict[str, Any] = {},
        converters: Dict[str, Callable] = {
            "name": lambda x: x.lower(),
            "symbol": lambda x: x.capitalize()
        },
        element_cls: Type = NamedTuple,
        json_file: str = resource_filename(__name__, "data/elements.json"),
        decimals: Optional[int] = 4,
    ):
        pass  # pragma: no cover


Elements = Elementable()
