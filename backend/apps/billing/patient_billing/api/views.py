"""Patient Billing API views."""

from __future__ import annotations

from typing import Any

from apps.billing.patient_billing.api.serializers import (
    PatientBillingAccountCreateSerializer,
    PatientBillingAccountSerializer,
    PatientBillingAccountTransitionSerializer,
    PatientBillingAccountUpdateSerializer,
    PatientBillingStatementCreateSerializer,
    PatientBillingStatementSerializer,
    PatientGuarantorCreateSerializer,
    PatientGuarantorSerializer,
    PatientGuarantorUpdateSerializer,
    PatientResponsibilityCreateSerializer,
    PatientResponsibilitySerializer,
    PatientResponsibilityUpdateSerializer,
)
from apps.billing.patient_billing.models import (
    PatientBillingAccount,
    PatientFinancialResponsibility,
    PatientGuarantor,
)
from apps.billing.patient_billing.permissions import (
    CanCreatePatientBillingAccount,
    CanCreatePatientGuarantor,
    CanCreatePatientResponsibility,
    CanCreatePatientStatement,
    CanDeletePatientGuarantor,
    CanDeletePatientResponsibility,
    CanIssuePatientStatement,
    CanListPatientBillingAccounts,
    CanRestorePatientGuarantor,
    CanRestorePatientResponsibility,
    CanTransitionPatientBillingAccount,
    CanUpdatePatientBillingAccount,
    CanUpdatePatientGuarantor,
    CanUpdatePatientResponsibility,
    CanViewPatientGuarantor,
    CanViewPatientResponsibility,
    CanViewPatientStatement,
    CanVoidPatientStatement,
)
from apps.billing.patient_billing.selectors import (
    PatientBillingAccountSelector,
    PatientBillingStatementSelector,
    PatientGuarantorSelector,
)
from apps.billing.patient_billing.workflows import (
    PatientBillingAccountWorkflow,
    PatientBillingStatementWorkflow,
    PatientGuarantorWorkflow,
    PatientResponsibilityWorkflow,
)
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


def _organization(request: Any) -> Any:
    """Return explicit organization context and reject tenant mismatches."""

    organization = getattr(request, "organization", None)
    tenant = getattr(request, "tenant", None)
    if organization is None or tenant is None:
        raise PermissionDenied(
            "Explicit tenant and organization context are required.",
        )
    if organization.tenant_id != tenant.id:
        raise PermissionDenied(
            "Organization does not belong to the active tenant.",
        )
    return organization


def _actor(request: Any) -> Any:
    """Return the authenticated actor."""

    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated:
        raise PermissionDenied(
            "Authenticated user context is required.",
        )
    return user


class PatientBillingAccountListCreateAPIView(generics.ListCreateAPIView):
    """List or create patient billing accounts."""

    def get_permissions(self):
        """Return action-specific RBAC permissions."""

        permission = (
            CanCreatePatientBillingAccount
            if self.request.method == "POST"
            else CanListPatientBillingAccounts
        )
        return [permission()]

    def get_queryset(self):
        """Return organization-scoped accounts."""

        return PatientBillingAccountSelector.queryset(
            organization_id=_organization(self.request).id,
        )

    def get_serializer_class(self):
        """Select create or read serializer."""

        if self.request.method == "POST":
            return PatientBillingAccountCreateSerializer
        return PatientBillingAccountSerializer

    def perform_create(self, serializer):
        """Create through the workflow boundary."""

        organization = _organization(self.request)
        account = PatientBillingAccountWorkflow.create(
            actor=_actor(self.request),
            organization=organization,
            patient=serializer.validated_data["patient"],
            account_number=serializer.validated_data["account_number"],
            currency=serializer.validated_data.get("currency", "INR"),
            opening_balance=serializer.validated_data.get("opening_balance", 0),
            credit_limit=serializer.validated_data.get("credit_limit", 0),
            notes=serializer.validated_data.get("notes", ""),
        )
        serializer.instance = account


class PatientBillingAccountDetailAPIView(generics.RetrieveUpdateAPIView):
    """Retrieve or update one patient billing account."""

    def get_permissions(self):
        """Return action-specific RBAC permissions."""

        if self.request.method in {"PUT", "PATCH"}:
            return [CanUpdatePatientBillingAccount()]
        return [CanListPatientBillingAccounts()]

    def get_queryset(self):
        """Return organization-scoped accounts."""

        return PatientBillingAccountSelector.queryset(
            organization_id=_organization(self.request).id,
        )

    def get_serializer_class(self):
        """Select detail or update serializer."""

        if self.request.method in {"PUT", "PATCH"}:
            return PatientBillingAccountUpdateSerializer
        return PatientBillingAccountSerializer

    def perform_update(self, serializer):
        """Update through the workflow boundary."""

        account = PatientBillingAccountWorkflow.update(
            actor=_actor(self.request),
            organization=_organization(self.request),
            instance=self.get_object(),
            validated_data=serializer.validated_data,
        )
        serializer.instance = account


class PatientBillingAccountTransitionAPIView(generics.UpdateAPIView):
    """Transition a patient billing account lifecycle state."""

    permission_classes = (CanTransitionPatientBillingAccount,)
    serializer_class = PatientBillingAccountTransitionSerializer

    def get_queryset(self):
        """Return organization-scoped accounts."""

        return PatientBillingAccountSelector.queryset(
            organization_id=_organization(self.request).id,
        )

    def update(self, request, *args, **kwargs):
        """Transition through the workflow boundary."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = PatientBillingAccountWorkflow.transition(
            actor=_actor(request),
            organization=_organization(request),
            account_id=self.get_object().id,
            status=serializer.validated_data["status"],
        )
        return Response(
            PatientBillingAccountSerializer(account).data,
            status=status.HTTP_200_OK,
        )


class PatientGuarantorListCreateAPIView(generics.ListCreateAPIView):
    """List or create patient guarantors."""

    def get_permissions(self):
        """Return action-specific RBAC permissions."""

        if self.request.method == "POST":
            return [CanCreatePatientGuarantor()]
        return [CanViewPatientGuarantor()]

    def get_queryset(self):
        """Return organization-scoped guarantors."""

        return PatientGuarantorSelector.queryset(
            organization_id=_organization(self.request).id,
        )

    def get_serializer_class(self):
        """Select create or read serializer."""

        if self.request.method == "POST":
            return PatientGuarantorCreateSerializer
        return PatientGuarantorSerializer

    def perform_create(self, serializer):
        """Create through the workflow boundary."""

        organization = _organization(self.request)
        patient = serializer.validated_data["patient"]
        validated_data = {
            key: value
            for key, value in serializer.validated_data.items()
            if key != "patient"
        }
        guarantor = PatientGuarantorWorkflow.create(
            actor=_actor(self.request),
            organization=organization,
            patient=patient,
            validated_data=validated_data,
        )
        serializer.instance = guarantor


class PatientGuarantorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or soft-delete a guarantor."""

    def get_permissions(self):
        """Return action-specific RBAC permissions."""

        if self.request.method == "DELETE":
            return [CanDeletePatientGuarantor()]
        if self.request.method in {"PUT", "PATCH"}:
            return [CanUpdatePatientGuarantor()]
        return [CanViewPatientGuarantor()]

    def get_queryset(self):
        """Return organization-scoped guarantors."""

        return PatientGuarantorSelector.queryset(
            organization_id=_organization(self.request).id,
        )

    def get_serializer_class(self):
        """Select update or read serializer."""

        if self.request.method in {"PUT", "PATCH"}:
            return PatientGuarantorUpdateSerializer
        return PatientGuarantorSerializer

    def perform_update(self, serializer):
        """Update through the workflow boundary."""

        serializer.instance = PatientGuarantorWorkflow.update(
            actor=_actor(self.request),
            organization=_organization(self.request),
            instance=self.get_object(),
            validated_data=serializer.validated_data,
        )

    def perform_destroy(self, instance):
        """Soft-delete through the workflow boundary."""

        PatientGuarantorWorkflow.delete(
            actor=_actor(self.request),
            organization=_organization(self.request),
            instance=instance,
        )


class PatientGuarantorRestoreAPIView(generics.UpdateAPIView):
    """Restore a soft-deleted guarantor."""

    permission_classes = (CanRestorePatientGuarantor,)
    serializer_class = PatientGuarantorSerializer

    def get_queryset(self):
        """Return organization-scoped deleted guarantors."""

        return PatientGuarantor.all_objects.filter(
            organization_id=_organization(self.request).id,
            is_deleted=True,
        )

    def update(self, request, *args, **kwargs):
        """Restore through the workflow boundary."""

        guarantor = PatientGuarantorWorkflow.restore(
            actor=_actor(request),
            organization=_organization(request),
            guarantor_id=self.get_object().id,
        )
        return Response(
            PatientGuarantorSerializer(guarantor).data,
            status=status.HTTP_200_OK,
        )


class PatientResponsibilityListCreateAPIView(generics.ListCreateAPIView):
    """List or create financial responsibility records."""

    def get_permissions(self):
        """Return action-specific RBAC permissions."""

        if self.request.method == "POST":
            return [CanCreatePatientResponsibility()]
        return [CanViewPatientResponsibility()]

    def get_queryset(self):
        """Return responsibility records within the organization."""

        return PatientFinancialResponsibility.objects.select_related(
            "account",
            "guarantor",
        ).filter(
            account__organization_id=_organization(self.request).id,
        )

    def get_serializer_class(self):
        """Select create or read serializer."""

        if self.request.method == "POST":
            return PatientResponsibilityCreateSerializer
        return PatientResponsibilitySerializer

    def perform_create(self, serializer):
        """Create through the workflow boundary."""

        organization = _organization(self.request)
        account = get_object_or_404(
            PatientBillingAccount.objects,
            id=self.kwargs["account_id"],
            organization_id=organization.id,
        )
        responsibility = PatientResponsibilityWorkflow.create(
            actor=_actor(self.request),
            organization=organization,
            account=account,
            validated_data=serializer.validated_data,
        )
        serializer.instance = responsibility


class PatientResponsibilityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or soft-delete financial responsibility."""

    def get_permissions(self):
        """Return action-specific RBAC permissions."""

        if self.request.method == "DELETE":
            return [CanDeletePatientResponsibility()]
        if self.request.method in {"PUT", "PATCH"}:
            return [CanUpdatePatientResponsibility()]
        return [CanViewPatientResponsibility()]

    def get_queryset(self):
        """Return organization-scoped responsibility records."""

        return PatientFinancialResponsibility.objects.select_related(
            "account",
            "guarantor",
        ).filter(
            account__organization_id=_organization(self.request).id,
        )

    def get_serializer_class(self):
        """Select update or read serializer."""

        if self.request.method in {"PUT", "PATCH"}:
            return PatientResponsibilityUpdateSerializer
        return PatientResponsibilitySerializer

    def perform_update(self, serializer):
        """Update through the workflow boundary."""

        serializer.instance = PatientResponsibilityWorkflow.update(
            actor=_actor(self.request),
            organization=_organization(self.request),
            instance=self.get_object(),
            validated_data=serializer.validated_data,
        )

    def perform_destroy(self, instance):
        """Soft-delete through the workflow boundary."""

        PatientResponsibilityWorkflow.delete(
            actor=_actor(self.request),
            organization=_organization(self.request),
            instance=instance,
        )


class PatientResponsibilityRestoreAPIView(generics.UpdateAPIView):
    """Restore a soft-deleted responsibility."""

    permission_classes = (CanRestorePatientResponsibility,)
    serializer_class = PatientResponsibilitySerializer

    def get_queryset(self):
        """Return organization-scoped deleted responsibility records."""

        return PatientFinancialResponsibility.all_objects.filter(
            account__organization_id=_organization(self.request).id,
            is_deleted=True,
        )

    def update(self, request, *args, **kwargs):
        """Restore through the workflow boundary."""

        responsibility = PatientResponsibilityWorkflow.restore(
            actor=_actor(request),
            organization=_organization(request),
            responsibility_id=self.get_object().id,
        )
        return Response(
            PatientResponsibilitySerializer(responsibility).data,
            status=status.HTTP_200_OK,
        )


class PatientBillingStatementListAPIView(generics.ListAPIView):
    """List patient billing statements."""

    permission_classes = (CanViewPatientStatement,)
    serializer_class = PatientBillingStatementSerializer

    def get_queryset(self):
        """Return organization-scoped statements."""

        return PatientBillingStatementSelector.queryset(
            organization_id=_organization(self.request).id,
        )


class PatientBillingStatementGenerateAPIView(generics.CreateAPIView):
    """Generate a patient billing statement."""

    permission_classes = (CanCreatePatientStatement,)
    serializer_class = PatientBillingStatementCreateSerializer

    def create(self, request, *args, **kwargs):
        """Generate a statement through the workflow boundary."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organization = _organization(request)
        account = get_object_or_404(
            PatientBillingAccount.objects,
            id=serializer.validated_data["account_id"],
            organization_id=organization.id,
        )
        statement = PatientBillingStatementWorkflow.generate(
            actor=_actor(request),
            organization=organization,
            account_id=account.id,
            period_start=serializer.validated_data["period_start"],
            period_end=serializer.validated_data["period_end"],
        )
        return Response(
            PatientBillingStatementSerializer(statement).data,
            status=status.HTTP_201_CREATED,
        )


class PatientBillingStatementIssueAPIView(generics.UpdateAPIView):
    """Issue one patient billing statement."""

    permission_classes = (CanIssuePatientStatement,)
    serializer_class = PatientBillingStatementSerializer

    def get_queryset(self):
        """Return organization-scoped statements."""

        return PatientBillingStatementSelector.queryset(
            organization_id=_organization(self.request).id,
        )

    def update(self, request, *args, **kwargs):
        """Issue through the workflow boundary."""

        statement = PatientBillingStatementWorkflow.issue(
            actor=_actor(request),
            organization=_organization(request),
            statement_id=self.get_object().id,
        )
        return Response(
            PatientBillingStatementSerializer(statement).data,
            status=status.HTTP_200_OK,
        )


class PatientBillingStatementVoidAPIView(generics.UpdateAPIView):
    """Void one patient billing statement."""

    permission_classes = (CanVoidPatientStatement,)
    serializer_class = PatientBillingStatementSerializer

    def get_queryset(self):
        """Return organization-scoped statements."""

        return PatientBillingStatementSelector.queryset(
            organization_id=_organization(self.request).id,
        )

    def update(self, request, *args, **kwargs):
        """Void through the workflow boundary."""

        statement = PatientBillingStatementWorkflow.void(
            actor=_actor(request),
            organization=_organization(request),
            statement_id=self.get_object().id,
        )
        return Response(
            PatientBillingStatementSerializer(statement).data,
            status=status.HTTP_200_OK,
        )


__all__ = (
    "PatientBillingAccountDetailAPIView",
    "PatientBillingAccountListCreateAPIView",
    "PatientBillingAccountTransitionAPIView",
    "PatientBillingStatementGenerateAPIView",
    "PatientBillingStatementIssueAPIView",
    "PatientBillingStatementListAPIView",
    "PatientBillingStatementVoidAPIView",
    "PatientGuarantorDetailAPIView",
    "PatientGuarantorListCreateAPIView",
    "PatientGuarantorRestoreAPIView",
    "PatientResponsibilityDetailAPIView",
    "PatientResponsibilityListCreateAPIView",
    "PatientResponsibilityRestoreAPIView",
)
