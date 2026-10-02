from apps.clinical.encounters.models import Encounter


def get_encounters(*, organization_id, include_deleted=False):
    manager = Encounter.all_objects if include_deleted else Encounter.objects
    return manager.filter(organization_id=organization_id).select_related(
        "organization", "appointment", "patient", "provider"
    )


def get_encounter(*, organization_id, encounter_id, include_deleted=False):
    return get_encounters(
        organization_id=organization_id,
        include_deleted=include_deleted,
    ).get(pk=encounter_id)
