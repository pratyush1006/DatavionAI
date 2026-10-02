from __future__ import annotations

import uuid

from django.test import TestCase

from apps.imaging.constants.choices import (
    ContrastStatus,
    ImagingOrderStatus,
    ImagingStudyStatus,
)
from apps.imaging.models import (
    ContrastAssessment,
    ImagingModality,
    ImagingProcedure,
    ImagingWorkflowState,
    ImagingWorkflowTransition,
    RadiologyReport,
)
from apps.imaging.services.cect import clear_contrast, record_contrast_administration
from apps.imaging.services.orders import create_imaging_order
from apps.imaging.services.studies import create_study
from apps.imaging.services.workflow import (
    complete_acquisition,
    complete_order,
    finalize_report,
    mark_order_ready,
    mark_study_arrived,
    mark_study_ready,
    move_to_interpretation,
    schedule_order,
    start_order,
    start_study,
)


class ImagingWorkflowTests(TestCase):
    def setUp(self):
        self.tenant_id = uuid.uuid4()
        self.other_tenant_id = uuid.uuid4()
        self.patient_id = uuid.uuid4()
        self.actor_id = uuid.uuid4()
        modality = ImagingModality.objects.create(
            tenant_id=self.tenant_id,
            code="CT-01",
            name="CT Scanner",
            modality_type="ct",
        )
        self.procedure = ImagingProcedure.objects.create(
            tenant_id=self.tenant_id,
            procedure_code="CT-CHEST-CECT",
            name="CT Chest with Contrast",
            modality=modality,
            contrast_required=True,
            cect=True,
        )
        self.order = create_imaging_order(
            tenant_id=self.tenant_id,
            patient_id=self.patient_id,
            clinical_indication="Diagnostic evaluation",
            order_number="WF-ORD-001",
            ordering_provider_id=self.actor_id,
        )

    def _schedule(self):
        mark_order_ready(order_id=self.order.id, tenant_id=self.tenant_id)
        schedule_order(order_id=self.order.id, tenant_id=self.tenant_id)

    def test_order_workflow_is_stateful_and_audited(self):
        self._schedule()
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, ImagingOrderStatus.SCHEDULED)
        state = ImagingWorkflowState.objects.get(
            tenant_id=self.tenant_id,
            entity_type="ImagingOrder",
            entity_id=self.order.id,
        )
        self.assertEqual(state.current_state, "scheduled")
        self.assertEqual(state.version, 3)
        self.assertEqual(
            ImagingWorkflowTransition.objects.filter(
                tenant_id=self.tenant_id,
                entity_type="ImagingOrder",
                entity_id=self.order.id,
            ).count(),
            2,
        )

    def test_illegal_order_transition_rejected(self):
        from apps.imaging.workflows.engine import WorkflowEngineError

        with self.assertRaises(WorkflowEngineError):
            complete_order(order_id=self.order.id, tenant_id=self.tenant_id)

    def test_cect_blocks_acquisition_until_administered(self):
        self._schedule()
        study = create_study(
            tenant_id=self.tenant_id,
            order_id=self.order.id,
            procedure_id=self.procedure.id,
            accession_number="WF-ACC-001",
        )
        mark_study_arrived(study_id=study.id, tenant_id=self.tenant_id)
        mark_study_ready(study_id=study.id, tenant_id=self.tenant_id)
        with self.assertRaises(ValueError):
            start_study(study_id=study.id, tenant_id=self.tenant_id)
        assessment = ContrastAssessment.objects.create(
            tenant_id=self.tenant_id,
            study=study,
            status=ContrastStatus.SCREENING,
            allergy_screened=True,
            renal_screened=True,
            pregnancy_screened=True,
        )
        clear_contrast(
            assessment_id=assessment.id,
            tenant_id=self.tenant_id,
            assessed_by_id=self.actor_id,
        )
        record_contrast_administration(
            assessment_id=assessment.id,
            tenant_id=self.tenant_id,
            administration_reference="CECT-ADMIN-001",
            actor_id=self.actor_id,
        )
        start_study(study_id=study.id, tenant_id=self.tenant_id)
        complete_acquisition(
            study_id=study.id, tenant_id=self.tenant_id, acquired_by_id=self.actor_id
        )
        study.refresh_from_db()
        self.assertEqual(study.status, ImagingStudyStatus.ACQUIRED)

    def test_full_clinical_reporting_path(self):
        self._schedule()
        study = create_study(
            tenant_id=self.tenant_id,
            order_id=self.order.id,
            procedure_id=self.procedure.id,
            accession_number="WF-ACC-002",
        )
        mark_study_arrived(study_id=study.id, tenant_id=self.tenant_id)
        mark_study_ready(study_id=study.id, tenant_id=self.tenant_id)
        assessment = ContrastAssessment.objects.create(
            tenant_id=self.tenant_id,
            study=study,
            status=ContrastStatus.SCREENING,
            allergy_screened=True,
            renal_screened=True,
            pregnancy_screened=True,
        )
        clear_contrast(
            assessment_id=assessment.id,
            tenant_id=self.tenant_id,
            assessed_by_id=self.actor_id,
        )
        record_contrast_administration(
            assessment_id=assessment.id, tenant_id=self.tenant_id
        )
        start_study(study_id=study.id, tenant_id=self.tenant_id)
        complete_acquisition(study_id=study.id, tenant_id=self.tenant_id)
        move_to_interpretation(study_id=study.id, tenant_id=self.tenant_id)
        report = RadiologyReport.objects.create(
            tenant_id=self.tenant_id, study=study, impression="No acute abnormality."
        )
        finalize_report(
            report_id=report.id, tenant_id=self.tenant_id, radiologist_id=self.actor_id
        )
        start_order(order_id=self.order.id, tenant_id=self.tenant_id)
        complete_order(order_id=self.order.id, tenant_id=self.tenant_id)
        report.refresh_from_db()
        study.refresh_from_db()
        self.order.refresh_from_db()
        self.assertEqual(report.status, "final")
        self.assertEqual(study.status, ImagingStudyStatus.FINAL)
        self.assertEqual(self.order.status, ImagingOrderStatus.COMPLETED)

    def test_tenant_boundary_blocks_workflow_access(self):
        from django.core.exceptions import ObjectDoesNotExist

        with self.assertRaises(ObjectDoesNotExist):
            mark_order_ready(order_id=self.order.id, tenant_id=self.other_tenant_id)
