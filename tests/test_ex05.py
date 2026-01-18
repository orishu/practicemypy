"""
Tests for Exercise 5: ParamSpec and Concatenate

Run with: pytest tests/test_ex05.py -v
"""

import pytest
import time
from exercises.ex05_paramspec import (
    log_call,
    time_it,
    retry,
    cache_result,
    with_user,
    with_connection,
    Connection,
    validate_args,
    transform_result,
    log_method,
    require_auth,
)


class TestLogCall:
    def test_preserves_return(self, capsys):
        @log_call
        def greet(name: str) -> str:
            return f"Hello, {name}"

        result = greet("Alice")
        assert result == "Hello, Alice"
        assert "Calling greet" in capsys.readouterr().out

    def test_preserves_args(self, capsys):
        @log_call
        def add(a: int, b: int, c: int = 0) -> int:
            return a + b + c

        assert add(1, 2) == 3
        assert add(1, 2, c=3) == 6


class TestTimeIt:
    def test_returns_tuple(self):
        @time_it
        def quick() -> str:
            return "done"

        result, elapsed = quick()
        assert result == "done"
        assert elapsed >= 0
        assert elapsed < 1  # Should be very fast

    def test_measures_time(self):
        @time_it
        def slow() -> int:
            time.sleep(0.05)
            return 42

        result, elapsed = slow()
        assert result == 42
        assert elapsed >= 0.04  # Allow some tolerance


class TestRetry:
    def test_succeeds_first_try(self):
        @retry(3)
        def always_works(x: int) -> int:
            return x * 2

        assert always_works(5) == 10

    def test_succeeds_after_retry(self):
        attempts = [0]

        @retry(3)
        def fails_twice(x: int) -> int:
            attempts[0] += 1
            if attempts[0] < 3:
                raise ValueError("not yet")
            return x

        assert fails_twice(42) == 42
        assert attempts[0] == 3

    def test_exhausts_retries(self):
        @retry(2)
        def always_fails() -> None:
            raise RuntimeError("always")

        with pytest.raises(RuntimeError, match="always"):
            always_fails()


class TestCacheResult:
    def test_caches_results(self):
        call_count = [0]

        @cache_result
        def expensive(n: int) -> int:
            call_count[0] += 1
            return n * 2

        assert expensive(5) == 10
        assert expensive(5) == 10
        assert expensive(5) == 10
        assert call_count[0] == 1  # Only called once

    def test_different_args(self):
        call_count = [0]

        @cache_result
        def expensive(n: int) -> int:
            call_count[0] += 1
            return n * 2

        assert expensive(1) == 2
        assert expensive(2) == 4
        assert expensive(1) == 2
        assert call_count[0] == 2  # Called for each unique arg


class TestWithUser:
    def test_valid_user(self, capsys):
        @with_user
        def save(user: str, doc: str) -> str:
            return f"{user} saved {doc}"

        result = save("alice", "report.txt")
        assert result == "alice saved report.txt"
        assert "alice" in capsys.readouterr().out

    def test_invalid_user(self):
        @with_user
        def save(user: str, doc: str) -> str:
            return f"{user} saved {doc}"

        with pytest.raises(ValueError, match="Invalid user"):
            save("", "doc.txt")


class TestWithConnection:
    def test_injects_connection(self):
        @with_connection
        def query(conn: Connection, table: str) -> list[str]:
            return conn.execute(f"SELECT * FROM {table}")

        result = query("users")  # Note: no conn argument!
        assert len(result) == 1
        assert "users" in result[0]

    def test_multiple_args(self):
        @with_connection
        def query(conn: Connection, table: str, limit: int = 10) -> str:
            return f"SELECT * FROM {table} LIMIT {limit}"

        assert query("users", limit=5) == "SELECT * FROM users LIMIT 5"


class TestValidateArgs:
    def test_valid_args(self):
        @validate_args(lambda x: x > 0)
        def add(a: int, b: int) -> int:
            return a + b

        assert add(1, 2) == 3

    def test_invalid_args(self):
        @validate_args(lambda x: x > 0)
        def add(a: int, b: int) -> int:
            return a + b

        with pytest.raises(ValueError, match="Validation failed"):
            add(-1, 2)

    def test_invalid_kwargs(self):
        @validate_args(lambda x: isinstance(x, int))
        def process(a: int, b: int = 0) -> int:
            return a + b

        with pytest.raises(ValueError, match="Validation failed"):
            process(1, b="not an int")


class TestTransformResult:
    def test_transforms(self):
        @transform_result(str.upper)
        def greet(name: str) -> str:
            return f"hello, {name}"

        assert greet("world") == "HELLO, WORLD"

    def test_type_change(self):
        @transform_result(len)
        def greet(name: str) -> str:
            return f"hello, {name}"

        result = greet("world")
        assert result == 12  # len("hello, world")
        assert isinstance(result, int)


class TestLogMethod:
    def test_logs_method_call(self, capsys):
        class Calculator:
            def __init__(self, name: str):
                self.name = name

            @log_method
            def add(self, a: int, b: int) -> int:
                return a + b

        calc = Calculator("BasicCalc")
        result = calc.add(1, 2)
        assert result == 3
        assert "BasicCalc.add called" in capsys.readouterr().out

    def test_without_name_attr(self, capsys):
        class Simple:
            @log_method
            def method(self) -> str:
                return "done"

        s = Simple()
        assert s.method() == "done"
        assert "Simple.method called" in capsys.readouterr().out


class TestRequireAuth:
    def test_authorized(self):
        class Panel:
            def __init__(self, user: str, roles: dict):
                self.current_user = user
                self.user_roles = roles

            @require_auth("admin")
            def delete(self, item_id: int) -> bool:
                return True

        panel = Panel("alice", {"alice": "admin"})
        assert panel.delete(123) is True

    def test_unauthorized(self):
        class Panel:
            def __init__(self, user: str, roles: dict):
                self.current_user = user
                self.user_roles = roles

            @require_auth("admin")
            def delete(self, item_id: int) -> bool:
                return True

        panel = Panel("bob", {"bob": "user"})
        with pytest.raises(PermissionError, match="does not have admin role"):
            panel.delete(123)
