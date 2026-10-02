from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.telemedicine.services import ParticipantService
from apps.telemedicine.workflows._base import TelemedicineWorkflow


class ParticipantInvitationWorkflow(TelemedicineWorkflow):
    workflow_name = "telemedicine.participant.invite"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        result = ParticipantService.invite(
            session_id=payload["session_id"],
            user_id=payload["user_id"],
            participant_type=payload["participant_type"],
            organization_id=payload["organization_id"],
        )
        return self._ok(
            context,
            data=result,
            message="Telemedicine operation completed.",
            code="telemedicine_participant_invite",
        )
