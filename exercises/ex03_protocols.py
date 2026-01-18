"""
Exercise 3: Protocols (Structural Subtyping)
============================================

Protocols define a set of methods/attributes that a type must have,
WITHOUT requiring inheritance. This is "structural subtyping" or "duck typing
with type safety".

Unlike ABC (Abstract Base Classes), a class doesn't need to explicitly inherit
from a Protocol - it just needs to have the right methods.

Key concepts:
- Protocol: Base class for defining structural types
- @runtime_checkable: Makes isinstance() work with Protocols
- Combining Protocols with generics

Run tests with: pytest tests/test_ex03.py -v
Run type checker with: mypy exercises/ex03_protocols.py
"""

from typing import TypeVar, Protocol, runtime_checkable

# =============================================================================
# PART 1: Basic Protocols
# =============================================================================

# TODO: Define a Protocol called 'Drawable' with a single method:
#       draw(self) -> str
#
# Example:
#   class Drawable(Protocol):
#       def draw(self) -> str: ...
#
# Note: The ... (ellipsis) is used in Protocol methods - no implementation needed


class Circle:
    """A circle that can be drawn."""

    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"Circle(radius={self.radius})"


class Rectangle:
    """A rectangle that can be drawn."""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def draw(self) -> str:
        return f"Rectangle({self.width}x{self.height})"


class Point:
    """A point - NOT drawable (no draw method)."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


def render(shape):
    """
    Render a shape by calling its draw() method.

    This function should accept ANY object that has a draw() -> str method,
    without requiring inheritance from a common base class.

    Examples:
        render(Circle(5)) -> "Rendering: Circle(radius=5)"
        render(Rectangle(3, 4)) -> "Rendering: Rectangle(3x4)"

    TODO: Add type hint using the Drawable protocol.
    """
    return f"Rendering: {shape.draw()}"


def render_all(shapes):
    """
    Render multiple shapes.

    TODO: Add type hint for a list of Drawable objects.
    """
    return [render(s) for s in shapes]


# =============================================================================
# PART 2: Protocols with Properties
# =============================================================================

# Protocols can also require properties/attributes, not just methods.

# TODO: Define a Protocol called 'Named' that requires:
#       - A property 'name' of type str
#
# Hint: Use @property in the Protocol definition


class User:
    def __init__(self, name: str, email: str):
        self._name = name
        self.email = email

    @property
    def name(self) -> str:
        return self._name


class Product:
    def __init__(self, name: str, price: float):
        self.name = name  # This is a plain attribute, which also satisfies the Protocol!
        self.price = price


class AnonymousThing:
    """This has no name - should NOT satisfy Named protocol."""

    def __init__(self, value: int):
        self.value = value


def greet(obj):
    """
    Greet something by its name.

    TODO: Add type hint using the Named protocol.
    """
    return f"Hello, {obj.name}!"


# =============================================================================
# PART 3: Runtime Checkable Protocols
# =============================================================================

# By default, you can't use isinstance() with Protocols.
# Adding @runtime_checkable allows runtime checks.

# TODO: Define a runtime_checkable Protocol called 'Closeable' that requires:
#       - A method close(self) -> None
#
# Hint:
#   @runtime_checkable
#   class Closeable(Protocol):
#       def close(self) -> None: ...


class FileHandle:
    def __init__(self, path: str):
        self.path = path
        self.is_open = True

    def close(self) -> None:
        self.is_open = False


class Connection:
    def __init__(self, host: str):
        self.host = host
        self.connected = True

    def close(self) -> None:
        self.connected = False


class SimpleValue:
    """This has no close() method."""

    def __init__(self, value: int):
        self.value = value


def maybe_close(obj):
    """
    Close an object if it's Closeable.

    This demonstrates runtime checking of Protocols.

    Returns True if the object was closed, False otherwise.

    TODO:
    1. Define the Closeable protocol above with @runtime_checkable
    2. Add a type hint (the input could be anything)
    3. Use isinstance() to check if obj matches Closeable
    """
    # TODO: Implement the isinstance check and close if applicable
    # if isinstance(obj, Closeable):
    #     obj.close()
    #     return True
    # return False
    pass  # Replace with implementation


# =============================================================================
# PART 4: Generic Protocols
# =============================================================================

# Protocols can be generic, combining structural subtyping with type parameters.

# TODO: Define a generic Protocol called 'Container' with:
#       - A method get(self) -> T
#       - A method set(self, value: T) -> None
#
# Hint:
#   T = TypeVar('T')
#   class Container(Protocol[T]):
#       def get(self) -> T: ...
#       def set(self, value: T) -> None: ...


class IntHolder:
    """Holds an integer value."""

    def __init__(self, value: int):
        self._value = value

    def get(self) -> int:
        return self._value

    def set(self, value: int) -> None:
        self._value = value


class StringHolder:
    """Holds a string value."""

    def __init__(self, value: str):
        self._value = value

    def get(self) -> str:
        return self._value

    def set(self, value: str) -> None:
        self._value = value


def double_container_value(container):
    """
    Double the value in a numeric container.

    TODO: Add type hint accepting Container[int] or Container[float]
    Hint: You might need a union or a constrained TypeVar
    """
    current = container.get()
    container.set(current * 2)


def swap_containers(c1, c2):
    """
    Swap the values between two containers of the same type.

    TODO: Add type hints using the generic Container protocol.
    Both containers should hold the same type.
    """
    temp = c1.get()
    c1.set(c2.get())
    c2.set(temp)


# =============================================================================
# PART 5: Challenge - Combining Protocols
# =============================================================================

# You can create new Protocols that combine multiple Protocols.

# TODO: Define these Protocols:
# 1. Readable: has a method read(self) -> str
# 2. Writable: has a method write(self, data: str) -> None
# 3. ReadWritable: combines both Readable and Writable
#
# Hint for combining:
#   class ReadWritable(Readable, Writable, Protocol):
#       ...


class InMemoryFile:
    """An in-memory file that can be read and written."""

    def __init__(self):
        self._content = ""

    def read(self) -> str:
        return self._content

    def write(self, data: str) -> None:
        self._content = data


class ReadOnlyBuffer:
    """A buffer that can only be read."""

    def __init__(self, content: str):
        self._content = content

    def read(self) -> str:
        return self._content


class WriteOnlyLog:
    """A log that can only be written to."""

    def __init__(self):
        self._entries: list[str] = []

    def write(self, data: str) -> None:
        self._entries.append(data)

    def get_entries(self) -> list[str]:
        return self._entries


def read_content(source):
    """
    Read content from a Readable source.

    TODO: Add type hint using Readable protocol.
    """
    return source.read()


def write_content(dest, data):
    """
    Write content to a Writable destination.

    TODO: Add type hints using Writable protocol.
    """
    dest.write(data)


def copy_content(source, dest):
    """
    Copy content from a Readable source to a Writable destination.

    TODO: Add type hints using the individual protocols.
    """
    data = source.read()
    dest.write(data)


def update_content(target, transformer):
    """
    Read from a ReadWritable, transform the content, and write it back.

    Args:
        target: A ReadWritable object
        transformer: A function that transforms strings

    TODO:
    1. Add type hint for target using ReadWritable protocol
    2. Add type hint for transformer (Callable[[str], str])
    """
    content = target.read()
    new_content = transformer(content)
    target.write(new_content)
