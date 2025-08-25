The following is a design document for Snappylapy, outlining its target audience, guiding principles, and non-functional requirements. It serves as a reference for developers working on the project and helps ensure that the design decisions align with the overall goals of the library.

# Target Audience
The target audience for Snappylapy includes software developers working with mutable data objects, such as those involved in AI or external API endpoint calls. This audience may also include data engineers and data scientists who are writing production-quality code that requires thorough testing.

> This is for the lazy developer that wants to write tests fast and manage them easily.

The developer experience should be good both running tests from a test runner in an IDE and from the command line.

# Guiding Principles of Design
When making design decisions, the following principles should be considered and guide api design, implementation and tone of the outputs and documentation.

1. Snappylapy always allow linters, type checkers and IDEs to provide useful feedback and show documentation. Meaning all public functions should allow ctrl+space completion, type hints and well written docstrings.
2. Snappylapy make all parts of the poject easily extensible and provide examples of how to extend them. When users are extending the project, the principles in point 1 should still apply.
3. Always write tests for all public functions, such that no breaking changes can be made without the tests failing. If a breaking change is made, always update the major version number. (applicable after version 1.0.0)
4. In the snappylapy we always provide examples of how to use the library, and make the examples as simple as possible. The examples should be runnable (included in test suite) and should cover all the main use cases of the library.
5. The Snappylapy public APIs should be expressive and explicit over concise and implicit. This means that the API should be easy to understand and use, even if it is a bit more verbose.
6. Always provide a way to get the raw data, even if it is not the default. This is to allow for more advanced users to use the library in ways that are not directly supported by the library.
7. Snappylapy should be performing well on large data structures. We always tests if code performs well with large inputs (it is okay disabling some features for large inputs, but it should be quick).

# Top 3-Non-Functional Requirements for Snappylapy
1. 🎉 **Enjoyability**: Snappylapy should be fun and easy to use, providing an enjoyable experience and satisfying user experience.
2. 🧩 **Extensibility**: Snappylapy should be easy to extend and should provide examples of how to extend it.
3. 📚 **Usability**: Snappylapy should be well documented and easy to use and should provide many examples of how to use it. It should provide good error messages and helpful messages about actions that can be taken to fix the error. Snappylapy should be easy to learn, just by installing the package. The features should be easy to discover just by exploring the package api from the IDE.
