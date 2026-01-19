"""
Tests for Exercise 8: NewType, TypeAlias, Annotated, and cast

Run with: pytest tests/test_ex08.py -v
"""

import pytest
from exercises.ex08_newtypes_aliases_annotated import (
    get_user_by_id,
    get_product_by_id,
    send_email,
    create_user_id,
    create_email,
    parse_json,
    make_request,
    register_callback,
    calculate_area,
    get_layer_polygons,
    set_age,
    set_username,
    set_discount,
    MinLen,
    MaxLen,
    validate_field,
    get_config_value,
    parse_int_safely,
    find_first_string,
    deserialize_user,
    Order,
    create_customer_id,
    create_invoice_id,
    create_payment_id,
    link_payment_to_invoice,
    get_customer_invoices,
)


class TestNewType:
    def test_get_user_by_id(self):
        result = get_user_by_id(42)
        assert result["id"] == 42
        assert "User_42" in result["name"]

    def test_get_product_by_id(self):
        result = get_product_by_id(100)
        assert result["id"] == 100
        assert "Product_100" in result["name"]

    def test_send_email(self):
        result = send_email("test@example.com", "Hello", "Body")
        assert "test@example.com" in result
        assert "Hello" in result

    def test_create_user_id_valid(self):
        user_id = create_user_id(123)
        assert user_id == 123

    def test_create_user_id_invalid(self):
        with pytest.raises(ValueError, match="positive"):
            create_user_id(0)
        with pytest.raises(ValueError, match="positive"):
            create_user_id(-5)

    def test_create_email_valid(self):
        email = create_email("user@example.com")
        assert email == "user@example.com"

    def test_create_email_invalid(self):
        with pytest.raises(ValueError, match="Invalid email"):
            create_email("not-an-email")


class TestTypeAlias:
    def test_parse_json_object(self):
        result = parse_json('{"key": "value"}')
        assert result == {"key": "value"}

    def test_parse_json_array(self):
        result = parse_json('[1, 2, 3]')
        assert result == [1, 2, 3]

    def test_parse_json_primitive(self):
        assert parse_json('"hello"') == "hello"
        assert parse_json('42') == 42
        assert parse_json('true') is True
        assert parse_json('null') is None

    def test_make_request_no_headers(self):
        result = make_request("https://example.com")
        assert result["url"] == "https://example.com"
        assert result["headers"] == {}
        assert result["status"] == 200

    def test_make_request_with_headers(self):
        headers = {"Authorization": "Bearer token", "Content-Type": "application/json"}
        result = make_request("https://api.example.com", headers)
        assert result["headers"] == headers

    def test_register_callback(self):
        called = []
        def my_callback(msg):
            called.append(msg)

        result = register_callback("test", my_callback)
        assert result is True

    def test_calculate_area_triangle(self):
        # Triangle with vertices at (0,0), (4,0), (0,3)
        # Area = 1/2 * base * height = 1/2 * 4 * 3 = 6
        triangle = [(0.0, 0.0), (4.0, 0.0), (0.0, 3.0)]
        area = calculate_area(triangle)
        assert area == pytest.approx(6.0)

    def test_calculate_area_square(self):
        # Square with vertices at (0,0), (2,0), (2,2), (0,2)
        # Area = 2 * 2 = 4
        square = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]
        area = calculate_area(square)
        assert area == pytest.approx(4.0)

    def test_calculate_area_degenerate(self):
        # Less than 3 points
        assert calculate_area([]) == 0.0
        assert calculate_area([(0.0, 0.0)]) == 0.0
        assert calculate_area([(0.0, 0.0), (1.0, 1.0)]) == 0.0

    def test_get_layer_polygons(self):
        layers = {
            "foreground": [[(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]],
            "background": [[(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]],
        }
        fg = get_layer_polygons(layers, "foreground")
        assert len(fg) == 1

        missing = get_layer_polygons(layers, "nonexistent")
        assert missing == []


class TestAnnotated:
    def test_set_age_valid(self):
        assert set_age(25) == 25
        assert set_age(1) == 1

    def test_set_age_invalid(self):
        with pytest.raises(ValueError, match="positive"):
            set_age(0)
        with pytest.raises(ValueError, match="positive"):
            set_age(-5)

    def test_set_username_valid(self):
        assert set_username("alice") == "alice"
        assert set_username("a") == "a"

    def test_set_username_invalid(self):
        with pytest.raises(ValueError, match="empty"):
            set_username("")

    def test_set_discount_valid(self):
        assert set_discount(0) == 0
        assert set_discount(50) == 50
        assert set_discount(100) == 100

    def test_set_discount_invalid(self):
        with pytest.raises(ValueError, match="between 0 and 100"):
            set_discount(-1)
        with pytest.raises(ValueError, match="between 0 and 100"):
            set_discount(101)


class TestValidateField:
    def test_min_length_pass(self):
        from typing import Annotated
        Username = Annotated[str, MinLen(3)]
        valid, error = validate_field("alice", Username)
        assert valid is True
        assert error is None

    def test_min_length_fail(self):
        from typing import Annotated
        Username = Annotated[str, MinLen(3)]
        valid, error = validate_field("ab", Username)
        assert valid is False
        assert "short" in error.lower()

    def test_max_length_pass(self):
        from typing import Annotated
        ShortStr = Annotated[str, MaxLen(5)]
        valid, error = validate_field("hello", ShortStr)
        assert valid is True

    def test_max_length_fail(self):
        from typing import Annotated
        ShortStr = Annotated[str, MaxLen(5)]
        valid, error = validate_field("toolongstring", ShortStr)
        assert valid is False
        assert "long" in error.lower()

    def test_combined_constraints(self):
        from typing import Annotated
        Username = Annotated[str, MinLen(3), MaxLen(10)]

        # Too short
        valid, _ = validate_field("ab", Username)
        assert valid is False

        # Just right
        valid, _ = validate_field("alice", Username)
        assert valid is True

        # Too long
        valid, _ = validate_field("verylongusername", Username)
        assert valid is False


class TestCast:
    def test_get_config_value(self):
        config = {"name": "myapp", "version": "1.0", "debug": True}
        assert get_config_value(config, "name") == "myapp"
        assert get_config_value(config, "version") == "1.0"

    def test_parse_int_safely_int(self):
        data = {"count": 42}
        assert parse_int_safely(data, "count") == 42

    def test_parse_int_safely_string(self):
        data = {"count": "42"}
        assert parse_int_safely(data, "count") == 42

    def test_parse_int_safely_missing(self):
        data = {}
        assert parse_int_safely(data, "count") is None

    def test_find_first_string(self):
        assert find_first_string([1, 2, "hello", 3]) == "hello"
        assert find_first_string(["first", "second"]) == "first"
        assert find_first_string([1, 2, 3]) is None
        assert find_first_string([]) is None

    def test_deserialize_user(self):
        data = {"id": 123, "name": "Alice", "email": "alice@example.com"}
        result = deserialize_user(data)
        assert result["id"] == 123
        assert result["name"] == "Alice"
        assert result["email"] == "alice@example.com"


class TestOrder:
    def test_order_creation(self):
        items = [
            {"name": "Widget", "price": 10.0, "quantity": 2},
            {"name": "Gadget", "price": 25.0, "quantity": 1},
        ]
        order = Order(1, 100, items)
        assert order.order_id == 1
        assert order.customer_id == 100
        assert order.status == "pending"

    def test_calculate_total(self):
        items = [
            {"name": "Widget", "price": 10.0, "quantity": 2},  # 20
            {"name": "Gadget", "price": 25.0, "quantity": 1},  # 25
        ]
        order = Order(1, 100, items)
        total = order.calculate_total()
        assert total == 45.0
        assert order.total == 45.0

    def test_order_workflow(self):
        order = Order(1, 100, [])
        assert order.status == "pending"

        order.ship()
        assert order.status == "shipped"

        order.deliver()
        assert order.status == "delivered"

    def test_invalid_ship(self):
        order = Order(1, 100, [])
        order.status = "cancelled"
        with pytest.raises(ValueError, match="Cannot ship"):
            order.ship()

    def test_invalid_deliver(self):
        order = Order(1, 100, [])
        # Can't deliver if not shipped
        with pytest.raises(ValueError, match="Cannot deliver"):
            order.deliver()

    def test_order_from_dict(self):
        data = {
            "order_id": 42,
            "customer_id": 100,
            "items": [{"name": "Item", "price": 5.0, "quantity": 1}],
        }
        order = Order.from_dict(data)
        assert order.order_id == 42
        assert order.customer_id == 100
        assert len(order.items) == 1


class TestIdSystem:
    def test_create_customer_id(self):
        cid = create_customer_id(100)
        assert cid == 100

    def test_create_invoice_id(self):
        iid = create_invoice_id(200)
        assert iid == 200

    def test_create_payment_id(self):
        pid = create_payment_id(300)
        assert pid == 300

    def test_link_payment_to_invoice(self):
        payment_id = create_payment_id(1)
        invoice_id = create_invoice_id(2)
        result = link_payment_to_invoice(payment_id, invoice_id)
        assert result is True

    def test_get_customer_invoices(self):
        customer_id = create_customer_id(100)
        invoices = get_customer_invoices(customer_id)
        assert isinstance(invoices, list)
