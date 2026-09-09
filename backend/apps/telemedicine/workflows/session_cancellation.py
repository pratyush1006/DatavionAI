from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.telemedicine.constants import SessionStatus
from apps.telemedicine.services import SessionService
from apps.telemedicine.workflows._base import TelemedicineWorkflow


class SessionCancellationWorkflow(TelemedicineWorkflow):
    workflow_name = "telemedicine.session.cancel"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        result = SessionService.transition(
            session_id=payload["session_id"],
            target_status=SessionStatus.CANCELLED,
            organization_id=payload["organization_id"],
            cancellation_reason=payload.get("cancellation_reason", ""),
        )
        return self._ok(
            context,
            data=result,
            message="Telemedicine operation completed.",
            code="telemedicine_session_cancel",
        )
