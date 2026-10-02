"""Clinical Notes integration; canonical note ownership remains apps.notes."""

from apps.notes.models import ClinicalNote


def create_clinical_note(
    *, organization, patient, encounter, title, content, metadata=None
):
    names = {f.name for f in ClinicalNote._meta.get_fields()}
    kwargs = {"organization": organization, "patient": patient}
    if "encounter" in names:
        kwargs["encounter"] = encounter
    if "title" in names:
        kwargs["title"] = title
    if "content" in names:
        kwargs["content"] = content
    elif "body" in names:
        kwargs["body"] = content
    if "metadata" in names:
        kwargs["metadata"] = metadata or {}
    return ClinicalNote.objects.create(**kwargs)
