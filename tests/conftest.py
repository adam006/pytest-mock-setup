import pytest
from unittest.mock import MagicMock

from src.pytest_extended_mock import ExtendedMock


def pytest_configure(config):
    # Replace MagicMock with our ExtendedMock
    import unittest.mock

    unittest.mock.MagicMock = ExtendedMock

