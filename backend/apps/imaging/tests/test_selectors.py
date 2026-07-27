"""
Tests for imaging selectors.
"""

from __future__ import annotations

from datetime import date

from apps.ai.tests.factories import AIModelFactory
from apps.common.tests.base import BaseTestCase
from apps.imaging.constants import (
    AIAnalysisType,
    Modality,
    ReportStatus,
)
from apps.imaging.selectors import (
    AIAnalysisSelector,
    ReportSelector,
    StudySelector,
)
from apps.imaging.tests.factories import (
    AIAnalysisFactory,
    ReportFactory,
    StudyFactory,
)


class StudySelectorTestCase(BaseTestCase):
    """
    Test cases for StudySelector.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.xray_study = StudyFactory(
            organization=self.organization,
            patient=self.patient,
            modality=Modality.XR,
            study_date=date(2024, 1, 15),
            study_description="Chest X-Ray",
        )

        self.ct_study = StudyFactory(
            organization=self.organization,
            patient=self.patient,
            modality=Modality.CT,
            study_date=date(2024, 1, 16),
        )

    def test_queryset(self) -> None:
        """
        queryset() should return a queryset.
        """

        queryset = StudySelector.queryset()

        self.assertIn(
            self.xray_study,
            queryset,
        )

    def test_get(self) -> None:
        """
        get() should return the requested study.
        """

        study = StudySelector.get(
            study_id=str(self.xray_study.id),
        )

        self.assertEqual(
            study,
            self.xray_study,
        )

    def test_list(self) -> None:
        """
        list() should return all studies.
        """

        studies = StudySelector.list()

        self.assertEqual(
            studies.count(),
            2,
        )

    def test_list_by_patient(self) -> None:
        """
        list_by_patient() should filter by patient.
        """

        studies = StudySelector.list_by_patient(
            patient_id=str(self.xray_study.patient_id),
        )

        self.assertEqual(
            studies.count(),
            2,
        )

    def test_list_by_organization(self) -> None:
        """
        list_by_organization() should filter by organization.
        """

        studies = StudySelector.list_by_organization(
            organization=self.organization,
        )

        self.assertEqual(
            studies.count(),
            2,
        )

    def test_list_by_modality(self) -> None:
        """
        list_by_modality() should filter by modality.
        """

        studies = StudySelector.list_by_modality(
            modality=Modality.XR,
        )

        self.assertEqual(
            studies.count(),
            1,
        )

        self.assertEqual(
            studies.first(),
            self.xray_study,
        )

    def test_search(self) -> None:
        """
        search() should find matching studies.
        """

        studies = StudySelector.search(
            query="Chest",
        )

        self.assertIn(
            self.xray_study,
            studies,
        )

    def test_count(self) -> None:
        """
        count() should return the study count.
        """

        self.assertEqual(
            StudySelector.count(
                organization=self.organization,
            ),
            2,
        )


class ReportSelectorTestCase(BaseTestCase):
    """
    Test cases for ReportSelector.
    """

    def setUp(self) -> None:
        super().setUp()

        self.study = StudyFactory(
            organization=self.organization,
            patient=self.create_patient(),
        )

        self.draft_report = ReportFactory(
            study=self.study,
            status=ReportStatus.DRAFT,
        )

        self.finalized_study = StudyFactory(
            organization=self.organization,
            patient=self.create_patient(),
        )

        self.finalized_report = ReportFactory(
            study=self.finalized_study,
            status=ReportStatus.FINALIZED,
        )

    def test_queryset(self) -> None:
        """
        queryset() should return a queryset.
        """

        queryset = ReportSelector.queryset()

        self.assertIn(
            self.draft_report,
            queryset,
        )

    def test_get(self) -> None:
        """
        get() should return the requested report.
        """

        report = ReportSelector.get(
            report_id=str(self.draft_report.id),
        )

        self.assertEqual(
            report,
            self.draft_report,
        )

    def test_list(self) -> None:
        """
        list() should return all reports.
        """

        reports = ReportSelector.list()

        self.assertEqual(
            reports.count(),
            2,
        )

    def test_list_by_study(self) -> None:
        """
        list_by_study() should filter by study.
        """

        reports = ReportSelector.list_by_study(
            study_id=str(self.study.id),
        )

        self.assertEqual(
            reports.count(),
            1,
        )

    def test_list_by_radiologist(self) -> None:
        """
        list_by_radiologist() should filter by radiologist.
        """

        employee = self.create_employee()

        self.draft_report.reported_by = employee
        self.draft_report.save()

        reports = ReportSelector.list_by_radiologist(
            employee_id=str(employee.id),
        )

        self.assertEqual(
            reports.count(),
            1,
        )

    def test_search(self) -> None:
        """
        search() should find matching reports.
        """

        reports = ReportSelector.search(
            query="Normal",
        )

        self.assertIn(
            self.draft_report,
            reports,
        )

    def test_count(self) -> None:
        """
        count() should return the report count.
        """

        self.assertEqual(
            ReportSelector.count(
                organization=self.organization,
            ),
            2,
        )


class AIAnalysisSelectorTestCase(BaseTestCase):
    """
    Test cases for AIAnalysisSelector.
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

        self.classification_analysis = AIAnalysisFactory(
            study=self.study,
            ai_model=self.ai_model,
            analysis_type=AIAnalysisType.CLASSIFICATION,
            is_reviewed=True,
        )

        self.segmentation_analysis = AIAnalysisFactory(
            study=self.study,
            ai_model=self.ai_model,
            analysis_type=AIAnalysisType.SEGMENTATION,
            is_reviewed=False,
        )

    def test_list(self) -> None:
        """
        list() should return all AI analyses.
        """

        analyses = AIAnalysisSelector.list()

        self.assertEqual(
            analyses.count(),
            2,
        )

    def test_get(self) -> None:
        """
        get() should return the requested AI analysis.
        """

        analysis = AIAnalysisSelector.get(
            analysis_id=str(self.classification_analysis.id),
        )

        self.assertEqual(
            analysis,
            self.classification_analysis,
        )

    def test_list_by_study(self) -> None:
        """
        list_by_study() should filter by study.
        """

        analyses = AIAnalysisSelector.list_by_study(
            study_id=str(self.study.id),
        )

        self.assertEqual(
            analyses.count(),
            2,
        )

    def test_list_by_model(self) -> None:
        """
        list_by_model() should filter by AI model.
        """

        analyses = AIAnalysisSelector.list_by_model(
            ai_model_id=str(self.ai_model.id),
        )

        self.assertEqual(
            analyses.count(),
            2,
        )

    def test_list_unreviewed(self) -> None:
        """
        list_unreviewed() should return unreviewed analyses.
        """

        analyses = AIAnalysisSelector.list_unreviewed()

        self.assertEqual(
            analyses.count(),
            1,
        )

        self.assertEqual(
            analyses.first(),
            self.segmentation_analysis,
        )

    def test_search(self) -> None:
        """
        search() should find matching AI analyses.
        """

        analyses = AIAnalysisSelector.search(
            query="classification",
        )

        self.assertIn(
            self.classification_analysis,
            analyses,
        )


__all__ = [
    "AIAnalysisSelectorTestCase",
    "ReportSelectorTestCase",
    "StudySelectorTestCase",
]
