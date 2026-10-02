from apps.imaging.services.cect import clear_contrast, record_contrast_administration


def clear_cect_contrast(*, assessment_id, tenant_id, assessed_by_id):
    return clear_contrast(
        assessment_id=assessment_id, tenant_id=tenant_id, assessed_by_id=assessed_by_id
    )


def administer_cect_contrast(
    *, assessment_id, tenant_id, administration_reference="", actor_id=None
):
    return record_contrast_administration(
        assessment_id=assessment_id,
        tenant_id=tenant_id,
        administration_reference=administration_reference,
        actor_id=actor_id,
    )
