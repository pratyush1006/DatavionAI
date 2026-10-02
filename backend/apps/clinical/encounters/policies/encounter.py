from apps.clinical.encounters.permissions import EncounterPermission


class EncounterPolicy:
    def can_view(self, *, actor, organization):
        return EncounterPermission.has(
            user=actor, permission=EncounterPermission.VIEW, organization=organization
        )

    def can_create(self, *, actor, organization):
        return EncounterPermission.has(
            user=actor, permission=EncounterPermission.CREATE, organization=organization
        )

    def can_update(self, *, actor, organization):
        return EncounterPermission.has(
            user=actor, permission=EncounterPermission.UPDATE, organization=organization
        )

    def can_delete(self, *, actor, organization):
        return EncounterPermission.has(
            user=actor, permission=EncounterPermission.DELETE, organization=organization
        )

    def can_transition(self, *, actor, organization):
        return EncounterPermission.has(
            user=actor,
            permission=EncounterPermission.TRANSITION,
            organization=organization,
        )
