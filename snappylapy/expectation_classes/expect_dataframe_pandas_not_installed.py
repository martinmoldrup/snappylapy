"""Stub class for when optional dependencies is missing."""


class DummyDataFrame:
    """Dummy type to use as a stand-in for pd.DataFrame in type annotations."""


class PandasNotInstalledStandIn:
    """Raise ImportError on any method call, indicating missing optional dependency."""

    DataFrame = DummyDataFrame
    _error_message = (
        "pandas is required for DataframeExpect but is not installed. Install pandas to use DataframeExpect."
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Allow instantiation; all other accesses raise ImportError."""
        # args and kwargs are unused, but included for compatibility

    def __getattribute__(self, name: str) -> object:
        """Raise ImportError on any attribute/method access except __init__."""
        if name == "__init__":
            return object.__getattribute__(self, name)
        raise ImportError(self._error_message)

    def __call__(self, *args: object, **kwargs: object) -> None:  # noqa: ARG002
        """Raise ImportError when attempting to call the object."""
        raise ImportError(self._error_message)
