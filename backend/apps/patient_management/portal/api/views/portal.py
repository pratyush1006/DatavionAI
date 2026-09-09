"""
Patient Portal API views.
"""

from __future__ import annotations

from uuid import UUID

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.portal.api.serializers import (
    PatientPortalAccountCreateSerializer,
    PatientPortalAccountDetailSerializer,
    PatientPortalAccountListSerializer,
    PatientPortalAccountUpdateSerializer,
    PatientPortalLifecycleSerializer,
)
from apps.patient_management.portal.models import PatientPortalAccount
from apps.patient_management.portal.permissions import (
    CanCreatePatientPortal,
    CanDeletePatientPortal,
    CanInvitePatientPortal,
    CanListPatientPortal,
    CanRestorePatientPortal,
    CanTransitionPatientPortal,
    CanViewPatientPortal,
)
from apps.patient_management.portal.policies import PatientPortalPolicy
from apps.patient_management.portal.selectors import (
    get_portal_account,
    list_portal_accounts,
)
from apps.patient_management.portal.workflows import (
    PatientPortalCreationRequest,
    PatientPortalCreationWorkflow,
    PatientPortalDeletionRequest,
    PatientPortalDeletionWorkflow,
    PatientPortalInvitationRequest,
    PatientPortalInvitationWorkflow,
    PatientPortalLifecycleRequest,
    PatientPortalLifecycleWorkflow,
    PatientPortalRestoreRequest,
    PatientPortalRestoreWorkflow,
    PatientPortalUpdateRequest,
    PatientPortalUpdateWorkflow,
)


def _resolve_tenant(request):
    """Resolve the tenant from the established request context."""

    tenant = getattr(request, "tenant", None)
    if tenant is not None:
        return tenant

    role = request.user.organization_roles.select_related(
        "organization__tenant"
    ).first()
    if role is None:
        raise PermissionError(
            "Authenticated user has no organization membership.",
        )

    return role.organization.tenant


def _resolve_organization(request, tenant):
    """Resolve the organization from the established request context."""

    organization = getattr(request, "organization", None)
    if organization is not None:
        if organization.tenant_id != tenant.pk:
            raise PermissionError(
                "Organization does not belong to the active tenant.",
            )
        return organization

    role = (
        request.user.organization_roles.select_related("organization")
        .filter(organization__tenant_id=tenant.pk)
        .first()
    )
    if role is None:
        raise PermissionError(
            "Authenticated user has no organization membership.",
        )

    return role.organization


class PatientPortalAccountListCreateAPIView(APIView):
    """List and create patient portal accounts."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return organization-scoped portal accounts."""

        tenant = _resolve_tenant(request)
        organization = _resolve_organization(request, tenant)
        policy = PatientPortalPolicy()

        if not policy.can_list(
            actor=request.user,
            organization=organization,
        ):
            CanListPatientPortal().has_permission(
                request,
                self,
            )

        queryset = list_portal_accounts(
            tenant_id=tenant.pk,
            organization_id=organization.pk,
        )
        serializer = PatientPortalAccountListSerializer(
            queryset,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        """Create a patient portal account."""

        tenant = _resolve_tenant(request)
        organization = _resolve_organization(request, tenant)

        serializer = PatientPortalAccountCreateSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        if not PatientPortalPolicy().can_create(
            actor=request.user,
            organization=organization,
        ):
            CanCreatePatientPortal().has_permission(
                request,
                self,
            )

        workflow = PatientPortalCreationWorkflow(
            request=PatientPortalCreationRequest(
                organization_id=organization.pk,
                patient_id=serializer.validated_data.pop("patient_id"),
                data=serializer.validated_data,
            ),
        )
        result = workflow.run(
            context=WorkflowContext(
                actor_id=request.user.pk,
                tenant_id=tenant.pk,
                workflow_name="patient_portal.create",
            ),
        )
        return Response(
            PatientPortalAccountDetailSerializer(
                result.data,
            ).data,
            status=201,
        )


class PatientPortalAccountDetailAPIView(APIView):
    """Retrieve, update, and delete one portal account."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, account_id: UUID):
        """Return one portal account."""

        tenant = _resolve_tenant(request)
        organization = _resolve_organization(request, tenant)
        account = get_portal_account(
            tenant_id=tenant.pk,
            organization_id=organization.pk,
            account_id=account_id,
        )

        if not PatientPortalPolicy().can_view(
            actor=request.user,
            account=account,
        ):
            CanViewPatientPortal().has_permission(request, self)

        return Response(
            PatientPortalAccountDetailSerializer(account).data,
        )

    def patch(self, request, account_id: UUID):
        """Update one portal account."""

        tenant = _resolve_tenant(request)
        organization = _resolve_organization(request, tenant)
        serializer = PatientPortalAccountUpdateSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        workflow = PatientPortalUpdateWorkflow(
            request=PatientPortalUpdateRequest(
                organization_id=organization.pk,
                account_id=account_id,
                data=serializer.validated_data,
            ),
        )
        result = workflow.run(
            context=WorkflowContext(
                actor_id=request.user.pk,
                tenant_id=tenant.pk,
                workflow_name="patient_portal.update",
            ),
        )
        return Response(
            PatientPortalAccountDetailSerializer(
                result.data,
            ).data,
        )

    def delete(self, request, account_id: UUID):
        """Soft-delete one portal account."""

        tenant = _resolve_tenant(request)
        organization = _resolve_organization(request, tenant)

        account = get_portal_account(
            tenant_id=tenant.pk,
            organization_id=organization.pk,
            account_id=account_id,
        )

        if not PatientPortalPolicy().can_delete(
            actor=request.user,
            account=account,
        ):
            CanDeletePatientPortal().has_permission(request, self)

        workflow = PatientPortalDeletionWorkflow(
            request=PatientPortalDeletionRequest(
                organization_id=organization.pk,
                account_id=account_id,
            ),
        )
        result = workflow.run(
            context=WorkflowContext(
                actor_id=request.user.pk,
                tenant_id=tenant.pk,
                workflow_name="patient_portal.delete",
            ),
        )
        return Response(
            PatientPortalAccountDetailSerializer(
                result.data,
            ).data,
        )


class PatientPortalAccountLifecycleAPIView(APIView):
    """Transition one portal account through its lifecycle."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, account_id: UUID):
        """Apply one strict lifecycle transition."""

        tenant = _resolve_tenant(request)
        organization = _resolve_organization(request, tenant)
        serializer = PatientPortalLifecycleSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        account = get_portal_account(
            tenant_id=tenant.pk,
            organization_id=organization.pk,
            account_id=account_id,
        )

        if not PatientPortalPolicy().can_transition(
            actor=request.user,
            account=account,
        ):
            CanTransitionPatientPortal().has_permission(request, self)

        workflow = PatientPortalLifecycleWorkflow(
            request=PatientPortalLifecycleRequest(
                organization_id=organization.pk,
                account_id=account_id,
                status=serializer.validated_data["status"],
            ),
        )
        result = workflow.run(
            context=WorkflowContext(
                actor_id=request.user.pk,
                tenant_id=tenant.pk,
                workflow_name="patient_portal.lifecycle",
            ),
        )
        return Response(
            PatientPortalAccountDetailSerializer(
                result.data,
            ).data,
        )


class PatientPortalAccountRestoreAPIView(APIView):
    """Restore one soft-deleted portal account."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, account_id: UUID):
        """Restore a deleted portal account."""

        tenant = _resolve_tenant(request)
        organization = _resolve_organization(request, tenant)

        account = PatientPortalAccount.all_objects.get(
            pk=account_id,
            organization_id=organization.pk,
            organization__tenant_id=tenant.pk,
            is_deleted=True,
        )

        if not PatientPortalPolicy().can_restore(
            actor=request.user,
            account=account,
        ):
            CanRestorePatientPortal().has_permission(request, self)

        workflow = PatientPortalRestoreWorkflow(
            request=PatientPortalRestoreRequest(
                organization_id=organization.pk,
                account_id=account_id,
            ),
        )
        result = workflow.run(
            context=WorkflowContext(
                actor_id=request.user.pk,
                tenant_id=tenant.pk,
                workflow_name="patient_portal.restore",
            ),
        )
        return Response(
            PatientPortalAccountDetailSerializer(
                result.data,
            ).data,
        )


class PatientPortalAccountInvitationAPIView(APIView):
    """Issue an invitation for one invited portal account."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, account_id: UUID):
        """Issue the invitation through the portal workflow."""

        tenant = _resolve_tenant(request)
        organization = _resolve_organization(request, tenant)
        account = get_portal_account(
            tenant_id=tenant.pk,
            organization_id=organization.pk,
            account_id=account_id,
        )

        if not PatientPortalPolicy().can_invite(
            actor=request.user,
            account=account,
        ):
            CanInvitePatientPortal().has_permission(request, self)

        workflow = PatientPortalInvitationWorkflow(
            request=PatientPortalInvitationRequest(
                organization_id=organization.pk,
                account_id=account_id,
            ),
        )
        result = workflow.run(
            context=WorkflowContext(
                actor_id=request.user.pk,
                tenant_id=tenant.pk,
                workflow_name="patient_portal.invite",
            ),
        )
        return Response(
            PatientPortalAccountDetailSerializer(result.data).data,
        )


__all__ = (
    "PatientPortalAccountDetailAPIView",
    "PatientPortalAccountInvitationAPIView",
    "PatientPortalAccountLifecycleAPIView",
    "PatientPortalAccountListCreateAPIView",
    "PatientPortalAccountRestoreAPIView",
)
