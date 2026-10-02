from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.telemedicine.services import RecordingService
from apps.telemedicine.workflows._base import TelemedicineWorkflow


class RecordingStartWorkflow(TelemedicineWorkflow):
    workflow_name = "telemedicine.recording.start"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        result = RecordingService.start(
            session_id=payload["session_id"], organization_id=payload["organization_id"]
        )
        return self._ok(
            context,
            data=result,
            message="Telemedicine operation completed.",
            code="telemedicine_recording_start",
        )
