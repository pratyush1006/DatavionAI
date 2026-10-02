"""
HTTP type aliases.

Provides reusable type aliases shared across the DatavionAI
HTTP framework.
"""

from __future__ import annotations

from collections.abc import Mapping

type Headers = Mapping[str, str]


type QueryParameters = Mapping[
    str,
    str | int | float | bool | None,
]


type JSONPrimitive = str | int | float | bool | None


type JSONValue = JSONPrimitive | list["JSONValue"] | dict[str, "JSONValue"]


type JSONMapping = Mapping[
    str,
    JSONValue,
]


type ResponseData = bytes | str | JSONMapping | list[JSONValue] | None


__all__: tuple[str, ...] = (
    "Headers",
    "JSONMapping",
    "JSONPrimitive",
    "JSONValue",
    "QueryParameters",
    "ResponseData",
)
