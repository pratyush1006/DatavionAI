"""
Workflow execution mixins.

Provides workflow-driven API operations
for DatavionOS modules.

Supports:

- Workflow based create
- Workflow based update
- Workflow based destroy
- Tenant aware workflow context
- DRF serializer integration
"""

from __future__ import annotations

from typing import Any, ClassVar

from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from apps.core.workflows import (
    WorkflowContext,
)


class WorkflowMixin:
    """
    Shared workflow helpers.
    """

    def get_workflow_context(
        self,
    ) -> WorkflowContext:
        """
        Build workflow execution context.

        Tenant resolution priority:

        1. Tenant injected by middleware
        2. Tenant resolved from user's organization
        """

        tenant = self.current_tenant

        if tenant is None:
            user = self.request.user

            organization_role = user.organization_roles.select_related(
                "organization__tenant",
            ).first()

            if organization_role is not None:
                tenant = organization_role.organization.tenant

        if tenant is None:
            raise RuntimeError(
                "Tenant context is required.",
            )

        return WorkflowContext(
            actor_id=self.request.user.id,
            tenant_id=tenant.id,
        )


class WorkflowCreateMixin(
    WorkflowMixin,
):
    """
    Execute create operations through workflows.
    """

    create_workflow: ClassVar[Any | None] = None

    def has_create_workflow(
        self,
    ) -> bool:

        return self.create_workflow is not None

    def create(
        self,
        request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Workflow based create handler.

        Workflow persists entity.
        Returns detail representation.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        self.perform_workflow_create(
            serializer,
        )

        instance = serializer.instance

        detail_serializer = getattr(
            self,
            "detail_serializer_class",
            None,
        )

        if detail_serializer is not None and instance is not None:
            serializer = detail_serializer(
                instance,
                context={
                    "request": request,
                },
            )

        return self.created_response(
            data=serializer.data,
        )

    def execute_create_workflow(
        self,
        *,
        validated_data: dict[str, Any],
    ):

        workflow = self.create_workflow(
            request=self.build_workflow_request(
                validated_data,
            ),
        )

        return workflow.execute(
            context=self.get_workflow_context(),
        )

    def perform_workflow_create(
        self,
        serializer: BaseSerializer,
    ):
        """
        Execute workflow create.
        """

        result = self.execute_create_workflow(
            validated_data=(serializer.validated_data),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        serializer.instance = self.resolve_workflow_created_instance(
            result,
        )

    def resolve_workflow_created_instance(
        self,
        result,
    ):
        """
        Resolve created domain object.

        Workflow returns DTOs.

        Example:

            EmployeeCreationData(
                employee_id=UUID(...)
            )

        API serializers require
        the actual model instance.

        Supported identifiers:

        - employee_id
        - department_id
        - patient_id
        - appointment_id
        - id
        """

        data = result.data

        if data is None:
            return None

        object_id = None

        workflow_identifier_fields = (
            "employee_id",
            "department_id",
            "patient_id",
            "appointment_id",
            "claim_id",
            "id",
        )

        for field_name in workflow_identifier_fields:
            if hasattr(
                data,
                field_name,
            ):
                object_id = getattr(
                    data,
                    field_name,
                )
                break

        if object_id is None:
            return data

        return self.get_queryset().get(
            id=object_id,
        )

    def build_workflow_request(
        self,
        validated_data,
    ):
        raise NotImplementedError


class WorkflowUpdateMixin(
    WorkflowMixin,
):
    """
    Execute update operations through workflows.
    """

    update_workflow: ClassVar[Any | None] = None

    def has_update_workflow(
        self,
    ) -> bool:

        return self.update_workflow is not None

    def perform_workflow_update(
        self,
        serializer: BaseSerializer,
    ):

        instance = self.get_object()

        workflow = self.update_workflow(
            request=self.build_update_workflow_request(
                instance,
                serializer.validated_data,
            ),
        )

        result = workflow.execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        serializer.instance = instance

    def build_update_workflow_request(
        self,
        instance,
        validated_data,
    ):
        raise NotImplementedError


class WorkflowDestroyMixin(
    WorkflowMixin,
):
    """
    Execute delete operations through workflows.
    """

    delete_workflow: ClassVar[Any | None] = None

    def has_delete_workflow(
        self,
    ) -> bool:

        return self.delete_workflow is not None

    def perform_workflow_destroy(
        self,
        instance,
    ):

        workflow = self.delete_workflow(
            request=self.build_delete_workflow_request(
                instance,
            ),
        )

        result = workflow.execute(
            context=self.get_workflow_context(),
        )

        if not result.success:
            raise RuntimeError(
                result.message,
            )

        return result

    def build_delete_workflow_request(
        self,
        instance,
    ):
        raise NotImplementedError


__all__ = (
    "WorkflowCreateMixin",
    "WorkflowUpdateMixin",
    "WorkflowDestroyMixin",
)
