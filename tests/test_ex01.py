"""
Tests for Exercise 1: Generic Types Basics

Run with: pytest tests/test_ex01.py -v

These tests verify both runtime behavior AND type correctness.
The type comments show what mypy should infer - your implementation
should match these types.
"""

import pytest
from exercises.ex01_generics_basics import (
    first_element,
    identity,
    swap_dict,
    make_pair,
    Box,
    Pair,
    Stack,
)


class TestFirstElement:
    def test_int_list(self):
        result = first_element([1, 2, 3])
        assert result == 1

    def test_str_list(self):
        result = first_element(["a", "b", "c"])
        assert result == "a"

    def test_empty_list(self):
        result = first_element([])
        assert result is None

    def test_single_element(self):
        result = first_element([42])
        assert result == 42


class TestIdentity:
    def test_int(self):
        result = identity(42)
        assert result == 42

    def test_str(self):
        result = identity("hello")
        assert result == "hello"

    def test_list(self):
        original = [1, 2, 3]
        result = identity(original)
        assert result is original


class TestSwapDict:
    def test_str_to_int(self):
        result = swap_dict({"a": 1, "b": 2})
        assert result == {1: "a", 2: "b"}

    def test_int_to_str(self):
        result = swap_dict({1: "x", 2: "y"})
        assert result == {"x": 1, "y": 2}

    def test_empty_dict(self):
        result = swap_dict({})
        assert result == {}


class TestMakePair:
    def test_mixed_types(self):
        result = make_pair(1, "a")
        assert result == (1, "a")

    def test_same_types(self):
        result = make_pair("x", "y")
        assert result == ("x", "y")

    def test_is_tuple(self):
        result = make_pair(1, 2)
        assert isinstance(result, tuple)


class TestBox:
    def test_int_box(self):
        box = Box(42)
        assert box.get() == 42

    def test_str_box(self):
        box = Box("hello")
        assert box.get() == "hello"

    def test_set_value(self):
        box = Box(1)
        box.set(100)
        assert box.get() == 100

    def test_list_box(self):
        box = Box([1, 2, 3])
        assert box.get() == [1, 2, 3]


class TestPair:
    def test_creation(self):
        p = Pair("name", 42)
        assert p.first == "name"
        assert p.second == 42

    def test_swap(self):
        p = Pair("a", 1)
        swapped = p.swap()
        assert swapped.first == 1
        assert swapped.second == "a"

    def test_swap_returns_new_pair(self):
        p = Pair("a", 1)
        swapped = p.swap()
        assert p is not swapped
        assert p.first == "a"  # Original unchanged


class TestStack:
    def test_push_and_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert s.pop() == 2
        assert s.pop() == 1

    def test_pop_empty(self):
        s = Stack()
        assert s.pop() is None

    def test_peek(self):
        s = Stack()
        s.push(42)
        assert s.peek() == 42
        assert s.peek() == 42  # Peek doesn't remove

    def test_peek_empty(self):
        s = Stack()
        assert s.peek() is None

    def test_is_empty(self):
        s = Stack()
        assert s.is_empty() is True
        s.push(1)
        assert s.is_empty() is False
        s.pop()
        assert s.is_empty() is True

    def test_string_stack(self):
        s = Stack()
        s.push("a")
        s.push("b")
        assert s.pop() == "b"
