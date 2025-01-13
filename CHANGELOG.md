# Change log
All notable changes to this project will be documented in this file.

## [0.2.0]
- Better error messages by using pytest assertion rewriting
- Allow users to set the snapshot directory when using the load_snapshot fixture
- Add CLI for for init and clear commands
- Added automated generation of documentation using mkdocs
  
## [0.1.1]
- Update dependencies with the lower bounds of package compatibility
- Refactor to make code easier for users of package to modify and extend

## [0.1.0]
- Added fixture for loading snapshots from previous tests (load_snapshot fixture)
- Added the snappylapy marker for tests that depend on previous tests (pytest.mark.snappylapy). This will be used for more advanced features in the future.

## [0.0.2]
- 🐞 Added fix for python 3.9, by refactoring incompatible type annotation
- Loosened the version requirements for pytest (until the lower bound have been discovered, with automated testing)
- Improved metadata for pypi

## [0.0.1]
- Initial release of Snappylapy
- Implemented basic snapshot testing functionality for dict, list, bytes and str data types