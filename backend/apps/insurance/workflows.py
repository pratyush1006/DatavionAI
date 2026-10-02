from apps.core.workflows import WorkflowContext, WorkflowResult
from apps.insurance import services


class InsuranceCreateWorkflow:
    def execute(self, *, context: WorkflowContext, model, organization, data):
        return WorkflowResult.ok(
            data=services.create(model=model, organization=organization, data=data)
        )


class InsuranceUpdateWorkflow:
    def execute(
        self, *, context: WorkflowContext, model, organization, object_id, data
    ):
        return WorkflowResult.ok(
            data=services.update(
                model=model, object_id=object_id, organization=organization, data=data
            )
        )


class InsuranceDeleteWorkflow:
    def execute(
        self, *, context: WorkflowContext, model, organization, object_id, actor
    ):
        return WorkflowResult.ok(
            data=services.soft_delete(
                model=model, object_id=object_id, organization=organization, actor=actor
            )
        )


class InsuranceRestoreWorkflow:
    def execute(self, *, context: WorkflowContext, model, organization, object_id):
        return WorkflowResult.ok(
            data=services.restore(
                model=model, object_id=object_id, organization=organization
            )
        )
