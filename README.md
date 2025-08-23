# Snappylapy
   
Welcome to **Snappylapy**, a powerful and intuitive snapshot testing plugin for Python's pytest framework. Snappylapy simplifies the process of capturing and verifying snapshots of your data, ensuring your code behaves as expected across different runs. With Snappylapy, you can save snapshots in a human-readable format and deserialize them for robust integration testing, providing a clear separation layer to help isolate errors and maintain code integrity.  

## Installation
To get started with Snappylapy, install the package via pip, uv or poetry:  

```bash
pip install snappylapy
```

```bash
uv add snappylapy
```

```bash
poetry add snappylapy
```

## Key Features
- **Human-Readable Snapshots**: Save snapshots in a format that's easy to read and understand, making it simpler to review changes and debug issues.  
- **Serialization and Deserialization**: Snapshots can be serialized and deserialized, allowing for flexible and reusable test cases.  
- **Easy to Use**: Seamlessly integrates with pytest, enabling you to capture and verify snapshots with minimal setup. The fully typed fixtures and rich editor support provide intuitive code completion and guidance, making your workflow faster and more productive.
- **Customizable Output**: Store snapshots in a location (static or dynamic) of your choice, enabling you to organize and manage your test data effectively.
- **Editor Integration**: Can show a diff comparison in VS code when a snapshot test fails, for easy comparison between test results and snapshots.

## Benefits of Snapshot Testing
Snapshot testing is a powerful technique for verifying the output of your code by comparing it to a stored snapshot. This approach offers several benefits, including:

- Immutability Verification: Quickly detect unintended changes or regressions by comparing current output to stored snapshots.
- Faster Test Creation: Simplify the process of writing and maintaining tests by capturing snapshots once and letting the framework handle comparisons.
- Documentation: Use snapshots as a form of documentation, providing a clear record of expected output and behavior.
- Version Control Integration: Include snapshots in your version control system to aid in code reviews and track changes over time.
- Pull Request Reviews: Enhance PR reviews by showing exactly how changes affect the application's output, ensuring thorough and effective evaluations.
   
## Why Snappylapy?  
   
When working on a test suite for a project, it’s important to ensure tests are independent. This is to avoid situations where changes in one part of the code cause failures in tests for other unrelated areas, making it challenging to isolate and fix errors. Snappylapy addresses this by providing a mechanism to capture snapshots of your data and use them in your later tests, ensuring that each component can be tested independently. While also making sure that they are dependent enought to test the integration between them. It provides serialization and deserialization of the snapshots, making it easy to reuse them in different test cases. This is aimed at function working with large and complex data structures (dataframes or large nested dictionaries.)
   
### Example  
   
```python
from snappylapy import Expect
from mypackage import my_function
   
def test_snapshot_dict(expect: Expect):
    """Test snapshot with dictionary data."""
    data: dict = my_function()
    expect(data).to_match_snapshot()
    # or expect.dict(data).to_match_snapshot()
```

In this example, `snappylapy` captures the output of `my_function` and compares it against a stored snapshot. If the output changes unexpectedly, pytest will flag the test, allowing you to review the differences and ensure your code behaves as expected.

Snappylapy can use the snapshots created for inputs in another test. You can think of it as automated/easier mock data generation and management.
```python
import pytest
from snappylapy import Expect, LoadSnapshot

def test_snapshot_dict(expect: Expect):
    """Test snapshot with dictionary data."""
    expect({
        "name": "John Doe",
        "age": 31
    }).to_match_snapshot()

@pytest.mark.snappylapy(depends=[test_snapshot_dict])
def test_load_snapshot_from_file(load_snapshot: LoadSnapshot):
    """Test loading snapshot data created in test_snapshot_dict from a file using the deserializer."""
    data = load_snapshot.dict()
    # Normally you would use the data as an input for some other function
    # For demonstration, we will just assert the data matches the expected snapshot
    assert data == {"name": "John Doe", "age": 31}
```

This can be great for external dependencies, for example an AI service, that might change response over time. With this approach we can isolate the changes to the service and still make succeding tests pass.

## The output structure

The results is split into two folders, for ease of comparison, and for handling stochastic/variable outputs (timestamps, generated ids, llm outputs, third party api responses etc).

- __test_results__: Updated every time the tests is ran. Compare with snapshots when doing snapshot style assertions. Add this to your .gitignore file.
- __snapshots__: Updated only when --snapshot-update flag is used when running the test suite. Commit this to your version control system.

## Usage
Snapshots can be updated when running pytest:

```bash
pytest --snapshot-update
```

Alternatively, you can use the CLI command to update snapshots:

```bash
snappylapy update
```

## Fixtures and roadmap
Registers pytest fixtures:
- expect
- load_snapshot

Supported data types
- ✅ .txt - if you provide a string
- ✅ .json - for all other objects
- ✅ custom (decode the data yourself and provide a file extension)

### Supported data types to snapshot test
Snappylapy uses jsonpickle to serialize into json, this means that it can handle almost any Python object out of the box, including:

- Built-in types: str, int, float, bool, None
- Collections: list, tuple, set, dict
- NumPy arrays and pandas DataFrames (with optional dependencies)
- Custom classes (with jsonpickle support)

It is also possible to serialize objects yourself and provide them as a string or bytes data. Then it will be stored and loaded as-is. This means that with snappylapy it is possible to serialize and deserialize any Python object, even those not natively supported.

Snappylapy is your go-to tool for efficient and reliable snapshot testing in Python. By maintaining clear boundaries between different parts of your code, Snappylapy helps you isolate errors, streamline debugging, and ensure your code remains robust and maintainable.

## Contributing
We welcome contributions to Snappylapy! If you have ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request on our GitHub repository. We appreciate your feedback and support in making Snappylapy even better for the community.
