# ExtendedMock Pytest Plugin

Welcome to the **ExtendedMock Pytest Plugin**! This plugin enhances Python's `unittest.mock.MagicMock` with additional functionality inspired by the setup and verification patterns found in popular .NET mocking libraries like **Moq**. If you've ever used Moq and loved its fluent API for configuring mock behavior, this plugin will feel like home.

## What is ExtendedMock?

`ExtendedMock` is a drop-in replacement for `unittest.mock.MagicMock` that adds a `setup` method, allowing you to configure mock behavior for specific arguments. This makes it easier to write expressive and precise tests by defining exactly what your mock should return (or raise) when called with certain arguments.

### Key Features:
- **Fluent API**: Configure mock behavior using a clean, chainable `setup` method.
- **Argument-Specific Behavior**: Define return values or exceptions for specific argument combinations.
- **Seamless Integration**: Works out of the box with `pytest` and replaces `MagicMock` automatically.
- **Familiar to .NET Developers**: If you've used Moq, you'll feel right at home with the `setup` method.

---

## Usage

### Basic Example

Here's how you can use `ExtendedMock` in your tests:

```python
from unittest.mock import MagicMock

def test_extended_mock():
    mock = MagicMock()
    
    # Configure the mock to return "Hello, World!" when called with ("foo", bar=42)
    mock.setup("foo", bar=42, return_value="Hello, World!")
    
    # Call the mock with the configured arguments
    result = mock("foo", bar=42)
    
    assert result == "Hello, World!"
```

### Raising Exceptions

You can also configure the mock to raise an exception for specific arguments:

```python
def test_extended_mock_with_exception():
    mock = MagicMock()
    
    # Configure the mock to raise a ValueError when called with ("error",)
    mock.setup("error", return_value=ValueError("Something went wrong!"))
    
    # Call the mock with the configured arguments
    with pytest.raises(ValueError):
        mock("error")
```

### Default Behavior

If the mock is called with arguments that don't match any configured setup, it falls back to the default `MagicMock` behavior:

```python
def test_extended_mock_default_behavior():
    mock = MagicMock()
    
    # No setup configured, so it returns a new MagicMock instance
    result = mock("unconfigured", args=123)
    
    assert isinstance(result, MagicMock)
```

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
mock = MagicMock()
mock.setup("foo", 42, return_value="Hello, World!")
```

---

## How It Works

The `ExtendedMock` class extends `unittest.mock.MagicMock` and adds a `_setup_data` dictionary to store configurations. When the mock is called, it checks if the arguments match any configured setup. If a match is found, it returns the configured value or raises the configured exception. If no match is found, it falls back to the default `MagicMock` behavior.

---

## Contributing

We welcome contributions! If you have ideas for improvements or find a bug, please open an issue or submit a pull request on [GitHub](https://github.com/yourusername/pytest-extendedmock).

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
