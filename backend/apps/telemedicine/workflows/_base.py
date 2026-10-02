from apps.core.workflows import BaseWorkflow, WorkflowResult


class TelemedicineWorkflow(BaseWorkflow):
    domain = "telemedicine"

    def _ok(self, context, *, data, message, code):
        return WorkflowResult.ok(context=context, data=data, message=message, code=code)
