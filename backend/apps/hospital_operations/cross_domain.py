"""Concrete adapters for executing canonical cross-domain workflow."""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from uuid import uuid4

from django.utils import timezone


def create_encounter(*, organization, patient, provider, appointment):
    from apps.clinical.encounters.constants import EncounterStatus
    from apps.clinical.encounters.models import Encounter

    return Encounter.objects.create(
        organization=organization,
        appointment=appointment,
        patient=patient,
        provider=provider,
        encounter_number=f"HOP-E2E-{uuid4().hex[:12].upper()}",
        status=EncounterStatus.IN_PROGRESS,
        chief_complaint="Hospital Operations E2E",
        history_of_present_illness="",
        assessment="",
        plan="",
        clinical_notes="Cross-domain workflow certification",
        duration_minutes=0,
        is_billable=True,
    )


def create_laboratory_order(*, organization, patient, provider, encounter):
    from apps.clinical.laboratories.constants import (
        LaboratoryOrderStatus,
        LaboratoryPriority,
    )
    from apps.clinical.laboratories.models import Laboratory, LaboratoryOrder

    laboratory = Laboratory.objects.create(
        organization=organization,
        code=f"HOP-LAB-{uuid4().hex[:8].upper()}",
        name="Hospital Operations E2E Laboratory",
        description="",
        phone="",
        email="",
        address={},
        timezone="UTC",
        status="active",
        appointment_enabled=True,
        home_collection_enabled=False,
    )
    return LaboratoryOrder.objects.create(
        organization=organization,
        patient=patient,
        provider=provider,
        encounter=encounter,
        laboratory=laboratory,
        order_number=f"HOP-LAB-{uuid4().hex[:10].upper()}",
        priority=LaboratoryPriority.ROUTINE,
        status=LaboratoryOrderStatus.ORDERED,
        ordered_at=timezone.now(),
        clinical_notes="Hospital Operations E2E",
        instructions="",
    )


def create_imaging_order(*, tenant, patient, provider, encounter):
    from apps.imaging.services.orders import create_imaging_order

    return create_imaging_order(
        tenant_id=tenant.id,
        patient_id=patient.id,
        encounter_id=encounter.id,
        clinical_indication="Hospital Operations E2E imaging",
        order_number=f"HOP-IMG-{uuid4().hex[:10].upper()}",
        ordering_provider_id=provider.id,
        priority="routine",
        actor_id=provider.id,
    )


def create_pharmacy_order(*, organization, patient, provider, encounter):
    from apps.clinical.medications.constants import (
        MedicationDosageForm,
        MedicationRoute,
    )
    from apps.clinical.medications.models import Medication
    from apps.clinical.prescriptions.constants import (
        PrescriptionFrequency,
        PrescriptionStatus,
    )
    from apps.clinical.prescriptions.models import Prescription
    from apps.pharmacy.models import MedicationBatch, Pharmacy, PharmacyProduct
    from apps.pharmacy.services.dispensing import create_dispensing_order

    medication = Medication.objects.create(
        organization=organization,
        medication_code=f"HOP-MED-{uuid4().hex[:8].upper()}",
        generic_name="Amoxicillin",
        brand_name="Amoxicillin",
        strength="500",
        strength_unit="mg",
        dosage_form=MedicationDosageForm.TABLET,
        route=MedicationRoute.ORAL,
        manufacturer="Datavion E2E",
        description="",
        is_controlled=False,
    )
    prescription = Prescription.objects.create(
        organization=organization,
        patient=patient,
        provider=provider,
        encounter=encounter,
        medication=medication,
        prescription_number=f"HOP-RX-{uuid4().hex[:10].upper()}",
        status=PrescriptionStatus.ACTIVE,
        dosage=1,
        dosage_unit="tablet",
        frequency=PrescriptionFrequency.THREE_TIMES_DAILY,
        quantity=3,
        duration_days=1,
        refills=0,
        start_date=timezone.localdate(),
        end_date=timezone.localdate(),
        instructions="E2E test prescription.",
        is_prn=False,
        notes="Hospital Operations E2E",
    )
    pharmacy = Pharmacy.objects.create(
        organization=organization,
        code=f"HOP-PH-{uuid4().hex[:8].upper()}",
        name="Hospital Operations E2E Pharmacy",
    )
    product = PharmacyProduct.objects.create(
        organization=organization,
        pharmacy=pharmacy,
        medication=medication,
        sku=f"HOP-SKU-{uuid4().hex[:8].upper()}",
        selling_price=Decimal("10.00"),
    )
    batch = MedicationBatch.objects.create(
        product=product,
        batch_number=f"HOP-BATCH-{uuid4().hex[:8].upper()}",
        expiry_date=timezone.localdate() + timedelta(days=180),
    )
    return create_dispensing_order(
        organization=organization,
        pharmacy=pharmacy,
        prescription=prescription,
        dispense_number=f"HOP-DISP-{uuid4().hex[:10].upper()}",
        lines=[
            {
                "product": product,
                "batch": batch,
                "quantity_prescribed": Decimal("1"),
                "quantity_dispensed": Decimal("0"),
            }
        ],
    )


def create_rcm_charge(*, actor, tenant, organization, patient):
    from apps.revenue_cycle.charge_capture.services import ChargeCaptureService

    return ChargeCaptureService.create(
        actor=actor,
        tenant_id=tenant.id,
        organization=organization,
        patient=patient,
        service_code="HOP-E2E",
        description="Hospital Operations E2E operational charge",
        quantity=Decimal("1"),
        unit_price=Decimal("100.00"),
        idempotency_key=f"HOP-RCM-{uuid4().hex}",
    )


def execute_notification(*, patient):
    from apps.common.notifications.channels import InAppNotificationChannel
    from apps.common.notifications.models import Notification, NotificationRecipient

    notification = Notification(
        name="HOSPITAL_OPERATIONS_E2E",
        channel="in_app",
        recipient=NotificationRecipient(
            recipient_id=str(patient.id), name="Hospital Operations E2E"
        ),
        payload={"patient_id": str(patient.id), "workflow": "hospital_operations"},
    )
    return InAppNotificationChannel().send(notification)


def execute_audit(*, organization, actor, admission):
    from apps.platform.audit.services.audit import AuditService

    return AuditService.log_create(
        organization=organization,
        user=actor,
        module="hospital_operations",
        object_type="Admission",
        object_id=str(admission.id),
        new_values={"admission_id": str(admission.id), "workflow": "cross_domain_e2e"},
    )


def execute_ai(*, tenant, organization, patient, admission):
    from apps.ai.models import AIModuleReference
    from apps.ai.services.chat import generate
    from apps.ai.services.registry import ensure_department_applications

    application = ensure_department_applications(
        tenant=tenant, organization=organization
    )[0]
    reference = AIModuleReference.objects.create(
        tenant=tenant,
        organization=organization,
        module_code="hospital_operations",
        resource_type="admission",
        resource_id=str(admission.id),
        patient_id=patient.id,
        metadata={"capability": "patient_flow_summary", "advisory_only": True},
    )
    return generate(
        application=application,
        tenant=tenant,
        organization=organization,
        module_reference=reference,
        messages=[
            {
                "role": "user",
                "content": "Summarize operational patient flow for this admission.",
            }
        ],
        provider_name="mock",
    )
