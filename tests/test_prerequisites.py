"""Tests for runtime precondition helpers."""

from typing import Any, Iterable, cast

import pytest

from prerequisites import (
    require,
    require_all_in_all,
    require_all_of_type,
    require_all_same_type,
    require_one_in_all,
    require_one_of_types,
    require_type,
    require_type_or_none,
)


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


def test_require_type_returns_original_value_for_valid_type() -> None:
    """Confirm `require_type` returns the original value when the type matches."""
    value = 7
    assert require_type(value, int) == value


def test_require_type_raises_for_invalid_expected_type_argument() -> None:
    """Ensure `require_type` fails fast when expected_type is not a type."""
    with pytest.raises(TypeError, match="expected_type must be a type"):
        require_type(1, cast(type[Any], "int"))


def test_require_one_of_types_raises_for_disallowed_type() -> None:
    """Confirm `require_one_of_types` raises when value type is not allowed."""
    with pytest.raises(TypeError):
        require_one_of_types(1, (dict, str))


def test_require_one_of_types_raises_for_non_type_entries() -> None:
    """Ensure invalid allowed type entries still surface a TypeError."""
    with pytest.raises(TypeError):
        require_one_of_types("value", cast(Iterable[type[Any]], (int, "str")))


def test_require_all_of_type_raises_for_mixed_iterable() -> None:
    """Confirm `require_all_of_type` rejects iterables with mixed element types."""
    with pytest.raises(TypeError):
        require_all_of_type([1, 2, 3, "a"], int)


def test_require_all_of_type_raises_for_invalid_expected_type_argument() -> None:
    """Ensure `require_all_of_type` fails fast when expected_type is not a type."""
    with pytest.raises(TypeError, match="expected_type must be a type"):
        require_all_of_type([1, 2, 3], cast(type[Any], "int"))


def test_require_all_same_type_accepts_empty_iterable() -> None:
    """Cover the empty iterable edge case, which should pass vacuously."""
    assert require_all_same_type([]) == []


def test_require_all_same_type_raises_for_mixed_types() -> None:
    """Ensure `require_all_same_type` rejects mixed element types."""
    with pytest.raises(TypeError):
        require_all_same_type(["test", 1])


def test_require_all_same_type_treats_bool_and_int_as_mixed_types() -> None:
    """Ensure exact type matching is enforced rather than subclass compatibility."""
    with pytest.raises(TypeError):
        require_all_same_type([True, 1])


def test_require_all_same_type_handles_unhashable_elements() -> None:
    """Guard regression where unhashable items caused internal set conversion errors."""
    values = [{"a": 1}, {"b": 2}]
    assert require_all_same_type(values) == values


def test_require_all_same_type_validates_allowed_types() -> None:
    """Ensure allowed types are enforced after same-type validation passes."""
    with pytest.raises(TypeError):
        require_all_same_type([1, 2, 3], (str,))


def test_require_type_or_none_accepts_none_and_matching_type() -> None:
    """Verify `require_type_or_none` accepts None and values of expected type."""
    assert require_type_or_none(None, int) is None
    assert require_type_or_none(21, int) == 21


def test_require_type_or_none_raises_for_invalid_non_none_value() -> None:
    """Ensure `require_type_or_none` rejects non-None values of unexpected type."""
    with pytest.raises(TypeError):
        require_type_or_none(1, str)
