"""
Base workflow API views for the DatavionOS platform.

Provides framework-level workflow execution APIs.

Supports:

- Action based endpoints
- Workflow services
- Tenant context
- Organization context
- Audit hooks
- Event ready execution
"""

from __future__ import annotations

from typing import Any, ClassVar, Final, Protocol

from django.core.exceptions import ImproperlyConfigured
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.common.api.base_generics import BaseGenericAPIView


class WorkflowService(Protocol):
    """
    Protocol implemented by workflow services.
    """

    def __call__(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Execute the workflow.
        """
        ...


class BaseWorkflowAPIView(BaseGenericAPIView):
    """
    Base API view for workflow actions.

    Examples:

    - Approve
    - Reject
    - Verify
    - Complete
    - Cancel
    - Archive
    - Activate
    - Suspend
    """

    workflow_service: ClassVar[WorkflowService | None] = None

    lookup_url_kwarg: ClassVar[str] = "uuid"

    serializer_class: ClassVar[type[Serializer]]

    def get_object(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Return the workflow resource.

        Subclasses must implement.
        """

        raise NotImplementedError(
            "Subclasses must implement get_object().",
        )

    def _base_context(self) -> dict[str, object]:
        """
        Return the common workflow context.
        """

        return {
            "user": self.current_user,
            "tenant": self.current_tenant,
            "organization": self.current_organization,
        }

    def get_workflow_kwargs(
        self,
        *,
        request: Request,
        resource: Any,
    ) -> dict[str, object]:
        """
        Build workflow execution context.
        """

        context = self._base_context()

        context.update(
            {
                "instance": resource,
                "request": request,
            },
        )

        return context

    def before_execute(
        self,
        *,
        request: Request,
        resource: Any,
    ) -> None:
        """
        Hook executed before the workflow.
        """

    def after_execute(
        self,
        *,
        request: Request,
        resource: Any,
        result: Any,
    ) -> None:
        """
        Hook executed after the workflow.
        """

    def create_audit_context(
        self,
        *,
        request: Request,
        resource: Any,
    ) -> dict[str, object]:
        """
        Build audit metadata.

        Applications may override.
        """

        context = self._base_context()
        context["resource"] = resource

        return context

    def get_workflow_service(
        self,
    ) -> WorkflowService:
        """
        Return the configured workflow service.
        """

        service = type(self).workflow_service

        if service is None:
            raise ImproperlyConfigured(
                "'workflow_service' must be configured.",
            )

        return service

    def execute_workflow(
        self,
        *,
        request: Request,
    ) -> Any:
        """
        Execute the configured workflow.
        """

        lookup_value = self.kwargs[self.lookup_url_kwarg]

        resource = self.get_object(lookup_value)

        self.before_execute(
            request=request,
            resource=resource,
        )

        result = self.get_workflow_service()(
            **self.get_workflow_kwargs(
                request=request,
                resource=resource,
            ),
        )

        self.after_execute(
            request=request,
            resource=resource,
            result=result,
        )

        return result

    def build_response_data(
        self,
        *,
        result: Any,
    ) -> dict[str, object]:
        """
        Build the workflow response payload.
        """

        return {
            "workflow": result,
        }

    def get_success_status(
        self,
    ) -> int:
        """
        Return the success HTTP status.
        """

        return status.HTTP_200_OK

    def post(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Execute the workflow action.
        """

        result = self.execute_workflow(
            request=request,
        )

        serializer = self.get_serializer(
            self.build_response_data(
                result=result,
            ),
        )

        serializer.is_valid(
            raise_exception=True,
        )

        return self.success_response(
            data=serializer.validated_data,
            status_code=self.get_success_status(),
        )


__all__: Final[tuple[str, ...]] = (
    "BaseWorkflowAPIView",
    "WorkflowService",
)
