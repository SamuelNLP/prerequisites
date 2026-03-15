"""Decorator-based argument validation from runtime type hints."""

import inspect
import types

from collections.abc import Callable
from functools import wraps
from typing import (
    Any,
    ParamSpec,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from prerequisites.types import require_one_of_types, require_type

ParamType = ParamSpec("ParamType")
ReturnType = TypeVar("ReturnType")


def _validate_union_hint(value: Any, hint: Any) -> None:
    """
    Validate a value against a union hint.

    Parameters
    ----------
    value : Any
        Runtime value being validated.
    hint : Any
        Union hint resolved from ``typing.get_type_hints``.

    Raises
    ------
    TypeError
        Raised when ``value`` does not match any supported union member, or
        when the union contains unsupported members.

    Notes
    -----
    Parameterized members such as ``list[int]`` are reduced to their runtime
    outer type (``list``).

    """
    allowed_types: list[type[Any]] = []

    for union_hint in get_args(hint):
        if union_hint is Any:
            return

        if union_hint is None:
            allowed_types.append(type(None))
            continue

        origin = get_origin(union_hint)
        if origin is not None and isinstance(origin, type):
            allowed_types.append(origin)
            continue

        if isinstance(union_hint, type):
            allowed_types.append(union_hint)
            continue

        continue

    if not allowed_types:
        return

    require_one_of_types(value, tuple(allowed_types))


def _validate_value_against_hint(
    value: Any,
    hint: Any,
) -> None:
    """
    Validate one runtime value against a resolved type hint.

    Parameters
    ----------
    value : Any
        Runtime value being validated.
    hint : Any
        Type hint resolved from ``typing.get_type_hints``.

    Raises
    ------
    TypeError
        Raised when ``value`` does not satisfy ``hint``.

    Notes
    -----
    Validation is shallow. Parameterized hints are validated by their outer
    runtime type only.

    """
    if hint is Any:
        return

    if hint is None or hint is type(None):
        require_type(value, type(None))
        return

    origin = get_origin(hint)

    if origin is Union or origin is types.UnionType:
        _validate_union_hint(
            value,
            hint,
        )
        return

    target_type: type[Any] | None = None

    if origin is not None and isinstance(origin, type):
        target_type = origin
    elif isinstance(hint, type):
        target_type = hint

    if target_type is not None:
        require_type(value, target_type)
        return

    return


def validate_types(
    function: Callable[ParamType, ReturnType],
) -> Callable[ParamType, ReturnType]:
    """
    Validate call arguments from function type hints.

    Parameters
    ----------
    function : Callable[ParamType, ReturnType]
        Function to wrap.

    Returns
    -------
    Callable[ParamType, ReturnType]
        Wrapped function validated at call time.

    Raises
    ------
    TypeError
        Raised at call time when an annotated argument does not match its hint.

    Notes
    -----
    Parameterized hints are validated at the outer type only. For example,
    ``list[int]`` checks that the value is a ``list``.

    """
    signature = inspect.signature(function)
    resolved_hints: dict[str, Any] | None = None

    @wraps(function)
    def wrapper(*args: ParamType.args, **kwargs: ParamType.kwargs) -> ReturnType:
        nonlocal resolved_hints

        if resolved_hints is None:
            resolved_hints = get_type_hints(function)

        bound_arguments = signature.bind(*args, **kwargs)
        bound_arguments.apply_defaults()

        for argument_name, argument_value in bound_arguments.arguments.items():
            if argument_name in {"self", "cls"}:
                continue

            hint = resolved_hints.get(argument_name)
            if hint is None:
                continue

            _validate_value_against_hint(argument_value, hint)

        return function(*args, **kwargs)

    return wrapper
