<div align="center">
<img src="https://raw.githubusercontent.com/martinmoldrup/snappylapy/refs/heads/main/docs/snappylapy-logo.svg" alt="Snappylapy Logo" style="width:200px;"/>

<h1> Snappylapy</h1>
<h3>Pytest Plugin for Snapshot Testing</h3>
</div>
<p align="center">
<strong>
Effortlessly capture, diff, and reuse complex, non-deterministic, and AI-generated data structures for reliable and fast pytest runs — ideal for data engineering and machine learning workflows.
</strong>
</p>
<!-- Badges -->
<p align="center">
    <a href="https://github.com/martinmoldrup/snappylapy/blob/main/CHANGELOG.md"><img src="https://img.shields.io/badge/status-beta-yellow" alt="Beta Status"/></a>
    <a href="https://github.com/martinmoldrup/snappylapy/blob/main/LICENSE"><img src="https://img.shields.io/github/license/martinmoldrup/snappylapy" alt="License"/></a>
    <a href="https://martinmoldrup.github.io/snappylapy/"><img src="https://img.shields.io/badge/docs-MkDocs-blue" alt="Documentation"/></a>
    <a href="https://github.com/martinmoldrup/snappylapy/blob/main/CHANGELOG.md"><img src="https://img.shields.io/github/v/tag/martinmoldrup/snappylapy?label=version&logo=github&color=purple" alt="Version"/></a>
    <br/>
    <!-- Quality Assurance steps. Note the success of these steps is enforced in the CI pipeline. -->
    <a href="https://github.com/martinmoldrup/snappylapy/actions/workflows/continuous_integration.yaml"><img src="https://img.shields.io/badge/type%20check-mypy-success?logo=python" alt="mypy"/></a>
    <a href="https://github.com/martinmoldrup/snappylapy/actions/workflows/continuous_integration.yaml"><img src="https://img.shields.io/badge/lint-ruff-success?logo=ruff" alt="ruff"/></a>
    <a href="https://github.com/martinmoldrup/snappylapy/actions/workflows/continuous_integration.yaml"><img src="https://img.shields.io/badge/tested%20with-pytest-success?logo=pytest" alt="pytest"/></a>
    <a href="https://github.com/martinmoldrup/snappylapy/blob/main/pyproject.toml"><img src="https://img.shields.io/badge/package%20manager-uv-success?logo=uv" alt="uv"/></a>
    <a href="https://github.com/martinmoldrup/toolit"><img src="https://img.shields.io/badge/command%20runner-toolit-success" alt="toolit"/></a>
</p>

---

Welcome to **Snappylapy**, a powerful and intuitive snapshot testing plugin for Python's pytest framework. Snappylapy simplifies the process of capturing and verifying snapshots of your data, ensuring your code behaves as expected across different test case runs. With Snappylapy, you can save snapshots in a human-readable format and deserialize them for robust integration testing, providing a clear separation layer to help isolate errors and maintain code integrity. 

Snappylapy is following the api-style of the very popular Jest testing framework, making it familiar and easy to use for JavaScript developers.

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
- **AI Coding Agent Integration**: Snappylapy integrates its commands with AI coding agents such as GitHub Copilot, Cursor, and Claude Code.

## Benefits of Snapshot Testing
Snapshot testing is a powerful technique for verifying the output of your code by comparing it to a stored snapshot. This approach offers several benefits, including:

- Immutability Verification: Quickly detect unintended changes or regressions by comparing current output to stored snapshots.
- Faster Test Creation: Simplify the process of writing and maintaining tests by capturing snapshots once and letting the framework handle comparisons.
- Documentation: Use snapshots as a form of documentation, providing a clear record of expected output and behavior.
- Version Control Integration: Include snapshots in your version control system to aid in code reviews and track changes over time.
- Pull Request Reviews: Enhance PR reviews by showing exactly how changes affect the application's output, ensuring thorough and effective evaluations.
   
## Why Snappylapy?  
   
When working on a test suite for a project, it’s important to ensure tests are independent. This is to avoid situations where changes in one part of the code cause failures in tests for other unrelated areas, making it challenging to isolate and fix errors. Snappylapy addresses this by providing a mechanism to capture snapshots of your data and use them in your later tests, ensuring that each component can be tested independently. While also making sure that they are dependent enough to test the integration between them. It provides serialization and deserialization of the snapshots, making it easy to reuse them in different test cases. This is aimed at function working with large and complex data structures (dataframes or large nested dictionaries.)
   
### Example - Basic Snapshot Test

`test_expect_snapshot_dict.py`
```python
from snappylapy import Expect

def generate_dict(size: int) -> dict[str, int]:
    """Function to test."""
    return {f"key_{i}": i for i in range(size)}

def test_snapshot_dict(expect: Expect):
    """Test snapshot with dictionary data."""
    data: dict = generate_dict(100)
    expect(data).to_match_snapshot()
    # or expect.dict(data).to_match_snapshot()
```

In this example, `snappylapy` captures the output of `my_function` and compares it against a stored snapshot. If the output changes unexpectedly, pytest will flag the test, allowing you to review the differences and ensure your code behaves as expected.

### Example - Loading Snapshots for Integration Testing
Snappylapy can use the snapshots created for inputs in another test. You can think of it as automated/easier mock data generation and management.

`test_expect_and_loadsnapshot.py`
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

This can be great for external dependencies, for example an AI service, that might change response over time.

Snapshot testing with Snappylapy helps keep unit tests independent. By capturing and loading snapshots of test data, each test checks only its own behavior and does not rely on the results of other tests. This means that if one test fails, it won’t cause unrelated tests to fail, making it easier to find and fix problems quickly.

### Example - Custom Snapshot Location
In snappylapy, you can customize the output directory for your snapshots. This is useful for organizing your test data or separating snapshots for different test suites.

`test_expect_snapshot_custom_dir.py`
```python
import pytest
from snappylapy import Expect

@pytest.mark.snappylapy(output_dir="custom_dir")
def test_snapshot_with_custom_directories(expect: Expect):
    """Test snapshot with custom directories."""
    expect.string("Hello World").to_match_snapshot()
```
In this example, the snapshot for the test will be stored in the `custom_dir` directory instead of the default root directory location. This allows you to organize your snapshots based on your project's structure or testing needs.

```
custom_dir
    __snapshots__
        [test_expect_snapshot_custom_dir][test_snapshot_with_custom_directories].string.txt
    __test_results__
        [test_expect_snapshot_custom_dir][test_snapshot_with_custom_directories].string.txt
```

### Example - Multiple Snapshot Folders
A common use case is to have multiple test case folders, each with their own input data. Snappylapy can handle this with ease using the `foreach_folder_in` parameter.

`test_data` example folder structure
```
test_cases
    case1
        input.json
    case2
        input.json
    ...
```
When we add the `foreach_folder_in` parameter to the `snappylapy` marker, it will run the test for each folder inside the specified directory, and it will include a `test_directory` fixture to access the current folder being tested.

> Important: You must ensure that the test function has a `test_directory` input parameter of type `pathlib.Path` to access the current test case folder. You cannot use another name for this parameter.

`test_expect_snapshot_multiple_folders.py`
```python
import json
import pytest
import pathlib
from snappylapy import Expect


def transform_data(data: dict) -> dict:
    """A sample transformation function."""
    # Example transformation: add a new key-value pair
    data["transformed"] = True
    return data


@pytest.mark.snappylapy(foreach_folder_in="test_data")
def test_snapshot_parametrized_multiple_test_case_folders(test_directory: pathlib.Path, expect: Expect) -> None:
    """Test snapshot with multiple folders."""
    data = json.loads((test_directory / "input.json").read_text())
    transformed_data = transform_data(data)
    expect.dict(transformed_data).to_match_snapshot()
```

After running the test, snapshots will be created for each folder inside `test_data`, allowing you to manage and compare snapshots for multiple test cases easily.

```
test_cases
    case1
        input.json
        __snapshots__
            [test_expect_snapshot_multiple_folders][test_snapshot_parametrized_multiple_test_case_folders].dict.json
    case2
        input.json
        __snapshots__
            [test_expect_snapshot_multiple_folders][test_snapshot_parametrized_multiple_test_case_folders].dict.json
    ...
```

This setup provides a clear and organized way to manage snapshots for multiple test cases, making it easier to maintain and review your test data.

## The output structure

The results is split into two folders, for ease of comparison, and for handling stochastic/variable outputs (timestamps, generated ids, llm outputs, third party api responses etc).

- `__test_results__`: Updated every time the tests is ran. Compare with snapshots when doing snapshot style assertions. Add this to your .gitignore file (this can be done automatically when using the `snappylapy init` command).
- `__snapshots__`: Updated only when `--snapshot-update` flag is used when running the test suite, or using the `snappylapy update` command. Commit this to your version control system.

When you perform partial matches against snapshots, any changes in your test outputs are saved to the `__test_results__` folder. This means you can review differences between your current test results and the stored snapshots in `__snapshots__` without modifying your baseline snapshots. As a result, you can easily track changes and debug issues, while keeping your reference snapshots unchanged until you intentionally update them. It is easy to compare the two files using a diff tool or your code editor's built-in comparison features.

## Usage
Snapshots can be updated when running pytest:

```bash
pytest --snapshot-update
```

Alternatively, you can use the CLI command to update snapshots:

```bash
snappylapy update
```

### Pytest Fixtures
Registers pytest fixtures:
- `expect`: A fixture that provides methods to create snapshot expectations for various data types (e.g., dict, list, string, bytes, DataFrame).
- `load_snapshot`: A fixture that loads snapshot data from a file.


### Supported data types to snapshot test
Snappylapy uses jsonpickle to serialize into json, this means that it can handle almost any Python object out of the box, including:

- Built-in types: str, int, float, bool, None
- Collections: list, tuple, set, dict
- NumPy arrays and pandas DataFrames (with optional dependencies)
- Custom classes (with jsonpickle support)

It is also possible to serialize objects yourself and provide them as a string or bytes data. Then it will be stored and loaded as-is. This means that with snappylapy it is possible to serialize and deserialize any Python object, even those not natively supported.

Supported output file formats:
- ✅ .txt - if you provide a string
- ✅ .json - for all other objects
- ✅ .csv - for pandas DataFrames
- ✅ custom (decode the data yourself and provide a file extension)

### Tasks for VSCode integration (available for github copilot agents)
Snappylapy can make its CLI commands available for AI coding agents like GitHub Copilot, Cursor and Claude Code. 

One example of how to do this is by registering tasks in VSCode. We use toolit, to make the integration seamless. To register the tasks, run the following command:

```bash
toolit create-vscode-tasks-json
```

> WARNING: This will overwrite any existing tasks.json file in the .vscode folder.


## Contributing
We welcome contributions to Snappylapy! If you have ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request on our GitHub repository. We appreciate your feedback and support in making Snappylapy even better for the community.

Snappylapy is your go-to tool for efficient and reliable snapshot testing in Python. By maintaining clear boundaries between different parts of your code, Snappylapy helps you isolate errors, streamline debugging, and ensure your code remains robust and maintainable.
