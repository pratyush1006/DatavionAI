from apps.imaging.models import ImagingDocumentLink


def document_links(*, tenant_id, study_id):
    return ImagingDocumentLink.objects.filter(
        tenant_id=tenant_id, study_id=study_id
    ).order_by("created_at")
