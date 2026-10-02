from apps.clinical.diagnoses.permissions import DiagnosisPermission


class DiagnosisPolicy:
    def can_view(self, *, actor, organization):
        return DiagnosisPermission.has(
            user=actor, permission=DiagnosisPermission.VIEW, organization=organization
        )

    def can_create(self, *, actor, organization):
        return DiagnosisPermission.has(
            user=actor, permission=DiagnosisPermission.CREATE, organization=organization
        )

    def can_update(self, *, actor, organization):
        return DiagnosisPermission.has(
            user=actor, permission=DiagnosisPermission.UPDATE, organization=organization
        )

    def can_delete(self, *, actor, organization):
        return DiagnosisPermission.has(
            user=actor, permission=DiagnosisPermission.DELETE, organization=organization
        )
