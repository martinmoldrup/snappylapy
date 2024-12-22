"""

"""
from abc import ABC, abstractmethod
from typing import List
import pathlib
import inspect


class Snapshot:
    DEFAULT_SNAPSHOTS_OUTPUT_DIR = pathlib.Path("__snapshots__")
    DEFAULT_TEST_RESULTS_OUTPUT_DIR = pathlib.Path("__test_results__")

    def __init__(self, update_snapshots: bool = False) -> None:
        self.snapshot_output_dir = self.DEFAULT_SNAPSHOTS_OUTPUT_DIR
        self.test_results_output_dir = self.DEFAULT_TEST_RESULTS_OUTPUT_DIR
        self.filename: str | None = None
        self.snapshot_update = update_snapshots

    def __call__(self,
                 data_to_snapshot: bytes,
                 name: str = "",
                 filetype="txt") -> None:
        """Save the to the output directory."""
        if not isinstance(data_to_snapshot, bytes):
            raise ValueError("Only bytes are supported so far, more to come. Please create a request in github issues.")
        if name:
            self.filename = f"{name}.{filetype}"
        else:
            self.filename = self.get_filename(filetype)
        output_path = self.test_results_output_dir / self.filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(data_to_snapshot)

    def get_filename(self, filetype: str) -> str:
        frame = inspect.currentframe()
        while frame:
            is_in_current_module = frame.f_code.co_filename == __file__
            if not is_in_current_module:
                return f"{frame.f_code.co_name}.{filetype}"
            frame = frame.f_back
        raise ValueError("Could not determine the filename from the stack")

    def read_snapshot(self) -> bytes:
        snapshot_path = self.snapshot_output_dir / self.filename
        if not snapshot_path.exists():
            return b"<No snapshot>"
        return snapshot_path.read_bytes()

    def read_test_results(self) -> bytes:
        test_results_path = self.test_results_output_dir / self.filename
        if not test_results_path.exists():
            return b"<No test results>"
        return test_results_path.read_bytes()

    def __eq__(self, value: object) -> bool:
        assert isinstance(value, bytes), "Only bytes are supported"
        self.__call__(data_to_snapshot=value)
        return self._exact_match_with_snapshot()

    def _update_snapshot(self) -> None:
        snapshot_path = self.snapshot_output_dir / self.filename
        if self.snapshot_update or not snapshot_path.exists():
            test_results_path = self.test_results_output_dir / self.filename
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            snapshot_path.write_bytes(test_results_path.read_bytes())

    def _exact_match_with_snapshot(self) -> bool:
        self._update_snapshot()
        return self.read_snapshot() == self.read_test_results()

    def assert_immutable(self):
        assert self._exact_match_with_snapshot()
