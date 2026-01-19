"""
Exercise 7: ClassVar, Final, and Self
======================================

This exercise covers type hints for class-level patterns:

1. ClassVar: Distinguish class variables from instance variables
   - Class variables are shared across all instances
   - Instance variables are unique to each instance
   - ClassVar[T] tells the type checker "this belongs to the class, not instances"

2. Final: Mark values that shouldn't be reassigned
   - Final constants that shouldn't change
   - Final attributes set once in __init__
   - Helps catch accidental reassignment bugs

3. @final: Prevent subclassing or overriding
   - @final on a class: cannot be subclassed
   - @final on a method: cannot be overridden
   - Useful for security, correctness, and optimization

4. Self: Type hint for "the current class"
   - Enables proper typing for fluent interfaces (method chaining)
   - Factory methods that return the same type
   - Works correctly with inheritance

Run tests with: pytest tests/test_ex07.py -v
Run type checker with: mypy exercises/ex07_classvar_final_self.py
"""

from typing import ClassVar, Final, final, Self


# =============================================================================
# PART 1: ClassVar - Class vs Instance Variables
# =============================================================================

# ClassVar marks variables that belong to the class, not instances.
# Without ClassVar, mypy assumes variables are instance attributes.


class Counter:
    """
    A counter that tracks both individual count and total across all instances.

    Example:
        c1 = Counter()
        c2 = Counter()
        c1.increment()
        c1.increment()
        c2.increment()
        c1.count -> 2  (instance-specific)
        c2.count -> 1  (instance-specific)
        Counter.total_increments -> 3  (shared across all)

    TODO:
    1. Add ClassVar[int] type hint to total_increments
    2. Add int type hint to count
    """

    total_increments = 0  # TODO: Add ClassVar type hint

    def __init__(self):
        self.count = 0  # TODO: Add type hint

    def increment(self):
        self.count += 1
        Counter.total_increments += 1

    @classmethod
    def get_total(cls) -> int:
        return cls.total_increments

    @classmethod
    def reset_total(cls) -> None:
        cls.total_increments = 0


class Config:
    """
    Application configuration with defaults and instance overrides.

    Class variables hold defaults, instance variables hold overrides.

    Example:
        Config.default_timeout -> 30  (class default)
        Config.max_retries -> 3  (class default)

        c = Config(timeout=60)
        c.timeout -> 60  (instance override)
        c.retries -> 3  (uses class default via property)

    TODO:
    1. Add ClassVar type hints to class variables
    2. Add instance variable type hints
    """

    default_timeout = 30  # TODO: ClassVar[int]
    max_retries = 3  # TODO: ClassVar[int]
    valid_modes = ["debug", "production", "test"]  # TODO: ClassVar[list[str]]

    def __init__(self, timeout=None, retries=None, mode="production"):
        self.timeout = timeout  # TODO: Add type hint (int | None)
        self.retries = retries  # TODO: Add type hint (int | None)
        self.mode = mode  # TODO: Add type hint (str)

    def get_timeout(self):
        """Return instance timeout or class default."""
        # TODO: Add return type hint
        if self.timeout is not None:
            return self.timeout
        return Config.default_timeout

    def get_retries(self):
        """Return instance retries or class default."""
        # TODO: Add return type hint
        if self.retries is not None:
            return self.retries
        return Config.max_retries


# =============================================================================
# PART 2: Final - Immutable Values
# =============================================================================

# Final marks values that shouldn't be reassigned.
# This catches bugs where constants are accidentally modified.

# TODO: Add Final type hints to these module-level constants
MAX_CONNECTIONS = 100
DEFAULT_HOST = "localhost"
SUPPORTED_PROTOCOLS = ("http", "https", "ws", "wss")


class DatabasePool:
    """
    A database connection pool with immutable configuration.

    Some values are set once and should never change.

    Example:
        pool = DatabasePool("postgres://localhost/db", max_size=10)
        pool.connection_string  # Can read
        pool.connection_string = "..."  # Should be type error!

    TODO:
    1. Add Final type hints where values shouldn't change after __init__
    2. Consider which attributes are truly immutable
    """

    def __init__(self, connection_string, max_size=10):
        # These should be Final - set once, never changed
        self.connection_string = connection_string  # TODO: Final[str]
        self.max_size = max_size  # TODO: Final[int]

        # These can change during runtime
        self.current_size = 0  # Not Final - changes as connections are added
        self._connections = []  # Not Final - modified by acquire/release

    def acquire(self):
        """Acquire a connection from the pool."""
        # TODO: Add return type (str | None)
        if self.current_size < self.max_size:
            self.current_size += 1
            conn = f"conn_{self.current_size}"
            self._connections.append(conn)
            return conn
        return None

    def release(self, conn):
        """Release a connection back to the pool."""
        # TODO: Add type hints
        if conn in self._connections:
            self._connections.remove(conn)
            self.current_size -= 1


class AppSettings:
    """
    Application settings that are fixed after initialization.

    TODO: Use Final for all attributes that shouldn't change.
    """

    def __init__(self, app_name, version, debug=False):
        self.app_name = app_name  # TODO: Final[str]
        self.version = version  # TODO: Final[str]
        self.debug = debug  # TODO: Final[bool]

    def get_info(self):
        """Return app info string."""
        # TODO: Add return type
        mode = "debug" if self.debug else "production"
        return f"{self.app_name} v{self.version} ({mode})"


# =============================================================================
# PART 3: @final - Prevent Subclassing and Overriding
# =============================================================================

# @final on a class prevents it from being subclassed.
# @final on a method prevents it from being overridden.


# TODO: Add @final decorator to prevent subclassing
class SecurityToken:
    """
    A security token that should not be subclassed.

    Subclassing could bypass security checks, so we prevent it.

    TODO: Add @final decorator to this class.
    """

    def __init__(self, user_id, permissions):
        self.user_id = user_id  # TODO: Add type hints
        self.permissions = permissions  # TODO: Add type hints

    def has_permission(self, permission):
        """Check if token has a specific permission."""
        # TODO: Add type hints
        return permission in self.permissions

    def validate(self):
        """Validate the token."""
        # TODO: Add return type
        return self.user_id is not None and len(self.permissions) > 0


class BaseHandler:
    """
    Base class for request handlers.

    Some methods can be overridden, others cannot.

    TODO: Add @final to methods that shouldn't be overridden.
    """

    def __init__(self, name):
        self.name = name  # TODO: Add type hint

    # This method should NOT be overridable - it contains security logic
    def validate_request(self, request):
        """
        Validate a request. Subclasses cannot override this.

        TODO: Add @final decorator and type hints.
        """
        if not isinstance(request, dict):
            return False
        if "auth" not in request:
            return False
        return True

    # This method CAN be overridden by subclasses
    def handle(self, request):
        """
        Handle a request. Subclasses should override this.

        TODO: Add type hints (no @final here).
        """
        return {"handler": self.name, "status": "ok"}

    # This method should NOT be overridable - logging format is fixed
    def log_request(self, request):
        """
        Log a request. Format is fixed, cannot be overridden.

        TODO: Add @final decorator and type hints.
        """
        return f"[{self.name}] Request received"


class JsonHandler(BaseHandler):
    """A handler that processes JSON requests."""

    def handle(self, request):
        # This is allowed - handle() is not final
        if self.validate_request(request):
            return {"handler": self.name, "type": "json", "data": request}
        return {"error": "invalid request"}


# =============================================================================
# PART 4: Self - Methods Returning the Same Type
# =============================================================================

# Self represents "the type of the current class".
# Essential for fluent interfaces and factory methods.


class StringBuilder:
    """
    A fluent string builder with method chaining.

    Example:
        result = (StringBuilder()
            .append("Hello")
            .append(" ")
            .append("World")
            .to_upper()
            .build())
        # result -> "HELLO WORLD"

    TODO: Use Self as return type for chainable methods.
    """

    def __init__(self):
        self._parts = []  # TODO: Add type hint (list[str])

    def append(self, text):
        """
        Append text to the builder.

        TODO: Add type hints. Return type should be Self.
        """
        self._parts.append(text)
        return self

    def append_line(self, text):
        """
        Append text followed by a newline.

        TODO: Return type should be Self.
        """
        self._parts.append(text)
        self._parts.append("\n")
        return self

    def to_upper(self):
        """
        Convert all accumulated text to uppercase.

        TODO: Return type should be Self.
        """
        self._parts = [p.upper() for p in self._parts]
        return self

    def to_lower(self):
        """
        Convert all accumulated text to lowercase.

        TODO: Return type should be Self.
        """
        self._parts = [p.lower() for p in self._parts]
        return self

    def clear(self):
        """
        Clear all accumulated text.

        TODO: Return type should be Self.
        """
        self._parts = []
        return self

    def build(self):
        """Build the final string."""
        # TODO: Add return type (str)
        return "".join(self._parts)


class QueryBuilder:
    """
    A SQL query builder with method chaining.

    Example:
        query = (QueryBuilder("users")
            .select("name", "email")
            .where("active = true")
            .order_by("name")
            .limit(10)
            .build())

    TODO: Use Self for all chainable methods.
    """

    def __init__(self, table):
        self._table = table  # TODO: Add type hint
        self._columns = ["*"]  # TODO: Add type hint
        self._where_clauses = []  # TODO: Add type hint
        self._order_by_col = None  # TODO: Add type hint
        self._limit_val = None  # TODO: Add type hint

    def select(self, *columns):
        """Select specific columns."""
        # TODO: Add type hints, return Self
        self._columns = list(columns)
        return self

    def where(self, clause):
        """Add a WHERE clause."""
        # TODO: Add type hints, return Self
        self._where_clauses.append(clause)
        return self

    def order_by(self, column):
        """Add ORDER BY clause."""
        # TODO: Add type hints, return Self
        self._order_by_col = column
        return self

    def limit(self, n):
        """Add LIMIT clause."""
        # TODO: Add type hints, return Self
        self._limit_val = n
        return self

    def build(self):
        """Build the SQL query string."""
        # TODO: Add return type (str)
        parts = [f"SELECT {', '.join(self._columns)} FROM {self._table}"]
        if self._where_clauses:
            parts.append(f"WHERE {' AND '.join(self._where_clauses)}")
        if self._order_by_col:
            parts.append(f"ORDER BY {self._order_by_col}")
        if self._limit_val is not None:
            parts.append(f"LIMIT {self._limit_val}")
        return " ".join(parts)


# =============================================================================
# PART 5: Self with Inheritance
# =============================================================================

# Self shines when you have class hierarchies.
# Without Self, factory methods return the base type, not the subclass.


class Shape:
    """
    Base class for shapes with a factory method.

    TODO: Use Self so subclasses return their own type.
    """

    def __init__(self, x, y):
        self.x = x  # TODO: Add type hints
        self.y = y

    @classmethod
    def at_origin(cls):
        """
        Create a shape at the origin (0, 0).

        TODO: Return type should be Self, not Shape.
        This way Circle.at_origin() returns Circle, not Shape.
        """
        return cls(0, 0)

    def move(self, dx, dy):
        """
        Move the shape and return self for chaining.

        TODO: Return type should be Self.
        """
        self.x += dx
        self.y += dy
        return self

    def copy(self):
        """
        Create a copy of this shape.

        TODO: Return type should be Self.
        """
        return self.__class__(self.x, self.y)


class Circle(Shape):
    """A circle shape."""

    def __init__(self, x, y, radius=1.0):
        super().__init__(x, y)
        self.radius = radius  # TODO: Add type hint

    def scale(self, factor):
        """
        Scale the circle's radius.

        TODO: Return type should be Self.
        """
        self.radius *= factor
        return self

    def copy(self):
        """Create a copy of this circle."""
        # TODO: Return type should be Self
        return self.__class__(self.x, self.y, self.radius)


class Rectangle(Shape):
    """A rectangle shape."""

    def __init__(self, x, y, width=1.0, height=1.0):
        super().__init__(x, y)
        self.width = width  # TODO: Add type hints
        self.height = height

    def scale(self, factor):
        """
        Scale the rectangle's dimensions.

        TODO: Return type should be Self.
        """
        self.width *= factor
        self.height *= factor
        return self

    def copy(self):
        """Create a copy of this rectangle."""
        # TODO: Return type should be Self
        return self.__class__(self.x, self.y, self.width, self.height)


# =============================================================================
# PART 6: Challenge - Combining ClassVar, Final, and Self
# =============================================================================


class IDGenerator:
    """
    A generator that creates unique IDs.

    - Uses ClassVar for the shared counter
    - Uses Final for the prefix (immutable after creation)
    - Uses Self for fluent configuration

    Example:
        gen = IDGenerator("USER").with_separator("-")
        gen.next_id() -> "USER-1"
        gen.next_id() -> "USER-2"

        gen2 = IDGenerator("ORDER").with_separator("_").with_padding(5)
        gen2.next_id() -> "ORDER_00001"
        gen2.next_id() -> "ORDER_00002"

    TODO:
    1. Add ClassVar for _counter
    2. Add Final for prefix
    3. Add Self for fluent methods
    """

    _counter = 0  # TODO: ClassVar[int] - shared across all instances

    def __init__(self, prefix):
        self.prefix = prefix  # TODO: Final[str]
        self._separator = "-"  # TODO: Add type hint
        self._padding = 0  # TODO: Add type hint

    def with_separator(self, sep):
        """Set the separator between prefix and number."""
        # TODO: Return Self
        self._separator = sep
        return self

    def with_padding(self, width):
        """Set zero-padding width for the number."""
        # TODO: Return Self
        self._padding = width
        return self

    def next_id(self):
        """Generate the next unique ID."""
        # TODO: Add return type (str)
        IDGenerator._counter += 1
        if self._padding > 0:
            num_str = str(IDGenerator._counter).zfill(self._padding)
        else:
            num_str = str(IDGenerator._counter)
        return f"{self.prefix}{self._separator}{num_str}"

    @classmethod
    def reset(cls):
        """Reset the counter (mainly for testing)."""
        # TODO: Add return type (None)
        cls._counter = 0
