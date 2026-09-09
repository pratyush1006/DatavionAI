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
- Standardized API responses
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

        1. Tenant injected by middleware.
        2. Tenant resolved from the user's organization.
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
        """
        Return whether this API view has a creation workflow.
        """

        return self.create_workflow is not None

    def create(
        self,
        request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Workflow based create handler.

        The workflow persists the entity and the API returns
        the detail representation of the created model instance.
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
        """
        Construct and execute the configured creation workflow.
        """

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
    ) -> None:
        """
        Execute the creation workflow.
        """

        result = self.execute_create_workflow(
            validated_data=serializer.validated_data,
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
        Resolve the created domain object.

        Workflows return lightweight DTOs containing an entity
        identifier. API serializers require the actual model instance.

        Supported identifiers:

        - organization_id
        - employee_id
        - department_id
        - patient_id
        - appointment_id
        - claim_id
        - id
        """

        data = result.data

        if data is None:
            return None

        object_id = None

        workflow_identifier_fields = (
            "organization_id",
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
        """
        Build the workflow request DTO.

        Concrete API views must implement this method when
        create_workflow is configured.
        """

        raise NotImplementedError


class WorkflowUpdateMixin(
    WorkflowMixin,
):
    """
    Execute update operations through workflows.

    The mixin owns the complete DRF update lifecycle so workflow-driven
    updates still return the platform-standard DatavionOS response envelope.

    Response contract:

        {
            "success": true,
            "message": "...",
            "data": {...},
            "meta": {...}
        }
    """

    update_workflow: ClassVar[Any | None] = None

    def has_update_workflow(
        self,
    ) -> bool:
        """
        Return whether this API view has an update workflow.
        """

        return self.update_workflow is not None

    def update(
        self,
        request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Execute a workflow-driven PUT/PATCH update.

        This intentionally overrides DRF's default ``update`` method.

        DRF's default implementation returns a raw ``Response`` containing
        ``serializer.data``. DatavionOS APIs require all successful resource
        mutations to use the standardized response envelope.

        PATCH semantics are preserved through the ``partial`` flag.
        """

        partial = kwargs.pop(
            "partial",
            False,
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        self.perform_workflow_update(
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

        message = getattr(
            self,
            "update_success_message",
            "Updated successfully.",
        )

        return self.success_response(
            data=serializer.data,
            message=message,
        )

    def perform_workflow_update(
        self,
        serializer: BaseSerializer,
    ) -> None:
        """
        Execute the update workflow.

        The serializer is already bound to the current model instance
        by ``update()``. Reuse that instance instead of resolving it
        from the URL a second time.
        """

        instance = serializer.instance

        if instance is None:
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
        """
        Build the update workflow request DTO.

        Concrete API views must implement this method when
        update_workflow is configured.
        """

        raise NotImplementedError


class WorkflowDestroyMixin(
    WorkflowMixin,
):
    """
    Execute destroy operations through workflows.
    """

    delete_workflow: ClassVar[Any | None] = None

    def has_delete_workflow(
        self,
    ) -> bool:
        """
        Return whether this API view has a deletion workflow.
        """

        return self.delete_workflow is not None

    def perform_workflow_destroy(
        self,
        instance,
    ):
        """
        Execute the deletion workflow.
        """

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
        """
        Build the deletion workflow request DTO.

        Concrete API views must implement this method when
        delete_workflow is configured.
        """

        raise NotImplementedError


__all__ = (
    "WorkflowCreateMixin",
    "WorkflowUpdateMixin",
    "WorkflowDestroyMixin",
)
