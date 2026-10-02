class RecordingPolicy:
    @staticmethod
    def can_manage(*, actor, recording) -> bool:
        return bool(
            actor
            and actor.is_authenticated
            and recording.session.organization_id
            == getattr(actor, "organization_id", None)
        )
