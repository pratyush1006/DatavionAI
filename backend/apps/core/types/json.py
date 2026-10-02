"""
JSON type aliases for the Datavion AI platform.
"""

from __future__ import annotations

type JSONPrimitive = str | int | float | bool | None

type JSONValue = JSONPrimitive | dict[str, "JSONValue"] | list["JSONValue"]

type JSONObject = dict[str, JSONValue]
type JSONArray = list[JSONValue]

__all__ = [
    "JSONArray",
    "JSONObject",
    "JSONPrimitive",
    "JSONValue",
]
