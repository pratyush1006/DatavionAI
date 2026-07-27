"""
JSON type aliases for the Datavion AI platform.
"""

from __future__ import annotations

from typing import TypeAlias

JSONPrimitive: TypeAlias = str | int | float | bool | None

JSONValue: TypeAlias = JSONPrimitive | dict[str, "JSONValue"] | list["JSONValue"]

JSONObject: TypeAlias = dict[str, JSONValue]
JSONArray: TypeAlias = list[JSONValue]

__all__ = [
    "JSONArray",
    "JSONObject",
    "JSONPrimitive",
    "JSONValue",
]
