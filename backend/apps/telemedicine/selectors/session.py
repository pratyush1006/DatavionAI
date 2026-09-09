from django.db.models import QuerySet

from apps.telemedicine.models import TelemedicineSession


class SessionSelector:
    @staticmethod
    def queryset(*, organization_id=None) -> QuerySet[TelemedicineSession]:
        qs = TelemedicineSession.objects.select_related(
            "organization", "patient", "provider", "appointment"
        )
        if organization_id is not None:
            qs = qs.filter(organization_id=organization_id)
        return qs

    @classmethod
    def get(cls, *, session_id, organization_id=None) -> TelemedicineSession:
        return cls.queryset(organization_id=organization_id).get(session_id=session_id)

    @classmethod
    def for_update(cls, *, session_id, organization_id=None) -> TelemedicineSession:
        return (
            cls.queryset(organization_id=organization_id)
            .select_for_update()
            .get(session_id=session_id)
        )
