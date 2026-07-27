"""
Factories for Imaging tests.
"""

from __future__ import annotations

from datetime import datetime

import factory

from apps.ai.tests.factories import AIModelFactory
from apps.clinical.patients.tests.factories import PatientFactory
from apps.imaging.constants import (
    AIAnalysisType,
    Modality,
    ReportStatus,
    StudyStatus,
)
from apps.imaging.models import AIAnalysis, ImageInstance, Report, Series, Study
from apps.platform.organizations.tests.factories import OrganizationFactory


class StudyFactory(factory.django.DjangoModelFactory):
    """
    Factory for Study model.
    """

    class Meta:
        model = Study

    organization = factory.SubFactory(
        OrganizationFactory,
    )

    patient = factory.SubFactory(
        PatientFactory,
    )

    study_instance_uid = factory.Sequence(
        lambda n: f"1.2.3.4.{n:06d}",
    )

    accession_number = factory.Sequence(
        lambda n: f"ACC{n:06d}",
    )

    study_date = factory.LazyFunction(
        datetime.now,
    )

    modality = Modality.XR

    study_description = ""

    referring_physician = ""

    status = StudyStatus.SCHEDULED


class SeriesFactory(factory.django.DjangoModelFactory):
    """
    Factory for Series model.
    """

    class Meta:
        model = Series

    study = factory.SubFactory(
        StudyFactory,
    )

    series_instance_uid = factory.Sequence(
        lambda n: f"1.2.3.4.5.{n:06d}",
    )

    series_number = factory.Sequence(
        lambda n: n + 1,
    )

    modality = Modality.XR

    series_description = ""

    number_of_instances = 0


class ImageInstanceFactory(factory.django.DjangoModelFactory):
    """
    Factory for ImageInstance model.
    """

    class Meta:
        model = ImageInstance

    series = factory.SubFactory(
        SeriesFactory,
    )

    sop_instance_uid = factory.Sequence(
        lambda n: f"1.2.3.4.5.6.{n:06d}",
    )

    instance_number = factory.Sequence(
        lambda n: n + 1,
    )

    rows = 512

    columns = 512

    bits_allocated = 16

    storage_path = "/tmp/image.dcm"

    thumbnail_path = ""

    file_size = 1024


class ReportFactory(factory.django.DjangoModelFactory):
    """
    Factory for Report model.
    """

    class Meta:
        model = Report

    study = factory.SubFactory(
        StudyFactory,
    )

    report_text = "No acute findings."

    findings = ""

    impression = "Normal study."

    recommendations = ""

    reported_by = None

    status = ReportStatus.DRAFT


class AIAnalysisFactory(factory.django.DjangoModelFactory):
    """
    Factory for AIAnalysis model.
    """

    class Meta:
        model = AIAnalysis

    study = factory.SubFactory(
        StudyFactory,
    )

    ai_model = factory.SubFactory(
        AIModelFactory,
    )

    analysis_type = AIAnalysisType.CLASSIFICATION

    input_image_ids = []

    result = {"classification": "normal", "probability": 0.95}

    confidence_score = 0.95

    findings = []

    is_reviewed = False

    reviewed_by = None

    reviewed_at = None


__all__ = [
    "AIAnalysisFactory",
    "ImageInstanceFactory",
    "ReportFactory",
    "SeriesFactory",
    "StudyFactory",
]
