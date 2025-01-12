

--8<-- "README.md"

## Design Decisions
### Why not match automatically based on the type of the value?
**Why require the user to provide the type when using expect fixture (e.g. expect.string("Hello world")), instead of inferring it from the value type (e.g. expect('Hello world'))?**

This is done for better code editor code completions and better type checking. When using ctrl+space in the code editor, the user will see the available options and documentation for the type. Even though it is bit more verbose, it is more explicit and and allows for a better developer experience.

