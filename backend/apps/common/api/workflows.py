"""
Base workflow API views for the Datavion AI platform.
"""

from __future__ import annotations

from typing import Any, Protocol

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class WorkflowService(Protocol):
    """
    Protocol implemented by workflow services.
    """

    def __call__(
        self,
        **kwargs: Any,
    ) -> object:
        """
        Execute the workflow.
        """
        ...


class BaseWorkflowAPIView(
    GenericAPIView,
):
    """
    Base API view for workflow endpoints.

    Workflow endpoints execute an action against an existing
    resource instead of performing CRUD operations.

    Examples
    --------
    - Approve
    - Reject
    - Verify
    - Record
    - Complete
    - Cancel
    - Archive
    - Activate
    - Suspend
    - Invite
    """

    workflow_service: WorkflowService | None = None

    lookup_url_kwarg = "uuid"

    def get_object(
        self,
        *args,
        **kwargs,
    ):
        """
        Return the workflow resource.

        Subclasses must implement.
        """

        raise NotImplementedError

    def get_workflow_kwargs(
        self,
        *,
        request: Request,
        resource: Any,
    ) -> dict[str, Any]:
        """
        Return keyword arguments passed to the workflow service.

        Override when additional context is required.
        """

        return {
            "instance": resource,
        }

    def before_execute(
        self,
        *,
        request: Request,
        resource: Any,
    ) -> None:
        """
        Hook executed before the workflow.

        Override when additional preprocessing is required.
        """

    def execute_workflow(
        self,
        *,
        request: Request,
    ) -> object:
        """
        Execute the configured workflow service.
        """

        if self.workflow_service is None:
            raise NotImplementedError(
                "workflow_service must be configured.",
            )

        resource = self.get_object(
            self.kwargs[self.lookup_url_kwarg],
        )

        self.before_execute(
            request=request,
            resource=resource,
        )

        return self.workflow_service(
            **self.get_workflow_kwargs(
                request=request,
                resource=resource,
            ),
        )

    def after_execute(
        self,
        *,
        request: Request,
        result: object,
    ) -> None:
        """
        Hook executed after the workflow.

        Override for audit logging,
        notifications, events, etc.
        """

    def build_response_data(
        self,
        *,
        result: object,
    ) -> dict[str, Any]:
        """
        Build the workflow response payload.

        Override in subclasses when a workflow
        requires a custom response.
        """

        return {
            "success": True,
        }

    def get_success_status(
        self,
    ) -> int:
        """
        Return the HTTP success status code.
        """

        return status.HTTP_200_OK

    def post(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Execute the workflow.
        """

        result = self.execute_workflow(
            request=request,
        )

        self.after_execute(
            request=request,
            result=result,
        )

        payload = self.build_response_data(
            result=result,
        )

        serializer = self.get_serializer(
            payload,
        )

        return Response(
            serializer.data,
            status=self.get_success_status(),
        )


__all__ = [
    "BaseWorkflowAPIView",
    "WorkflowService",
]
