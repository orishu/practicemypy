"""
Exercise 4: Callable Types and @overload
========================================

This exercise covers two important typing features:

1. Callable: Type hints for functions and callable objects
   - Basic syntax: Callable[[ArgType1, ArgType2], ReturnType]
   - Callable with no args: Callable[[], ReturnType]
   - Callable accepting any args: Callable[..., ReturnType]

2. @overload: Declaring multiple signatures for a single function
   - Useful when return type depends on input types
   - The overloads are for the type checker only - not runtime

Run tests with: pytest tests/test_ex04.py -v
Run type checker with: mypy exercises/ex04_callable_and_overload.py
"""

from typing import Callable, overload, TypeVar, Literal

# =============================================================================
# PART 1: Basic Callable Types
# =============================================================================


def apply_twice(func, value):
    """
    Apply a function twice to a value: func(func(value))

    Examples:
        apply_twice(lambda x: x + 1, 5) -> 7
        apply_twice(str.upper, "hi") -> "HI"  (already upper, so no change)

    TODO: Add type hints.
    - func should be a Callable that takes one argument and returns the same type
    - value should be that same type
    - return type should also be that same type

    Hint: You'll need a TypeVar, and Callable[[T], T]
    """
    return func(func(value))


def call_with_logging(func, *args):
    """
    Call a function and print what happened.

    Returns a tuple of (function_name, result).

    Examples:
        call_with_logging(abs, -5) -> ("abs", 5)
        call_with_logging(max, 1, 2, 3) -> ("max", 3)

    TODO: Add type hints.
    - func can be any callable (use Callable[..., T] for arbitrary args)
    - *args can be anything
    - Return type should be tuple[str, T]

    Hint: Callable[..., T] means "callable returning T with any arguments"
    """
    result = func(*args)
    return (func.__name__, result)


def make_repeater(n):
    """
    Return a function that repeats a string n times.

    Examples:
        repeat3 = make_repeater(3)
        repeat3("ha") -> "hahaha"

    TODO: Add type hints.
    - n is an int
    - Return type is a Callable that takes str and returns str

    Hint: Callable[[str], str]
    """
    def repeater(s: str) -> str:
        return s * n
    return repeater


# =============================================================================
# PART 2: Higher-Order Functions with Callable
# =============================================================================

T = TypeVar('T')
U = TypeVar('U')


def map_list(func, items):
    """
    Apply a function to each item in a list.

    Examples:
        map_list(str.upper, ["a", "b"]) -> ["A", "B"]
        map_list(lambda x: x * 2, [1, 2, 3]) -> [2, 4, 6]

    TODO: Add type hints using TypeVars.
    - func transforms T -> U
    - items is list[T]
    - return is list[U]
    """
    return [func(item) for item in items]


def filter_list(predicate, items):
    """
    Filter a list using a predicate function.

    Examples:
        filter_list(lambda x: x > 0, [-1, 0, 1, 2]) -> [1, 2]
        filter_list(str.isupper, ["A", "b", "C"]) -> ["A", "C"]

    TODO: Add type hints.
    - predicate takes T and returns bool
    - items is list[T]
    - return is list[T] (same type, filtered)
    """
    return [item for item in items if predicate(item)]


def compose(f, g):
    """
    Compose two functions: compose(f, g)(x) == f(g(x))

    Examples:
        add1 = lambda x: x + 1
        double = lambda x: x * 2
        add1_then_double = compose(double, add1)
        add1_then_double(5) -> 12  # double(add1(5)) = double(6) = 12

    TODO: Add type hints with three TypeVars (A, B, C).
    - g: A -> B
    - f: B -> C
    - return: A -> C
    """
    def composed(x):
        return f(g(x))
    return composed


# =============================================================================
# PART 3: Callable as Class Attribute
# =============================================================================


class EventHandler:
    """
    An event handler that stores and calls callback functions.

    Examples:
        handler = EventHandler()
        handler.on_success = lambda msg: print(f"Success: {msg}")
        handler.on_error = lambda code, msg: print(f"Error {code}: {msg}")
        handler.trigger_success("Done!")
        handler.trigger_error(404, "Not found")

    TODO: Add type hints for the callback attributes.
    - on_success: takes a str message, returns None
    - on_error: takes an int code and str message, returns None
    - Both can be None (not set)
    """

    def __init__(self):
        self.on_success = None
        self.on_error = None

    def trigger_success(self, message: str) -> None:
        if self.on_success:
            self.on_success(message)

    def trigger_error(self, code: int, message: str) -> None:
        if self.on_error:
            self.on_error(code, message)


# =============================================================================
# PART 4: @overload - Multiple Signatures
# =============================================================================

# @overload lets you declare multiple type signatures for a function.
# This is useful when the return type depends on the input type.
#
# Pattern:
#   @overload
#   def func(x: int) -> int: ...
#   @overload
#   def func(x: str) -> str: ...
#   def func(x: int | str) -> int | str:
#       # actual implementation
#
# The @overload versions are ONLY for the type checker - they use ...
# The final version (no decorator) is the actual implementation.


@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...

def double(x: int | str) -> int | str:
    """
    Double a value - works differently for int vs str.

    Examples:
        double(5) -> 10  (type: int)
        double("ha") -> "haha"  (type: str)

    The overloads above are already defined. This implementation is complete.
    Study how the @overload pattern works.
    """
    if isinstance(x, int):
        return x * 2
    return x + x


# TODO: Add @overload signatures for this function
def parse_value(value, as_int):
    """
    Parse a string value, optionally as an integer.

    Examples:
        parse_value("42", True) -> 42  (type: int)
        parse_value("42", False) -> "42"  (type: str)
        parse_value("hello", False) -> "hello"  (type: str)

    TODO: Add two @overload signatures above this function:
    1. When as_int is Literal[True], return int
    2. When as_int is Literal[False], return str

    Then update this function's signature to be the union.

    Hint: Use Literal[True] and Literal[False] for the overloads
    """
    if as_int:
        return int(value)
    return value


# TODO: Add @overload signatures for this function
def get_item(data, index, default=None):
    """
    Get an item from a list with an optional default.

    The return type depends on whether a default is provided:
    - With no default: returns T | None (might be None if index out of bounds)
    - With default: returns T (guaranteed to have a value)

    Examples:
        get_item([1, 2, 3], 0) -> 1  (type: int | None)
        get_item([1, 2, 3], 10) -> None  (type: int | None)
        get_item([1, 2, 3], 10, -1) -> -1  (type: int)

    TODO: Add two @overload signatures:
    1. (data: list[T], index: int) -> T | None
    2. (data: list[T], index: int, default: T) -> T

    This is tricky! The presence/absence of the default changes the return type.
    """
    try:
        return data[index]
    except IndexError:
        return default


# =============================================================================
# PART 5: Challenge - Retry Decorator with Callable
# =============================================================================


def retry(max_attempts):
    """
    A decorator that retries a function up to max_attempts times.

    Usage:
        @retry(3)
        def flaky_function():
            # might fail sometimes
            pass

    TODO: Add complete type hints to this decorator.

    This is challenging! The decorator:
    - Takes max_attempts: int
    - Returns a decorator that takes a Callable
    - That decorator returns a Callable with the same signature

    Hint: The inner function should preserve the type of the decorated function.
    You might want to use TypeVar for the return type at minimum.

    For a simpler version, just ensure the return type is preserved.
    For advanced: look into ParamSpec (we'll cover this in a future exercise).
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
            raise last_exception
        return wrapper
    return decorator


# =============================================================================
# PART 6: Challenge - Overload with Union Discrimination
# =============================================================================


class Success:
    def __init__(self, value: str):
        self.value = value


class Failure:
    def __init__(self, error: str):
        self.error = error


Result = Success | Failure


# TODO: Add @overload signatures for handle_result
def handle_result(result):
    """
    Handle a Result, extracting the value or error.

    Examples:
        handle_result(Success("data")) -> "data"  (type: str)
        handle_result(Failure("oops")) -> "oops"  (type: str)

    This function already returns str in both cases, but the overloads
    document the different paths through the code.

    TODO: Add overloads for Success and Failure inputs.
    This is more for documentation than type narrowing, but it's
    a common pattern you'll see in codebases.
    """
    if isinstance(result, Success):
        return result.value
    return result.error
