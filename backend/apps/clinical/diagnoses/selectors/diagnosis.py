from apps.clinical.diagnoses.models import Diagnosis


def get_diagnoses(*, organization_id, encounter_id=None, include_deleted=False):
    manager = Diagnosis.all_objects if include_deleted else Diagnosis.objects
    queryset = manager.filter(organization_id=organization_id).select_related(
        "organization",
        "encounter",
        "encounter__patient",
        "encounter__provider",
    )
    if encounter_id is not None:
        queryset = queryset.filter(encounter_id=encounter_id)
    return queryset


def get_diagnosis(*, organization_id, diagnosis_id, include_deleted=False):
    return get_diagnoses(
        organization_id=organization_id,
        include_deleted=include_deleted,
    ).get(pk=diagnosis_id)
