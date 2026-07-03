from jestspectation import Any, FloatApprox
import jestspectation

jestspectation.configure().pytest_all_diffs = True

def test_goodbye():
    assert 1.0 == Any(float)

def test_dict():
    assert {
        "a": 1,
        "b": 2,
        "c": 3.0,
    } == {
        "a": 1,
        "b": Any(int),
        "c": FloatApprox(2.5, magnitude=0.5)
    }