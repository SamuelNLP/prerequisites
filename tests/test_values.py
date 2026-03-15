"""Tests for value-based prerequisite helpers."""

import pytest

from prerequisites.values import require, require_all_in_all, require_one_in_all


def test_require_raises_value_error_when_condition_is_false() -> None:
    """Verify `require` rejects false conditions with the provided message."""
    with pytest.raises(ValueError, match="condition failed"):
        require(False, "condition failed")


def test_require_one_in_all_raises_when_all_conditions_are_false() -> None:
    """Ensure `require_one_in_all` fails when no condition is met."""
    with pytest.raises(ValueError):
        require_one_in_all([False, 1 < 0, 2 < 1])


def test_require_all_in_all_raises_when_any_condition_is_false() -> None:
    """Ensure `require_all_in_all` fails when one condition is not met."""
    with pytest.raises(ValueError):
        require_all_in_all([True, 2 > 1, False])
