from __future__ import annotations

import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.imaging.constants.choices import (
    ContrastStatus,
    ImagingReportStatus,
    ImagingStudyStatus,
)
from apps.imaging.models import (
    ContrastAssessment,
    ImagingModality,
    ImagingProcedure,
    ImagingStudy,
    RadiologyReport,
)
from apps.imaging.services.cect import (
    CECTWorkflowError,
    clear_contrast,
    record_contrast_administration,
)
from apps.imaging.services.orders import create_imaging_order
from apps.imaging.services.revenue_cycle import link_charge
from apps.imaging.services.workflow import (
    complete_acquisition,
    finalize_report,
    start_study,
)


class ImagingProductionContractTests(TestCase):
    def setUp(self):
        self.tenant_id = uuid.uuid4()
        self.other_tenant_id = uuid.uuid4()
        self.patient_id = uuid.uuid4()
        self.provider_id = uuid.uuid4()

        modality = ImagingModality.objects.create(
            tenant_id=self.tenant_id,
            code="CT-01",
            name="CT Scanner",
            modality_type="ct",
        )
        procedure = ImagingProcedure.objects.create(
            tenant_id=self.tenant_id,
            procedure_code="CT-CHEST",
            name="CT Chest",
            modality=modality,
            contrast_required=False,
            cect=False,
        )
        order = create_imaging_order(
            tenant_id=self.tenant_id,
            patient_id=self.patient_id,
            clinical_indication="Diagnostic evaluation",
            order_number="ORD-001",
            ordering_provider_id=self.provider_id,
        )
        self.study = ImagingStudy.objects.create(
            tenant_id=self.tenant_id,
            accession_number="ACC-001",
            order=order,
            procedure=procedure,
            patient_id=self.patient_id,
        )

    def test_tenant_scoping_query(self):
        self.assertFalse(
            ImagingStudy.objects.filter(
                tenant_id=self.other_tenant_id, id=self.study.id
            ).exists()
        )

    def test_cect_requires_screening(self):
        assessment = ContrastAssessment.objects.create(
            tenant_id=self.tenant_id,
            study=self.study,
            status=ContrastStatus.SCREENING,
        )
        with self.assertRaises(CECTWorkflowError):
            clear_contrast(
                assessment_id=assessment.id,
                tenant_id=self.tenant_id,
                assessed_by_id=self.provider_id,
            )

    def test_cect_clear_then_administer(self):
        assessment = ContrastAssessment.objects.create(
            tenant_id=self.tenant_id,
            study=self.study,
            status=ContrastStatus.SCREENING,
            allergy_screened=True,
            renal_screened=True,
            pregnancy_screened=True,
        )
        clear_contrast(
            assessment_id=assessment.id,
            tenant_id=self.tenant_id,
            assessed_by_id=self.provider_id,
        )
        assessment.refresh_from_db()
        self.assertEqual(assessment.status, ContrastStatus.CLEARED)

        record_contrast_administration(
            assessment_id=assessment.id,
            tenant_id=self.tenant_id,
            administration_reference="ADMIN-001",
        )
        assessment.refresh_from_db()
        self.assertEqual(assessment.status, ContrastStatus.ADMINISTERED)

    def test_acquisition_lifecycle(self):
        start_study(study_id=self.study.id, tenant_id=self.tenant_id)
        complete_acquisition(
            study_id=self.study.id,
            tenant_id=self.tenant_id,
            acquired_by_id=self.provider_id,
        )
        self.study.refresh_from_db()
        self.assertEqual(self.study.status, ImagingStudyStatus.ACQUIRED)

    def test_final_report_requires_impression(self):
        report = RadiologyReport(
            tenant_id=self.tenant_id,
            study=self.study,
            status=ImagingReportStatus.FINAL,
            impression="",
        )
        with self.assertRaises(ValidationError):
            report.full_clean()

    def test_finalize_report_moves_study_to_final(self):
        report = RadiologyReport.objects.create(
            tenant_id=self.tenant_id,
            study=self.study,
            impression="No acute abnormality.",
        )
        finalize_report(
            report_id=report.id,
            tenant_id=self.tenant_id,
            radiologist_id=self.provider_id,
        )
        report.refresh_from_db()
        self.study.refresh_from_db()
        self.assertEqual(report.status, ImagingReportStatus.FINAL)
        self.assertEqual(self.study.status, ImagingStudyStatus.FINAL)

    def test_charge_link_is_idempotent(self):
        charge_id = uuid.uuid4()
        first = link_charge(
            study_id=self.study.id,
            charge_id=charge_id,
            procedure_code="CT-CHEST-CECT",
            tenant_id=self.tenant_id,
            idempotency_key="charge-001",
        )
        second = link_charge(
            study_id=self.study.id,
            charge_id=charge_id,
            procedure_code="CT-CHEST-CECT",
            tenant_id=self.tenant_id,
            idempotency_key="charge-001",
        )
        self.assertEqual(first.id, second.id)
