"""Patient Referral API endpoints."""

from __future__ import annotations

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.workflows import WorkflowContext
from apps.patient_management.referrals.api.filters import PatientReferralFilter
from apps.patient_management.referrals.api.serializers import (
    PatientReferralCreateSerializer,
    PatientReferralDetailSerializer,
    PatientReferralListSerializer,
    PatientReferralTransitionSerializer,
    PatientReferralUpdateSerializer,
)
from apps.patient_management.referrals.permissions import (
    CanCreatePatientReferral,
    CanDeletePatientReferral,
    CanListPatientReferral,
    CanRestorePatientReferral,
    CanTransitionPatientReferral,
    CanUpdatePatientReferral,
    CanViewPatientReferral,
)
from apps.patient_management.referrals.policies import PatientReferralPolicy
from apps.patient_management.referrals.selectors import (
    get_referral,
    list_referrals,
)
from apps.patient_management.referrals.workflows import (
    ReferralCreationRequest,
    ReferralCreationWorkflow,
    ReferralDeletionRequest,
    ReferralDeletionWorkflow,
    ReferralLifecycleRequest,
    ReferralLifecycleWorkflow,
    ReferralRestoreRequest,
    ReferralRestoreWorkflow,
    ReferralUpdateRequest,
    ReferralUpdateWorkflow,
)


def _tenant_id(request):
    """Resolve the tenant from explicit request context."""

    tenant = getattr(getattr(request, "tenant", None), "id", None)
    if tenant is None:
        raise RuntimeError("Tenant context is required.")
    return tenant


def _organization(request):
    """Resolve and validate the organization from explicit request context."""

    organization = getattr(request, "organization", None)
    if organization is None:
        raise RuntimeError("Organization context is required.")

    if organization.tenant_id != _tenant_id(request):
        raise RuntimeError("Organization and tenant context do not match.")

    return organization


def _context(request, workflow_name):
    """Build a canonical workflow context for the current request."""

    return WorkflowContext.create(
        tenant_id=_tenant_id(request),
        actor_id=request.user.pk,
        workflow_name=workflow_name,
    )


def _workflow_response(
    result, serializer_class=None, *, success_status=status.HTTP_200_OK
):
    """Convert a workflow result into a consistent API response."""

    if not result.success:
        response_status = {
            "patient_referral_permission_denied": status.HTTP_403_FORBIDDEN,
            "patient_referral_not_found": status.HTTP_404_NOT_FOUND,
            "patient_referral_duplicate_number": status.HTTP_409_CONFLICT,
            "patient_referral_validation_error": status.HTTP_400_BAD_REQUEST,
            "patient_referral_invalid_transition": status.HTTP_400_BAD_REQUEST,
            "patient_referral_conflict": status.HTTP_409_CONFLICT,
            "workflow_execution_error": status.HTTP_500_INTERNAL_SERVER_ERROR,
        }.get(
            result.code,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        return Response(
            {"detail": result.message, "code": result.code},
            status=response_status,
        )

    if serializer_class is None:
        return Response(
            {"message": result.message, "code": result.code},
            status=success_status,
        )

    return Response(
        serializer_class(result.data).data,
        status=success_status,
    )


class PatientReferralListCreateAPIView(APIView):
    """List and create organization-scoped patient referrals."""

    def get_permissions(self):
        """Return method-specific RBAC permission adapters."""

        permission_map = {
            "GET": CanListPatientReferral,
            "POST": CanCreatePatientReferral,
        }
        permission_class = permission_map.get(
            self.request.method,
            IsAuthenticated,
        )
        return [permission_class()]

    def get(self, request):
        """Return filtered referrals within the active tenant boundary."""

        organization = _organization(request)
        tenant_id = _tenant_id(request)

        if not PatientReferralPolicy.can_list(
            user=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        queryset = list_referrals(
            tenant_id=tenant_id,
            organization_id=organization.id,
        )
        filtered = PatientReferralFilter(
            request.query_params,
            queryset=queryset,
        ).qs

        return Response(
            PatientReferralListSerializer(
                filtered,
                many=True,
            ).data,
        )

    def post(self, request):
        """Create a referral through its domain workflow."""

        serializer = PatientReferralCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = _organization(request)
        if serializer.validated_data["organization_id"] != organization.id:
            return Response(
                {"detail": "Organization boundary violation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        result = ReferralCreationWorkflow(
            request=ReferralCreationRequest(
                organization_id=organization.id,
                patient_id=serializer.validated_data["patient_id"],
                data={
                    key: value
                    for key, value in serializer.validated_data.items()
                    if key not in {"patient_id", "organization_id"}
                },
            ),
        ).execute(
            context=_context(request, "patient_referral.create"),
        )

        if not result.success:
            return _workflow_response(result)

        try:
            referral = get_referral(
                referral_id=result.data.referral_id,
                tenant_id=_tenant_id(request),
                organization_id=organization.id,
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "detail": "Created referral could not be retrieved.",
                    "code": "patient_referral_retrieval_error",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            PatientReferralDetailSerializer(referral).data,
            status=status.HTTP_201_CREATED,
        )


class PatientReferralDetailAPIView(APIView):
    """Retrieve, update, and soft-delete one referral."""

    def get_permissions(self):
        """Return method-specific RBAC permission adapters."""

        permission_map = {
            "GET": CanViewPatientReferral,
            "PATCH": CanUpdatePatientReferral,
            "DELETE": CanDeletePatientReferral,
        }
        permission_class = permission_map.get(
            self.request.method,
            IsAuthenticated,
        )
        return [permission_class()]

    def _get_referral(self, request, pk):
        """Resolve one referral within the active tenant and organization."""

        try:
            return get_referral(
                referral_id=pk,
                tenant_id=_tenant_id(request),
                organization_id=_organization(request).id,
            )
        except ObjectDoesNotExist:
            return None

    def get(self, request, pk):
        """Return one tenant-scoped referral."""

        referral = self._get_referral(request, pk)
        if referral is None:
            return Response(
                {"detail": "Patient referral was not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(PatientReferralDetailSerializer(referral).data)

    def patch(self, request, pk):
        """Update mutable referral fields through its workflow."""

        serializer = PatientReferralUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = _organization(request)
        referral = self._get_referral(request, pk)
        if referral is None:
            return Response(
                {"detail": "Patient referral was not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        result = ReferralUpdateWorkflow(
            request=ReferralUpdateRequest(
                organization_id=organization.id,
                referral_id=referral.id,
                data=serializer.validated_data,
            ),
        ).execute(
            context=_context(request, "patient_referral.update"),
        )
        return _workflow_response(
            result,
            PatientReferralDetailSerializer,
        )

    def delete(self, request, pk):
        """Soft-delete a referral through its workflow."""

        organization = _organization(request)
        referral = self._get_referral(request, pk)
        if referral is None:
            return Response(
                {"detail": "Patient referral was not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        result = ReferralDeletionWorkflow(
            request=ReferralDeletionRequest(
                organization_id=organization.id,
                referral_id=referral.id,
            ),
        ).execute(
            context=_context(request, "patient_referral.delete"),
        )
        return _workflow_response(
            result,
            success_status=status.HTTP_200_OK,
        )


class PatientReferralTransitionAPIView(APIView):
    """Transition a referral through its strict lifecycle."""

    permission_classes = (
        IsAuthenticated,
        CanTransitionPatientReferral,
    )

    def post(self, request, pk):
        """Transition a referral through the lifecycle workflow."""

        serializer = PatientReferralTransitionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = _organization(request)
        try:
            referral = get_referral(
                referral_id=pk,
                tenant_id=_tenant_id(request),
                organization_id=organization.id,
            )
        except ObjectDoesNotExist:
            return Response(
                {
                    "detail": "Patient referral was not found.",
                    "code": "patient_referral_not_found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not PatientReferralPolicy.can_transition(
            user=request.user,
            referral=referral,
        ):
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        result = ReferralLifecycleWorkflow(
            request=ReferralLifecycleRequest(
                organization_id=organization.id,
                referral_id=referral.id,
                target_status=serializer.validated_data["target_status"],
            ),
        ).execute(
            context=_context(request, "patient_referral.lifecycle"),
        )
        return _workflow_response(
            result,
            PatientReferralDetailSerializer,
        )


class PatientReferralRestoreAPIView(APIView):
    """Restore a deleted referral through its workflow."""

    permission_classes = (
        IsAuthenticated,
        CanRestorePatientReferral,
    )

    def post(self, request, pk):
        """Restore one referral inside the tenant boundary."""

        organization = _organization(request)
        result = ReferralRestoreWorkflow(
            request=ReferralRestoreRequest(
                organization_id=organization.id,
                referral_id=pk,
            ),
        ).execute(
            context=_context(request, "patient_referral.restore"),
        )
        return _workflow_response(
            result,
            PatientReferralDetailSerializer,
        )


__all__ = (
    "PatientReferralDetailAPIView",
    "PatientReferralListCreateAPIView",
    "PatientReferralRestoreAPIView",
    "PatientReferralTransitionAPIView",
)
