import uuid

from django.db import transaction

from apps.patient_management.patients.models import Patient

from ..models import Laboratory, LaboratoryOrder, LaboratoryOrderItem, LaboratoryTest
from .audit import audit
from .events import event
from .idempotency import get_or_create_request
from .laboratory import LaboratoryServiceError


@transaction.atomic
def create_order(
    *,
    organization_id,
    patient_id,
    laboratory_id,
    tests,
    appointment_id=None,
    encounter_id=None,
    ordering_provider_id=None,
    priority="routine",
    clinical_indication="",
    actor_id=None,
    idempotency_key=None,
):
    if not tests:
        raise LaboratoryServiceError("At least one test is required.")
    patient = Patient.objects.get(id=patient_id, organization_id=organization_id)
    lab = Laboratory.objects.get(
        id=laboratory_id, organization_id=organization_id, is_deleted=False
    )
    if idempotency_key:
        existing, created = get_or_create_request(
            organization_id=organization_id,
            key=idempotency_key,
            operation="create_order",
        )
        if not created and existing.resource_id:
            return LaboratoryOrder.objects.get(
                id=existing.resource_id,
                organization_id=organization_id,
                is_deleted=False,
            )
    appointment = None
    if appointment_id:
        from apps.clinical.appointments.models import Appointment

        appointment = Appointment.objects.get(
            id=appointment_id, organization_id=organization_id, is_deleted=False
        )
        if str(appointment.patient_id) != str(patient.id):
            raise LaboratoryServiceError(
                "Appointment patient does not match laboratory order patient."
            )
    resolved, seen = [], set()
    for value in tests:
        test = (
            value
            if isinstance(value, LaboratoryTest)
            else LaboratoryTest.objects.get(
                id=value, organization_id=organization_id, is_deleted=False
            )
        )
        if test.id in seen:
            raise LaboratoryServiceError(
                "Duplicate laboratory tests are not allowed in an order."
            )
        if test.status != "active":
            raise LaboratoryServiceError("Inactive laboratory tests cannot be ordered.")
        seen.add(test.id)
        resolved.append(test)
    order = LaboratoryOrder.objects.create(
        organization_id=organization_id,
        patient=patient,
        laboratory=lab,
        appointment=appointment,
        encounter_id=encounter_id,
        ordering_provider_id=ordering_provider_id,
        order_number=f"ORD-{uuid.uuid4().hex[:12].upper()}",
        status="ordered",
        priority=priority,
        clinical_indication=clinical_indication,
    )
    for test in resolved:
        LaboratoryOrderItem.objects.create(
            order=order, test=test, price=test.price, instructions=test.instructions
        )
    if idempotency_key:
        existing.resource_type = "LaboratoryOrder"
        existing.resource_id = order.id
        existing.response_payload = {"order_id": str(order.id)}
        existing.save(
            update_fields=[
                "resource_type",
                "resource_id",
                "response_payload",
                "updated_at",
            ]
        )
    audit(organization_id, actor_id, "order.created", "LaboratoryOrder", order.id)
    event(organization_id, "laboratory.order.created", "LaboratoryOrder", order.id)
    return order
