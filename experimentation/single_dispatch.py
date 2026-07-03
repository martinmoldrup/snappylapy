"""
We might want to use the single dispatch, to make it easier to use the API.

I would like the user to be able to avoid specifying the type of the argument, and just use the function directly.
"""
from functools import singledispatchmethod, singledispatch
from typing import Any, Callable, Type, Union, overload
from typing import overload

@overload
def process(value: int) -> int:
    """Overload for int."""
    ...

@overload
def process(value: str) -> str:
    """Overload for str."""
    ...

@overload
def process(value: float) -> float:
    """Overload for float."""
    ...

@overload
def process(value: Any) -> Union[int, str, float]:
    """Catch-all overload."""
    ...

def process(value: Any) -> Union[int, str, float]:
    """Run singledispatch handler."""
    return _process(value)

@singledispatch
def _process(value: Any) -> Union[int, str, float]:
    """Process a value based on its type."""
    raise NotImplementedError(f"Unsupported type: {type(value)}")

@_process.register
def _(value: int) -> int:
    """Process integer."""
    return value * 2

@_process.register
def _(value: str) -> str:
    """Process string."""
    return value.upper()

@_process.register
def _(value: float) -> float:
    """Process float."""
    return value + 0.5

# Example usage
res_int = process(10)
res_str = process("hello")
res_float = process(3.14)


###
# Class example using single dispatch
###

class SingleDispatchDemo:
    """
    Test class for single dispatch functionality. Shows the same as above, but where process is defined in __call__ instead.
    """

    @overload
    def __call__(self, value: int) -> int:
        """Overload for int."""
        ...

    @overload
    def __call__(self, value: str) -> str:
        """Overload for str."""
        ...

    @overload
    def __call__(self, value: Any) -> Union[int, str]:
        """Catch-all overload."""
        ...

    def __call__(self, value: Any) -> Union[int, str, float]:
        """Run singledispatch handler."""
        return self._process(value)

    @singledispatchmethod
    def _process(self, value: Any) -> Union[int, str, float]:
        """Process a value based on its type."""
        raise NotImplementedError(f"Unsupported type: {type(value)}")

    @_process.register
    def _(self, value: int) -> int:
        """Process integer."""
        return value * 2

    @_process.register
    def _(self, value: str) -> str:
        """Process string."""
        return value.upper()

    @_process.register
    def _(self, value: float) -> float:
        """Process float."""
        return value + 0.5


tsd = SingleDispatchDemo()
res_int_tsd = tsd(10)
res_str_tsd = tsd("hello")
res_float_tsd = tsd(3.14)

print(res_int_tsd, res_str_tsd, res_float_tsd)

################
# Extensible example
###############


class ExtensibleDispatcher:
    """A class that allows registering new type handlers without modifying the base class."""

    @overload
    def __call__(self, value: int) -> int:
        ...

    @overload
    def __call__(self, value: str) -> str:
        ...

    @overload
    def __call__(self, value: Any) -> Union[int, str]:
        ...

    def __init__(self) -> None:
        """Initialize the dispatcher and register default handlers."""
        self._dispatcher = singledispatch(self._default_handler)
        self._dispatcher.register(int, self._handle_int)
        self._dispatcher.register(str, self._handle_str)

    def __call__(self, value: Any) -> Union[int, str]:
        """Dispatch to the correct handler based on type."""
        return self._dispatcher(value)

    def _default_handler(self, value: Any) -> Union[int, str]:
        """Default handler for unsupported types."""
        raise NotImplementedError(f"Unsupported type: {type(value)}")

    def _handle_int(self, value: int) -> int:
        """Handle int."""
        return value * 2

    def _handle_str(self, value: str) -> str:
        """Handle str."""
        return value.upper()

    def register(self, typ: Type[Any], func: Callable[[Any], Any]) -> None:
        """Register a new type handler."""
        self._dispatcher.register(typ, func)

# Usage: extend with float support without modifying the base class

def handle_float(value: float) -> float:
    """Handle float."""
    return value + 0.5

dispatcher: ExtensibleDispatcher = ExtensibleDispatcher()
dispatcher.register(float, handle_float)

res_int = dispatcher(10)
res_str = dispatcher("hello")
res_float = dispatcher(3.14)  # TODO: This shows a mypy error, but works at runtime. Need to fix this.

print(res_int, res_str, res_float)