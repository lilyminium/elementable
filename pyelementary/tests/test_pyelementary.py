
from tkinter import E
import pytest
from pyelementary import Element, Elementary

from .base import BaseTestElementary
from .datafiles import VEGETABLES_JSON


class TestStandardElementary(BaseTestElementary):
    element_class = Element

    @pytest.mark.parametrize("mass", [119.90220163, 119.9022])
    def test_get_mass_single(self, mass):
        el = self.element_class(mass=mass)
        assert el.atomic_number == 50

    def test_get_covalent_radius_multiple(self):
        els = self.element_class(covalent_radius=1.39)
        assert len(els) == 5
        atomic_numbers = [el.atomic_number for el in els]
        assert atomic_numbers == [24, 46, 50, 51, 53]


class TestCustomElementary:

    @pytest.fixture(scope="class")
    def element_class(self):
        return Elementary(json_file=VEGETABLES_JSON)

    def test_create(self, element_class):
        assert element_class.n_elements == 3

    def test_custom_access(self, element_class):
        carrot = element_class(name="carrot")
        assert carrot.color == "orange"

        carrot2 = element_class(n_leaves=3)
        assert carrot is carrot2
