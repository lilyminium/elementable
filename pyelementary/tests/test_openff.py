
from .base import BaseTestElementary
from pyelementary import Elementary

import pytest
units = pytest.importorskip("openff.units")
unit = units.unit


class TestOpenFFElementary(BaseTestElementary):

    element_class = Elementary(
        units=dict(
            mass=unit.amu,
            covalent_radius=unit.angstrom
        ),
    )

    @pytest.mark.parametrize("mass", [
        119.90220163 * unit.amu,
        119.9022 * unit.amu,
        1.9910228997796515e-07 * unit.fg
    ])
    def test_get_mass_single(self, mass):
        el = self.element_class(mass=mass)
        assert el.atomic_number == 50

    @pytest.mark.parametrize("covalent_radius", [
        1.39 * unit.angstrom,
        0.139 * unit.nm,
    ])
    def test_get_covalent_radius_multiple(self, covalent_radius):
        els = self.element_class(covalent_radius=covalent_radius)
        assert len(els) == 5
        atomic_numbers = [el.atomic_number for el in els]
        assert atomic_numbers == [24, 46, 50, 51, 53]
