from unittest.mock import ANY

import pytest

from pytest_extended_mock import ExtendedMock


class Service:
    def fetch(self, ids):
        pass


@pytest.mark.parametrize(
    ("args", "kwargs"),
    [
        (("value1", "value2"), {}),
        ((), {"name": "test", "id": 123}),
        (("value3",), {"option": True}),
        (([1, 2],), {"filters": {"active": True}}),
    ],
)
def test_setup_returns_value_for_matching_call(args, kwargs):
    mock = ExtendedMock()
    mock.setup("other", return_value="other result")
    mock.setup(*args, return_value="result", **kwargs)

    assert mock(*args, **kwargs) == "result"


def test_setup_matches_any():
    mock = ExtendedMock()
    mock.setup(ANY, option=True, return_value="result")

    assert mock("anything", option=True) == "result"


def test_latest_setup_wins():
    mock = ExtendedMock()
    mock.setup("value", return_value="first")
    mock.setup("value", return_value="second")

    assert mock("value") == "second"


@pytest.mark.parametrize(
    ("args", "kwargs"),
    [
        (("value1", "value2", "extra"), {}),
        (("value1",), {}),
        (("value1", "value2"), {"option": True}),
    ],
)
def test_unmatched_call_returns_return_value(args, kwargs):
    mock = ExtendedMock()
    mock.return_value = "default"
    mock.setup("value1", "value2", return_value="result")

    assert mock(*args, **kwargs) == "default"


def test_unmatched_call_without_return_value_returns_child_mock():
    mock = ExtendedMock()
    mock.setup("value", return_value="result")

    assert mock("other") is mock.return_value


@pytest.mark.parametrize("exception", [ValueError, ValueError("whoops")])
def test_setup_raises(exception):
    mock = ExtendedMock()
    mock.setup("value", raises=exception)

    with pytest.raises(ValueError):
        mock("value")


def test_setup_returns_exception_given_as_return_value():
    expected = ValueError("whoops")
    mock = ExtendedMock()
    mock.setup("value", return_value=expected)

    assert mock("value") is expected


def test_matched_calls_are_recorded():
    mock = ExtendedMock()
    mock.setup("value", return_value="result")

    mock("value")
    mock("other")

    assert mock.call_count == 2
    mock.assert_any_call("value")
    mock.assert_called_with("other")


def test_child_mock_supports_setup():
    mock = ExtendedMock()
    mock.service.fetch.setup([1], return_value="result")

    assert mock.service.fetch([1]) == "result"


def test_patch_with_spec_set(mocker):
    fetch = mocker.patch.object(Service, "fetch", new_callable=ExtendedMock, spec_set=True)
    fetch.setup([1], return_value="result")

    assert Service().fetch([1]) == "result"
