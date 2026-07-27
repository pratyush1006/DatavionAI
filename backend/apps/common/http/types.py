"""
HTTP type aliases.

Provides reusable type aliases shared across the DatavionAI
HTTP framework.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TypeAlias

Headers: TypeAlias = Mapping[str, str]


QueryParameters: TypeAlias = Mapping[
    str,
    str | int | float | bool | None,
]


JSONPrimitive: TypeAlias = str | int | float | bool | None


JSONValue: TypeAlias = JSONPrimitive | list["JSONValue"] | dict[str, "JSONValue"]


JSONMapping: TypeAlias = Mapping[
    str,
    JSONValue,
]


ResponseData: TypeAlias = bytes | str | JSONMapping | list[JSONValue] | None


__all__: tuple[str, ...] = (
    "Headers",
    "JSONMapping",
    "JSONPrimitive",
    "JSONValue",
    "QueryParameters",
    "ResponseData",
)
