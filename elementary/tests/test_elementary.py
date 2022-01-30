"""
Unit and regression test for the elementary package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import elementary


def test_elementary_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "elementary" in sys.modules
