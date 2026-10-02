from apps.notes.constants import NoteStatus
from apps.notes.rbac import has_permission


class ClinicalNotePolicy:
    @staticmethod
    def same_org(*, actor, note):
        return bool(
            actor
            and actor.is_authenticated
            and note.organization_id == getattr(actor, "organization_id", None)
        )

    @classmethod
    def can_view(cls, *, actor, note):
        return cls.same_org(actor=actor, note=note) and has_permission(
            user=actor, organization=note.organization, permission="notes.view"
        )

    @classmethod
    def can_edit(cls, *, actor, note):
        return (
            cls.can_view(actor=actor, note=note)
            and note.status in {NoteStatus.DRAFT, NoteStatus.IN_REVIEW}
            and has_permission(
                user=actor, organization=note.organization, permission="notes.update"
            )
        )

    @classmethod
    def can_review(cls, *, actor, note):
        return (
            cls.can_view(actor=actor, note=note)
            and note.status == NoteStatus.DRAFT
            and has_permission(
                user=actor, organization=note.organization, permission="notes.approve"
            )
        )

    @classmethod
    def can_sign(cls, *, actor, note):
        return (
            cls.can_view(actor=actor, note=note)
            and note.status == NoteStatus.IN_REVIEW
            and has_permission(
                user=actor, organization=note.organization, permission="notes.sign"
            )
        )

    @classmethod
    def can_amend(cls, *, actor, note):
        return (
            cls.can_view(actor=actor, note=note)
            and note.status in {NoteStatus.SIGNED, NoteStatus.AMENDED}
            and has_permission(
                user=actor, organization=note.organization, permission="notes.update"
            )
        )
