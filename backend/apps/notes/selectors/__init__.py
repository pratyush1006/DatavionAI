"""
Notes selectors package.

Exposes the public selector classes used to query clinical notes and
note templates.
"""

from __future__ import annotations

from .note import NoteSelector, TemplateSelector

__all__ = [
    "NoteSelector",
    "TemplateSelector",
]
