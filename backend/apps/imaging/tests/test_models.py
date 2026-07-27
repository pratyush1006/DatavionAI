"""
Tests for Imaging models.
"""

from __future__ import annotations

from datetime import date

from apps.ai.tests.factories import AIModelFactory
from apps.common.tests.base import BaseTestCase
from apps.imaging.constants import (
    AIAnalysisType,
    Modality,
    ReportStatus,
    StudyStatus,
)
from apps.imaging.models import AIAnalysis, ImageInstance, Report, Series, Study


class StudyModelTestCase(BaseTestCase):
    """
    Test cases for the Study model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.study = Study.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            study_instance_uid="1.2.3.4.5.6.7.8.9",
            accession_number="ACC000001",
            study_date=date(2024, 1, 15),
            modality=Modality.XR,
            study_description="Chest X-Ray",
            referring_physician="Dr. Smith",
            status=StudyStatus.SCHEDULED,
        )

    def test_study_creation(self) -> None:
        """
        Study should be created successfully.
        """

        self.assertEqual(
            self.study.organization,
            self.organization,
        )

        self.assertEqual(
            self.study.study_instance_uid,
            "1.2.3.4.5.6.7.8.9",
        )

        self.assertEqual(
            self.study.modality,
            Modality.XR,
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the study display name.
        """

        self.assertIn(
            "1.2.3.4.5.6.7.8.9",
            str(self.study),
        )

    def test_default_status(self) -> None:
        """
        Default study status should be applied.
        """

        study = Study.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            study_instance_uid="1.2.3.4.5.6.7.8.10",
            study_date=date(2024, 1, 15),
            modality=Modality.CT,
        )

        self.assertEqual(
            study.status,
            StudyStatus.SCHEDULED,
        )

    def test_unique_study_instance_uid(self) -> None:
        """
        Study instance UID should be unique.
        """

        with self.assertRaises(Exception):
            Study.objects.create(
                organization=self.organization,
                patient=self.create_patient(),
                study_instance_uid="1.2.3.4.5.6.7.8.9",
                study_date=date(2024, 1, 15),
                modality=Modality.CT,
            )

    def test_meta_table_name(self) -> None:
        """
        Study model should use the configured database table.
        """

        self.assertEqual(
            Study._meta.db_table,
            "imaging_studies",
        )


class SeriesModelTestCase(BaseTestCase):
    """
    Test cases for the Series model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.study = Study.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            study_instance_uid="1.2.3.4.5.6.7.8.9",
            study_date=date(2024, 1, 15),
            modality=Modality.XR,
        )

        self.series = Series.objects.create(
            study=self.study,
            series_instance_uid="1.2.3.4.5.6.7.8.9.1",
            series_number=1,
            modality=Modality.XR,
            number_of_instances=2,
        )

    def test_series_creation(self) -> None:
        """
        Series should be created successfully.
        """

        self.assertEqual(
            self.series.study,
            self.study,
        )

        self.assertEqual(
            self.series.series_number,
            1,
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the series display name.
        """

        self.assertIn(
            "Series 1",
            str(self.series),
        )

    def test_default_number_of_instances(self) -> None:
        """
        Default number of instances should be 0.
        """

        series = Series.objects.create(
            study=self.study,
            series_instance_uid="1.2.3.4.5.6.7.8.9.2",
            series_number=2,
            modality=Modality.XR,
        )

        self.assertEqual(
            series.number_of_instances,
            0,
        )


class ImageInstanceModelTestCase(BaseTestCase):
    """
    Test cases for the ImageInstance model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.study = Study.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            study_instance_uid="1.2.3.4.5.6.7.8.9",
            study_date=date(2024, 1, 15),
            modality=Modality.XR,
        )

        self.series = Series.objects.create(
            study=self.study,
            series_instance_uid="1.2.3.4.5.6.7.8.9.1",
            series_number=1,
            modality=Modality.XR,
        )

        self.image_instance = ImageInstance.objects.create(
            series=self.series,
            sop_instance_uid="1.2.3.4.5.6.7.8.9.1.1",
            instance_number=1,
            rows=512,
            columns=512,
            bits_allocated=16,
            storage_path="/tmp/image.dcm",
        )

    def test_image_instance_creation(self) -> None:
        """
        ImageInstance should be created successfully.
        """

        self.assertEqual(
            self.image_instance.series,
            self.series,
        )

        self.assertEqual(
            self.image_instance.rows,
            512,
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the image instance display name.
        """

        self.assertIn(
            "Instance 1",
            str(self.image_instance),
        )

    def test_optional_thumbnail(self) -> None:
        """
        Thumbnail path should be optional.
        """

        self.assertEqual(
            self.image_instance.thumbnail_path,
            "",
        )


class ReportModelTestCase(BaseTestCase):
    """
    Test cases for the Report model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.study = Study.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            study_instance_uid="1.2.3.4.5.6.7.8.9",
            study_date=date(2024, 1, 15),
            modality=Modality.XR,
        )

        self.report = Report.objects.create(
            study=self.study,
            report_text="No acute cardiopulmonary process.",
            findings="Clear lungs.",
            impression="Normal chest X-ray.",
            recommendations="Follow up as needed.",
            status=ReportStatus.DRAFT,
        )

    def test_report_creation(self) -> None:
        """
        Report should be created successfully.
        """

        self.assertEqual(
            self.report.study,
            self.study,
        )

        self.assertEqual(
            self.report.status,
            ReportStatus.DRAFT,
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the report display name.
        """

        self.assertIn(
            "Report for",
            str(self.report),
        )

    def test_one_to_one_relationship(self) -> None:
        """
        Study should have a one-to-one relationship with Report.
        """

        self.assertEqual(
            self.study.report,
            self.report,
        )


class AIAnalysisModelTestCase(BaseTestCase):
    """
    Test cases for the AIAnalysis model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.study = Study.objects.create(
            organization=self.organization,
            patient=self.create_patient(),
            study_instance_uid="1.2.3.4.5.6.7.8.9",
            study_date=date(2024, 1, 15),
            modality=Modality.XR,
        )

        self.ai_model = AIModelFactory(
            organization=self.organization,
            name="Chest X-Ray Classifier",
            version="1.0",
        )

        self.analysis = AIAnalysis.objects.create(
            study=self.study,
            ai_model=self.ai_model,
            analysis_type=AIAnalysisType.CLASSIFICATION,
            input_image_ids=["1", "2"],
            result={"classification": "normal", "probability": 0.95},
            confidence_score=0.95,
            findings=[{"location": "left_lung", "type": "nodule"}],
        )

    def test_ai_analysis_creation(self) -> None:
        """
        AIAnalysis should be created successfully.
        """

        self.assertEqual(
            self.analysis.study,
            self.study,
        )

        self.assertEqual(
            self.analysis.ai_model,
            self.ai_model,
        )

        self.assertEqual(
            self.analysis.confidence_score,
            0.95,
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the AI analysis display name.
        """

        self.assertIn(
            "AI Analysis",
            str(self.analysis),
        )

    def test_default_is_reviewed(self) -> None:
        """
        Default is_reviewed should be False.
        """

        self.assertFalse(
            self.analysis.is_reviewed,
        )


__all__ = [
    "AIAnalysisModelTestCase",
    "ImageInstanceModelTestCase",
    "ReportModelTestCase",
    "SeriesModelTestCase",
    "StudyModelTestCase",
]
