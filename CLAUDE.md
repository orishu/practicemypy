# CLAUDE.md - Project Context for Claude Code

## Project Overview

This is **Practice MyPy** - a hands-on project for learning Python's type system through exercises. Each exercise teaches specific typing concepts with stub functions that need type hints added.

## Project Structure

```
practicemypy/
├── exercises/           # Exercise files (ex01_*.py through ex08_*.py)
├── tests/               # Corresponding test files (test_ex01.py through test_ex08.py)
├── README.md            # User-facing documentation
└── CLAUDE.md            # This file
```

## Exercise Progression

1. **ex01_generics_basics.py** - TypeVar, Generic classes
2. **ex02_typevar_constraints.py** - Constrained and bounded TypeVars
3. **ex03_protocols.py** - Protocols, @runtime_checkable, structural subtyping
4. **ex04_callable_and_overload.py** - Callable types, @overload, Literal
5. **ex05_paramspec.py** - ParamSpec, Concatenate for decorators
6. **ex06_typeddict_and_guards.py** - TypedDict, TypeGuard, NotRequired
7. **ex07_classvar_final_self.py** - ClassVar, Final, @final, Self
8. **ex08_newtypes_aliases_annotated.py** - NewType, TypeAlias, Annotated, cast

## Commands

```bash
# Run tests for an exercise
uv run pytest tests/test_ex01.py -v

# Run mypy type checking
uv run mypy exercises/ex01_generics_basics.py

# Run all tests
uv run pytest -v
```

## Exercise File Pattern

Each exercise file follows this structure:

1. **Module docstring** - Explains concepts covered, provides examples
2. **Parts** - Numbered sections (PART 1, PART 2, etc.) progressing in difficulty
3. **TODO comments** - Mark what the user needs to add
4. **Working runtime code** - Functions work at runtime, just need type hints
5. **Challenge section** - Final part is more difficult, combines concepts

Example function pattern:
```python
def some_function(param):
    """
    Description of what the function does.

    Examples:
        some_function(1) -> 2

    TODO: Add type hints for parameters and return type.
    """
    return param * 2  # Implementation works, needs type hints
```

## Creating New Exercises

When asked to create exercise N:

1. **Choose concepts** - Pick the next logical typing concepts not yet covered
2. **Create exercise file** - `exercises/ex{N:02d}_{topic}.py`
3. **Create test file** - `tests/test_ex{N:02d}.py`
4. **Update README.md** - Add section describing the new exercise
5. **Verify** - Run `uv run pytest tests/test_exNN.py -v` to ensure tests pass

### Key patterns:
- Functions should work at runtime (tests pass) but lack type hints
- Use `# TODO:` comments to guide the user
- Include docstrings with examples showing expected types
- Progress from basic to advanced within each exercise
- Final "Challenge" section combines multiple concepts
- All tests should pass with the stub implementations

## Git Workflow

- **main branch** - Contains unsolved exercises (no type hints)
- User solves exercises in a separate branch
- When generating new exercises, create them on main (unsolved state)

## Common Mypy Issues Users May Encounter

1. **TypedDict with conditional keys** - Use explicit type annotation on variable, then add keys
2. **NewType** - Must call the NewType to brand a value: `UserId(42)` not just `42`
3. **Self** - Import from typing, use for methods returning same class type
4. **ParamSpec** - Use `P.args` and `P.kwargs` in wrapper functions
