# ExtendedMock Pytest Plugin

Welcome to the **ExtendedMock Pytest Plugin**! This plugin enhances Python's `unittest.mock.MagicMock` with additional functionality inspired by the setup and verification patterns found in popular .NET mocking libraries like **Moq**. If you've ever used Moq and loved its fluent API for configuring mock behavior, this plugin will feel like home.

## What is ExtendedMock?

`ExtendedMock` is a drop-in replacement for `unittest.mock.MagicMock` that adds a `setup` method, allowing you to configure mock behavior for specific arguments. This makes it easier to write expressive and precise tests by defining exactly what your mock should return (or raise) when called with certain arguments.

### Key Features:
- **Fluent API**: Configure mock behavior using a clean, chainable `setup` method.
- **Argument-Specific Behavior**: Define return values or exceptions for specific argument combinations.
- **Opt-in**: Use `ExtendedMock` where you want it, directly or through `mocker.patch(..., new_callable=ExtendedMock)`. Every other `MagicMock` is left alone.
- **Still a MagicMock**: Calls are recorded, so `assert_called_with` and friends keep working alongside `setup`.
- **Familiar to .NET Developers**: If you've used Moq, you'll feel right at home with the `setup` method.

---

## Usage
### find on pypi [link](https://pypi.org/project/pytest-extended-mock/)
### install
```bash
pip install pytest-extended-mock
```

### Basic Example

Here's how you can use `ExtendedMock` in your tests:

```python
from pytest_extended_mock import ExtendedMock

def test_extended_mock():
    mock = ExtendedMock()
    
    # Configure the mock to return "Hello, World!" when called with ("foo", bar=42)
    mock.setup("foo", bar=42, return_value="Hello, World!")
    
    # Call the mock with the configured arguments
    result = mock("foo", bar=42)
    
    assert result == "Hello, World!"
```

Example with `mocker.patch`
```python
from pytest_extended_mock import ExtendedMock

def test_mocker_patch(mocker):
    mock = mocker.patch("your_path", new_callable=ExtendedMock)

    mock.setup("foo", return_value="bar")

    result = mock("foo")

    assert result == "bar"
```

### Raising Exceptions

You can also configure the mock to raise an exception, given as a class or an instance, for specific arguments:

```python
def test_extended_mock_with_exception():
    mock = ExtendedMock()
    
    # Configure the mock to raise a ValueError when called with ("error",)
    mock.setup("error", raises=ValueError("Something went wrong!"))
    
    # Call the mock with the configured arguments
    with pytest.raises(ValueError):
        mock("error")
```

### Default Behavior

If the mock is called with arguments that don't match any configured setup, it falls back to the default `MagicMock` behavior and returns its `return_value`:

```python
def test_extended_mock_default_behavior():
    mock = ExtendedMock()
    mock.setup("configured", return_value="result")
    mock.return_value = "default"
    
    assert mock("unconfigured", args=123) == "default"
```

### Matchers

Setups are compared with `==`, so arguments don't need to be hashable, and matchers such as `unittest.mock.ANY` work:

```python
from unittest.mock import ANY

def test_extended_mock_any():
    mock = ExtendedMock()
    mock.setup(ANY, [1, 2], return_value="result")
    
    assert mock("anything", [1, 2]) == "result"
```

When more than one setup matches, the most recent one wins.

---

## Why Use ExtendedMock?

If you've ever found yourself writing repetitive code to configure `MagicMock` instances for different argument combinations, `ExtendedMock` is here to save the day. It provides a more expressive and concise way to define mock behavior, making your tests easier to read and maintain.

### For .NET Developers

If you're coming from the .NET world and have used libraries like **Moq**, you'll find the `setup` method very familiar. It mirrors the `Setup` and `Returns` methods in Moq, allowing you to define mock behavior in a similar way. For example:

```csharp
// Moq in .NET
var mock = new Mock<IService>();
mock.Setup(x => x.DoSomething("foo", 42)).Returns("Hello, World!");
```

```python
# ExtendedMock in Python
mock = ExtendedMock()
mock.do_something.setup("foo", 42, return_value="Hello, World!")
```

---

## How It Works

The `ExtendedMock` class extends `unittest.mock.MagicMock`. Each `setup` call stores the expected call and sets the mock's `side_effect` to a function that compares each call against the stored setups. A match returns the configured value or raises the configured exception; anything else falls back to the mock's `return_value`. Because `setup` uses `side_effect`, it replaces any `side_effect` you set yourself. Attributes of an `ExtendedMock` are `ExtendedMock`s too, so `mock.service.fetch.setup(...)` works.

---

## Contributing

We welcome contributions! If you have ideas for improvements or find a bug, please open an issue or submit a pull request on [GitHub](https://github.com/adam006/pytest-mock-setup).

---

## License

This project is licensed under the MIT License.

---

## Keywords

- pytest
- mocking
- unittest
- MagicMock
- Moq
- .NET
- testing
- fluent API
- mock setup

---

Happy testing! 🚀
