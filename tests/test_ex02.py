"""
Tests for Exercise 2: TypeVar Constraints and Bounds

Run with: pytest tests/test_ex02.py -v
"""

import pytest
from exercises.ex02_typevar_constraints import (
    add_numbers,
    double_it,
    Animal,
    Dog,
    Cat,
    Fish,
    get_loudest,
    make_speak_twice,
    Score,
    Name,
    SortedContainer,
    JsonValue,
    XmlValue,
    Cache,
)


class TestAddNumbers:
    def test_add_ints(self):
        result = add_numbers(1, 2)
        assert result == 3
        assert isinstance(result, int)

    def test_add_floats(self):
        result = add_numbers(1.5, 2.5)
        assert result == 4.0
        assert isinstance(result, float)

    def test_add_negative(self):
        result = add_numbers(-5, 3)
        assert result == -2


class TestDoubleIt:
    def test_double_string(self):
        result = double_it("abc")
        assert result == "abcabc"

    def test_double_bytes(self):
        result = double_it(b"xyz")
        assert result == b"xyzxyz"

    def test_empty_string(self):
        result = double_it("")
        assert result == ""


class TestGetLoudest:
    def test_loudest_dog(self):
        dogs = [Dog("Rex"), Dog("Buddy Longname")]
        result = get_loudest(dogs)
        assert result.name == "Buddy Longname"

    def test_loudest_cat(self):
        cats = [Cat("Whiskers"), Cat("Mr. Fluffington")]
        result = get_loudest(cats)
        assert result.name == "Mr. Fluffington"

    def test_single_animal(self):
        dogs = [Dog("Solo")]
        result = get_loudest(dogs)
        assert result.name == "Solo"

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            get_loudest([])


class TestMakeSpeakTwice:
    def test_dog(self):
        dog = Dog("Rex")
        animal, s1, s2 = make_speak_twice(dog)
        assert animal is dog
        assert s1 == s2
        assert "Woof" in s1

    def test_cat(self):
        cat = Cat("Whiskers")
        animal, s1, s2 = make_speak_twice(cat)
        assert animal is cat
        assert "Meow" in s1


class TestSortedContainer:
    def test_scores(self):
        sc = SortedContainer()
        sc.add(Score(50))
        sc.add(Score(30))
        sc.add(Score(70))
        all_items = sc.get_all()
        assert [s.value for s in all_items] == [30, 50, 70]

    def test_names(self):
        sc = SortedContainer()
        sc.add(Name("Charlie"))
        sc.add(Name("Alice"))
        sc.add(Name("Bob"))
        all_items = sc.get_all()
        assert [n.name for n in all_items] == ["Alice", "Bob", "Charlie"]

    def test_get_min(self):
        sc = SortedContainer()
        sc.add(Score(50))
        sc.add(Score(30))
        assert sc.get_min().value == 30

    def test_get_max(self):
        sc = SortedContainer()
        sc.add(Score(50))
        sc.add(Score(70))
        assert sc.get_max().value == 70

    def test_empty_min(self):
        sc = SortedContainer()
        assert sc.get_min() is None

    def test_empty_max(self):
        sc = SortedContainer()
        assert sc.get_max() is None


class TestCache:
    def test_json_cache(self):
        cache = Cache()
        json_val = JsonValue({"debug": True})
        cache.put("config", json_val)
        result = cache.get("config")
        assert result is json_val

    def test_xml_cache(self):
        cache = Cache()
        xml_val = XmlValue("greeting", "Hello")
        cache.put("msg", xml_val)
        result = cache.get("msg")
        assert result is xml_val

    def test_get_missing(self):
        cache = Cache()
        assert cache.get("missing") is None

    def test_get_serialized(self):
        cache = Cache()
        cache.put("data", JsonValue({"x": 1}))
        result = cache.get_serialized("data")
        assert result == '{"x": 1}'

    def test_get_serialized_missing(self):
        cache = Cache()
        assert cache.get_serialized("missing") is None

    def test_xml_serialized(self):
        cache = Cache()
        cache.put("tag", XmlValue("note", "content"))
        result = cache.get_serialized("tag")
        assert result == "<note>content</note>"
