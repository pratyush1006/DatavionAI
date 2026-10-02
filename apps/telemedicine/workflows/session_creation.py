from apps.core.workflows import WorkflowContext,WorkflowResult
from apps.telemedicine.workflows._base import TelemedicineWorkflow
from apps.telemedicine.services import SessionService

class SessionCreationWorkflow(TelemedicineWorkflow):
 workflow_name="telemedicine.session.create"
 def _run(self,*,context:WorkflowContext)->WorkflowResult:
  payload=self.payload; result=SessionService.create(validated_data=payload); return self._ok(context,data=result,message="Telemedicine operation completed.",code="telemedicine_session_create")
