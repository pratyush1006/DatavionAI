"""
Master Patient Index API views.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.mpi.api.serializers import (
    MPICandidateSerializer,
    MPICreateSerializer,
    MPIDetailSerializer,
    MPILifecycleSerializer,
    MPIListSerializer,
    MPIMatchCreateSerializer,
    MPIMergeSerializer,
    MPIReviewSerializer,
    MPIUpdateSerializer,
)
from apps.patient_management.mpi.permissions import (
    CanCreateMPI,
    CanDeleteMPI,
    CanListMPI,
    CanMatchMPI,
    CanMergeMPI,
    CanRestoreMPI,
    CanReverseMergeMPI,
    CanReviewMPI,
    CanTransitionMPI,
    CanViewMPI,
)
from apps.patient_management.mpi.policies import MPIPolicy
from apps.patient_management.mpi.selectors import (
    get_mpi_record,
    list_mpi_candidates,
    list_mpi_records,
)
from apps.patient_management.mpi.workflows import (
    MPICreationRequest,
    MPICreationWorkflow,
    MPIDeletionRequest,
    MPIDeletionWorkflow,
    MPILifecycleRequest,
    MPILifecycleWorkflow,
    MPIMatchingRequest,
    MPIMatchingWorkflow,
    MPIMergeRequest,
    MPIMergeWorkflow,
    MPIRestoreRequest,
    MPIRestoreWorkflow,
    MPIReverseMergeRequest,
    MPIReverseMergeWorkflow,
    MPIReviewRequest,
    MPIReviewWorkflow,
    MPIUpdateRequest,
    MPIUpdateWorkflow,
)


def _organization(request):
    """Resolve the request organization using the project's tenant context."""

    organization = getattr(request, "tenant_organization", None)
    if organization is not None:
        return organization

    role = request.user.organization_roles.select_related(
        "organization__tenant"
    ).first()
    if role is None:
        raise PermissionError("No organization context is available.")
    return role.organization


def _workflow_context(request, workflow_name):
    """Build a workflow context from the authenticated request."""

    from apps.core.workflows import WorkflowContext

    organization = _organization(request)
    return WorkflowContext(
        tenant_id=organization.tenant_id,
        actor_id=request.user.pk,
        workflow_name=workflow_name,
    )


class MPIListCreateAPIView(APIView):
    """List and create organization-scoped MPI records."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return MPI records visible to the authenticated actor."""

        organization = _organization(request)
        CanListMPI().has_permission(request, self)
        if not MPIPolicy().can_list(
            actor=request.user,
            organization=organization,
        ):
            raise PermissionError("You cannot list MPI records.")

        records = list_mpi_records(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
        )
        return Response(MPIListSerializer(records, many=True).data)

    def post(self, request):
        """Create an MPI record through the workflow boundary."""

        organization = _organization(request)
        CanCreateMPI().has_permission(request, self)
        serializer = MPICreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        workflow = MPICreationWorkflow(
            request=MPICreationRequest(
                organization_id=organization.pk,
                patient_id=serializer.validated_data.pop("patient_id"),
                data=serializer.validated_data,
            ),
        )
        result = workflow.run(
            context=_workflow_context(request, "patient_mpi.create"),
        )
        return Response(
            MPIDetailSerializer(result.data).data,
            status=201,
        )


class MPIDetailAPIView(APIView):
    """Retrieve, update, and delete one MPI record."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, record_id):
        """Return one MPI record."""

        organization = _organization(request)
        record = get_mpi_record(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
            record_id=record_id,
        )
        CanViewMPI().has_permission(request, self)
        if not MPIPolicy().can_view(actor=request.user, record=record):
            raise PermissionError("You cannot view this MPI record.")
        return Response(MPIDetailSerializer(record).data)

    def patch(self, request, record_id):
        """Update one MPI record."""

        organization = _organization(request)
        serializer = MPIUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow = MPIUpdateWorkflow(
            request=MPIUpdateRequest(
                organization_id=organization.pk,
                record_id=record_id,
                data=serializer.validated_data,
            ),
        )
        result = workflow.run(
            context=_workflow_context(request, "patient_mpi.update"),
        )
        return Response(MPIDetailSerializer(result.data).data)

    def delete(self, request, record_id):
        """Soft-delete one MPI record."""

        organization = _organization(request)
        CanDeleteMPI().has_permission(request, self)
        workflow = MPIDeletionWorkflow(
            request=MPIDeletionRequest(
                organization_id=organization.pk,
                record_id=record_id,
            ),
        )
        result = workflow.run(
            context=_workflow_context(request, "patient_mpi.delete"),
        )
        return Response(MPIDetailSerializer(result.data).data)


class MPILifecycleAPIView(APIView):
    """Transition an MPI record through its lifecycle."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, record_id):
        """Apply a strict MPI lifecycle transition."""

        organization = _organization(request)
        CanTransitionMPI().has_permission(request, self)
        serializer = MPILifecycleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow = MPILifecycleWorkflow(
            request=MPILifecycleRequest(
                organization_id=organization.pk,
                record_id=record_id,
                status=serializer.validated_data["status"],
            ),
        )
        result = workflow.run(
            context=_workflow_context(request, "patient_mpi.lifecycle"),
        )
        return Response(MPIDetailSerializer(result.data).data)


class MPIRestoreAPIView(APIView):
    """Restore a soft-deleted MPI record."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, record_id):
        """Restore one MPI record."""

        organization = _organization(request)
        CanRestoreMPI().has_permission(request, self)
        workflow = MPIRestoreWorkflow(
            request=MPIRestoreRequest(
                organization_id=organization.pk,
                record_id=record_id,
            ),
        )
        result = workflow.run(
            context=_workflow_context(request, "patient_mpi.restore"),
        )
        return Response(MPIDetailSerializer(result.data).data)


class MPICandidateListAPIView(APIView):
    """List and generate MPI candidate matches."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return candidate matches."""

        organization = _organization(request)
        CanReviewMPI().has_permission(request, self)
        candidates = list_mpi_candidates(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
        )
        return Response(MPICandidateSerializer(candidates, many=True).data)

    def post(self, request):
        """Generate a candidate match."""

        organization = _organization(request)
        CanMatchMPI().has_permission(request, self)
        serializer = MPIMatchCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        left_id = serializer.validated_data["left_record_id"]
        right_id = serializer.validated_data["right_record_id"]
        workflow = MPIMatchingWorkflow(
            request=MPIMatchingRequest(
                organization_id=organization.pk,
                left_record_id=left_id,
                right_record_id=right_id,
            ),
        )
        result = workflow.run(
            context=_workflow_context(request, "patient_mpi.match"),
        )
        return Response(
            MPICandidateSerializer(result.data).data,
            status=201,
        )


class MPICandidateReviewAPIView(APIView):
    """Review one MPI candidate match."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, candidate_id):
        """Confirm or reject a candidate match."""

        organization = _organization(request)
        CanReviewMPI().has_permission(request, self)
        serializer = MPIReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow = MPIReviewWorkflow(
            request=MPIReviewRequest(
                organization_id=organization.pk,
                candidate_id=candidate_id,
                status=serializer.validated_data["status"],
            ),
        )
        result = workflow.run(
            context=_workflow_context(request, "patient_mpi.review"),
        )
        return Response(MPICandidateSerializer(result.data).data)


class MPIMergeAPIView(APIView):
    """Merge two MPI records administratively."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Merge a duplicate MPI record into a survivor."""

        organization = _organization(request)
        CanMergeMPI().has_permission(request, self)
        serializer = MPIMergeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow = MPIMergeWorkflow(
            request=MPIMergeRequest(
                organization_id=organization.pk,
                survivor_id=serializer.validated_data["survivor_id"],
                duplicate_id=serializer.validated_data["duplicate_id"],
                candidate_id=serializer.validated_data["candidate_id"],
            ),
        )
        result = workflow.run(
            context=_workflow_context(request, "patient_mpi.merge"),
        )
        return Response(MPIDetailSerializer(result.data).data)


class MPIReverseMergeAPIView(APIView):
    """Reverse an administrative MPI merge."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, record_id):
        """Reverse the selected merged record."""

        organization = _organization(request)
        CanReverseMergeMPI().has_permission(request, self)
        workflow = MPIReverseMergeWorkflow(
            request=MPIReverseMergeRequest(
                organization_id=organization.pk,
                duplicate_id=record_id,
            ),
        )
        result = workflow.run(
            context=_workflow_context(request, "patient_mpi.reverse_merge"),
        )
        return Response(MPIDetailSerializer(result.data).data)


__all__ = (
    "MPICandidateListAPIView",
    "MPICandidateReviewAPIView",
    "MPIDetailAPIView",
    "MPIListCreateAPIView",
    "MPILifecycleAPIView",
    "MPIMergeAPIView",
    "MPIReverseMergeAPIView",
    "MPIRestoreAPIView",
)
