from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.telemedicine.constants import ParticipantStatus
from apps.telemedicine.services import ParticipantService
from apps.telemedicine.workflows._base import TelemedicineWorkflow


class ParticipantJoinWorkflow(TelemedicineWorkflow):
    workflow_name = "telemedicine.participant.join"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        result = ParticipantService.transition(
            participant_id=payload["participant_id"],
            organization_id=payload["organization_id"],
            target_status=ParticipantStatus.JOINED,
        )
        return self._ok(
            context,
            data=result,
            message="Telemedicine operation completed.",
            code="telemedicine_participant_join",
        )
