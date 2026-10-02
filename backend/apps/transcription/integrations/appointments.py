def validate_appointment_context(*, appointment, organization_id, patient_id):
    if (
        appointment is not None
        and getattr(appointment, "organization_id", None) != organization_id
    ):
        raise ValueError("Appointment belongs to another organization.")
