"""
Tests for Exercise 6: TypedDict and Type Guards

Run with: pytest tests/test_ex06.py -v
"""

import pytest
from exercises.ex06_typeddict_and_guards import (
    distance_from_origin,
    translate_point,
    get_display_name,
    get_user_email_or_default,
    create_user,
    get_employee_city,
    is_remote_employee,
    create_employee,
    is_point2d,
    is_user_profile,
    process_points,
    safe_get_distance,
    is_text_message,
    is_image_message,
    is_video_message,
    get_message_preview,
    count_messages_by_type,
)


class TestPoint2D:
    def test_distance_from_origin(self):
        assert distance_from_origin({"x": 3, "y": 4}) == 5.0
        assert distance_from_origin({"x": 0, "y": 0}) == 0.0
        assert distance_from_origin({"x": 1, "y": 0}) == 1.0

    def test_translate_point(self):
        result = translate_point({"x": 1, "y": 2}, 10, 20)
        assert result == {"x": 11, "y": 22}

    def test_translate_returns_new_dict(self):
        original = {"x": 1, "y": 2}
        result = translate_point(original, 10, 20)
        assert result is not original
        assert original == {"x": 1, "y": 2}  # unchanged


class TestUserProfile:
    def test_get_display_name(self):
        assert get_display_name({"id": 1, "name": "Alice"}) == "Alice"
        assert get_display_name({"id": 2, "name": "Bob", "email": "bob@x.com"}) == "Bob"

    def test_get_email_when_present(self):
        user = {"id": 1, "name": "Alice", "email": "alice@example.com"}
        assert get_user_email_or_default(user, "n/a") == "alice@example.com"

    def test_get_email_when_missing(self):
        user = {"id": 1, "name": "Alice"}
        assert get_user_email_or_default(user, "n/a") == "n/a"

    def test_create_user_minimal(self):
        result = create_user(1, "Alice")
        assert result == {"id": 1, "name": "Alice"}

    def test_create_user_with_email(self):
        result = create_user(2, "Bob", email="bob@x.com")
        assert result == {"id": 2, "name": "Bob", "email": "bob@x.com"}

    def test_create_user_with_all_fields(self):
        result = create_user(3, "Carol", email="carol@x.com", age=30)
        assert result == {"id": 3, "name": "Carol", "email": "carol@x.com", "age": 30}


class TestNestedTypedDict:
    def test_get_employee_city(self):
        emp = {
            "id": 1,
            "name": "Alice",
            "company": {
                "name": "Acme Corp",
                "address": {
                    "street": "123 Main St",
                    "city": "Boston",
                    "country": "USA",
                },
            },
        }
        assert get_employee_city(emp) == "Boston"

    def test_is_remote_employee_true(self):
        emp = {
            "id": 1,
            "name": "Bob",
            "company": {
                "name": "Remote Inc",
                "address": {"street": "1 Web Way", "city": "Internet", "country": "WWW"},
            },
            "remote": True,
        }
        assert is_remote_employee(emp) is True

    def test_is_remote_employee_false(self):
        emp = {
            "id": 2,
            "name": "Carol",
            "company": {
                "name": "Office Corp",
                "address": {"street": "2 Desk Dr", "city": "NYC", "country": "USA"},
            },
            "remote": False,
        }
        assert is_remote_employee(emp) is False

    def test_is_remote_employee_missing(self):
        emp = {
            "id": 3,
            "name": "Dave",
            "company": {
                "name": "Default Co",
                "address": {"street": "3 Lane", "city": "LA", "country": "USA"},
            },
        }
        assert is_remote_employee(emp) is False

    def test_create_employee_minimal(self):
        result = create_employee(1, "Alice", "Acme", "123 Main", "Boston", "USA")
        assert result["id"] == 1
        assert result["name"] == "Alice"
        assert result["company"]["name"] == "Acme"
        assert result["company"]["address"]["city"] == "Boston"
        assert "remote" not in result

    def test_create_employee_with_remote(self):
        result = create_employee(2, "Bob", "Remote Inc", "1 Web", "Internet", "WWW", remote=True)
        assert result["remote"] is True


class TestTypeGuards:
    def test_is_point2d_valid(self):
        assert is_point2d({"x": 1, "y": 2}) is True
        assert is_point2d({"x": 0, "y": 0}) is True
        assert is_point2d({"x": -5, "y": 10}) is True

    def test_is_point2d_invalid(self):
        assert is_point2d({"x": 1}) is False  # missing y
        assert is_point2d({"y": 2}) is False  # missing x
        assert is_point2d({"x": "1", "y": 2}) is False  # wrong type
        assert is_point2d({"x": 1, "y": "2"}) is False  # wrong type
        assert is_point2d([1, 2]) is False  # not a dict
        assert is_point2d("point") is False
        assert is_point2d(None) is False

    def test_is_user_profile_valid(self):
        assert is_user_profile({"id": 1, "name": "Alice"}) is True
        assert is_user_profile({"id": 2, "name": "Bob", "email": "b@x.com"}) is True
        assert is_user_profile({"id": 3, "name": "Carol", "age": 25}) is True
        assert is_user_profile({"id": 4, "name": "Dave", "email": "d@x.com", "age": 30}) is True

    def test_is_user_profile_invalid(self):
        assert is_user_profile({"name": "Alice"}) is False  # missing id
        assert is_user_profile({"id": 1}) is False  # missing name
        assert is_user_profile({"id": "1", "name": "Alice"}) is False  # id wrong type
        assert is_user_profile({"id": 1, "name": 123}) is False  # name wrong type
        assert is_user_profile({"id": 1, "name": "A", "email": 123}) is False  # email wrong type
        assert is_user_profile({"id": 1, "name": "A", "age": "25"}) is False  # age wrong type


class TestTypeGuardUsage:
    def test_process_points(self):
        data = [
            {"x": 1, "y": 2},
            {"x": 3},  # invalid
            {"x": 4, "y": 5},
            "not a point",
            {"x": "6", "y": 7},  # invalid type
        ]
        result = process_points(data)
        assert result == [{"x": 1, "y": 2}, {"x": 4, "y": 5}]

    def test_process_points_empty(self):
        assert process_points([]) == []

    def test_process_points_all_invalid(self):
        assert process_points([{"x": 1}, {"y": 2}, "bad"]) == []

    def test_safe_get_distance_valid(self):
        assert safe_get_distance({"x": 3, "y": 4}) == 5.0
        assert safe_get_distance({"x": 0, "y": 0}) == 0.0

    def test_safe_get_distance_invalid(self):
        assert safe_get_distance({"x": 3}) is None
        assert safe_get_distance("not a point") is None
        assert safe_get_distance(None) is None
        assert safe_get_distance([3, 4]) is None


class TestDiscriminatedUnions:
    def test_is_text_message(self):
        assert is_text_message({"type": "text", "content": "hello"}) is True
        assert is_text_message({"type": "image", "url": "http://..."}) is False
        assert is_text_message({"type": "video", "url": "http://...", "duration": 60}) is False

    def test_is_image_message(self):
        assert is_image_message({"type": "image", "url": "http://..."}) is True
        assert is_image_message({"type": "image", "url": "http://...", "alt_text": "A photo"}) is True
        assert is_image_message({"type": "text", "content": "hello"}) is False

    def test_is_video_message(self):
        assert is_video_message({"type": "video", "url": "http://...", "duration": 120}) is True
        assert is_video_message({"type": "text", "content": "hello"}) is False

    def test_get_message_preview_text(self):
        msg = {"type": "text", "content": "Hello, world!"}
        assert get_message_preview(msg) == "Text: Hello, world!"

    def test_get_message_preview_image_with_alt(self):
        msg = {"type": "image", "url": "http://example.com/cat.jpg", "alt_text": "A cute cat"}
        assert get_message_preview(msg) == "Image: A cute cat"

    def test_get_message_preview_image_without_alt(self):
        msg = {"type": "image", "url": "http://example.com/photo.jpg"}
        assert get_message_preview(msg) == "Image: [no description]"

    def test_get_message_preview_video(self):
        msg = {"type": "video", "url": "http://example.com/video.mp4", "duration": 125}
        assert get_message_preview(msg) == "Video: 2:05"

    def test_get_message_preview_video_short(self):
        msg = {"type": "video", "url": "http://example.com/clip.mp4", "duration": 5}
        assert get_message_preview(msg) == "Video: 0:05"

    def test_count_messages_by_type(self):
        messages = [
            {"type": "text", "content": "hi"},
            {"type": "text", "content": "bye"},
            {"type": "image", "url": "http://..."},
            {"type": "video", "url": "http://...", "duration": 60},
            {"type": "text", "content": "hello"},
        ]
        result = count_messages_by_type(messages)
        assert result == {"text": 3, "image": 1, "video": 1}

    def test_count_messages_empty(self):
        result = count_messages_by_type([])
        assert result == {"text": 0, "image": 0, "video": 0}
