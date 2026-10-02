from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, is_dataclass
from dataclasses import fields as dataclass_fields
from inspect import Parameter, signature
from typing import Any, cast

from django.db import transaction

from apps.billing.finance.services.audit import record_audit
from apps.billing.finance.services.events import enqueue_event
from apps.billing.finance.services.idempotency import execute_idempotent
from apps.core.workflows import BaseWorkflow, WorkflowResult


@dataclass(frozen=True, slots=True)
class FinanceWorkflowRequest:
    organization: Any
    payload: dict[str, Any] = field(default_factory=dict)
    actor_id: Any = None
    instance_id: Any = None
    idempotency_key: str | None = None


def _workflow_result(
    result: Any, *, context: Any = None, metadata: dict[str, Any] | None = None
):
    """Adapt to the project's actual WorkflowResult contract.

    DatavionOS WorkflowResult implementations vary across releases. Some
    expose a callable success factory; others are dataclasses/slots objects
    whose constructor requires a keyword-only context. Finance must honor the
    runtime contract instead of assuming a single constructor shape.
    """
    meta = metadata or {}

    factory = getattr(WorkflowResult, "success", None)
    if callable(factory):
        for args, factory_kwargs in (
            ((result,), {"metadata": meta, "context": context}),
            ((result,), {"metadata": meta}),
            ((result,), {"context": context}),
            ((result,), {}),
        ):
            try:
                return factory(*args, **factory_kwargs)
            except TypeError:
                continue

    try:
        params: Mapping[str, Parameter] = signature(WorkflowResult).parameters
    except (TypeError, ValueError):
        params = {}

    kwargs: dict[str, Any] = {}
    for name in params:
        if name == "self":
            continue
        if name == "context":
            kwargs[name] = context
        elif name == "success":
            kwargs[name] = True
        elif name in {"result", "data", "value", "payload"}:
            kwargs[name] = result
        elif name == "metadata":
            kwargs[name] = meta
        elif name == "error":
            kwargs[name] = None
    if kwargs:
        try:
            return WorkflowResult(**kwargs)
        except TypeError:
            pass

    try:
        return cast(Any, WorkflowResult)(
            success=True, result=result, data=result, metadata=meta, context=context
        )
    except TypeError:
        pass

    if is_dataclass(WorkflowResult):
        kwargs = {}
        for f in dataclass_fields(WorkflowResult):
            if f.name == "success":
                kwargs[f.name] = True
            elif f.name == "context":
                kwargs[f.name] = context
            elif f.name in {"result", "data", "value", "payload"}:
                kwargs[f.name] = result
            elif f.name == "metadata":
                kwargs[f.name] = meta
            elif f.name == "error":
                kwargs[f.name] = None
        if kwargs:
            return WorkflowResult(**kwargs)
    raise TypeError("Unsupported apps.core.workflows.WorkflowResult contract.")


class FinanceWorkflow(BaseWorkflow):
    name = "finance.unknown"
    handler: Callable[..., Any] | None = None
    event_type = "finance.workflow.completed"

    def _run(self, context, request):
        if request.organization is None or self.handler is None:
            raise ValueError("Invalid Finance workflow context.")
        return self.handler(
            organization=request.organization,
            data=request.payload,
            instance_id=request.instance_id,
        )

    def execute(self, context, request):
        def run_once():
            with transaction.atomic():
                result = self._run(context, request)
                record_audit(
                    organization=request.organization,
                    workflow=self.name,
                    entity_type=result.__class__.__name__,
                    entity_id=getattr(result, "pk", None),
                    actor_id=request.actor_id,
                    payload=request.payload,
                )
                enqueue_event(
                    organization=request.organization,
                    event_type=self.event_type,
                    aggregate_type=result.__class__.__name__,
                    aggregate_id=getattr(result, "pk", None),
                    payload={"workflow": self.name},
                )
                return result

        if request.organization is None or self.handler is None:
            raise ValueError("Invalid Finance workflow context.")
        if request.idempotency_key:
            result, replayed = execute_idempotent(
                organization=request.organization,
                workflow=self.name,
                key=request.idempotency_key,
                execute=run_once,
            )
            return _workflow_result(
                result, context=context, metadata={"replayed": replayed}
            )
        return _workflow_result(run_once(), context=context)
