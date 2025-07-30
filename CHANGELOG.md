# Change log
All notable changes to this project will be documented in this file.

*NOTE:* Version 0.X.X might have breaking changes in bumps of the minor version number. This is because the project is still in early development and the API is not yet stable. It will still be marked clearly in the release notes.

## [0.5.0] - 2025-07-30
- 🆕 Add new cli command for easy update of snapshots without the need to rerun tests. Added: `snappylapy update` CLI command that will update the snapshots that have changed or create new snapshots.

## [0.4.0] - 2025-06-08
- 🆕 Add support for pandas DataFrame assertions (pandas is an optional dependency, and snappylapy can be used without it)
- 🆕 Add new simpler and more intuitive Expect API. We can use expect() calls and an overload will select the appropriate Expect class based on the type of the input. This is in contrast with expect.dict(), expect.list(), etc. This is not a breaking change, since the old API is still supported.

## [0.3.2] - 2025-04-26
- 🐞 Bug fix of test_directory fixture, not loading correctly depending fixture

## [0.3.1] - 2025-01-29
- 🐞 Fix load_snapshot fixture not loading correctly
- 🐞 Fix wrong naming for cases where custom name is falsy
- Change the ident property of json to make it more human readable 


## [0.3.0] - 2025-01-26
- Add snappylapy parametization functionality to snappylapy and allow it to be loaded in the load_snapshot fixture
- Do reporting showing count of updated, created and deleted snapshots
- **Breaking Changes**
  - Change setting of path to only have a single path configurable and update such it is configured through the marker
  - Make the folder names of __snapshots__ and __test_results__ enforced to be fixed (needed for cleanup and diffing)
  - Rename output file names of snapshots to match [filename][testname][name].extention conversion
## [0.2.1] - 2025-01-13
- Added missing dependency for typer to make the CLI work

## [0.2.0] - 2025-01-13
- Better error messages by using pytest assertion rewriting
- Allow users to set the snapshot directory when using the load_snapshot fixture
- Add CLI for for init and clear commands
- Added automated generation of documentation using mkdocs
  
## [0.1.1] - 2025-01-10
- Update dependencies with the lower bounds of package compatibility
- Refactor to make code easier for users of package to modify and extend

## [0.1.0] - 2025-01-08
- Added fixture for loading snapshots from previous tests (load_snapshot fixture)
- Added the snappylapy marker for tests that depend on previous tests (pytest.mark.snappylapy). This will be used for more advanced features in the future.

## [0.0.2] - 2025-01-07
- 🐞 Added fix for python 3.9, by refactoring incompatible type annotation
- Loosened the version requirements for pytest (until the lower bound have been discovered, with automated testing)
- Improved metadata for pypi

## [0.0.1] - 2025-01-06
- Initial release of Snappylapy
- Implemented basic snapshot testing functionality for dict, list, bytes and str data types