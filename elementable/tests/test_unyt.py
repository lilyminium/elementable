import pytest

from elementable import Elementable

from .base import BaseTestElementable

pytest.importorskip("unyt")


class TestUnytElementable(BaseTestElementable):
    from unyt import amu, angstrom, fg, nm

    element_class = Elementable(
        units=dict(
            mass=amu,
            covalent_radius=angstrom
        ),
    )

    @pytest.mark.parametrize("mass", [
        119.90220163 * amu,
        119.9022 * amu,
        1.9910228997796515e-07 * fg
    ])
    def test_get_mass_single(self, mass):
        el = self.element_class(mass=mass)
        assert el.atomic_number == 50

    @pytest.mark.parametrize("covalent_radius", [
        1.39 * angstrom,
        0.139 * nm,
    ])
    def test_get_covalent_radius_multiple(self, covalent_radius):
        els = self.element_class(covalent_radius=covalent_radius)
        assert len(els) == 5
        atomic_numbers = [el.atomic_number for el in els]
        assert atomic_numbers == [24, 46, 50, 51, 53]
