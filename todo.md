Markdown Checkbox VSCode Extension
- ctl+shift+enter to toggle checkbox

# Todo
- [ ] Update README.md with example of how to use the parameterization functionality
- [ ] Do a significant boost in testing both manually and adding automated tests
- [ ] Update README.md such that todo items is shown here instead of in the README.md
- [ ] Add removal command of orphaned snapshots to snappylapy cli
- [ ] Raise a helpful error if a fixture was never used (to avoid certain types of errors (a loop over an iterator with no elements, etc))
- [ ] Raise an useful error if we write to the same snapshot file multiple times in the same testing
- [ ] Add information to the print log about what custom name the snapshot failed on (when loading a list of generated snapshots)
- [ ] Currently the expect() function saves files in the __test_results__ folder. Reconsider this design, for instance when pipeline failed due to permission error. It might create a bad user experience, since the save of files is not core to the functionality.
- [ ] Reconsider deleting the __test_results__ folder when starting a test session.
- [ ] CLI command to update snapshots will also update snapshots not needed, but used for other assertions.

# Backlog
- [ ] - **Provides a wide set of assertions**: The package provides a wide set of assertions to make it easy to compare different types of data, for do fuzzy matching or ignore certain parts of the data that are variable.
- [ ] - **Diff Report Generation**: Generate a diff and results report in html format for easy comparison between test results and snapshots.
   - [ ] A diff report in html can be generated with `pytest --snappylapy-html=report.html`

# Done
- [X] ~~*Make the installation of pandas optional (as it is not needed for the basic functionality)*~~ [2025-07-31]
- [X] ~~*Improve api so that expect can be used directly which seems more natural*~~ [2025-07-31]
- [X] ~~*Add a generic fallback handler for all other datatypes that is not supported today*~~ [2025-08-23]
- [X] ~~*BUG: When using falsy values as name the custom name is not used*~~ [2025-01-29]
- [X] ~~*Add snappylapy parametization functionality to snappylapy and allow it to be loaded in the load_snapshot fixture*~~ [2025-01-19]
- [X] ~~*Make the folder names of __snapshots__ and __test_results__ enforced to be fixed (needed for cleanup and diffing)*~~ [2025-01-19]
- [X] ~~*Change setting of path to only have a single path configurable and update such it is configured through the marker*~~ [2025-01-19]
- [X] ~~*Do reporting showing count of updated, created and deleted snapshots*~~ [2025-01-18]
- [X] ~~*Rename output file names of snapshots to match [filename][testname][name].extention conversion*~~ [2025-01-15]

# Roadmap

Registers fixtures:
- expect ✅
- load_snapshot ✅

Supported data types
- .txt ✅
- .json ✅
- .csv ❌
- .yaml ❌
- .jsonl ❌

Planned data types:

| Python Type         | Default Output file type | Implementation Status     |
|---------------------|--------------------------|---------------------------|
| bytes               | .txt                     | ✅                       |
| pd.DataFrame        | .csv                     | ✅ (missing csv support) |
| pd.Series           | .csv                     | ❌                       |
| np.ndarray          | .csv                     | ❌                       |
| dict                | .json                    | ✅                       |
| list                | .json                    | ✅                       |
| tuple               | .json                    | ❌                       |
| set                 | .json                    | ❌                       |
| str                 | .txt                     | ✅                       |
| int                 | .txt                     | ❌                       |
| float               | .txt                     | ❌                       |
| bool                | .txt                     | ❌                       |
| datetime.datetime   | .txt                     | ❌                       |
| datetime.date       | .txt                     | ❌                       |
| datetime.time       | .txt                     | ❌                       |
| pathlib.Path        | .txt                     | ❌                       |
| decimal.Decimal     | .txt                     | ❌                       |
| uuid.UUID           | .txt                     | ❌                       |
| pydantic.BaseModel  | .json                    | ❌                       |
| python dataclasses  | .json                    | ❌                       |

todo: Update and check how many of these are actually supported with the generic jsonpickle updates.