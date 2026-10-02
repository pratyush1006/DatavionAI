def validate_encounter_context(*, encounter, organization_id, patient_id):
    if encounter is None:
        return
    if getattr(encounter, "organization_id", None) != organization_id:
        raise ValueError("Encounter belongs to another organization.")
    if getattr(encounter, "patient_id", None) and str(encounter.patient_id) != str(
        patient_id
    ):
        raise ValueError("Encounter belongs to another patient.")
