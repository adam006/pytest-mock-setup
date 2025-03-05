from unittest.mock import MagicMock

import pytest


class SomeClass:
    def do_stuff(self):
        print("Hello World")


def test_with_extended_mock(mocker):
    my_mock = mocker.patch("tests.SomeClass")

    my_mock.do_stuff.setup(return_value="Hello World")

    # Set up with positional args only
    my_mock.setup(args=("value1", "value2"), return_value="result1")

    # Set up with kwargs only
    my_mock.setup(kwargs={"name": "test", "id": 123}, return_value="result2")

    # Set up with both args and kwargs
    my_mock.setup(args=("value3",), kwargs={"option": True}, return_value="result3")

    expected_exception = Exception("whoops")
    my_mock.setup(args=("something_else",), return_value=expected_exception)

    # Test exact matches
    assert my_mock("value1", "value2") == "result1"
    assert my_mock(name="test", id=123) == "result2"
    assert my_mock("value3", option=True) == "result3"

    # Different args or kwargs won't match
    assert my_mock("value1", "value2", "extra") != "result1"  # Additional arg
    assert my_mock("value1") != "result1"  # Missing arg
    assert my_mock(name="test") != "result2"  # Missing kwarg

    assert my_mock.do_stuff() == "Hello World"

    assert isinstance(my_mock.some_call, MagicMock)

    with pytest.raises(Exception, match="whoops"):
        my_mock("something_else")
