"""
Tests for Exercise 3: Protocols

Run with: pytest tests/test_ex03.py -v
"""

import pytest
from exercises.ex03_protocols import (
    Circle,
    Rectangle,
    Point,
    render,
    render_all,
    User,
    Product,
    greet,
    FileHandle,
    Connection,
    SimpleValue,
    maybe_close,
    IntHolder,
    StringHolder,
    double_container_value,
    swap_containers,
    InMemoryFile,
    ReadOnlyBuffer,
    WriteOnlyLog,
    read_content,
    write_content,
    copy_content,
    update_content,
)


class TestDrawable:
    def test_render_circle(self):
        c = Circle(5)
        result = render(c)
        assert result == "Rendering: Circle(radius=5)"

    def test_render_rectangle(self):
        r = Rectangle(3, 4)
        result = render(r)
        assert result == "Rendering: Rectangle(3x4)"

    def test_render_all(self):
        shapes = [Circle(1), Rectangle(2, 3)]
        results = render_all(shapes)
        assert len(results) == 2
        assert "Circle" in results[0]
        assert "Rectangle" in results[1]


class TestNamed:
    def test_greet_user(self):
        user = User("Alice", "alice@example.com")
        result = greet(user)
        assert result == "Hello, Alice!"

    def test_greet_product(self):
        product = Product("Widget", 9.99)
        result = greet(product)
        assert result == "Hello, Widget!"


class TestCloseable:
    def test_close_file_handle(self):
        fh = FileHandle("/tmp/test")
        assert fh.is_open is True
        result = maybe_close(fh)
        assert result is True
        assert fh.is_open is False

    def test_close_connection(self):
        conn = Connection("localhost")
        assert conn.connected is True
        result = maybe_close(conn)
        assert result is True
        assert conn.connected is False

    def test_not_closeable(self):
        val = SimpleValue(42)
        result = maybe_close(val)
        assert result is False


class TestContainer:
    def test_double_int_holder(self):
        holder = IntHolder(21)
        double_container_value(holder)
        assert holder.get() == 42

    def test_swap_int_containers(self):
        c1 = IntHolder(1)
        c2 = IntHolder(2)
        swap_containers(c1, c2)
        assert c1.get() == 2
        assert c2.get() == 1

    def test_swap_string_containers(self):
        c1 = StringHolder("hello")
        c2 = StringHolder("world")
        swap_containers(c1, c2)
        assert c1.get() == "world"
        assert c2.get() == "hello"


class TestReadWritable:
    def test_read_from_file(self):
        f = InMemoryFile()
        f.write("test content")
        result = read_content(f)
        assert result == "test content"

    def test_read_from_buffer(self):
        buf = ReadOnlyBuffer("readonly content")
        result = read_content(buf)
        assert result == "readonly content"

    def test_write_to_file(self):
        f = InMemoryFile()
        write_content(f, "new content")
        assert f.read() == "new content"

    def test_write_to_log(self):
        log = WriteOnlyLog()
        write_content(log, "entry 1")
        write_content(log, "entry 2")
        assert log.get_entries() == ["entry 1", "entry 2"]

    def test_copy_content(self):
        source = ReadOnlyBuffer("copy me")
        dest = InMemoryFile()
        copy_content(source, dest)
        assert dest.read() == "copy me"

    def test_update_content(self):
        f = InMemoryFile()
        f.write("hello")
        update_content(f, str.upper)
        assert f.read() == "HELLO"

    def test_update_with_lambda(self):
        f = InMemoryFile()
        f.write("world")
        update_content(f, lambda s: f"Hello, {s}!")
        assert f.read() == "Hello, world!"
