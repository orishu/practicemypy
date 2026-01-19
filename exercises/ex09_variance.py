"""
Exercise 9: Variance - Covariance and Contravariance
=====================================================

Variance describes how subtyping between generic types relates to subtyping
of their type parameters. This is one of the most important (and often
confusing) concepts in type theory.

The Problem:
    If Dog is a subtype of Animal, is list[Dog] a subtype of list[Animal]?

    Intuitively, you might say "yes" - but it's actually unsafe!

    def add_cat(animals: list[Animal]) -> None:
        animals.append(Cat())  # This is valid for list[Animal]

    dogs: list[Dog] = [Dog(), Dog()]
    add_cat(dogs)  # If allowed, we just put a Cat in a list of Dogs!

Three kinds of variance:

1. Invariant (default): list[Dog] is NOT a subtype of list[Animal]
   - Safe for both reading AND writing
   - Most mutable containers are invariant

2. Covariant: Sequence[Dog] IS a subtype of Sequence[Animal]
   - Safe for reading only (producers/sources)
   - Use TypeVar(..., covariant=True)

3. Contravariant: Callable[[Animal], None] IS a subtype of Callable[[Dog], None]
   - Safe for writing only (consumers/sinks)
   - Use TypeVar(..., contravariant=True)

Run tests with: pytest tests/test_ex09.py -v
Run type checker with: mypy exercises/ex09_variance.py
"""

from typing import TypeVar, Generic, Callable, Sequence, Iterable
from abc import ABC, abstractmethod


# =============================================================================
# PART 1: Understanding the Problem - Why Invariance Matters
# =============================================================================

class Animal:
    """Base class for all animals."""
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} makes a sound"


class Dog(Animal):
    """A dog is an Animal."""
    def speak(self) -> str:
        return f"{self.name} says woof!"

    def fetch(self) -> str:
        return f"{self.name} fetches the ball"


class Cat(Animal):
    """A cat is an Animal."""
    def speak(self) -> str:
        return f"{self.name} says meow!"

    def scratch(self) -> str:
        return f"{self.name} scratches the furniture"


# This demonstrates WHY list is invariant:

def add_animal(animals, animal):
    """
    Add an animal to a list.

    TODO: Add type hints (animals: list[Animal], animal: Animal) -> None

    Note: If list were covariant, this would be unsafe!
    Someone could pass list[Dog] and we'd add a Cat to it.
    """
    animals.append(animal)


def get_first_animal(animals):
    """
    Get the first animal from a list.

    TODO: Add type hints (animals: list[Animal]) -> Animal | None

    Reading from the list is safe - we always get an Animal.
    """
    if animals:
        return animals[0]
    return None


# =============================================================================
# PART 2: Covariance - Read-Only/Producer Types
# =============================================================================

# Covariant types are safe for READING (producing values).
# If Dog <: Animal, then Producer[Dog] <: Producer[Animal]
# "The output can be more specific"

# TODO: Create a covariant TypeVar
# T_co = TypeVar('T_co', covariant=True)


class ReadOnlyBox:
    """
    A box that can only be read from, not written to.

    Because we can only GET values (never PUT), it's safe to be covariant.
    A ReadOnlyBox[Dog] can be used wherever ReadOnlyBox[Animal] is expected.

    TODO:
    1. Define T_co = TypeVar('T_co', covariant=True)
    2. Make this class Generic[T_co]
    3. Add type hints to methods
    """

    def __init__(self, value):
        self._value = value

    def get(self):
        """Get the value from the box."""
        return self._value

    def peek(self):
        """Same as get - just another way to read."""
        return self._value


def process_animal_box(box):
    """
    Process any box containing an Animal.

    TODO: Add type hint using ReadOnlyBox[Animal]

    Because ReadOnlyBox is covariant, this should accept:
    - ReadOnlyBox[Animal]
    - ReadOnlyBox[Dog]  (Dog is subtype of Animal)
    - ReadOnlyBox[Cat]  (Cat is subtype of Animal)
    """
    animal = box.get()
    return animal.speak()


class ImmutableList:
    """
    An immutable list that only supports reading.

    Like tuple, this can be covariant because you can't add wrong types.

    TODO:
    1. Make this covariant over its element type
    2. Add type hints to all methods
    """

    def __init__(self, items):
        self._items = tuple(items)  # Store as tuple for immutability

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def first(self):
        """Get the first item, or None if empty."""
        if self._items:
            return self._items[0]
        return None


# =============================================================================
# PART 3: Contravariance - Write-Only/Consumer Types
# =============================================================================

# Contravariant types are safe for WRITING (consuming values).
# If Dog <: Animal, then Consumer[Animal] <: Consumer[Dog]
# "The input can be more general"

# This seems backwards! But think about it:
# A function that can handle ANY Animal can certainly handle a Dog.
# So Callable[[Animal], None] can be used where Callable[[Dog], None] is needed.

# TODO: Create a contravariant TypeVar
# T_contra = TypeVar('T_contra', contravariant=True)


class WriteOnlyBox:
    """
    A box that can only be written to, not read from.

    Because we can only PUT values (never GET), it's safe to be contravariant.
    A WriteOnlyBox[Animal] can be used wherever WriteOnlyBox[Dog] is expected,
    because if it accepts any Animal, it certainly accepts Dogs.

    TODO:
    1. Define T_contra = TypeVar('T_contra', contravariant=True)
    2. Make this class Generic[T_contra]
    3. Add type hints
    """

    def __init__(self):
        self._values = []

    def put(self, value):
        """Put a value into the box."""
        self._values.append(value)

    def count(self):
        """Return how many items have been put in."""
        return len(self._values)


def fill_dog_box(box, dogs):
    """
    Fill a box with dogs.

    TODO: Add type hints.
    box should be WriteOnlyBox[Dog] - but because WriteOnlyBox is
    contravariant, WriteOnlyBox[Animal] should also be accepted!

    (A box that accepts any Animal can certainly accept Dogs)
    """
    for dog in dogs:
        box.put(dog)


class Handler(ABC):
    """
    Abstract handler that processes items of a specific type.

    Handlers are contravariant - a handler for Animal can handle Dogs.

    TODO:
    1. Make this contravariant
    2. Add type hints
    """

    @abstractmethod
    def handle(self, item):
        """Handle an item."""
        pass


class AnimalHandler(Handler):
    """Handles any animal by making it speak."""

    def handle(self, item):
        return item.speak()


class Sink:
    """
    A sink that consumes values (write-only).

    Common examples: loggers, event handlers, output streams.

    TODO: Make contravariant with proper type hints.
    """

    def __init__(self, name):
        self.name = name
        self._received = []

    def send(self, value):
        """Send a value to this sink."""
        self._received.append(value)

    def get_received(self):
        """Get all received values (for testing)."""
        return list(self._received)


# =============================================================================
# PART 4: Callable Variance
# =============================================================================

# Callable is the classic example of mixed variance:
# - Contravariant in argument types (inputs)
# - Covariant in return type (output)
#
# Callable[[Animal], Dog] is a subtype of Callable[[Dog], Animal]
# Because:
# - It accepts MORE types (any Animal, not just Dogs) - contravariant
# - It returns MORE specific type (Dog, not just Animal) - covariant


def apply_to_dog(func, dog):
    """
    Apply a function to a dog.

    TODO: Add type hints.
    func: Callable[[Dog], str]

    But because Callable is contravariant in args, a function that
    accepts ANY Animal should also work here.
    """
    return func(dog)


def make_dog_speaker():
    """
    Return a function that makes dogs speak.

    TODO: Add return type hint -> Callable[[Dog], str]
    """
    def speaker(dog):
        return dog.speak()
    return speaker


def make_animal_speaker():
    """
    Return a function that makes any animal speak.

    TODO: Add return type hint -> Callable[[Animal], str]

    This can be used wherever Callable[[Dog], str] is expected,
    because it accepts a MORE general type (any Animal).
    """
    def speaker(animal):
        return animal.speak()
    return speaker


# Function that demonstrates callable variance
def register_dog_callback(callback):
    """
    Register a callback that will be called with a Dog.

    TODO: Add type hints.
    callback: Callable[[Dog], None]

    A callback that handles ANY Animal should be acceptable here.
    """
    # Simulate calling the callback
    dog = Dog("Buddy")
    callback(dog)


# =============================================================================
# PART 5: Real-World Variance Patterns
# =============================================================================


class EventSource:
    """
    A source of events (producer pattern).

    Covariant - if it produces Dogs, it can be used where Animal producer needed.

    TODO: Make covariant with type hints.
    """

    def __init__(self):
        self._listeners = []

    def subscribe(self, listener):
        """Subscribe a listener to events."""
        self._listeners.append(listener)

    def emit(self, event):
        """Emit an event to all listeners."""
        for listener in self._listeners:
            listener(event)


class EventListener:
    """
    A listener for events (consumer pattern).

    Contravariant - if it handles Animals, it can handle Dogs.

    TODO: Make contravariant with type hints.
    """

    def __init__(self, name):
        self.name = name
        self._events = []

    def __call__(self, event):
        """Handle an event."""
        self._events.append(event)

    def get_events(self):
        """Get all received events."""
        return list(self._events)


class Comparator:
    """
    A comparator that compares two items.

    Comparators are contravariant - a comparator for Animals
    can compare Dogs (since Dogs are Animals).

    TODO: Make contravariant with type hints.
    """

    @abstractmethod
    def compare(self, a, b):
        """
        Compare two items.
        Return negative if a < b, 0 if equal, positive if a > b.
        """
        pass


class AnimalByNameComparator(Comparator):
    """Compares animals by their name."""

    def compare(self, a, b):
        if a.name < b.name:
            return -1
        elif a.name > b.name:
            return 1
        return 0


def sort_dogs(dogs, comparator):
    """
    Sort a list of dogs using a comparator.

    TODO: Add type hints.
    comparator should be Comparator[Dog], but Comparator[Animal]
    should also work due to contravariance.
    """
    # Simple bubble sort for demonstration
    result = list(dogs)
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if comparator.compare(result[j], result[j + 1]) > 0:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


# =============================================================================
# PART 6: Challenge - Building a Type-Safe Pipeline
# =============================================================================


class Source:
    """
    A data source that produces values.

    Should be COVARIANT - Source[Dog] can be used as Source[Animal].

    TODO:
    1. Add covariant TypeVar and make Generic
    2. Add type hints to all methods
    """

    def __init__(self, items):
        self._items = list(items)
        self._index = 0

    def has_next(self):
        """Check if there are more items."""
        return self._index < len(self._items)

    def next(self):
        """Get the next item."""
        if not self.has_next():
            return None
        item = self._items[self._index]
        self._index += 1
        return item

    def reset(self):
        """Reset to the beginning."""
        self._index = 0


class Destination:
    """
    A data destination that consumes values.

    Should be CONTRAVARIANT - Destination[Animal] can be used as Destination[Dog].

    TODO:
    1. Add contravariant TypeVar and make Generic
    2. Add type hints to all methods
    """

    def __init__(self, name):
        self.name = name
        self._items = []

    def write(self, item):
        """Write an item to the destination."""
        self._items.append(item)

    def get_all(self):
        """Get all written items."""
        return list(self._items)


class Transformer:
    """
    A transformer that converts values from one type to another.

    Should be CONTRAVARIANT in input type (T_in) and COVARIANT in output type (T_out).

    This is like Callable - it consumes T_in and produces T_out.

    TODO:
    1. Define T_in (contravariant) and T_out (covariant) TypeVars
    2. Make Generic[T_in, T_out]
    3. Add type hints
    """

    def __init__(self, func):
        self._func = func

    def transform(self, value):
        """Transform a value."""
        return self._func(value)


def build_pipeline(source, transformer, destination):
    """
    Build a pipeline: source -> transformer -> destination.

    TODO: Add type hints that respect variance.

    The types should flow correctly:
    - Source produces values
    - Transformer consumes and produces
    - Destination consumes values
    """
    while source.has_next():
        item = source.next()
        if item is not None:
            transformed = transformer.transform(item)
            destination.write(transformed)


# Example transformers for testing

def make_animal_to_string_transformer():
    """
    Create a transformer that converts Animals to strings (their speech).

    TODO: Add return type hint.
    """
    return Transformer(lambda a: a.speak())


def make_dog_to_string_transformer():
    """
    Create a transformer that converts Dogs to strings (includes fetch).

    TODO: Add return type hint.
    """
    return Transformer(lambda d: f"{d.speak()} and {d.fetch()}")
