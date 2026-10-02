def validate_appointment_context(*, appointment, organization_id, patient_id):
    if appointment is None:
        return
    if getattr(appointment, "organization_id", None) != organization_id:
        raise ValueError("Appointment belongs to another organization.")
    if getattr(appointment, "patient_id", None) and str(appointment.patient_id) != str(
        patient_id
    ):
        raise ValueError("Appointment belongs to another patient.")
