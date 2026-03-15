"""Tests for decorator-based prerequisite helpers."""

from typing import Any

import pytest

from prerequisites.decorators import validate_types


def test_validate_types_validates_arguments_for_basic_annotations() -> None:
    """Ensure decorated functions validate basic argument type hints."""

    @validate_types
    def add(x: int, y: int) -> int:
        return x + y

    assert add(1, 2) == 3

    with pytest.raises(TypeError):
        add("1", 2)  # type: ignore[arg-type]


def test_validate_types_does_not_validate_return_type() -> None:
    """Ensure decorator enforces argument hints only, not return hints."""

    @validate_types
    def bad_return(x: int) -> int:
        return str(x)  # type: ignore[return-value]

    assert bad_return(1) == "1"


def test_validate_types_supports_union_and_none_values() -> None:
    """Ensure union annotations including None are accepted and validated."""

    @validate_types
    def identity(value: int | None) -> int | None:
        return value

    assert identity(1) == 1
    assert identity(None) is None

    with pytest.raises(TypeError):
        identity("1")  # type: ignore[arg-type]


def test_validate_types_handles_mixed_union_hints() -> None:
    """Ensure unions with parameterized and plain hints validate via fallback path."""

    @validate_types
    def consume(value: list[int] | str) -> int:
        return len(value)

    assert consume([1, 2]) == 2
    assert consume("ok") == 2

    with pytest.raises(TypeError):
        consume(1)  # type: ignore[arg-type]


def test_validate_types_allows_any_annotation() -> None:
    """Ensure `Any` annotations bypass type checks."""

    @validate_types
    def passthrough(value: Any) -> int:
        return 1

    assert passthrough(1) == 1
    assert passthrough("value") == 1


def test_validate_types_checks_none_annotation() -> None:
    """Ensure `None` annotation accepts only None values."""

    @validate_types
    def only_none(value: None) -> int:
        return 1

    assert only_none(None) == 1

    with pytest.raises(TypeError):
        only_none(1)  # type: ignore[arg-type]


def test_validate_types_shallow_mode_only_checks_outer_container() -> None:
    """Ensure shallow mode accepts invalid nested values when container type matches."""

    @validate_types
    def use_numbers(values: list[int]) -> int:
        return len(values)

    assert use_numbers(["a", "b"]) == 2  # type: ignore[list-item]


def test_validate_types_accepts_mismatched_list_items_in_shallow_mode() -> None:
    """Ensure list element hints are not enforced in first-level validation."""

    @validate_types
    def use_numbers(values: list[int]) -> int:
        return len(values)

    assert use_numbers([1, "a"]) == 2  # type: ignore[list-item]


def test_validate_types_accepts_mismatched_fixed_tuple_items_in_shallow_mode() -> None:
    """Ensure fixed tuple inner hints are not enforced in first-level validation."""

    @validate_types
    def read_pair(value: tuple[int, str]) -> str:
        return str(value[1])

    assert read_pair((1, "ok")) == "ok"
    assert read_pair((1, 2)) == "2"  # type: ignore[arg-type]


def test_validate_types_accepts_mismatched_variadic_tuple_items_in_shallow_mode() -> (
    None
):
    """Ensure variadic tuple item hints are not enforced in first-level validation."""

    @validate_types
    def total(values: tuple[int, ...]) -> int:
        return len(values)

    assert total((1, 2, 3)) == 3
    assert total((1, 2, "3")) == 3  # type: ignore[arg-type]


def test_validate_types_accepts_mismatched_dict_key_value_hints_in_shallow_mode() -> (
    None
):
    """Ensure dict inner hints are not enforced in first-level validation."""

    @validate_types
    def size(config: dict[str, bool]) -> int:
        return len(config)

    assert size({"enabled": True}) == 1
    assert size({1: "yes"}) == 1  # type: ignore[dict-item]


def test_validate_types_raises_for_outer_parameterized_type_mismatch() -> None:
    """Ensure outer container type mismatch is still rejected."""

    @validate_types
    def use_numbers(values: list[int]) -> int:
        return len(values)

    with pytest.raises(TypeError):
        use_numbers((1, 2))  # type: ignore[arg-type]


def test_validate_types_skips_unannotated_arguments() -> None:
    """Ensure unannotated parameters are ignored during argument validation."""

    @validate_types
    def consume(untyped, typed: int) -> int:  # type: ignore[no-untyped-def]
        return typed

    assert consume(object(), 1) == 1


def test_validate_types_works_with_instance_methods() -> None:
    """Ensure `self` is skipped during validation for bound methods."""

    class Service:
        @validate_types
        def handle(self, count: int) -> int:
            return count

    assert Service().handle(2) == 2
