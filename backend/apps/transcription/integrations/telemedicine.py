"""Telemedicine integration; session ownership remains apps.telemedicine."""

from apps.telemedicine.models import TelemedicineSession


def validate_telemedicine_session(*, organization_id, session_id, patient_id):
    s = TelemedicineSession.objects.filter(pk=session_id).first()
    if s is None:
        raise ValueError("Telemedicine session was not found.")
    if getattr(s, "organization_id", None) != organization_id:
        raise ValueError("Telemedicine session belongs to another organization.")
    if getattr(s, "patient_id", None) and str(s.patient_id) != str(patient_id):
        raise ValueError("Telemedicine session belongs to another patient.")
    return {"session_id": str(s.pk), "status": getattr(s, "status", "")}
