"""
Tests for Exercise 4: Callable and Overload

Run with: pytest tests/test_ex04.py -v
"""

import pytest
from exercises.ex04_callable_and_overload import (
    apply_twice,
    call_with_logging,
    make_repeater,
    map_list,
    filter_list,
    compose,
    EventHandler,
    double,
    parse_value,
    get_item,
    retry,
    Success,
    Failure,
    handle_result,
)


class TestApplyTwice:
    def test_increment(self):
        result = apply_twice(lambda x: x + 1, 5)
        assert result == 7

    def test_double(self):
        result = apply_twice(lambda x: x * 2, 3)
        assert result == 12

    def test_string(self):
        result = apply_twice(lambda s: s + "!", "hi")
        assert result == "hi!!"


class TestCallWithLogging:
    def test_abs(self):
        name, result = call_with_logging(abs, -5)
        assert name == "abs"
        assert result == 5

    def test_max(self):
        name, result = call_with_logging(max, 1, 2, 3)
        assert name == "max"
        assert result == 3

    def test_len(self):
        name, result = call_with_logging(len, [1, 2, 3])
        assert name == "len"
        assert result == 3


class TestMakeRepeater:
    def test_repeat_3(self):
        repeat3 = make_repeater(3)
        assert repeat3("ha") == "hahaha"

    def test_repeat_1(self):
        repeat1 = make_repeater(1)
        assert repeat1("x") == "x"

    def test_repeat_0(self):
        repeat0 = make_repeater(0)
        assert repeat0("anything") == ""


class TestMapList:
    def test_upper(self):
        result = map_list(str.upper, ["a", "b", "c"])
        assert result == ["A", "B", "C"]

    def test_double(self):
        result = map_list(lambda x: x * 2, [1, 2, 3])
        assert result == [2, 4, 6]

    def test_empty(self):
        result = map_list(str.upper, [])
        assert result == []

    def test_type_change(self):
        result = map_list(str, [1, 2, 3])
        assert result == ["1", "2", "3"]


class TestFilterList:
    def test_positive(self):
        result = filter_list(lambda x: x > 0, [-1, 0, 1, 2])
        assert result == [1, 2]

    def test_isupper(self):
        result = filter_list(str.isupper, ["A", "b", "C"])
        assert result == ["A", "C"]

    def test_none_match(self):
        result = filter_list(lambda x: x > 100, [1, 2, 3])
        assert result == []


class TestCompose:
    def test_add_then_double(self):
        add1 = lambda x: x + 1
        double = lambda x: x * 2
        add1_then_double = compose(double, add1)
        assert add1_then_double(5) == 12

    def test_double_then_add(self):
        add1 = lambda x: x + 1
        double = lambda x: x * 2
        double_then_add1 = compose(add1, double)
        assert double_then_add1(5) == 11

    def test_type_change(self):
        to_str = lambda x: str(x)
        add_exclaim = lambda s: s + "!"
        composed = compose(add_exclaim, to_str)
        assert composed(42) == "42!"


class TestEventHandler:
    def test_success_callback(self):
        handler = EventHandler()
        results = []
        handler.on_success = lambda msg: results.append(f"OK: {msg}")
        handler.trigger_success("Done")
        assert results == ["OK: Done"]

    def test_error_callback(self):
        handler = EventHandler()
        results = []
        handler.on_error = lambda code, msg: results.append(f"{code}: {msg}")
        handler.trigger_error(404, "Not found")
        assert results == ["404: Not found"]

    def test_no_callback(self):
        handler = EventHandler()
        # Should not raise even without callbacks set
        handler.trigger_success("test")
        handler.trigger_error(500, "error")


class TestDouble:
    def test_int(self):
        result = double(5)
        assert result == 10

    def test_str(self):
        result = double("ha")
        assert result == "haha"


class TestParseValue:
    def test_as_int_true(self):
        result = parse_value("42", True)
        assert result == 42
        assert isinstance(result, int)

    def test_as_int_false(self):
        result = parse_value("42", False)
        assert result == "42"
        assert isinstance(result, str)

    def test_string_value(self):
        result = parse_value("hello", False)
        assert result == "hello"


class TestGetItem:
    def test_valid_index(self):
        result = get_item([1, 2, 3], 0)
        assert result == 1

    def test_invalid_index_no_default(self):
        result = get_item([1, 2, 3], 10)
        assert result is None

    def test_invalid_index_with_default(self):
        result = get_item([1, 2, 3], 10, -1)
        assert result == -1

    def test_valid_index_with_default(self):
        result = get_item([1, 2, 3], 1, -1)
        assert result == 2


class TestRetry:
    def test_succeeds_first_try(self):
        @retry(3)
        def always_works():
            return "success"

        assert always_works() == "success"

    def test_succeeds_after_failures(self):
        attempts = [0]

        @retry(3)
        def fails_twice():
            attempts[0] += 1
            if attempts[0] < 3:
                raise ValueError("not yet")
            return "finally"

        assert fails_twice() == "finally"
        assert attempts[0] == 3

    def test_exhausts_retries(self):
        @retry(3)
        def always_fails():
            raise ValueError("always")

        with pytest.raises(ValueError, match="always"):
            always_fails()


class TestHandleResult:
    def test_success(self):
        result = handle_result(Success("data"))
        assert result == "data"

    def test_failure(self):
        result = handle_result(Failure("oops"))
        assert result == "oops"
