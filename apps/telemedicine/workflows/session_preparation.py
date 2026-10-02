from apps.core.workflows import WorkflowContext,WorkflowResult
from apps.telemedicine.workflows._base import TelemedicineWorkflow
from apps.telemedicine.services import SessionService

class SessionPreparationWorkflow(TelemedicineWorkflow):
 workflow_name="telemedicine.session.prepare"
 def _run(self,*,context:WorkflowContext)->WorkflowResult:
  payload=self.payload; result=SessionService.prepare(session_id=payload["session_id"],organization_id=payload["organization_id"]); return self._ok(context,data=result,message="Telemedicine operation completed.",code="telemedicine_session_prepare")
