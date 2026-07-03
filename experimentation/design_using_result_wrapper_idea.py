"""
Design idea rethinking the need for being close to existing snapshot libraries.

Istead we use jest style except with a more pythonic approach.

We aim with this api for explicitness, flexibility and extensibility, instead of reducing the verbosity and the learning curve.
"""
import pytest

class Expect:
    def __call__(self, parent):
        self.parent = parent
        return self

    def to_match_snapshot(self):
        pass

    def to_be(self, expected):
        pass

    def to_be_close_to(self, expected, delta):
        pass

    def to_equal(self, expected):
        pass

    def to_be_scrictly_equal_to(self, expected):
        pass

    def to_have_property(self, property_name):
        pass

    def to_thow_error(self):
        pass

    def to_be_none(self):
        pass

    def to_be_truthy(self):
        pass

    def to_be_falsy(self):
        pass

    def to_be_defined(self):
        pass

class ResultWrapper:
    def __init__(self):
        self.result = None
        self.expect = Expect(self)

    def _save_test_results(self, path, data):
        """Save the test results to a file, so they can be shown in reports."""
        pass

    def __call__(self, result):
        self._save_test_results("same_path", result)
        self.result = result

class ResultWrapperFactory:
    def string(self, result):
        return ResultWrapper()

    def bytes(self, result):
        return ResultWrapper()

import pytest

def function_to_test():
    return "Hello World"

def test_simple_string(result_wrapper: ResultWrapperFactory):
    result = function_to_test()
    r = result_wrapper.string(result)
    r.expect.to_match_snapshot()

######################
# Generated suggestion for improvement from AI
######################

import pytest  
  
def function_to_test():  
    return "Hello World"  
  
def test_simple_string(snapshot):  
    result = function_to_test()  
    snapshot.assert_match(result)  
  
def complex_function_to_test():  
    return {"key": "value", "timestamp": "2023-10-01T12:34:56"}  
  
def test_complex_structure(snapshot):  
    result = complex_function_to_test()  
    snapshot.result(result).expect.to_match_snapshot()  
  
def get_large_dataframe():  
    import pandas as pd  
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})  
  
def test_dataframe(snapshot):  
    df = get_large_dataframe()  
    snapshot.dataframe(df).expect.to_match_snapshot()

    # Could also be
    snapshot.set_dataframe(df).expect.to_match_snapshot()
  
def function_with_timestamp():  
    return {"data": "value", "timestamp": "2023-10-01T12:34:56"}  
  
def test_with_timestamp(snapshot):  
    result = function_with_timestamp()  
    snapshot.result(result).ignore_fields(["timestamp"]).expect.to_match_snapshot()  


