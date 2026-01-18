"""
Exercise 6: TypedDict and Type Guards
=====================================

This exercise covers two related concepts for working with structured data:

1. TypedDict: Type hints for dictionaries with specific string keys
   - Unlike dict[str, X], TypedDict specifies WHICH keys exist and their types
   - Perfect for JSON data, API responses, configuration objects

2. Type Guards: Custom functions that narrow types
   - TypeGuard: Narrows to a specific type if function returns True
   - TypeIs: Like TypeGuard but preserves type relationships (Python 3.13+)
   - Essential for safely handling union types and optional data

Why these matter:
    # Without TypedDict - no type safety for keys
    def get_user_email(user: dict) -> str:
        return user["email"]  # What if "email" doesn't exist?

    # With TypedDict - full key and value type checking
    def get_user_email(user: UserDict) -> str:
        return user["email"]  # Type checker knows this is str

Run tests with: pytest tests/test_ex06.py -v
Run type checker with: mypy exercises/ex06_typeddict_and_guards.py
"""

from typing import TypedDict, NotRequired, Required, TypeGuard, Any


# =============================================================================
# PART 1: Basic TypedDict
# =============================================================================

# TypedDict creates a dict type with specific keys and value types.
# All keys are required by default.

# TODO: Define a TypedDict called 'Point2D' with:
#       - x: int
#       - y: int
#
# Example:
#   class Point2D(TypedDict):
#       x: int
#       y: int


def distance_from_origin(point):
    """
    Calculate the distance from origin to a 2D point.

    Examples:
        distance_from_origin({"x": 3, "y": 4}) -> 5.0
        distance_from_origin({"x": 0, "y": 0}) -> 0.0

    TODO: Add type hint using Point2D TypedDict.
    """
    return (point["x"] ** 2 + point["y"] ** 2) ** 0.5


def translate_point(point, dx, dy):
    """
    Move a point by the given deltas.

    Returns a NEW Point2D (don't modify the original).

    Examples:
        translate_point({"x": 1, "y": 2}, 10, 20) -> {"x": 11, "y": 22}

    TODO: Add type hints. Returns a Point2D.
    """
    return {"x": point["x"] + dx, "y": point["y"] + dy}


# =============================================================================
# PART 2: TypedDict with Optional Keys
# =============================================================================

# Use NotRequired for keys that may or may not be present.
# Use Required to mark keys as required in a total=False TypedDict.

# TODO: Define a TypedDict called 'UserProfile' with:
#       - id: int (required)
#       - name: str (required)
#       - email: NotRequired[str] (optional)
#       - age: NotRequired[int] (optional)
#
# Hint:
#   class UserProfile(TypedDict):
#       id: int
#       name: str
#       email: NotRequired[str]
#       age: NotRequired[int]


def get_display_name(user):
    """
    Get the display name for a user.

    Examples:
        get_display_name({"id": 1, "name": "Alice"}) -> "Alice"
        get_display_name({"id": 2, "name": "Bob", "email": "bob@example.com"}) -> "Bob"

    TODO: Add type hint using UserProfile.
    """
    return user["name"]


def get_user_email_or_default(user, default):
    """
    Get the user's email, or a default if not present.

    Examples:
        get_user_email_or_default({"id": 1, "name": "A"}, "n/a") -> "n/a"
        get_user_email_or_default({"id": 1, "name": "A", "email": "a@b.com"}, "n/a") -> "a@b.com"

    TODO: Add type hints.
    """
    return user.get("email", default)


def create_user(user_id, name, email=None, age=None):
    """
    Create a new UserProfile dictionary.

    Examples:
        create_user(1, "Alice") -> {"id": 1, "name": "Alice"}
        create_user(2, "Bob", email="bob@x.com") -> {"id": 2, "name": "Bob", "email": "bob@x.com"}

    TODO: Add type hints. The return type should be UserProfile.
    Note: Only include optional keys if they're provided.
    """
    result = {"id": user_id, "name": name}
    if email is not None:
        result["email"] = email
    if age is not None:
        result["age"] = age
    return result


# =============================================================================
# PART 3: Nested TypedDicts
# =============================================================================

# TypedDicts can contain other TypedDicts for complex structures.

# TODO: Define these TypedDicts for an API response:
#
# class Address(TypedDict):
#     street: str
#     city: str
#     country: str
#
# class Company(TypedDict):
#     name: str
#     address: Address
#
# class Employee(TypedDict):
#     id: int
#     name: str
#     company: Company
#     remote: NotRequired[bool]


def get_employee_city(employee):
    """
    Get the city where an employee's company is located.

    Example:
        emp = {
            "id": 1,
            "name": "Alice",
            "company": {
                "name": "Acme",
                "address": {"street": "123 Main", "city": "Boston", "country": "USA"}
            }
        }
        get_employee_city(emp) -> "Boston"

    TODO: Add type hint using Employee.
    """
    return employee["company"]["address"]["city"]


def is_remote_employee(employee):
    """
    Check if an employee works remotely.

    Returns False if the 'remote' key is not present.

    TODO: Add type hints.
    """
    return employee.get("remote", False)


def create_employee(emp_id, name, company_name, street, city, country, remote=None):
    """
    Create a new Employee dictionary with nested structure.

    TODO: Add type hints. Return type should be Employee.
    """
    result = {
        "id": emp_id,
        "name": name,
        "company": {
            "name": company_name,
            "address": {
                "street": street,
                "city": city,
                "country": country,
            },
        },
    }
    if remote is not None:
        result["remote"] = remote
    return result


# =============================================================================
# PART 4: Type Guards
# =============================================================================

# Type guards are functions that help the type checker narrow types.
# They return bool but have a special return type annotation.

# Pattern:
#   def is_string(value: object) -> TypeGuard[str]:
#       return isinstance(value, str)
#
# After: if is_string(x):  # type checker now knows x is str


def is_point2d(value):
    """
    Check if a value is a valid Point2D dictionary.

    A valid Point2D has 'x' and 'y' keys that are both integers.

    Examples:
        is_point2d({"x": 1, "y": 2}) -> True
        is_point2d({"x": 1}) -> False
        is_point2d({"x": "1", "y": 2}) -> False
        is_point2d([1, 2]) -> False

    TODO:
    1. Add return type TypeGuard[Point2D]
    2. Add parameter type hint (use object or Any)
    3. Implement the validation logic
    """
    pass  # TODO: Implement


def is_user_profile(value):
    """
    Check if a value is a valid UserProfile dictionary.

    Must have 'id' (int) and 'name' (str).
    May optionally have 'email' (str) and 'age' (int).

    Examples:
        is_user_profile({"id": 1, "name": "Alice"}) -> True
        is_user_profile({"id": 1, "name": "Alice", "email": "a@b.com"}) -> True
        is_user_profile({"id": "1", "name": "Alice"}) -> False (id must be int)
        is_user_profile({"name": "Alice"}) -> False (missing id)

    TODO: Add TypeGuard return type and implement validation.
    """
    pass  # TODO: Implement


# =============================================================================
# PART 5: Using Type Guards for Safe Processing
# =============================================================================


def process_points(data):
    """
    Process a list of potential Point2D dicts, returning only valid ones.

    This function should use is_point2d to filter and type-narrow.

    Examples:
        process_points([{"x": 1, "y": 2}, {"x": 3}, {"x": 4, "y": 5}])
        -> [{"x": 1, "y": 2}, {"x": 4, "y": 5}]

    TODO:
    1. Add type hints: takes list[Any], returns list[Point2D]
    2. Use is_point2d to filter valid points
    """
    pass  # TODO: Implement


def safe_get_distance(data):
    """
    Safely calculate distance if data is a valid Point2D.

    Returns None if the data is not a valid Point2D.

    Examples:
        safe_get_distance({"x": 3, "y": 4}) -> 5.0
        safe_get_distance({"x": 3}) -> None
        safe_get_distance("not a point") -> None

    TODO:
    1. Add type hints: takes Any, returns float | None
    2. Use is_point2d to guard before calculating
    """
    pass  # TODO: Implement


# =============================================================================
# PART 6: Challenge - Discriminated Unions with TypedDict
# =============================================================================

# A common pattern is using a "type" or "kind" field to distinguish
# between different TypedDict variants.

# TODO: Define these TypedDicts for different message types:
#
# class TextMessage(TypedDict):
#     type: Literal["text"]
#     content: str
#
# class ImageMessage(TypedDict):
#     type: Literal["image"]
#     url: str
#     alt_text: NotRequired[str]
#
# class VideoMessage(TypedDict):
#     type: Literal["video"]
#     url: str
#     duration: int  # seconds
#
# Message = TextMessage | ImageMessage | VideoMessage

from typing import Literal


def is_text_message(msg):
    """
    Check if a message is a TextMessage.

    TODO: Add TypeGuard[TextMessage] return type and implement.
    """
    pass  # TODO: Implement


def is_image_message(msg):
    """
    Check if a message is an ImageMessage.

    TODO: Add TypeGuard[ImageMessage] return type and implement.
    """
    pass  # TODO: Implement


def is_video_message(msg):
    """
    Check if a message is a VideoMessage.

    TODO: Add TypeGuard[VideoMessage] return type and implement.
    """
    pass  # TODO: Implement


def get_message_preview(message):
    """
    Get a preview string for any message type.

    Examples:
        get_message_preview({"type": "text", "content": "Hello!"})
        -> "Text: Hello!"

        get_message_preview({"type": "image", "url": "http://...", "alt_text": "A cat"})
        -> "Image: A cat"

        get_message_preview({"type": "image", "url": "http://..."})
        -> "Image: [no description]"

        get_message_preview({"type": "video", "url": "http://...", "duration": 120})
        -> "Video: 2:00"

    TODO:
    1. Add type hint for message (use the Message union type)
    2. Implement using the type guards or isinstance checks
    3. Format duration as M:SS
    """
    pass  # TODO: Implement


def count_messages_by_type(messages):
    """
    Count how many messages of each type are in a list.

    Returns a dict with counts for each type.

    Example:
        count_messages_by_type([
            {"type": "text", "content": "hi"},
            {"type": "text", "content": "bye"},
            {"type": "image", "url": "..."},
        ])
        -> {"text": 2, "image": 1, "video": 0}

    TODO: Add type hints and implement.
    """
    pass  # TODO: Implement
