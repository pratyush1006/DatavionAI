from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.telemedicine.services import SessionService
from apps.telemedicine.workflows._base import TelemedicineWorkflow


class SessionUpdateWorkflow(TelemedicineWorkflow):
    workflow_name = "telemedicine.session.update"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        result = SessionService.update(
            session_id=payload["session_id"],
            organization_id=payload["organization_id"],
            validated_data=payload["validated_data"],
        )
        return self._ok(
            context,
            data=result,
            message="Telemedicine session updated.",
            code="telemedicine_session_update",
        )
