"""
Imaging permission classes.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class StudyPermission:
    """
    Imaging study permission codes.
    """

    VIEW = "imaging.study.view"
    CREATE = "imaging.study.create"
    UPDATE = "imaging.study.update"
    DELETE = "imaging.study.delete"
    UPLOAD = "imaging.study.upload"
    GENERATE_REPORT = "imaging.study.generate_report"


class CanViewStudy(BasePermission):
    """
    Permission required to view imaging studies.
    """

    permission_code = StudyPermission.VIEW


class CanCreateStudy(BasePermission):
    """
    Permission required to create imaging studies.
    """

    permission_code = StudyPermission.CREATE


class CanUpdateStudy(BasePermission):
    """
    Permission required to update imaging studies.
    """

    permission_code = StudyPermission.UPDATE


class CanDeleteStudy(BasePermission):
    """
    Permission required to delete imaging studies.
    """

    permission_code = StudyPermission.DELETE


class CanUploadStudy(BasePermission):
    """
    Permission required to upload images to a study.
    """

    permission_code = StudyPermission.UPLOAD


class CanGenerateReport(BasePermission):
    """
    Permission required to generate reports for a study.
    """

    permission_code = StudyPermission.GENERATE_REPORT


__all__ = [
    "CanCreateStudy",
    "CanDeleteStudy",
    "CanGenerateReport",
    "CanUploadStudy",
    "CanUpdateStudy",
    "CanViewStudy",
    "StudyPermission",
]
