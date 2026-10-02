from apps.core.workflows import WorkflowContext,WorkflowResult
from apps.telemedicine.workflows._base import TelemedicineWorkflow
from apps.telemedicine.services import ParticipantService
from apps.telemedicine.constants import ParticipantStatus

class ParticipantLeaveWorkflow(TelemedicineWorkflow):
 workflow_name="telemedicine.participant.leave"
 def _run(self,*,context:WorkflowContext)->WorkflowResult:
  payload=self.payload; result=ParticipantService.transition(participant_id=payload["participant_id"],organization_id=payload["organization_id"],target_status=ParticipantStatus.LEFT); return self._ok(context,data=result,message="Telemedicine operation completed.",code="telemedicine_participant_leave")
