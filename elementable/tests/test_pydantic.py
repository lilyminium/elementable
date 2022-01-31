
from unittest.mock import Mock

import pytest

from elementable import Elementable

from .base import BaseTestElementable

pydantic = pytest.importorskip("pydantic")

try:
    from openff.units import unit
except ImportError:
    unit = Mock()
    has_openff = False
else:
    has_openff = True


class TestPydanticElementable(BaseTestElementable):

    element_class = Elementable(
        element_cls=pydantic.BaseModel,
    )

    def test_json(self):
        h = self.element_class(atomic_number=1)
        assert h.atomic_number == 1
        h_dict = {
            "name": "hydrogen",
            "symbol": "H",
            "atomic_number": 1,
            "mass": 1.00782503223,
            "period": 1,
            "group": 1,
            "covalent_radius": 0.31
        }
        assert h.dict() == h_dict


@pytest.mark.skipif(not has_openff, reason="requires openff.units")
class TestUnitPydanticElementable(BaseTestElementable):
    from openff.units import unit

    element_class = Elementable(
        element_cls=pydantic.BaseModel,
        units=dict(
            mass=unit.amu,
            covalent_radius=unit.angstrom
        ),
    )
