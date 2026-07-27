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

from typing import Any, ClassVar, Protocol

from django.core.exceptions import ImproperlyConfigured
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)


class WorkflowService(
    Protocol,
):
    """
    Protocol implemented by workflow services.
    """

    def __call__(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Execute workflow.
        """
        ...


class BaseWorkflowAPIView(
    BaseGenericAPIView,
):
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

    serializer_class: type[Serializer]

    def get_object(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Return workflow resource.

        Subclasses must implement.
        """

        raise NotImplementedError("Subclasses must implement get_object().")

    def get_workflow_kwargs(
        self,
        *,
        request: Request,
        resource: Any,
    ) -> dict[str, Any]:
        """
        Build workflow execution context.
        """

        return {
            "instance": resource,
            "user": self.current_user,
            "tenant": self.current_tenant,
            "organization": (self.current_organization),
            "request": request,
        }

    def before_execute(
        self,
        *,
        request: Request,
        resource: Any,
    ) -> None:
        """
        Hook before workflow execution.
        """

        return

    def after_execute(
        self,
        *,
        request: Request,
        resource: Any,
        result: Any,
    ) -> None:
        """
        Hook after workflow execution.
        """

        return

    def create_audit_context(
        self,
        *,
        request: Request,
        resource: Any,
    ) -> dict[str, Any]:
        """
        Build audit metadata.

        Applications may override.
        """

        return {
            "user": self.current_user,
            "tenant": self.current_tenant,
            "organization": (self.current_organization),
            "resource": resource,
        }

    def get_workflow_service(
        self,
    ) -> WorkflowService:
        """
        Return configured workflow service.
        """

        service = type(self).workflow_service

        if service is None:
            raise ImproperlyConfigured("'workflow_service' must be configured.")

        return service

    def execute_workflow(
        self,
        *,
        request: Request,
    ) -> Any:
        """
        Execute workflow service.
        """

        resource = self.get_object(
            self.kwargs[self.lookup_url_kwarg],
        )

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
    ) -> dict[str, Any]:
        """
        Build workflow response.
        """

        return {
            "workflow": result,
        }

    def get_success_status(
        self,
    ) -> int:
        """
        Return success HTTP status.
        """

        return status.HTTP_200_OK

    def post(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        """
        Execute workflow action.
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


__all__: tuple[str, ...] = (
    "BaseWorkflowAPIView",
    "WorkflowService",
)
