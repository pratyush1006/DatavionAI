from django.db.models import QuerySet

from apps.telemedicine.models import Recording


class RecordingSelector:
    @staticmethod
    def queryset(*, organization_id=None) -> QuerySet[Recording]:
        qs = Recording.objects.select_related("session", "session__organization")
        if organization_id is not None:
            qs = qs.filter(session__organization_id=organization_id)
        return qs

    @classmethod
    def get(cls, *, recording_id, organization_id=None) -> Recording:
        return cls.queryset(organization_id=organization_id).get(
            recording_id=recording_id
        )
