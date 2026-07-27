"""
Permission classes for the Timeline Event module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class PatientTimelineEventPermission:
    VIEW = "timeline.view"
    CREATE = "timeline.create"
    UPDATE = "timeline.update"
    DELETE = "timeline.delete"


class CanViewPatientTimelineEvent(BasePermission):
    permission_code = PatientTimelineEventPermission.VIEW


class CanCreatePatientTimelineEvent(BasePermission):
    permission_code = PatientTimelineEventPermission.CREATE


class CanUpdatePatientTimelineEvent(BasePermission):
    permission_code = PatientTimelineEventPermission.UPDATE


class CanDeletePatientTimelineEvent(BasePermission):
    permission_code = PatientTimelineEventPermission.DELETE


__all__ = [
    "CanCreatePatientTimelineEvent",
    "CanDeletePatientTimelineEvent",
    "CanUpdatePatientTimelineEvent",
    "CanViewPatientTimelineEvent",
    "PatientTimelineEventPermission",
]
