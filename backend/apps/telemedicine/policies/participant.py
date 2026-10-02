class ParticipantPolicy:
    @staticmethod
    def can_manage(*, actor, participant) -> bool:
        return bool(
            actor
            and actor.is_authenticated
            and participant.session.organization_id
            == getattr(actor, "organization_id", None)
        )
