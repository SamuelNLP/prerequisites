"""Type-based prerequisite checks."""

from collections.abc import Iterable
from typing import Any, TypeVar

TypeX = TypeVar("TypeX")
TypeY = TypeVar("TypeY", bound=Iterable[Any])


def require_type(variable: TypeX, expected_type: type[Any]) -> TypeX:
    """
    Validate that a value is an instance of a specific type.

    Parameters
    ----------
    variable : TypeX
        Value to validate.
    expected_type : type[Any]
        Type that ``variable`` must satisfy.

    Returns
    -------
    TypeX
        The original ``variable`` when validation succeeds.

    Raises
    ------
    TypeError
        Raised when ``expected_type`` is not a concrete type or when
        ``variable`` is not an instance of ``expected_type``.

    """
    if not isinstance(expected_type, type):
        raise TypeError(
            f"expected_type must be a type, got {type(expected_type).__name__}."
        )

    if not isinstance(variable, expected_type):
        raise TypeError(
            f"Expected {expected_type.__name__}, got {type(variable).__name__}."
        )

    return variable


def require_one_of_types(variable: TypeX, allowed_types: Iterable[type[Any]]) -> TypeX:
    """
    Validate that a value matches at least one allowed type.

    Parameters
    ----------
    variable : TypeX
        Value to validate.
    allowed_types : Iterable[type[Any]]
        Accepted runtime types.

    Returns
    -------
    TypeX
        The original ``variable`` when validation succeeds.

    Raises
    ------
    TypeError
        Raised when ``variable`` is not an instance of any provided type.

    """
    if not any(isinstance(variable, allowed_type) for allowed_type in allowed_types):
        raise TypeError(
            f"Expected one of {allowed_types} types in variable, got {type(variable)}!"
        )

    return variable


def require_all_of_type(iterable: TypeY, expected_type: type[Any]) -> TypeY:
    """
    Validate that every item in an iterable matches one type.

    Parameters
    ----------
    iterable : TypeY
        Iterable whose items are validated.
    expected_type : type[Any]
        Required item type.

    Returns
    -------
    TypeY
        The original ``iterable`` when validation succeeds.

    Raises
    ------
    TypeError
        Raised when ``expected_type`` is not a concrete type or when at least
        one item is not an instance of ``expected_type``.

    """
    if not isinstance(expected_type, type):
        raise TypeError(
            f"expected_type must be a type, got {type(expected_type).__name__}."
        )

    if not all(isinstance(variable, expected_type) for variable in iterable):
        raise TypeError(f"Expected all values to be {expected_type.__name__}.")

    return iterable


def require_all_same_type(
    iterable: TypeY, allowed_types: Iterable[type[Any]] | None = None
) -> TypeY:
    """
    Validate that all items in an iterable have one exact runtime type.

    Parameters
    ----------
    iterable : TypeY
        Iterable whose items are validated.
    allowed_types : Iterable[type[Any]] | None, default=None
        Optional allowed types for the detected item type.

    Returns
    -------
    TypeY
        The original ``iterable`` when validation succeeds.

    Raises
    ------
    TypeError
        Raised when items do not share one exact type or when the detected
        type is not present in ``allowed_types``.

    Notes
    -----
    Type equality uses ``type(item) is type(first_item)`` rather than
    ``isinstance``.

    """
    iterator = iter(iterable)

    try:
        first_element = next(iterator)
    except StopIteration:
        return iterable

    if any(type(item) is not type(first_element) for item in iterator):
        raise TypeError("All elements of iterable must be of the same type.")

    if allowed_types is not None:
        require_one_of_types(first_element, allowed_types)

    return iterable


def require_type_or_none(
    variable: TypeX | None, expected_type: type[Any]
) -> TypeX | None:
    """
    Validate a value against a type while allowing ``None``.

    Parameters
    ----------
    variable : TypeX | None
        Value to validate.
    expected_type : type[Any]
        Required type when ``variable`` is not ``None``.

    Returns
    -------
    TypeX | None
        ``None`` when input is ``None``; otherwise the original value.

    Raises
    ------
    TypeError
        Raised when ``variable`` is not ``None`` and fails ``expected_type``.

    """
    if variable is None:
        return None
    return require_type(variable, expected_type)
