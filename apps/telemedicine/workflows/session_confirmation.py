from apps.core.workflows import WorkflowContext,WorkflowResult
from apps.telemedicine.workflows._base import TelemedicineWorkflow
from apps.telemedicine.services import SessionService
from apps.telemedicine.constants import SessionStatus

class SessionConfirmationWorkflow(TelemedicineWorkflow):
 workflow_name="telemedicine.session.confirm"
 def _run(self,*,context:WorkflowContext)->WorkflowResult:
  payload=self.payload; result=SessionService.transition(session_id=payload["session_id"],target_status=SessionStatus.CONFIRMED,organization_id=payload["organization_id"]); return self._ok(context,data=result,message="Telemedicine operation completed.",code="telemedicine_session_confirm")
