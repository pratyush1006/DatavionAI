from ..models import LaboratorySpecimen
from ..workflow_registry import SPECIMEN_TRANSITIONS
from .engine import transition


def transition_specimen(
    *, specimen_id, organization_id, target_state, actor_id=None, reason=""
):
    specimen = LaboratorySpecimen.objects.get(
        id=specimen_id,
        organization_id=organization_id,
        is_deleted=False,
    )

    def sync(state):
        specimen.status = state
        specimen.save(update_fields=["status", "updated_at"])

    return transition(
        organization_id=organization_id,
        workflow="specimen",
        entity_type="LaboratorySpecimen",
        entity_id=specimen.id,
        target_state=target_state,
        graph=SPECIMEN_TRANSITIONS,
        actor_id=actor_id,
        reason=reason,
        state_model=specimen.status,
        sync=sync,
    )
