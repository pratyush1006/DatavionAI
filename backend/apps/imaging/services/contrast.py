from apps.imaging.models import ContrastAssessment


def latest_assessment(*, tenant_id, study_id):
    return (
        ContrastAssessment.objects.filter(tenant_id=tenant_id, study_id=study_id)
        .order_by("-created_at")
        .first()
    )
