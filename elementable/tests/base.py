
import pytest
from hypothesis import given, strategies as st

from elementable.exceptions import ElementableError, InvalidElementError


class BaseTestElementable:

    @given(z=st.integers(min_value=0, max_value=117))
    def test_atomic_number(self, z):
        el = self.element_class.registry.atomic_number[z]
        assert self.element_class(atomic_number=z) is el
        assert el.atomic_number == z
        assert type(el.atomic_number) is int

    @given(z=st.integers(max_value=-1))
    def test_invalid_atomic_number_negative(self, z):
        with pytest.raises(InvalidElementError):
            self.element_class(atomic_number=z)

    @given(z=st.integers(min_value=118))
    def test_invalid_atomic_number(self, z):
        with pytest.raises(InvalidElementError):
            self.element_class(atomic_number=z)

    @pytest.mark.parametrize("z, symbol", [
        (0, "*"),
        (8, "O"),
        (113, "NH"),
    ])
    def test_symbols(self, z, symbol):
        el = self.element_class(symbol=symbol)
        assert self.element_class.registry.symbol[symbol.capitalize()] is el
        assert el.atomic_number == z
        assert self.element_class.registry.atomic_number[z] is el

    @pytest.mark.parametrize("z, name", [
        (0, ""),
        (8, "OXYGEN"),
        (113, "nihonium"),
    ])
    def test_names(self, z, name):
        el = self.element_class(name=name)
        assert self.element_class.registry.name[name.lower()] is el
        assert el.atomic_number == z
        assert self.element_class.registry.atomic_number[z] is el

    def test_get_period(self):
        pd5 = self.element_class(period=5)
        # assert isinstance(pd5[0], self.element_class)
        assert len(pd5) == 18

    def test_get_period_error(self):
        with pytest.raises(ElementableError):
            self.element_class(period=111)

    def test_get_period_and_group(self):
        indium = self.element_class(period=5, group=13)
        assert len(indium) == 1

        indium = indium[0]
        assert indium.atomic_number == 49
        assert indium is self.element_class.In

    def test_get_period_and_group_missing(self):
        no_matches = self.element_class(period=111, group=1)
        assert len(no_matches) == 0

    def test_get_none(self):
        with pytest.raises(InvalidElementError):
            self.element_class(group=None)
