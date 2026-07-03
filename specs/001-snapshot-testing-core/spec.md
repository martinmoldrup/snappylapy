# Feature Specification: Snapshot Testing for Python Pytest

**Feature Branch**: `<<developed_without_speckit>>`  
**Created**: October 16, 2025  
**Status**: Implemented (Documentation)
**Input**: User description: "Document existing snapshot testing capabilities in snappylapy"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and Verify Snapshots (Priority: P1)

As a developer writing tests, I want to capture the output of my functions as snapshots and automatically compare them against future test runs, so I can detect unintended changes in my code's behavior without manually writing assertions.

**Why this priority**: Snapshot testing is some of the core functionality of the library, and it informed the name "snappylapy".

**Independent Test**: Can be fully tested by writing a test that calls `expect(data).to_match_snapshot()`, running it to create the initial snapshot, and verifying that subsequent runs pass when data is unchanged and fail when data changes.

**Acceptance Scenarios**:

1. **Given** I have a function that returns a dictionary, **When** I call `expect(my_dict).to_match_snapshot()` in my test, **Then** the snapshot file is created in the `__snapshots__` directory with a human-readable format
2. **Given** a snapshot file exists from a previous test run, **When** I run the test again with unchanged output, **Then** the test passes
3. **Given** a snapshot file exists, **When** I run the test with modified output, **Then** the test fails and shows the differences between expected and actual values
4. **Given** I want to update snapshots after intentional changes, **When** I run tests with the `--snapshot-update` flag, **Then** all snapshot files are updated with the latest test results

---

### User Story 2 - Support Multiple Data Types (Priority: P1)

As a developer, I want to snapshot test different types of data (dictionaries, lists, strings, bytes, DataFrames, custom objects), so I can verify outputs regardless of their format.

**Why this priority**: Different functions return different data types. Without broad type support, the library would only work for specific use cases.

**Independent Test**: Can be tested independently by creating tests for each data type (dict, list, string, bytes, DataFrame, custom object) and verifying each creates appropriate snapshot files with correct serialization.

**Acceptance Scenarios**:

1. **Given** I have a function returning a dictionary, **When** I use `expect.dict(data).to_match_snapshot()` or `expect(data).to_match_snapshot()`, **Then** a JSON snapshot file is created with `.dict.json` extension
2. **Given** I have a function returning a list, **When** I use `expect.list(data).to_match_snapshot()` or `expect(data).to_match_snapshot()`, **Then** a JSON snapshot file is created with `.list.json` extension
3. **Given** I have a function returning a string, **When** I use `expect.string(data).to_match_snapshot()` or `expect(data).to_match_snapshot()`, **Then** a text snapshot file is created with `.string.txt` extension
4. **Given** I have a function returning bytes, **When** I use `expect.bytes(data).to_match_snapshot()` or `expect(data).to_match_snapshot()`, **Then** a snapshot file is created with `.bytes.txt` extension
5. **Given** I have a pandas DataFrame, **When** I use `expect.dataframe(df).to_match_snapshot()` or `expect(df).to_match_snapshot()`, **Then** a CSV snapshot file is created with `.dataframe.csv` extension
6. **Given** I have a custom Python object, **When** I use `expect.object(obj).to_match_snapshot()` or `expect(obj).to_match_snapshot()`, **Then** a JSON snapshot file is created using jsonpickle serialization with `.object.json` extension

---

### User Story 3 - Reuse Snapshots Across Tests (Priority: P2)

As a developer writing integration tests, I want to load snapshot data from one test and use it as input for another test, so I can create test chains that isolate failures without manually managing test data files.

**Why this priority**: This enables decoupled integration testing, which is a key differentiator for this library. It allows testing complex workflows without creating brittle dependencies.

**Independent Test**: Can be tested by creating two tests - one that saves a snapshot, another marked with `@pytest.mark.snappylapy(depends=[first_test])` that loads the snapshot using `load_snapshot.dict()` and verifies the data is correctly deserialized.

**Acceptance Scenarios**:

1. **Given** I have a test that creates a snapshot, **When** I create another test marked with `@pytest.mark.snappylapy(depends=[first_test])`, **Then** the dependent test runs after the first test
2. **Given** a dependent test is marked with `depends=[first_test]`, **When** I use the `load_snapshot` fixture, **Then** I can load the snapshot created by the first test
3. **Given** I call `load_snapshot.dict()`, **When** the previous test created a dictionary snapshot, **Then** I receive the deserialized dictionary object
4. **Given** I call `load_snapshot.list()`, **When** the previous test created a list snapshot, **Then** I receive the deserialized list object
5. **Given** I call `load_snapshot.string()`, **When** the previous test created a string snapshot, **Then** I receive the string value
6. **Given** I call `load_snapshot.bytes()`, **When** the previous test created a bytes snapshot, **Then** I receive the bytes value
7. **Given** I call `load_snapshot.dataframe()`, **When** the previous test created a DataFrame snapshot, **Then** I receive the deserialized pandas DataFrame

---

### User Story 4 - Organize Snapshots by Test (Priority: P2)

As a developer, I want snapshots to be automatically organized and named based on my test file and function names, so I can easily find and review snapshots without managing file naming myself.

**Why this priority**: Good organization is essential for maintainability as projects grow. Without this, snapshot files would be difficult to manage and review.

**Independent Test**: Can be tested by creating tests in different files and with different function names, then verifying the snapshot files are created with the correct naming pattern in the appropriate directory structure.

**Acceptance Scenarios**:

1. **Given** I have a test file named `test_my_feature.py` with a test function `test_my_scenario`, **When** I create a snapshot, **Then** the snapshot is saved as `[test_my_feature][test_my_scenario].<type>.<ext>` in the `__snapshots__` directory
2. **Given** I create a snapshot with a custom name, **When** I call `expect(data, name="custom_name").to_match_snapshot()`, **Then** the snapshot file includes the custom name: `[test_file][test_function][custom_name].<type>.<ext>`
3. **Given** I have parametrized tests, **When** each test variant creates a snapshot, **Then** each snapshot includes the parameter value in its filename
4. **Given** I use custom output directories via `@pytest.mark.snappylapy(output_dir="custom_dir")`, **When** I create snapshots, **Then** they are saved to the specified directory

---

### User Story 5 - Compare and Update Snapshots (Priority: P2)

As a developer, I want to easily see what changed in my snapshots and update them when changes are intentional, so I can review changes before accepting them into my test baseline.

**Why this priority**: Reviewing snapshot changes is critical for catching bugs. Developers need tools to understand what changed and decide whether to accept those changes.

**Independent Test**: Can be tested by making a change to test output, running `snappylapy diff` to verify diffs are shown, and running `snappylapy update` to verify snapshots are updated without re-running tests.

**Acceptance Scenarios**:

1. **Given** my test output has changed, **When** I run `snappylapy diff`, **Then** a visual diff is opened in my editor (VS Code) showing the differences between test results and snapshots
2. **Given** I have reviewed the changes and want to accept them, **When** I run `snappylapy update`, **Then** all snapshot files are updated to match the current test results without re-running tests
3. **Given** I want to update snapshots during test execution, **When** I run `pytest --snapshot-update`, **Then** tests run and all snapshots are updated automatically
4. **Given** some snapshots have changed and others haven't, **When** I run `snappylapy update`, **Then** only the changed snapshots are updated and I'm informed of the count
5. **Given** I run `snappylapy diff` when no snapshots have changed, **When** all snapshots match test results, **Then** I'm informed that no files have changed and no diffs are opened

---

### User Story 6 - Initialize and Clean Up (Priority: P3)

As a developer, I want to easily set up my project for snapshot testing and clean up test artifacts, so I can maintain a clean repository and proper version control practices.

**Why this priority**: While important for usability, this is supporting functionality. The core testing features are more critical.

**Independent Test**: Can be tested by running `snappylapy init` in a fresh repository and verifying `.gitignore` is updated, and running `snappylapy clear` to verify all snapshot directories are removed.

**Acceptance Scenarios**:

1. **Given** I'm setting up snappylapy in my project, **When** I run `snappylapy init`, **Then** `__test_results__/` is added to my `.gitignore` file
2. **Given** `.gitignore` already contains `__test_results__/`, **When** I run `snappylapy init`, **Then** I'm informed it's already configured and no duplicate entry is added
3. **Given** I want to remove all snapshot files, **When** I run `snappylapy clear`, **Then** I'm prompted to confirm deletion with a list of files that will be deleted
4. **Given** I'm certain I want to delete snapshots, **When** I run `snappylapy clear --force`, **Then** all `__snapshots__` and `__test_results__` directories are deleted without confirmation
5. **Given** I have no snapshot files, **When** I run `snappylapy clear`, **Then** I'm informed there are no files to delete

---

### User Story 7 - Parametrized Test Support (Priority: P3)

As a developer using parametrized tests, I want to create separate snapshots for each test parameter combination, so I can verify behavior across multiple input scenarios.

**Why this priority**: Parametrized tests are a common pattern, but this is an enhancement rather than core functionality.

**Independent Test**: Can be tested by creating a parametrized test with `@pytest.mark.snappylapy(foreach_folder_in="test_data")` and verifying separate snapshots are created for each parameter.

**Acceptance Scenarios**:

1. **Given** I mark a test with `@pytest.mark.snappylapy(foreach_folder_in="test_data")`, **When** the test runs, **Then** it's parametrized with one instance per subdirectory in the specified folder
2. **Given** a parametrized test creates snapshots, **When** each parameter variant runs, **Then** snapshots are stored in separate directories corresponding to each parameter value
3. **Given** a test depends on a parametrized test, **When** the dependent test runs, **Then** it's automatically parametrized to match the source test's parameters

---

### User Story 8 - AI Coding Assistant Integration (Priority: P3)

As a developer using AI coding assistants (GitHub Copilot, Cursor, Claude), I want snappylapy commands available as tasks, so I can manage snapshots without leaving my coding environment.

**Why this priority**: Nice-to-have developer experience enhancement. The CLI already provides all functionality.

**Independent Test**: Can be tested by running `toolit create-vscode-tasks-json` and verifying VS Code tasks are created that expose snappylapy commands to AI assistants.

**Acceptance Scenarios**:

1. **Given** I want to integrate with VS Code tasks, **When** I run `toolit create-vscode-tasks-json`, **Then** a `tasks.json` file is created with snappylapy commands exposed as tasks
2. **Given** tasks are registered, **When** I use an AI coding assistant, **Then** the assistant can execute snappylapy commands (init, update, clear, diff) on my behalf

---

### Edge Cases

- What happens when a snapshot file is manually modified or corrupted? System should detect the mismatch and fail the test with a clear error.
- What happens when tests are renamed or moved? Old snapshots will not be found; developers must manually rename snapshot files or recreate them.
- What happens when running tests in parallel? Each test should have isolated snapshot files based on test names, preventing conflicts.
- What happens when custom objects contain non-serializable data (file handles, network connections)? jsonpickle will attempt to serialize; if it fails, an error should be raised with guidance.
- What happens when loading a snapshot from a test that hasn't run yet? An error should be raised indicating the dependency test needs to run first.
- What happens when snapshot file extensions don't match the loader method used? An error may occur during deserialization; users should ensure loader method matches the snapshot type.
- What happens when pandas is not installed but DataFrame snapshot is attempted? A clear error message should indicate pandas is an optional dependency.
- What happens on Windows vs Linux regarding file paths and line endings? CSV serialization should be consistent across platforms; paths should use platform-agnostic handling.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a pytest fixture named `expect` that accepts various data types and creates snapshot files
- **FR-002**: System MUST support snapshot testing for dictionaries, lists, strings, bytes, pandas DataFrames, and custom objects
- **FR-003**: System MUST automatically detect the data type when using `expect(data)` and route to the appropriate serializer
- **FR-004**: System MUST allow explicit type specification via `expect.dict()`, `expect.list()`, `expect.string()`, `expect.bytes()`, `expect.dataframe()`, `expect.object()`
- **FR-005**: System MUST serialize dictionaries and lists to JSON format using jsonpickle
- **FR-006**: System MUST serialize strings to plain text files
- **FR-007**: System MUST serialize bytes to binary text files
- **FR-008**: System MUST serialize pandas DataFrames to CSV format
- **FR-009**: System MUST serialize custom objects to JSON using jsonpickle
- **FR-010**: System MUST store snapshots in a `__snapshots__` directory adjacent to test files
- **FR-011**: System MUST store test results in a `__test_results__` directory adjacent to test files
- **FR-012**: System MUST name snapshot files using the pattern `[test_filename][test_function_name][optional_custom_name].<type>.<extension>`
- **FR-013**: System MUST compare test results against existing snapshots during test execution
- **FR-014**: System MUST fail tests when test results differ from snapshots
- **FR-015**: System MUST provide clear diff output when snapshots don't match test results
- **FR-016**: System MUST update snapshot files when tests run with `--snapshot-update` flag
- **FR-017**: System MUST provide a `load_snapshot` fixture that loads previously created snapshots
- **FR-018**: System MUST provide loader methods for each data type: `load_snapshot.dict()`, `load_snapshot.list()`, `load_snapshot.string()`, `load_snapshot.bytes()`, `load_snapshot.dataframe()`
- **FR-019**: System MUST support test dependencies via `@pytest.mark.snappylapy(depends=[test_function])`
- **FR-020**: System MUST execute dependent tests after their dependency tests
- **FR-021**: System MUST allow dependent tests to load snapshots from their dependency tests
- **FR-022**: System MUST support parametrized tests via `@pytest.mark.snappylapy(foreach_folder_in="directory")`
- **FR-023**: System MUST create separate snapshots for each parametrized test variant
- **FR-024**: System MUST support custom output directories via `@pytest.mark.snappylapy(output_dir="path")`
- **FR-025**: System MUST provide a CLI command `snappylapy init` that adds `__test_results__/` to `.gitignore`
- **FR-026**: System MUST provide a CLI command `snappylapy update` that updates snapshot files without re-running tests
- **FR-027**: System MUST provide a CLI command `snappylapy clear` that removes all snapshot directories
- **FR-028**: System MUST provide a CLI command `snappylapy diff` that opens visual diffs in VS Code
- **FR-029**: System MUST provide a `--force` flag for `snappylapy clear` to skip confirmation prompts
- **FR-030**: System MUST delete test results directory files before running tests to ensure clean state
- **FR-031**: System MUST preserve snapshot files across test runs unless explicitly updated
- **FR-032**: System MUST be compatible with Python 3.10, 3.11, 3.12, 3.13, and 3.14
- **FR-033**: System MUST work on Windows, Linux, and macOS operating systems
- **FR-034**: System MUST provide type hints for all public APIs to enable IDE autocomplete
- **FR-035**: System MUST integrate with toolit to expose commands as VS Code tasks for AI assistants
- **FR-036**: System MUST handle large data structures efficiently without consuming excessive memory
- **FR-037**: System MUST provide human-readable snapshot formats suitable for code review
- **FR-038**: System MUST ensure cross-platform consistency in serialization (consistent line endings, path separators)

### Key Entities

- **Snapshot**: A stored representation of test output, saved as a file in `__snapshots__` directory with specific naming conventions and format based on data type
- **Test Result**: The current output of a test execution, stored temporarily in `__test_results__` directory for comparison with snapshots
- **Expect Fixture**: A pytest fixture that provides methods to create and verify snapshots for different data types
- **LoadSnapshot Fixture**: A pytest fixture that provides methods to load and deserialize snapshots from previous tests
- **Serializer**: A component that converts Python objects to file-storable formats (JSON, CSV, text) and deserializes them back
- **Snapshot Session**: A session-scoped object that manages snapshot state across all tests in a test run
- **Settings**: Configuration object that holds test metadata (filename, function name, directories, update mode)
- **Test Dependency**: A relationship between tests defined via pytest markers indicating one test depends on another's snapshot output

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can create a snapshot test in under 1 minute by adding a single line: `expect(data).to_match_snapshot()`
- **SC-002**: Snapshot files are human-readable and suitable for code review in pull requests
- **SC-003**: System correctly identifies snapshot mismatches and displays differences in test output
- **SC-004**: Developers can update all changed snapshots across an entire test suite with a single command (`snappylapy update` or `pytest --snapshot-update`)
- **SC-005**: System supports test suites with hundreds of snapshot files without performance degradation
- **SC-006**: Dependent tests correctly load snapshot data from previous tests 100% of the time when dependencies are properly configured
- **SC-007**: System works identically on Windows, Linux, and macOS with consistent snapshot file formats
- **SC-008**: 95% of common Python data types (dict, list, str, bytes, custom objects) can be snapshot tested without custom configuration
- **SC-009**: DataFrame snapshots with pandas are serialized to CSV format that is human-readable
- **SC-010**: Developers can review snapshot changes in VS Code diff view using `snappylapy diff` command
- **SC-011**: Test results directory (`__test_results__`) is automatically excluded from version control after running `snappylapy init`
- **SC-012**: All public APIs have complete type hints enabling full IDE autocomplete support
- **SC-013**: Snapshot test failures provide clear indication of what changed and where
- **SC-014**: System handles parametrized tests by creating one snapshot per parameter combination
- **SC-015**: AI coding assistants can execute snappylapy commands when integrated via toolit

