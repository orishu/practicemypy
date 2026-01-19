# Practice MyPy - Python Typing Exercises

A hands-on project for learning Python's type system through exercises.

## Setup

```bash
# Add development dependencies
uv add --dev pytest mypy

# Verify installation
uv run pytest --version
uv run mypy --version
```

## Exercises

Each exercise file contains:
- Docstrings explaining the concepts
- Stub functions/classes with `TODO` comments
- Working implementations that need type hints

### Exercise 1: Generic Types Basics
`exercises/ex01_generics_basics.py`
- TypeVar basics
- Generic functions
- Generic classes with `Generic[T]`

### Exercise 2: TypeVar Constraints and Bounds
`exercises/ex02_typevar_constraints.py`
- Constrained TypeVars (`TypeVar('T', int, str)`)
- Bounded TypeVars (`TypeVar('T', bound=SomeClass)`)
- Generic classes with bounds

### Exercise 3: Protocols (Structural Subtyping)
`exercises/ex03_protocols.py`
- Basic Protocols
- Protocols with properties
- `@runtime_checkable` Protocols
- Generic Protocols

### Exercise 4: Callable and @overload
`exercises/ex04_callable_and_overload.py`
- `Callable[[Args], Return]` type hints
- Higher-order functions
- `@overload` for multiple signatures
- `Literal` types with overloads

### Exercise 5: ParamSpec and Concatenate
`exercises/ex05_paramspec.py`
- `ParamSpec` for preserving function signatures in decorators
- `Concatenate` for adding/removing parameters
- Decorator factories with full type safety
- Method decorators with `self` handling

### Exercise 6: TypedDict and Type Guards
`exercises/ex06_typeddict_and_guards.py`
- `TypedDict` for typed dictionary structures (JSON, API responses)
- `NotRequired` for optional keys
- Nested `TypedDict` for complex structures
- `TypeGuard` for custom type narrowing functions
- Discriminated unions with `Literal` type fields

### Exercise 7: ClassVar, Final, and Self
`exercises/ex07_classvar_final_self.py`
- `ClassVar` for class variables vs instance variables
- `Final` for immutable values and constants
- `@final` decorator to prevent subclassing/overriding
- `Self` type for fluent interfaces and factory methods
- Proper typing for method chaining and inheritance

## Workflow

1. Read the exercise file and understand the concepts
2. Add type hints to functions/classes marked with `TODO`
3. Run tests to verify runtime behavior:
   ```bash
   uv run pytest tests/test_ex01.py -v
   ```
4. Run mypy to verify type correctness:
   ```bash
   uv run mypy exercises/ex01_generics_basics.py
   ```
5. Fix any type errors and repeat

## Tips

- Start with Exercise 1 and progress in order
- Read the docstrings carefully - they explain what types are expected
- When stuck, check Python's `typing` module docs
- The tests show expected runtime behavior; mypy checks type safety
