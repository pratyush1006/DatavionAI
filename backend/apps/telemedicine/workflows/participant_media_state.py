from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.telemedicine.services import ParticipantService
from apps.telemedicine.workflows._base import TelemedicineWorkflow


class ParticipantMediaStateWorkflow(TelemedicineWorkflow):
    workflow_name = "telemedicine.participant.media_state"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        p = self.payload
        result = ParticipantService.update_media_state(
            participant_id=p["participant_id"],
            organization_id=p["organization_id"],
            data=p["data"],
        )
        return self._ok(
            context,
            data=result,
            message="Participant media state updated.",
            code="telemedicine_participant_media_updated",
        )
