"""
Imaging-specific constants.
"""

from __future__ import annotations

from typing import Final

from django.db import models


class StudyStatus(models.TextChoices):
    """
    Imaging study lifecycle status.
    """

    SCHEDULED = "scheduled", "Scheduled"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
    ERROR = "error", "Error"


class Modality(models.TextChoices):
    """
    Supported DICOM modalities.
    """

    XR = "XR", "X-Ray"
    CT = "CT", "Computed Tomography"
    MR = "MR", "Magnetic Resonance"
    US = "US", "Ultrasound"
    NM = "NM", "Nuclear Medicine"
    PT = "PT", "Positron Emission Tomography"
    RF = "RF", "Radio Fluoroscopy"
    MG = "MG", "Mammography"
    DX = "DX", "Digital Radiography"
    CR = "CR", "Computed Radiography"
    OT = "OT", "Other"
    SC = "SC", "Secondary Capture"
    XA = "XA", "X-Ray Angiography"


class ReportStatus(models.TextChoices):
    """
    Radiology report lifecycle status.
    """

    DRAFT = "draft", "Draft"
    FINALIZED = "finalized", "Finalized"
    AMENDED = "amended", "Amended"


class AIAnalysisType(models.TextChoices):
    """
    Supported AI analysis types.
    """

    ANOMALY_DETECTION = "anomaly_detection", "Anomaly Detection"
    LESION_DETECTION = "lesion_detection", "Lesion Detection"
    CLASSIFICATION = "classification", "Classification"
    SEGMENTATION = "segmentation", "Segmentation"
    MEASUREMENT = "measurement", "Measurement"


DEFAULT_STUDY_STATUS: Final[str] = StudyStatus.SCHEDULED
DEFAULT_REPORT_STATUS: Final[str] = ReportStatus.DRAFT


__all__ = [
    "AIAnalysisType",
    "DEFAULT_REPORT_STATUS",
    "DEFAULT_STUDY_STATUS",
    "Modality",
    "ReportStatus",
    "StudyStatus",
]
