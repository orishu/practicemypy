"""
Tests for Exercise 7: ClassVar, Final, and Self

Run with: pytest tests/test_ex07.py -v
"""

import pytest
from exercises.ex07_classvar_final_self import (
    Counter,
    Config,
    MAX_CONNECTIONS,
    DEFAULT_HOST,
    SUPPORTED_PROTOCOLS,
    DatabasePool,
    AppSettings,
    SecurityToken,
    BaseHandler,
    JsonHandler,
    StringBuilder,
    QueryBuilder,
    Shape,
    Circle,
    Rectangle,
    IDGenerator,
)


class TestClassVar:
    def test_counter_instance_counts(self):
        Counter.reset_total()
        c1 = Counter()
        c2 = Counter()

        c1.increment()
        c1.increment()
        c2.increment()

        assert c1.count == 2
        assert c2.count == 1

    def test_counter_total_shared(self):
        Counter.reset_total()
        c1 = Counter()
        c2 = Counter()

        c1.increment()
        c1.increment()
        c2.increment()

        assert Counter.total_increments == 3
        assert Counter.get_total() == 3

    def test_config_class_defaults(self):
        assert Config.default_timeout == 30
        assert Config.max_retries == 3
        assert "debug" in Config.valid_modes

    def test_config_instance_overrides(self):
        c = Config(timeout=60, retries=5)
        assert c.get_timeout() == 60
        assert c.get_retries() == 5

    def test_config_uses_defaults(self):
        c = Config()
        assert c.get_timeout() == 30
        assert c.get_retries() == 3


class TestFinalConstants:
    def test_max_connections(self):
        assert MAX_CONNECTIONS == 100

    def test_default_host(self):
        assert DEFAULT_HOST == "localhost"

    def test_supported_protocols(self):
        assert "http" in SUPPORTED_PROTOCOLS
        assert "https" in SUPPORTED_PROTOCOLS
        assert len(SUPPORTED_PROTOCOLS) == 4


class TestDatabasePool:
    def test_immutable_config(self):
        pool = DatabasePool("postgres://localhost/db", max_size=5)
        assert pool.connection_string == "postgres://localhost/db"
        assert pool.max_size == 5

    def test_acquire_connections(self):
        pool = DatabasePool("postgres://localhost/db", max_size=2)

        conn1 = pool.acquire()
        assert conn1 is not None
        assert pool.current_size == 1

        conn2 = pool.acquire()
        assert conn2 is not None
        assert pool.current_size == 2

        conn3 = pool.acquire()
        assert conn3 is None  # Pool exhausted
        assert pool.current_size == 2

    def test_release_connections(self):
        pool = DatabasePool("postgres://localhost/db", max_size=2)
        conn = pool.acquire()
        pool.release(conn)
        assert pool.current_size == 0


class TestAppSettings:
    def test_settings_created(self):
        settings = AppSettings("MyApp", "1.0.0", debug=True)
        assert settings.app_name == "MyApp"
        assert settings.version == "1.0.0"
        assert settings.debug is True

    def test_get_info(self):
        settings = AppSettings("MyApp", "2.0.0", debug=False)
        info = settings.get_info()
        assert "MyApp" in info
        assert "2.0.0" in info
        assert "production" in info


class TestFinalDecorator:
    def test_security_token_validation(self):
        token = SecurityToken("user123", ["read", "write"])
        assert token.has_permission("read") is True
        assert token.has_permission("delete") is False
        assert token.validate() is True

    def test_invalid_token(self):
        token = SecurityToken(None, [])
        assert token.validate() is False

    def test_base_handler_validate(self):
        handler = BaseHandler("test")
        assert handler.validate_request({"auth": "token"}) is True
        assert handler.validate_request({}) is False
        assert handler.validate_request("not a dict") is False

    def test_base_handler_handle(self):
        handler = BaseHandler("test")
        result = handler.handle({"auth": "token"})
        assert result["handler"] == "test"
        assert result["status"] == "ok"

    def test_json_handler_override(self):
        handler = JsonHandler("json")
        result = handler.handle({"auth": "token", "data": "value"})
        assert result["type"] == "json"

    def test_handler_log_request(self):
        handler = BaseHandler("test")
        log = handler.log_request({"auth": "token"})
        assert "[test]" in log


class TestStringBuilder:
    def test_simple_build(self):
        result = StringBuilder().append("Hello").build()
        assert result == "Hello"

    def test_chained_append(self):
        result = (StringBuilder()
            .append("Hello")
            .append(" ")
            .append("World")
            .build())
        assert result == "Hello World"

    def test_append_line(self):
        result = (StringBuilder()
            .append_line("Line 1")
            .append_line("Line 2")
            .build())
        assert result == "Line 1\nLine 2\n"

    def test_to_upper(self):
        result = (StringBuilder()
            .append("hello")
            .to_upper()
            .build())
        assert result == "HELLO"

    def test_to_lower(self):
        result = (StringBuilder()
            .append("HELLO")
            .to_lower()
            .build())
        assert result == "hello"

    def test_clear(self):
        builder = StringBuilder().append("text")
        builder.clear()
        assert builder.build() == ""

    def test_complex_chain(self):
        result = (StringBuilder()
            .append("hello")
            .append(" world")
            .to_upper()
            .append("!")
            .build())
        assert result == "HELLO WORLD!"


class TestQueryBuilder:
    def test_simple_query(self):
        query = QueryBuilder("users").build()
        assert query == "SELECT * FROM users"

    def test_select_columns(self):
        query = QueryBuilder("users").select("name", "email").build()
        assert query == "SELECT name, email FROM users"

    def test_where_clause(self):
        query = (QueryBuilder("users")
            .where("active = true")
            .build())
        assert "WHERE active = true" in query

    def test_multiple_where(self):
        query = (QueryBuilder("users")
            .where("active = true")
            .where("age > 18")
            .build())
        assert "WHERE active = true AND age > 18" in query

    def test_order_by(self):
        query = (QueryBuilder("users")
            .order_by("name")
            .build())
        assert "ORDER BY name" in query

    def test_limit(self):
        query = (QueryBuilder("users")
            .limit(10)
            .build())
        assert "LIMIT 10" in query

    def test_full_query(self):
        query = (QueryBuilder("users")
            .select("name", "email")
            .where("active = true")
            .order_by("name")
            .limit(10)
            .build())
        assert query == "SELECT name, email FROM users WHERE active = true ORDER BY name LIMIT 10"


class TestShapeHierarchy:
    def test_shape_at_origin(self):
        shape = Shape.at_origin()
        assert shape.x == 0
        assert shape.y == 0

    def test_circle_at_origin(self):
        circle = Circle.at_origin()
        assert isinstance(circle, Circle)
        assert circle.x == 0
        assert circle.y == 0

    def test_rectangle_at_origin(self):
        rect = Rectangle.at_origin()
        assert isinstance(rect, Rectangle)
        assert rect.x == 0
        assert rect.y == 0

    def test_shape_move(self):
        shape = Shape(0, 0)
        result = shape.move(5, 10)
        assert result is shape  # Returns self
        assert shape.x == 5
        assert shape.y == 10

    def test_circle_move_chain(self):
        circle = Circle(0, 0, radius=5)
        result = circle.move(10, 10).scale(2)
        assert isinstance(result, Circle)
        assert circle.x == 10
        assert circle.radius == 10

    def test_circle_copy(self):
        original = Circle(5, 10, radius=3)
        copy = original.copy()
        assert isinstance(copy, Circle)
        assert copy is not original
        assert copy.x == 5
        assert copy.radius == 3

    def test_rectangle_copy(self):
        original = Rectangle(5, 10, width=20, height=30)
        copy = original.copy()
        assert isinstance(copy, Rectangle)
        assert copy is not original
        assert copy.width == 20
        assert copy.height == 30


class TestIDGenerator:
    def test_basic_id_generation(self):
        IDGenerator.reset()
        gen = IDGenerator("USER")
        assert gen.next_id() == "USER-1"
        assert gen.next_id() == "USER-2"

    def test_custom_separator(self):
        IDGenerator.reset()
        gen = IDGenerator("ORDER").with_separator("_")
        assert gen.next_id() == "ORDER_1"

    def test_padding(self):
        IDGenerator.reset()
        gen = IDGenerator("ID").with_padding(5)
        assert gen.next_id() == "ID-00001"
        assert gen.next_id() == "ID-00002"

    def test_fluent_configuration(self):
        IDGenerator.reset()
        gen = IDGenerator("REF").with_separator("::").with_padding(3)
        assert gen.next_id() == "REF::001"

    def test_shared_counter(self):
        IDGenerator.reset()
        gen1 = IDGenerator("A")
        gen2 = IDGenerator("B")

        assert gen1.next_id() == "A-1"
        assert gen2.next_id() == "B-2"  # Counter is shared!
        assert gen1.next_id() == "A-3"
