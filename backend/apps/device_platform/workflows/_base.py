from apps.core.workflows import BaseWorkflow, WorkflowResult


class DeviceWorkflow(BaseWorkflow):
    def _ok(
        self,
        context,
        *,
        data=None,
        message="Device operation completed.",
        code="device_platform_ok",
    ):
        return WorkflowResult(success=True, data=data, message=message, code=code)
