"""
Exercise 1: Generic Types Basics
================================

Python's typing system allows you to create generic types - types that are
parameterized by other types. This is similar to generics in Java/C# or
templates in C++.

Key concepts in this exercise:
- TypeVar: A type variable that acts as a placeholder for a specific type
- Generic: Base class for defining generic classes
- Using generic collections like list[T], dict[K, V]

Your task: Implement the functions and classes below so they pass the type
checker (mypy/pyright) AND the unit tests.

Run tests with: pytest tests/test_ex01.py -v
Run type checker with: mypy exercises/ex01_generics_basics.py
"""

from typing import TypeVar, Generic

# =============================================================================
# PART 1: Using TypeVar for Generic Functions
# =============================================================================

# TODO: Define a TypeVar named 'T' that can be any type
# Hint: T = TypeVar('T')


def first_element(items):
    """
    Return the first element of a list.

    The return type should match the element type of the input list.
    If the list is empty, return None.

    Examples:
        first_element([1, 2, 3]) -> 1  (type: int | None)
        first_element(["a", "b"]) -> "a"  (type: str | None)
        first_element([]) -> None

    TODO: Add proper type hints to the function signature.
    The function should be generic - if you pass list[int], you get int | None back.
    """
    if not items:
        return None
    return items[0]


def identity(value):
    """
    Return the value unchanged.

    This is the simplest generic function - it preserves the exact type
    of its input.

    Examples:
        identity(42) -> 42  (type: int)
        identity("hello") -> "hello"  (type: str)

    TODO: Add type hints so the return type matches the input type exactly.
    """
    return value


# =============================================================================
# PART 2: Generic Functions with Multiple Type Variables
# =============================================================================

# TODO: Define additional TypeVars K and V for key and value types


def swap_dict(d):
    """
    Swap keys and values in a dictionary.

    Examples:
        swap_dict({"a": 1, "b": 2}) -> {1: "a", 2: "b"}
        swap_dict({1: "x", 2: "y"}) -> {"x": 1, "y": 2}

    TODO: Add type hints using two TypeVars (K for keys, V for values).
    The return type should be dict[V, K] when input is dict[K, V].
    """
    return {v: k for k, v in d.items()}


def make_pair(first, second):
    """
    Create a tuple from two values of potentially different types.

    Examples:
        make_pair(1, "a") -> (1, "a")  (type: tuple[int, str])
        make_pair("x", "y") -> ("x", "y")  (type: tuple[str, str])

    TODO: Add type hints using two TypeVars so the tuple type is precise.
    """
    return (first, second)


# =============================================================================
# PART 3: Generic Classes
# =============================================================================


class Box:
    """
    A simple container that holds a single value of any type.

    This should be a generic class parameterized by the type it contains.

    Examples:
        box_int = Box(42)  # Box[int]
        box_int.get() -> 42
        box_int.set(100)

        box_str = Box("hello")  # Box[str]
        box_str.get() -> "hello"

    TODO:
    1. Make this class generic by inheriting from Generic[T]
    2. Add proper type hints to __init__, get, and set methods
    """

    def __init__(self, value):
        self._value = value

    def get(self):
        return self._value

    def set(self, value):
        self._value = value


class Pair:
    """
    A container holding two values of potentially different types.

    This demonstrates a generic class with multiple type parameters.

    Examples:
        p = Pair("name", 42)  # Pair[str, int]
        p.first -> "name"
        p.second -> 42
        p.swap() -> Pair[int, str] with (42, "name")

    TODO:
    1. Make this class generic with two type parameters
    2. Add type hints to all methods
    3. Note: swap() should return a NEW Pair with swapped types
    """

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def swap(self):
        """Return a new Pair with first and second swapped."""
        return Pair(self.second, self.first)


# =============================================================================
# PART 4: Challenge - Generic Stack
# =============================================================================


class Stack:
    """
    A generic stack (LIFO) data structure.

    Examples:
        s = Stack[int]()
        s.push(1)
        s.push(2)
        s.pop() -> 2
        s.peek() -> 1
        s.is_empty() -> False

    TODO:
    1. Make this class generic
    2. Add proper type hints
    3. push() should only accept items of the stack's type
    4. pop() and peek() should return the stack's type or None if empty
    """

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            return None
        return self._items.pop()

    def peek(self):
        if not self._items:
            return None
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0
