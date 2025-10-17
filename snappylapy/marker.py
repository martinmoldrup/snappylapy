"""Typed decorator for the snappylapy pytest marker."""

from __future__ import annotations

import pytest
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(slots=True)
class SnappylapyMarkerConfig:
    """
    Configuration options for the snappylapy pytest marker.

    Input parameters for the @pytest.mark.snappylapy() or @configure_snappylapy()
    decorator.
    """

    depends: list[Callable[..., Any]] | None = None
    output_dir: str | None = None
    foreach_folder_in: str | Path | None = None


def configure_snappylapy(
    *,
    depends: list[Callable[..., Any]] | None = None,
    output_dir: str | None = None,
    foreach_folder_in: str | Path | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorate a test function with the snappylapy marker and configuration.

    An alternative to using the pytest.mark.snappylapy marker directly.
    Provides type safety, linting, and IDE auto-completion for marker arguments.
    """
    kwargs: dict[str, Any] = {}
    if depends is not None:
        kwargs["depends"] = depends
    if output_dir is not None:
        kwargs["output_dir"] = output_dir
    if foreach_folder_in is not None:
        kwargs["foreach_folder_in"] = foreach_folder_in
    marker = pytest.mark.snappylapy(**kwargs)

    def _wrap(func: Callable[P, R]) -> Callable[P, R]:
        return marker(func)

    return _wrap
