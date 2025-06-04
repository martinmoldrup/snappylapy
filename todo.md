Markdown Checkbox VSCode Extension
- ctl+shift+enter to toggle checkbox

# Todo
- [ ] Improve api so that expect can be used directly which seems more natural
- [ ] Update README.md with example of how to use the parametization functionality
- [ ] Do a significant boost in testing both manually and adding automated tests
- [ ] Update README.md such that todo items is shown here instead of in the README.md
- [ ] Add removal command of ophaned snapshots to snappylapy cli
- [ ] Raise an useful error if it fixture was never used (to avoid certain types of errors (a loop over an iterator with no elements, etc))
- [ ] Raise an useful error if we write to the same snapshot file multiple times in the same testing
- [ ] Add information to the print log about what custom name the snapshot failed on (when loading a list of generated snapshots)

# Backlog
- [ ] A diff report in html can be generated with `pytest --snappylapy-html=report.html`

# Done
- [X] ~~*BUG: When using falsy values as name the custom name is not used*~~ [2025-01-29]
- [X] ~~*Add snappylapy parametization functionality to snappylapy and allow it to be loaded in the load_snapshot fixture*~~ [2025-01-19]
- [X] ~~*Make the folder names of __snapshots__ and __test_results__ enforced to be fixed (needed for cleanup and diffing)*~~ [2025-01-19]
- [X] ~~*Change setting of path to only have a single path configurable and update such it is configured through the marker*~~ [2025-01-19]
- [X] ~~*Do reporting showing count of updated, created and deleted snapshots*~~ [2025-01-18]
- [X] ~~*Rename output file names of snapshots to match [filename][testname][name].extention conversion*~~ [2025-01-15]