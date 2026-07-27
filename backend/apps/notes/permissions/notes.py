"""
Clinical Notes permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class NotePermission:
    """
    Clinical note permission codes.
    """

    VIEW = "note.view"
    CREATE = "note.create"
    UPDATE = "note.update"
    DELETE = "note.delete"
    SIGN = "note.sign"
    AMEND = "note.amend"


class CanViewNote(BasePermission):
    """
    Permission required to view clinical notes.
    """

    permission_code = NotePermission.VIEW


class CanCreateNote(BasePermission):
    """
    Permission required to create clinical notes.
    """

    permission_code = NotePermission.CREATE


class CanUpdateNote(BasePermission):
    """
    Permission required to update clinical notes.
    """

    permission_code = NotePermission.UPDATE


class CanDeleteNote(BasePermission):
    """
    Permission required to delete clinical notes.
    """

    permission_code = NotePermission.DELETE


class CanSignNote(BasePermission):
    """
    Permission required to sign clinical notes.
    """

    permission_code = NotePermission.SIGN


class CanAmendNote(BasePermission):
    """
    Permission required to amend clinical notes.
    """

    permission_code = NotePermission.AMEND


__all__ = [
    "NotePermission",
    "CanAmendNote",
    "CanCreateNote",
    "CanDeleteNote",
    "CanSignNote",
    "CanUpdateNote",
    "CanViewNote",
]
