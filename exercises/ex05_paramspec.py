"""
Exercise 5: ParamSpec and Concatenate
=====================================

In Exercise 4, you typed decorators using Callable[..., T]. This preserves
the return type but loses all parameter type information. ParamSpec solves this.

Key concepts:
- ParamSpec: Captures the complete parameter specification of a callable
- Concatenate: Adds parameters to the front of a ParamSpec
- Proper decorator typing that preserves full signatures

Why ParamSpec matters:
    @decorator
    def greet(name: str, excited: bool = False) -> str: ...

    # With Callable[..., T]: greet's parameters become (*args, **kwargs) - lost!
    # With ParamSpec: greet(name: str, excited: bool = False) -> str - preserved!

Run tests with: pytest tests/test_ex05.py -v
Run type checker with: mypy exercises/ex05_paramspec.py
"""

from typing import Callable, TypeVar, ParamSpec, Concatenate
from functools import wraps
import time

# =============================================================================
# PART 1: Basic ParamSpec Usage
# =============================================================================

# ParamSpec captures ALL parameters of a function as a unit.
# Use P.args and P.kwargs to forward them.

P = ParamSpec('P')
T = TypeVar('T')


def log_call(func):
    """
    A decorator that logs when a function is called.

    This should preserve the FULL signature of the decorated function.

    Example:
        @log_call
        def greet(name: str) -> str:
            return f"Hello, {name}"

        greet("Alice")  # Logs: "Calling greet"
                        # Returns: "Hello, Alice"

        # Type checker should know: greet(name: str) -> str
        # NOT: greet(*args, **kwargs) -> str

    TODO: Add type hints using ParamSpec.
    - func: Callable[P, T]
    - return: Callable[P, T]
    - Use @wraps(func) to preserve function metadata
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def time_it(func):
    """
    A decorator that measures execution time.

    Returns a tuple of (result, elapsed_seconds).

    Example:
        @time_it
        def slow_add(a: int, b: int) -> int:
            time.sleep(0.1)
            return a + b

        result, elapsed = slow_add(1, 2)
        # result = 3, elapsed ≈ 0.1

    Note: This changes the return type! The decorated function returns
    tuple[T, float] instead of just T.

    TODO: Add type hints.
    - func: Callable[P, T]
    - return: Callable[P, tuple[T, float]]
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        return (result, elapsed)
    return wrapper


# =============================================================================
# PART 2: Decorators with Arguments
# =============================================================================


def retry(max_attempts):
    """
    A decorator that retries a function up to max_attempts times.

    This is the same as Exercise 4, but now with proper ParamSpec typing!

    Example:
        @retry(3)
        def fetch_data(url: str, timeout: int = 30) -> dict:
            ...

        # Type checker should know:
        # fetch_data(url: str, timeout: int = 30) -> dict

    TODO: Add complete type hints using ParamSpec.
    The decorated function should preserve its exact signature.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
            if last_exception is not None:
                raise last_exception
            raise RuntimeError("No attempts made")
        return wrapper
    return decorator


def cache_result(func):
    """
    A simple memoization decorator.

    Caches results based on arguments (assumes hashable args).

    Example:
        @cache_result
        def expensive(n: int) -> int:
            print(f"Computing {n}")
            return n * 2

        expensive(5)  # Prints "Computing 5", returns 10
        expensive(5)  # No print, returns 10 (cached)

    TODO: Add type hints using ParamSpec.
    """
    cache: dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper


# =============================================================================
# PART 3: Concatenate - Adding Parameters
# =============================================================================

# Concatenate[X, Y, P] creates a new parameter spec with X, Y prepended to P.
# This is useful for decorators that add parameters to functions.


def with_user(func):
    """
    A decorator that adds a 'user' parameter to the front of a function.

    Example:
        @with_user
        def save_document(doc: str) -> bool:
            # How do we access the user? See below.
            ...

        # After decoration: save_document(user: str, doc: str) -> bool
        save_document("alice", "my document")

    Wait - this pattern doesn't quite work because the inner function
    can't access 'user'. Let's do it properly:

        def save_document(user: str, doc: str) -> bool:
            ...

        # We want to wrap it to validate the user first:
        @validate_user
        def save_document(user: str, doc: str) -> bool:
            ...

    TODO: Add type hints using Concatenate.
    - The original func takes (str, P...) -> T (user is first param)
    - We return a function with the same signature
    - Concatenate[str, P] means "str followed by whatever P captures"
    """
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user or not isinstance(user, str):
            raise ValueError("Invalid user")
        print(f"User '{user}' is calling {func.__name__}")
        return func(user, *args, **kwargs)
    return wrapper


def with_connection(func):
    """
    A decorator that injects a database connection as the first argument.

    Example:
        @with_connection
        def query_users(conn: Connection, filter: str) -> list[str]:
            return conn.execute(f"SELECT * FROM users WHERE {filter}")

        # After decoration: query_users(filter: str) -> list[str]
        # The connection is provided automatically!
        query_users("active = true")

    This is the opposite of with_user - we're REMOVING a parameter from
    the public signature by providing it automatically.

    TODO: Add type hints using Concatenate.
    - Original func: Callable[Concatenate[Connection, P], T]
    - Returned func: Callable[P, T]

    The Connection parameter is "consumed" by the decorator.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # In real code, you'd get this from a connection pool
        conn = Connection("fake://database")
        return func(conn, *args, **kwargs)
    return wrapper


class Connection:
    """A fake database connection for demonstration."""

    def __init__(self, url: str):
        self.url = url

    def execute(self, query: str) -> list[str]:
        return [f"Result for: {query}"]


# =============================================================================
# PART 4: Real-World Decorator Patterns
# =============================================================================


def validate_args(validator):
    """
    A decorator factory that validates all arguments before calling the function.

    Example:
        def is_positive(x):
            return x > 0

        @validate_args(is_positive)
        def process(a: int, b: int) -> int:
            return a + b

        process(1, 2)   # OK, returns 3
        process(-1, 2)  # Raises ValueError

    TODO: Add type hints.
    - validator is a Callable that takes any value and returns bool
    - The decorated function preserves its signature
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if not validator(arg):
                    raise ValueError(f"Validation failed for {arg}")
            for key, value in kwargs.items():
                if not validator(value):
                    raise ValueError(f"Validation failed for {key}={value}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


def transform_result(transformer):
    """
    A decorator that transforms the result of a function.

    Example:
        @transform_result(str.upper)
        def greet(name: str) -> str:
            return f"hello, {name}"

        greet("world")  # Returns "HELLO, WORLD"

    TODO: Add type hints.
    - transformer: Callable[[T], U]
    - func: Callable[P, T]
    - result: Callable[P, U]

    This decorator changes the return type!
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return transformer(result)
        return wrapper
    return decorator


# =============================================================================
# PART 5: Challenge - Method Decorators
# =============================================================================

# When decorating methods, remember that 'self' is the first argument.
# Concatenate can handle this elegantly.


def log_method(func):
    """
    A decorator for instance methods that logs calls with the instance info.

    Example:
        class Calculator:
            def __init__(self, name: str):
                self.name = name

            @log_method
            def add(self, a: int, b: int) -> int:
                return a + b

        calc = Calculator("BasicCalc")
        calc.add(1, 2)  # Logs: "BasicCalc.add called"

    TODO: Add type hints using Concatenate.
    - The first parameter after self is captured by ParamSpec
    - Use a TypeVar for 'self' to preserve the class type

    Hint: You'll need something like:
        Callable[Concatenate[S, P], T]
    where S is a TypeVar for self.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        name = getattr(self, 'name', self.__class__.__name__)
        print(f"{name}.{func.__name__} called")
        return func(self, *args, **kwargs)
    return wrapper


def require_auth(role):
    """
    A decorator for methods that checks user authorization.

    Example:
        class AdminPanel:
            def __init__(self, current_user: str, user_roles: dict[str, str]):
                self.current_user = current_user
                self.user_roles = user_roles

            @require_auth("admin")
            def delete_user(self, user_id: int) -> bool:
                return True  # deletion logic

        panel = AdminPanel("alice", {"alice": "admin", "bob": "user"})
        panel.delete_user(123)  # Works for alice

        panel2 = AdminPanel("bob", {"alice": "admin", "bob": "user"})
        panel2.delete_user(123)  # Raises PermissionError

    TODO: Add type hints.
    This is a decorator factory for methods.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            user = getattr(self, 'current_user', None)
            roles = getattr(self, 'user_roles', {})
            if roles.get(user) != role:
                raise PermissionError(f"User {user} does not have {role} role")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
