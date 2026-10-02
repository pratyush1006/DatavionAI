from __future__ import annotations

from apps.imaging.constants.choices import ContrastStatus, ImagingStudyStatus
from apps.imaging.models import ContrastAssessment, ImagingStudy
from apps.imaging.workflow_registry import STUDY_TRANSITIONS
from apps.imaging.workflows.engine import transition


def transition_study(*, study_id, tenant_id, target_state, actor_id=None, reason=""):
    study = ImagingStudy.objects.select_related("procedure").get(
        id=study_id, tenant_id=tenant_id
    )

    def guard(current, target):
        if target != ImagingStudyStatus.ACQUIRING or not study.procedure.cect:
            return
        assessment = ContrastAssessment.objects.filter(
            tenant_id=study.tenant_id, study_id=study.id
        ).first()
        if assessment is None:
            raise ValueError(
                "CECT study requires contrast screening before acquisition."
            )
        if assessment.status != ContrastStatus.ADMINISTERED:
            raise ValueError(
                "CECT study requires cleared and administered contrast before acquisition."
            )

    def sync(state):
        study.status = state
        study.save(update_fields=["status", "updated_at"])

    return transition(
        tenant_id=tenant_id,
        entity_type="ImagingStudy",
        entity_id=study.id,
        target_state=target_state,
        graph=STUDY_TRANSITIONS,
        actor_id=actor_id,
        reason=reason,
        state_model=study.status,
        guard=guard,
        sync=sync,
    )
