"""Value-based prerequisite checks."""

from collections.abc import Iterable


def require(condition: bool, message: str = "Requirement failed!") -> None:
    """
    Validate a single boolean condition.

    Parameters
    ----------
    condition : bool
        Condition that must evaluate to ``True``.
    message : str, default="Requirement failed!"
        Error message used when the condition is ``False``.

    Raises
    ------
    ValueError
        Raised when ``condition`` is ``False``.

    """
    if not condition:
        raise ValueError(message)


def require_one_in_all(
    collection_conditions: Iterable[bool],
    message: str = "Not even one requirement met!",
) -> None:
    """
    Validate that at least one condition in an iterable is true.

    Parameters
    ----------
    collection_conditions : Iterable[bool]
        Iterable of boolean conditions.
    message : str, default="Not even one requirement met!"
        Error message used when no condition is true.

    Raises
    ------
    ValueError
        Raised when all provided conditions are false.

    """
    if not any(collection_conditions):
        raise ValueError(message)


def require_all_in_all(
    collection_conditions: Iterable[bool],
    message: str = "Not all requirements met!",
) -> None:
    """
    Validate that all conditions in an iterable are true.

    Parameters
    ----------
    collection_conditions : Iterable[bool]
        Iterable of boolean conditions.
    message : str, default="Not all requirements met!"
        Error message used when any condition is false.

    Raises
    ------
    ValueError
        Raised when at least one condition is false.

    """
    if not all(collection_conditions):
        raise ValueError(message)
