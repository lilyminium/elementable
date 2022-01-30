from typing import Type, Dict, Any, NamedTuple, Optional, Callable
from types import MappingProxyType, new_class
from pkg_resources import resource_filename
from collections import namedtuple, defaultdict
import json

from .exceptions import InvalidElementError, ElementaryError

__all__ = ["Elementary", "Element"]


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


class Elementary(type):
    def __new__(
        cls,
        units: Dict[str, Any] = {},
        converters: Dict[str, Callable] = {
            "name": lambda x: x.lower(),
            "symbol": lambda x: x.capitalize()
        },
        element_cls: Type = NamedTuple,
        json_file: str = resource_filename(__name__, "data/elements.json"),
        decimals: Optional[int] = 4,
    ):

        # ===== load elements from json =====
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
                # if attr_name in units and attr_value is not None:
                #     attr_value = attr_value * units[attr_name]
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
                if initial_attr_types[attr_name] == float and key is not None:
                    if decimals is not None:
                        key = round(key, decimals)
                if key is not None:
                    registry[key].append(el)
            all_elements.append(el)

        clean_registries = {}
        for regname, regvalue in registries.items():
            if all(len(v) == 1 for v in regvalue.values()):
                regvalue = {k: v[0] for k, v in regvalue.items()}
            else:
                regvalue = {k: tuple(v) for k, v in regvalue.items()}

            clean_registries[regname] = regvalue

        sorted_attrs = sorted(registries)
        Registry = namedtuple("Registry", sorted_attrs)
        proxies = [MappingProxyType(clean_registries[k]) for k in sorted_attrs]
        Element.registry = Registry(*proxies)

        # ===== overwrite __new__ and __init__ =====

        def _get_key_and_value(key, value, getter):
            try:
                registry = getter(key)
            except (AttributeError, KeyError):
                raise ElementaryError(
                    f"{key} attribute not supported. Available keys: "
                    ", ".join(sorted_attrs)
                )
            if key in converters:
                value = converters[key](value)

            if key in units:
                value = (0 * units[key]) + value
                value /= units[key]
                value = initial_attr_types[key](value)

            if initial_attr_types[key] == float and decimals is not None:
                value = round(value, decimals)

            try:
                return registry[value]
            except KeyError:
                raise InvalidElementError(f"{key}={value}")

        def _element_new(cls, **kwargs):
            if len(kwargs) == 1:
                key = list(kwargs)[0]
                return _get_key_and_value(
                    key, kwargs[key], cls.registry.__getattribute__,
                )

            element_group = list(all_elements)
            for k, v in kwargs.items():
                sub_group = _get_key_and_value(
                    k, v, registries.__getitem__,
                )
                element_group = [x for x in element_group if x in sub_group]
            return tuple(sorted(element_group, key=lambda x: x.atomic_number))

        def _element_init(self, **kwargs):
            pass

        n_elements = len(all_elements)

        Element.__new__ = _element_new
        Element.__init__ = _element_init
        Element.n_elements = n_elements

        return Element

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
        pass


Element = Elementary()
