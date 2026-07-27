"""
Common type aliases for the Datavion AI platform.
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any, Final, TypeAlias

AnyDict: TypeAlias = dict[str, Any]
AnyList: TypeAlias = list[Any]
AnyTuple: TypeAlias = tuple[Any, ...]

StringDict: TypeAlias = dict[str, str]
StringList: TypeAlias = list[str]

ImmutableMapping: TypeAlias = Mapping[str, Any]
MutableStringMapping: TypeAlias = MutableMapping[str, Any]

StringSequence: TypeAlias = Sequence[str]

Headers: TypeAlias = Mapping[str, str]

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
