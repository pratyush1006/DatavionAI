from __future__ import annotations


def validate_telemedicine_context(*, organization_id, patient_id, session_id):
    if not session_id:
        return None
    try:
        from apps.telemedicine.models import TelemedicineSession

        session = TelemedicineSession.objects.filter(pk=session_id).first()
    except Exception:
        session = None
    if session is None:
        raise ValueError("Telemedicine session was not found.")
    if getattr(session, "organization_id", None) != organization_id:
        raise ValueError("Telemedicine session belongs to another organization.")
    if getattr(session, "patient_id", None) and str(session.patient_id) != str(
        patient_id
    ):
        raise ValueError("Telemedicine session belongs to another patient.")
    return session
