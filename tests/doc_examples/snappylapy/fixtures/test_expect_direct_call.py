import pytest
from snappylapy.fixtures import Expect


def test_expect_direct_call(expect: Expect) -> None:
    # Dict input
    data_dict: dict[str, int] = {"a": 1, "b": 2}
    expect(data_dict).to_match_snapshot()

    # List input
    data_list: list[int] = [1, 2, 3]
    expect(data_list).to_match_snapshot()

    # String input
    data_str: str = "pytest example"
    expect(data_str).to_match_snapshot()

    # Bytes input
    data_bytes: bytes = b"binary"
    expect(data_bytes).to_match_snapshot()

    # DataFrame input (requires pandas)
    try:
        import pandas as pd
    except ImportError:
        pass
    else:
        df: pd.DataFrame = pd.DataFrame({"x": [1, 2]})
        expect(df).to_match_snapshot()

    # Custom object input (falls back to ObjectExpect)
    class Custom:
        def __init__(self) -> None:
            self.value = 42
    custom_obj = Custom()
    expect(custom_obj).to_match_snapshot()