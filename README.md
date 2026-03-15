# prerequisites

Small runtime validation helpers for preconditions and type checks.

## Install

```bash
pip install prerequisites
```

## What it provides

- Value checks: `require`, `require_one_in_all`, `require_all_in_all`
- Type checks: `require_type`, `require_one_of_types`, `require_all_of_type`, `require_all_same_type`, `require_type_or_none`
- Decorator checks: `@validate_types` for argument validation using type hints

## Quick examples

### Value checks

```python
from prerequisites import require, require_all_in_all, require_one_in_all

require(2 > 1)
require_one_in_all([False, True, False])
require_all_in_all([True, 2 + 2 == 4])
```

### Type checks

```python
from prerequisites import (
    require_all_of_type,
    require_all_same_type,
    require_one_of_types,
    require_type,
    require_type_or_none,
)

require_type(10, int)
require_one_of_types(3.14, (int, float))
require_all_of_type([1, 2, 3], int)
require_all_same_type(["a", "b", "c"], (str,))
require_type_or_none(None, str)
```

### Decorator validation

```python
from prerequisites import validate_types

@validate_types
def add(a: int, b: int) -> int:
    return a + b

add(1, 2)      # ok
add("1", 2)   # raises TypeError
```

### Shallow container behavior

`@validate_types` validates only outer container types for parameterized hints.

```python
from prerequisites import validate_types

@validate_types
def count(values: list[int]) -> int:
    return len(values)

count([1, 2, 3])
count([1, "x"])  # valid in current shallow mode (still a list)
```

## Notes

- `@validate_types` validates function arguments only.
- Return annotations are not enforced.
- Errors raise `TypeError` or `ValueError` depending on the helper.
