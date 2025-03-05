import pytest
from unittest.mock import MagicMock


class ExtendedMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_data = {}

    def setup(self, args=None, kwargs=None, return_value=None):
        # Default to empty tuple and frozenset
        args = args if args is not None else ()
        kwargs = kwargs if kwargs is not None else {}
        frozen_kwargs = frozenset(kwargs.items()) if kwargs else frozenset()

        # Store the configuration
        key = (args, frozen_kwargs)
        self._setup_data[key] = return_value

        return self

    def __call__(self, *args, **kwargs):
        # Check if we have a specific setup for these arguments
        frozen_kwargs = frozenset(kwargs.items()) if kwargs else frozenset()
        exact_key = (args, frozen_kwargs)

        # If we have a specific setup, return that
        if exact_key in self._setup_data:
            value = self._setup_data[exact_key]
            if isinstance(value, Exception):
                raise value
            return value

        # Otherwise, fall back to default MagicMock behavior
        return super().__call__(*args, **kwargs)


def pytest_configure(config):
    # Replace MagicMock with our ExtendedMock
    import unittest.mock

    unittest.mock.MagicMock = ExtendedMock

