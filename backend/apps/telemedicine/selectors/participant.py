from django.db.models import QuerySet

from apps.telemedicine.models import Participant


class ParticipantSelector:
    @staticmethod
    def queryset(*, organization_id=None) -> QuerySet[Participant]:
        qs = Participant.objects.select_related(
            "session", "user", "session__organization"
        )
        if organization_id is not None:
            qs = qs.filter(session__organization_id=organization_id)
        return qs

    @classmethod
    def get(cls, *, participant_id, organization_id=None) -> Participant:
        return cls.queryset(organization_id=organization_id).get(pk=participant_id)

    @classmethod
    def for_update(cls, *, participant_id, organization_id=None) -> Participant:
        return (
            cls.queryset(organization_id=organization_id)
            .select_for_update()
            .get(pk=participant_id)
        )
