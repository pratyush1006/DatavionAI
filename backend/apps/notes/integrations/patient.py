from __future__ import annotations

from django.apps import apps


def get_patient(*, patient_id, organization_id):
    Patient = apps.get_model("patient_core", "Patient")
    patient = Patient.objects.filter(
        pk=patient_id, organization_id=organization_id
    ).first()
    if patient is None:
        raise ValueError("Patient was not found in the organization.")
    return patient
