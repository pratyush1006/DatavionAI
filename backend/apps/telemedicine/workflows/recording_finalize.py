from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.telemedicine.services import RecordingService
from apps.telemedicine.workflows._base import TelemedicineWorkflow


class RecordingFinalizeWorkflow(TelemedicineWorkflow):
    workflow_name = "telemedicine.recording.finalize"

    def _run(self, *, context: WorkflowContext) -> WorkflowResult:
        payload = self.payload
        result = RecordingService.finalize(
            recording_id=payload["recording_id"],
            organization_id=payload["organization_id"],
            recording_url=payload["recording_url"],
            duration_seconds=payload.get("duration_seconds"),
            file_size_bytes=payload.get("file_size_bytes"),
            transcript_url=payload.get("transcript_url", ""),
        )
        return self._ok(
            context,
            data=result,
            message="Telemedicine operation completed.",
            code="telemedicine_recording_finalize",
        )
