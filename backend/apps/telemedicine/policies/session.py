from apps.telemedicine.constants import SessionStatus


class SessionPolicy:
    @staticmethod
    def can_view(*, actor, session) -> bool:
        return bool(
            actor
            and actor.is_authenticated
            and session.organization_id == getattr(actor, "organization_id", None)
        )

    @staticmethod
    def can_mutate(*, actor, session) -> bool:
        return SessionPolicy.can_view(
            actor=actor, session=session
        ) and session.status not in {
            SessionStatus.COMPLETED,
            SessionStatus.CANCELLED,
            SessionStatus.NO_SHOW,
            SessionStatus.FAILED,
        }

    @staticmethod
    def can_start(*, actor, session) -> bool:
        return (
            SessionPolicy.can_view(actor=actor, session=session)
            and session.status == SessionStatus.READY
        )

    @staticmethod
    def can_complete(*, actor, session) -> bool:
        return (
            SessionPolicy.can_view(actor=actor, session=session)
            and session.status == SessionStatus.IN_PROGRESS
        )

    @staticmethod
    def can_cancel(*, actor, session) -> bool:
        return SessionPolicy.can_view(
            actor=actor, session=session
        ) and session.status in {
            SessionStatus.SCHEDULED,
            SessionStatus.CONFIRMED,
            SessionStatus.READY,
            SessionStatus.IN_PROGRESS,
        }
