from unittest.mock import MagicMock

import pytest
import string
import random

from src.pytest_extended_mock.plugin import ExtendedMock


class SomeClass:
    def do_stuff(self):
        print("Hello World")


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits

    random_string = "".join(random.choices(characters, k=length))

    return random_string


def run_test(my_mock):
    expected_do_stuff = generate_random_string()

    my_mock.do_stuff.setup(return_value=expected_do_stuff)

    # Set up with positional args only
    my_mock.setup("value1", "value2", return_value="result1")

    # Set up with kwargs only
    my_mock.setup(name="test", id=123, return_value="result2")

    # Set up with both args and kwargs
    my_mock.setup("value3", option=True, return_value="result3")

    expected_exception = Exception("whoops")
    my_mock.setup("something_else", return_value=expected_exception)

    # Test exact matches
    assert my_mock("value1", "value2") == "result1"
    assert my_mock(name="test", id=123) == "result2"
    assert my_mock("value3", option=True) == "result3"

    # Different args or kwargs won't match
    assert my_mock("value1", "value2", "extra") is None  # Additional arg
    assert my_mock("value1") is None  # Missing arg
    assert my_mock(name="test") is None  # Missing kwarg
    assert my_mock(generate_random_string()) is None

    assert my_mock.do_stuff() == expected_do_stuff

    # validate the default function is still there
    assert isinstance(my_mock.some_call, MagicMock)

    with pytest.raises(Exception, match="whoops"):
        my_mock("something_else")


def test_magic_mock():
    my_mock = ExtendedMock()

    run_test(my_mock)


def test_object_patch(mocker):
    mocker.patch.object(SomeClass, "do_stuff")
    some_class = SomeClass()

    some_class.do_stuff.setup(return_value="some stuff")

    assert some_class.do_stuff() == "some stuff"


def test_with_extended_mock(mocker):
    my_mock = mocker.patch("tests.SomeClass")

    run_test(my_mock)
