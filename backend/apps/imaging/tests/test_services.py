"""
Tests for imaging services.
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
from apps.imaging.models import AIAnalysis, Report, Study
from apps.imaging.services import AIAnalysisService, ReportService, StudyService
from apps.imaging.tests.factories import (
    AIAnalysisFactory,
    ReportFactory,
    StudyFactory,
)


class StudyServiceTestCase(BaseTestCase):
    """
    Test cases for StudyService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.study = StudyFactory(
            organization=self.organization,
            patient=self.create_patient(),
        )

    def test_create_study(self) -> None:
        """
        Study should be created successfully.
        """

        study = StudyService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.create_patient(),
                "study_instance_uid": "1.2.3.4.5.6.7.8.10",
                "study_date": date(2024, 1, 20),
                "modality": Modality.CT,
                "status": StudyStatus.SCHEDULED,
            },
        )

        self.assertIsInstance(
            study,
            Study,
        )

        self.assertEqual(
            study.modality,
            Modality.CT,
        )

    def test_create_study_persists_to_database(self) -> None:
        """
        Created study should be persisted.
        """

        initial_count = Study.objects.count()

        StudyService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.create_patient(),
                "study_instance_uid": "1.2.3.4.5.6.7.8.11",
                "study_date": date(2024, 1, 20),
                "modality": Modality.MR,
                "status": StudyStatus.SCHEDULED,
            },
        )

        self.assertEqual(
            Study.objects.count(),
            initial_count + 1,
        )

    def test_update_study(self) -> None:
        """
        Study should be updated successfully.
        """

        updated_study = StudyService.update(
            instance=self.study,
            validated_data={
                "study_description": "Updated description",
            },
        )

        updated_study.refresh_from_db()

        self.assertEqual(
            updated_study.study_description,
            "Updated description",
        )

    def test_cancel_study(self) -> None:
        """
        Study should be cancelled successfully.
        """

        cancelled_study = StudyService.cancel(
            instance=self.study,
        )

        cancelled_study.refresh_from_db()

        self.assertEqual(
            cancelled_study.status,
            StudyStatus.CANCELLED,
        )

    def test_complete_study(self) -> None:
        """
        Study should be completed successfully.
        """

        completed_study = StudyService.complete(
            instance=self.study,
        )

        completed_study.refresh_from_db()

        self.assertEqual(
            completed_study.status,
            StudyStatus.COMPLETED,
        )


class ReportServiceTestCase(BaseTestCase):
    """
    Test cases for ReportService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.study = StudyFactory(
            organization=self.organization,
            patient=self.create_patient(),
        )

        self.report = ReportFactory(
            study=self.study,
        )

    def test_create_report(self) -> None:
        """
        Report should be created successfully.
        """

        study = StudyFactory(
            organization=self.organization,
            patient=self.create_patient(),
        )

        report = ReportService.create(
            validated_data={
                "study": study,
                "report_text": "Normal findings.",
                "status": ReportStatus.DRAFT,
            },
        )

        self.assertIsInstance(
            report,
            Report,
        )

        self.assertEqual(
            report.report_text,
            "Normal findings.",
        )

    def test_create_report_persists_to_database(self) -> None:
        """
        Created report should be persisted.
        """

        initial_count = Report.objects.count()

        study = StudyFactory(
            organization=self.organization,
            patient=self.create_patient(),
        )

        ReportService.create(
            validated_data={
                "study": study,
                "report_text": "Another report.",
                "status": ReportStatus.DRAFT,
            },
        )

        self.assertEqual(
            Report.objects.count(),
            initial_count + 1,
        )

    def test_finalize_report(self) -> None:
        """
        Report should be finalized successfully.
        """

        finalized_report = ReportService.finalize(
            instance=self.report,
        )

        finalized_report.refresh_from_db()

        self.assertEqual(
            finalized_report.status,
            ReportStatus.FINALIZED,
        )

    def test_amend_report(self) -> None:
        """
        Report should be amended successfully.
        """

        amended_report = ReportService.amend(
            instance=self.report,
            validated_data={
                "report_text": "Amended findings.",
            },
        )

        amended_report.refresh_from_db()

        self.assertEqual(
            amended_report.status,
            ReportStatus.AMENDED,
        )

        self.assertEqual(
            amended_report.report_text,
            "Amended findings.",
        )


class AIAnalysisServiceTestCase(BaseTestCase):
    """
    Test cases for AIAnalysisService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.study = StudyFactory(
            organization=self.organization,
            patient=self.create_patient(),
        )

        self.ai_model = AIModelFactory(
            organization=self.organization,
            name="Test Model",
            version="1.0",
        )

        self.analysis = AIAnalysisFactory(
            study=self.study,
            ai_model=self.ai_model,
        )

    def test_create_ai_analysis(self) -> None:
        """
        AIAnalysis should be created successfully.
        """

        analysis = AIAnalysisService.create(
            validated_data={
                "study": self.study,
                "ai_model": self.ai_model,
                "analysis_type": AIAnalysisType.ANOMALY_DETECTION,
                "input_image_ids": ["1"],
                "result": {"anomalies": []},
                "confidence_score": 0.88,
                "findings": [],
            },
        )

        self.assertIsInstance(
            analysis,
            AIAnalysis,
        )

        self.assertEqual(
            analysis.analysis_type,
            AIAnalysisType.ANOMALY_DETECTION,
        )

    def test_create_ai_analysis_persists_to_database(self) -> None:
        """
        Created AIAnalysis should be persisted.
        """

        initial_count = AIAnalysis.objects.count()

        AIAnalysisService.create(
            validated_data={
                "study": self.study,
                "ai_model": self.ai_model,
                "analysis_type": AIAnalysisType.SEGMENTATION,
                "input_image_ids": ["1"],
                "result": {"segments": []},
                "findings": [],
            },
        )

        self.assertEqual(
            AIAnalysis.objects.count(),
            initial_count + 1,
        )

    def test_review_ai_analysis(self) -> None:
        """
        AIAnalysis should be reviewed successfully.
        """

        reviewed_analysis = AIAnalysisService.review(
            instance=self.analysis,
            reviewed_by=self.create_employee(),
        )

        reviewed_analysis.refresh_from_db()

        self.assertTrue(
            reviewed_analysis.is_reviewed,
        )

        self.assertIsNotNone(
            reviewed_analysis.reviewed_at,
        )


__all__ = [
    "AIAnalysisServiceTestCase",
    "ReportServiceTestCase",
    "StudyServiceTestCase",
]
