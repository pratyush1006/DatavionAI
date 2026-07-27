"""
Notes services package.

Exposes the public service classes used to manage clinical notes and
note templates.
"""

from __future__ import annotations

from .note import NoteService, TemplateService

__all__ = [
    "NoteService",
    "TemplateService",
]
