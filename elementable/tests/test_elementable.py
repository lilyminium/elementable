
import copy

import pytest
from elementable import Elements, Elementable
from elementable.exceptions import ElementableError

from .base import BaseTestElementable
from .datafiles import VEGETABLES_JSON


class TestStandardElementable(BaseTestElementable):
    element_class = Elements

    @pytest.mark.parametrize("mass", [119.90220163, 119.9022])
    def test_get_mass_single(self, mass):
        el = self.element_class(mass=mass)
        assert el.atomic_number == 50

    def test_get_covalent_radius_multiple(self):
        els = self.element_class(covalent_radius=1.39)
        assert len(els) == 5
        atomic_numbers = [el.atomic_number for el in els]
        assert atomic_numbers == [24, 46, 50, 51, 53]

    def test_copy(self):
        copied = copy.deepcopy(Elements.X)
        assert copied == Elements.X
        assert not copied is Elements.X


class TestCustomElementable:

    @pytest.fixture(scope="class")
    def element_class(self):
        return Elementable(json_file=VEGETABLES_JSON, key_attr="name")

    def test_create(self, element_class):
        assert element_class.n_elements == 3

    def test_custom_access(self, element_class):
        carrot = element_class(name="carrot")
        assert carrot.color == "orange"

        carrot2 = element_class(n_leaves=3)
        assert carrot is carrot2

    def test_invalid_access(self, element_class):
        with pytest.raises(
            ElementableError,
            match="parsnip attribute not supported",
        ):
            element_class(parsnip=3)
