"""
Exercise 2: TypeVar Constraints and Bounds
==========================================

TypeVars can be constrained in two ways:
1. Constraints: TypeVar('T', int, str) - T must be EXACTLY one of these types
2. Bounds: TypeVar('T', bound=SomeClass) - T must be SomeClass or a subclass

This exercise explores these powerful features.

Run tests with: pytest tests/test_ex02.py -v
Run type checker with: mypy exercises/ex02_typevar_constraints.py
"""

from typing import TypeVar, Generic
from abc import ABC, abstractmethod

# =============================================================================
# PART 1: Constrained TypeVars
# =============================================================================

# A constrained TypeVar can only be one of the specified types.
# Unlike Union, the type checker tracks WHICH specific type it is.

# TODO: Create a TypeVar 'Number' that can only be int or float
# Hint: Number = TypeVar('Number', int, float)


def add_numbers(a, b):
    """
    Add two numbers of the same type.

    The key insight: both arguments must be the SAME type (both int or both float),
    and the return type matches that type.

    This is different from Union[int, float] which would allow mixing!

    Examples:
        add_numbers(1, 2) -> 3  (type: int)
        add_numbers(1.5, 2.5) -> 4.0  (type: float)
        add_numbers(1, 2.5)  # Should be a TYPE ERROR - mixing types!

    TODO: Add type hints using a constrained TypeVar.
    """
    return a + b


# TODO: Create a TypeVar 'StringLike' constrained to str and bytes


def double_it(value):
    """
    Double a string or bytes value by concatenating it with itself.

    Examples:
        double_it("abc") -> "abcabc"  (type: str)
        double_it(b"xyz") -> b"xyzxyz"  (type: bytes)

    TODO: Add type hints using a constrained TypeVar.
    """
    return value + value


# =============================================================================
# PART 2: Bounded TypeVars
# =============================================================================

# A bounded TypeVar accepts the bound type OR ANY SUBCLASS of it.
# This is useful when you need to work with class hierarchies.


class Animal(ABC):
    """Base class for animals."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def speak(self) -> str:
        """Return the sound this animal makes."""
        pass


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says: Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says: Meow!"


class Fish(Animal):
    def speak(self) -> str:
        return f"{self.name} says: ..."


# TODO: Create a TypeVar 'A' bounded by Animal
# Hint: A = TypeVar('A', bound=Animal)


def get_loudest(animals):
    """
    Return the animal with the longest speak() output.

    The return type should preserve the specific animal type from the input.
    If you pass list[Dog], you get Dog back, not just Animal.

    Examples:
        dogs = [Dog("Rex"), Dog("Buddy")]
        get_loudest(dogs)  # Returns Dog, not Animal

    TODO: Add type hints using a bounded TypeVar.
    The input should be a list of some Animal subtype, and return that same subtype.
    """
    if not animals:
        raise ValueError("Empty list")
    return max(animals, key=lambda a: len(a.speak()))


def make_speak_twice(animal):
    """
    Make an animal speak and return a tuple of (animal, speech, speech).

    This demonstrates that bounded TypeVars preserve the specific type.

    TODO: Add type hints. The returned animal should have the same type as input.
    """
    speech = animal.speak()
    return (animal, speech, speech)


# =============================================================================
# PART 3: Bounded TypeVars with Generic Classes
# =============================================================================


class Comparable(ABC):
    """A class that can be compared to others of the same type."""

    @abstractmethod
    def compare_to(self, other: "Comparable") -> int:
        """
        Return negative if self < other, 0 if equal, positive if self > other.
        """
        pass


class Score(Comparable):
    def __init__(self, value: int):
        self.value = value

    def compare_to(self, other: "Score") -> int:
        return self.value - other.value

    def __repr__(self) -> str:
        return f"Score({self.value})"


class Name(Comparable):
    def __init__(self, name: str):
        self.name = name

    def compare_to(self, other: "Name") -> int:
        if self.name < other.name:
            return -1
        elif self.name > other.name:
            return 1
        return 0

    def __repr__(self) -> str:
        return f"Name({self.name!r})"


# TODO: Create a TypeVar 'C' bounded by Comparable


class SortedContainer:
    """
    A container that keeps items sorted using their compare_to method.

    This should be generic over any Comparable subtype.

    Examples:
        sc = SortedContainer[Score]()
        sc.add(Score(50))
        sc.add(Score(30))
        sc.add(Score(70))
        sc.get_all()  # [Score(30), Score(50), Score(70)]

    TODO:
    1. Make this generic with a bounded TypeVar
    2. Add type hints to all methods
    """

    def __init__(self):
        self._items = []

    def add(self, item):
        """Add an item and keep the list sorted."""
        self._items.append(item)
        # Simple insertion sort for clarity
        self._items.sort(key=lambda x: (x.compare_to(self._items[0]) if self._items else 0))
        # Actually, let's do a proper sort
        self._sort()

    def _sort(self):
        """Sort items using compare_to."""
        # Bubble sort for simplicity
        n = len(self._items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self._items[j].compare_to(self._items[j + 1]) > 0:
                    self._items[j], self._items[j + 1] = self._items[j + 1], self._items[j]

    def get_min(self):
        """Get the minimum item, or None if empty."""
        if not self._items:
            return None
        return self._items[0]

    def get_max(self):
        """Get the maximum item, or None if empty."""
        if not self._items:
            return None
        return self._items[-1]

    def get_all(self):
        """Get all items in sorted order."""
        return list(self._items)


# =============================================================================
# PART 4: Challenge - Combining Constraints
# =============================================================================


class Serializable(ABC):
    """Something that can be converted to a string representation."""

    @abstractmethod
    def serialize(self) -> str:
        pass


class JsonValue(Serializable):
    def __init__(self, data: dict):
        self.data = data

    def serialize(self) -> str:
        import json
        return json.dumps(self.data)


class XmlValue(Serializable):
    def __init__(self, tag: str, content: str):
        self.tag = tag
        self.content = content

    def serialize(self) -> str:
        return f"<{self.tag}>{self.content}</{self.tag}>"


# TODO: Create appropriate TypeVar(s) for the Cache class


class Cache:
    """
    A simple cache that stores Serializable values.

    The cache should:
    1. Be generic over any Serializable subtype
    2. Return the same subtype that was stored

    Examples:
        cache = Cache[JsonValue]()
        cache.put("config", JsonValue({"debug": True}))
        val = cache.get("config")  # Should be JsonValue, not just Serializable

    TODO:
    1. Make this generic with an appropriate bounded TypeVar
    2. Add type hints
    """

    def __init__(self):
        self._store = {}

    def put(self, key, value):
        """Store a value with the given key."""
        self._store[key] = value

    def get(self, key):
        """Get a value by key, or None if not found."""
        return self._store.get(key)

    def get_serialized(self, key):
        """Get the serialized form of a value, or None if not found."""
        value = self._store.get(key)
        if value is None:
            return None
        return value.serialize()
