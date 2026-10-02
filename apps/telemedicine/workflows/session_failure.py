from apps.core.workflows import WorkflowContext,WorkflowResult
from apps.telemedicine.workflows._base import TelemedicineWorkflow
from apps.telemedicine.services import SessionService
from apps.telemedicine.constants import SessionStatus

class SessionFailureWorkflow(TelemedicineWorkflow):
 workflow_name="telemedicine.session.fail"
 def _run(self,*,context:WorkflowContext)->WorkflowResult:
  payload=self.payload; result=SessionService.transition(session_id=payload["session_id"],target_status=SessionStatus.FAILED,organization_id=payload["organization_id"],failure_reason=payload.get("failure_reason","")); return self._ok(context,data=result,message="Telemedicine operation completed.",code="telemedicine_session_fail")
