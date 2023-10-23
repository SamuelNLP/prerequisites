# python-template
[![GitHub license](https://img.shields.io/github/license/SamuelNLP/pyhon-template)](https://github.com/SamuelNLP/pyhon-template/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/SamuelNLP/pyhon-template/branch/master/graph/badge.svg?token=5CGG6XOCIW)](https://codecov.io/gh/SamuelNLP/pyhon-template)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9a6c9cdfe8c94c7584b84da80f97ccc8)](https://app.codacy.com/gh/SamuelNLP/pyhon-template?utm_source=github.com&utm_medium=referral&utm_content=SamuelNLP/pyhon-template&utm_campaign=Badge_Grade_Settings)

This is a skeleton repo to be used as a python template for future projects.

## Guidelines

To make things easier, we're also using Python's [Black](https://black.readthedocs.io/en/stable/)
tool to deal with code formatting.

When developing code for this repository, please be sure you install the
[pre-commit hooks](https://pre-commit.com/#install):

```bash
cd path/to/repo
pre-commit install
```

Afterwards, whenever you try to commit changes, the pre-commit hooks
will run and inform you of possible warnings/errors that must be fixed.

## Utilities

### Profiling with cProfile and snakeviz

```bash
# using cProfile
python -m cProfile -o foo.stats foo.py

sudo pip install snakeviz
snakeviz foo.pstats

# The visualization is opened in the browser in: http://127.0.0.1:8080
```

### Profiling with line_profiles

Decorate the functions to profile with `@profile`:
```python
@profile
def slow_function(a, b, c):
    ...
```

run the `kernprof` command on the script:
```bash
kernprof -l script_to_profile.py
python -m line_profiler script_to_profile.py.lprof
```
