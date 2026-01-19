"""
Tests for Exercise 9: Variance - Covariance and Contravariance

Run with: pytest tests/test_ex09.py -v
"""

import pytest
from exercises.ex09_variance import (
    Animal,
    Dog,
    Cat,
    add_animal,
    get_first_animal,
    ReadOnlyBox,
    process_animal_box,
    ImmutableList,
    WriteOnlyBox,
    fill_dog_box,
    AnimalHandler,
    Sink,
    apply_to_dog,
    make_dog_speaker,
    make_animal_speaker,
    register_dog_callback,
    EventSource,
    EventListener,
    AnimalByNameComparator,
    sort_dogs,
    Source,
    Destination,
    Transformer,
    build_pipeline,
    make_animal_to_string_transformer,
    make_dog_to_string_transformer,
)


class TestInvariance:
    def test_add_animal(self):
        animals = []
        add_animal(animals, Dog("Rex"))
        add_animal(animals, Cat("Whiskers"))
        assert len(animals) == 2

    def test_get_first_animal(self):
        animals = [Dog("Rex"), Cat("Whiskers")]
        first = get_first_animal(animals)
        assert first.name == "Rex"

    def test_get_first_animal_empty(self):
        assert get_first_animal([]) is None


class TestCovariance:
    def test_readonly_box_get(self):
        box = ReadOnlyBox(Dog("Buddy"))
        dog = box.get()
        assert dog.name == "Buddy"

    def test_readonly_box_peek(self):
        box = ReadOnlyBox(42)
        assert box.peek() == 42

    def test_process_animal_box_with_dog(self):
        dog_box = ReadOnlyBox(Dog("Rex"))
        result = process_animal_box(dog_box)
        assert "Rex" in result
        assert "woof" in result

    def test_process_animal_box_with_cat(self):
        cat_box = ReadOnlyBox(Cat("Whiskers"))
        result = process_animal_box(cat_box)
        assert "Whiskers" in result
        assert "meow" in result

    def test_immutable_list_getitem(self):
        items = ImmutableList([1, 2, 3])
        assert items[0] == 1
        assert items[2] == 3

    def test_immutable_list_len(self):
        items = ImmutableList([1, 2, 3, 4, 5])
        assert len(items) == 5

    def test_immutable_list_iter(self):
        items = ImmutableList(["a", "b", "c"])
        result = list(items)
        assert result == ["a", "b", "c"]

    def test_immutable_list_first(self):
        items = ImmutableList([Dog("Rex"), Dog("Buddy")])
        first = items.first()
        assert first.name == "Rex"

    def test_immutable_list_first_empty(self):
        items = ImmutableList([])
        assert items.first() is None


class TestContravariance:
    def test_writeonly_box_put(self):
        box = WriteOnlyBox()
        box.put("hello")
        box.put("world")
        assert box.count() == 2

    def test_fill_dog_box(self):
        box = WriteOnlyBox()
        dogs = [Dog("Rex"), Dog("Buddy")]
        fill_dog_box(box, dogs)
        assert box.count() == 2

    def test_animal_handler(self):
        handler = AnimalHandler()
        result = handler.handle(Dog("Rex"))
        assert "Rex" in result
        assert "woof" in result

    def test_sink_send(self):
        sink = Sink("test")
        sink.send("message1")
        sink.send("message2")
        assert sink.get_received() == ["message1", "message2"]


class TestCallableVariance:
    def test_apply_to_dog_with_dog_func(self):
        speaker = make_dog_speaker()
        dog = Dog("Buddy")
        result = apply_to_dog(speaker, dog)
        assert "Buddy" in result
        assert "woof" in result

    def test_apply_to_dog_with_animal_func(self):
        # A function that works on ANY Animal should work on Dog
        speaker = make_animal_speaker()
        dog = Dog("Buddy")
        result = apply_to_dog(speaker, dog)
        assert "Buddy" in result

    def test_register_dog_callback(self):
        received = []

        def callback(dog):
            received.append(dog.name)

        register_dog_callback(callback)
        assert "Buddy" in received

    def test_register_dog_callback_with_animal_handler(self):
        # A callback that handles ANY Animal should work for Dogs
        received = []

        def animal_callback(animal):
            received.append(animal.speak())

        register_dog_callback(animal_callback)
        assert len(received) == 1
        assert "woof" in received[0]


class TestRealWorldPatterns:
    def test_event_source_and_listener(self):
        source = EventSource()
        listener = EventListener("test")

        source.subscribe(listener)
        source.emit("event1")
        source.emit("event2")

        assert listener.get_events() == ["event1", "event2"]

    def test_comparator_sort_dogs(self):
        dogs = [
            Dog("Charlie"),
            Dog("Alice"),
            Dog("Bob"),
        ]
        comparator = AnimalByNameComparator()
        sorted_dogs = sort_dogs(dogs, comparator)

        assert sorted_dogs[0].name == "Alice"
        assert sorted_dogs[1].name == "Bob"
        assert sorted_dogs[2].name == "Charlie"

    def test_comparator_already_sorted(self):
        dogs = [Dog("A"), Dog("B"), Dog("C")]
        comparator = AnimalByNameComparator()
        sorted_dogs = sort_dogs(dogs, comparator)
        assert [d.name for d in sorted_dogs] == ["A", "B", "C"]


class TestPipeline:
    def test_source_basic(self):
        source = Source([1, 2, 3])
        assert source.has_next() is True
        assert source.next() == 1
        assert source.next() == 2
        assert source.next() == 3
        assert source.has_next() is False
        assert source.next() is None

    def test_source_reset(self):
        source = Source([1, 2])
        source.next()
        source.next()
        source.reset()
        assert source.next() == 1

    def test_destination_write(self):
        dest = Destination("output")
        dest.write("a")
        dest.write("b")
        assert dest.get_all() == ["a", "b"]

    def test_transformer(self):
        transformer = Transformer(lambda x: x * 2)
        assert transformer.transform(5) == 10
        assert transformer.transform(3) == 6

    def test_build_pipeline_basic(self):
        source = Source([1, 2, 3])
        transformer = Transformer(lambda x: x * 10)
        destination = Destination("output")

        build_pipeline(source, transformer, destination)

        assert destination.get_all() == [10, 20, 30]

    def test_build_pipeline_with_animals(self):
        dogs = [Dog("Rex"), Dog("Buddy"), Dog("Max")]
        source = Source(dogs)
        transformer = make_animal_to_string_transformer()
        destination = Destination("speeches")

        build_pipeline(source, transformer, destination)

        speeches = destination.get_all()
        assert len(speeches) == 3
        assert all("woof" in s for s in speeches)

    def test_dog_transformer(self):
        transformer = make_dog_to_string_transformer()
        dog = Dog("Buddy")
        result = transformer.transform(dog)
        assert "woof" in result
        assert "fetch" in result

    def test_pipeline_empty_source(self):
        source = Source([])
        transformer = Transformer(lambda x: x)
        destination = Destination("output")

        build_pipeline(source, transformer, destination)

        assert destination.get_all() == []
