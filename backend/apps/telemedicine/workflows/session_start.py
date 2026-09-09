from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.telemedicine.constants import SessionStatus
from apps.telemedicine.services import SessionService
from apps.telemedicine.workflows._base import TelemedicineWorkflow


class SessionStartWorkflow(TelemedicineWorkflow):
    workflow_name = "telemedicine.session.start"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        result = SessionService.transition(
            session_id=payload["session_id"],
            target_status=SessionStatus.IN_PROGRESS,
            organization_id=payload["organization_id"],
        )
        return self._ok(
            context,
            data=result,
            message="Telemedicine operation completed.",
            code="telemedicine_session_start",
        )
