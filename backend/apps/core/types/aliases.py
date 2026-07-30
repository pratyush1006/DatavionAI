"""
Common type aliases for the Datavion AI platform.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any, Final

type AnyDict = dict[str, Any]
type AnyList = list[Any]
type AnyTuple = tuple[Any, ...]

type StringDict = dict[str, str]
type StringList = list[str]

type ImmutableMapping = Mapping[str, Any]
type MutableStringMapping = MutableMapping[str, Any]

type StringSequence = Sequence[str]

type Headers = Mapping[str, str]

DEFAULT_ENCODING: Final[str] = "utf-8"

__all__ = [
    "AnyDict",
    "AnyList",
    "AnyTuple",
    "DEFAULT_ENCODING",
    "Headers",
    "ImmutableMapping",
    "MutableStringMapping",
    "StringDict",
    "StringList",
    "StringSequence",
]
