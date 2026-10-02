def validate_encounter_context(*, encounter, organization_id, patient_id):
    if (
        encounter is not None
        and getattr(encounter, "organization_id", None) != organization_id
    ):
        raise ValueError("Encounter belongs to another organization.")
