"""Test a fixture that collect the results, so that multiple assertion errors can be reported."""
import pytest

class Expect:
    def __init__(self,errors: list):
 
        self.errors = errors

    def __call__(self, value):
        self.value = value
        return self

    def to_equal(self, expected):
        try:
            assert self.value == expected
        except AssertionError as e:
            self.errors.append(e)

    def to_be_greater_than(self, threshold):
        try:
            assert self.value > threshold
        except AssertionError as e:
            self.errors.append(e)



@pytest.fixture
def expect():
    """A fixture that collects multiple assertion errors."""
    errors = []

    yield Expect(errors=errors)

    if errors:
        error_messages = "\n".join(str(e) for e in errors)
        raise AssertionError(f"Multiple assertion errors:\n{error_messages}")
    
def test_multiple_assertions(expect: Expect):
    """Test multiple assertions and collect errors."""
    expect(5).to_equal(10)  # This will fail
    expect(5).to_be_greater_than(10)  # This will also fail
    expect(5).to_equal(5)  # This will pass
    expect(5).to_be_greater_than(3)  # This will pass

