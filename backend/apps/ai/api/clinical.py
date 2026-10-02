"""RBAC-protected clinical AI artifact and laboratory status APIs."""

from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.exceptions import AIAuthorizationError
from apps.ai.models import (
    AIApplication,
    AIClinicalArtifact,
    AIClinicalArtifactVersion,
    AIDoctorReview,
    AIModuleReference,
)
from apps.ai.permissions import AIAuthenticatedPermission
from apps.ai.services.clinical import create_artifact, review_artifact
from apps.ai.services.domain_tools import get_laboratory_order_status


def resolve_scope(request):
    organization = getattr(request, "organization", None) or getattr(
        request.user, "organization", None
    )
    tenant = getattr(request, "tenant", None) or (
        getattr(organization, "tenant", None) if organization else None
    )
    return tenant, organization


class ClinicalArtifactCreateSerializer(serializers.Serializer):
    application_code = serializers.CharField(max_length=40)
    artifact_type = serializers.ChoiceField(
        choices=[
            AIClinicalArtifact.NOTE_CLEANING,
            AIClinicalArtifact.PRESCRIPTION_DRAFT,
            AIClinicalArtifact.CLINICAL_SUMMARY,
        ]
    )
    module_code = serializers.CharField(max_length=120)
    resource_type = serializers.CharField(max_length=120)
    resource_id = serializers.CharField(max_length=160)
    source_content = serializers.CharField()
    normalized_content = serializers.CharField(required=False, allow_blank=True)
    structured_content = serializers.DictField(required=False)


class ClinicalArtifactCreateAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)

    def post(self, request):
        serializer = ClinicalArtifactCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        data = serializer.validated_data
        application = get_object_or_404(
            AIApplication,
            tenant=tenant,
            organization=organization,
            code=data["application_code"],
            status="active",
        )
        reference, _ = AIModuleReference.objects.get_or_create(
            tenant=tenant,
            organization=organization,
            module_code=data["module_code"],
            resource_type=data["resource_type"],
            resource_id=data["resource_id"],
        )
        try:
            artifact = create_artifact(
                user=request.user,
                tenant=tenant,
                organization=organization,
                application=application,
                module_reference=reference,
                artifact_type=data["artifact_type"],
                source_content=data["source_content"],
                normalized_content=data.get("normalized_content", ""),
                structured_content=data.get("structured_content", {}),
            )
        except AIAuthorizationError as exc:
            return Response({"detail": str(exc)}, status=403)
        return Response(
            {
                "artifact_id": str(artifact.uuid),
                "status": artifact.status,
                "version": artifact.current_version,
                "module_reference": {
                    "module_code": reference.module_code,
                    "resource_type": reference.resource_type,
                    "resource_id": reference.resource_id,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ClinicalArtifactReviewAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)

    def post(self, request, version_id):
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        version = get_object_or_404(
            AIClinicalArtifactVersion.objects.select_related("artifact"),
            uuid=version_id,
            artifact__tenant=tenant,
            artifact__organization=organization,
        )
        action = request.data.get("action")
        if action not in {
            AIDoctorReview.VERIFY,
            AIDoctorReview.SIGN,
            AIDoctorReview.REJECT,
        }:
            return Response({"detail": "Invalid review action."}, status=400)
        try:
            artifact = review_artifact(
                user=request.user,
                organization=organization,
                artifact_version=version,
                action=action,
                comments=request.data.get("comments", ""),
                signature_reference=request.data.get("signature_reference", ""),
            )
        except AIAuthorizationError as exc:
            return Response({"detail": str(exc)}, status=403)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=409)
        return Response(
            {
                "artifact_id": str(artifact.uuid),
                "status": artifact.status,
                "version": artifact.current_version,
            }
        )


class LaboratoryOrderStatusSerializer(serializers.Serializer):
    order_number = serializers.CharField(max_length=160)
    module_code = serializers.CharField(max_length=120, default="clinical.laboratories")
    resource_type = serializers.CharField(max_length=120, default="laboratory_order")


class LaboratoryOrderStatusAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)

    def post(self, request):
        serializer = LaboratoryOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        try:
            result = get_laboratory_order_status(
                user=request.user,
                tenant=tenant,
                organization=organization,
                **serializer.validated_data,
            )
        except AIAuthorizationError as exc:
            return Response({"detail": str(exc)}, status=403)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        if result is None:
            return Response({"detail": "Laboratory order not found."}, status=404)
        return Response(result)


class ClinicalNoteCleanSerializer(serializers.Serializer):
    application_code = serializers.CharField(max_length=40)
    module_code = serializers.CharField(max_length=120, default="notes")
    resource_type = serializers.CharField(max_length=120, default="clinical_note")
    resource_id = serializers.CharField(max_length=160)
    raw_note = serializers.CharField()
    model = serializers.CharField(max_length=160, required=False, default="gpt-4o-mini")
    provider_name = serializers.CharField(
        max_length=80, required=False, allow_blank=True
    )


class ClinicalNoteCleanAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)

    def post(self, request):
        serializer = ClinicalNoteCleanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        data = serializer.validated_data
        application = get_application(tenant, organization, data["application_code"])
        reference = get_reference(
            tenant,
            organization,
            data["module_code"],
            data["resource_type"],
            data["resource_id"],
        )
        try:
            artifact = clean_clinical_note(
                user=request.user,
                tenant=tenant,
                organization=organization,
                application=application,
                module_reference=reference,
                raw_note=data["raw_note"],
                model=data["model"],
                provider_name=data.get("provider_name") or None,
            )
        except AIAuthorizationError as exc:
            return Response({"detail": str(exc)}, status=403)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        return Response(
            {
                "artifact_id": str(artifact.uuid),
                "status": artifact.status,
                "version": artifact.current_version,
            },
            status=status.HTTP_201_CREATED,
        )


class PrescriptionDraftSerializer(serializers.Serializer):
    application_code = serializers.CharField(max_length=40)
    module_code = serializers.CharField(
        max_length=120, default="clinical.prescriptions"
    )
    resource_type = serializers.CharField(max_length=120, default="prescription")
    resource_id = serializers.CharField(max_length=160)
    clinical_context = serializers.CharField()
    model = serializers.CharField(max_length=160, required=False, default="gpt-4o-mini")
    provider_name = serializers.CharField(
        max_length=80, required=False, allow_blank=True
    )


class PrescriptionDraftAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)

    def post(self, request):
        serializer = PrescriptionDraftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        data = serializer.validated_data
        application = get_application(tenant, organization, data["application_code"])
        reference = get_reference(
            tenant,
            organization,
            data["module_code"],
            data["resource_type"],
            data["resource_id"],
        )
        try:
            artifact = draft_prescription(
                user=request.user,
                tenant=tenant,
                organization=organization,
                application=application,
                module_reference=reference,
                clinical_context=data["clinical_context"],
                model=data["model"],
                provider_name=data.get("provider_name") or None,
            )
        except AIAuthorizationError as exc:
            return Response({"detail": str(exc)}, status=403)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=400)
        return Response(
            {
                "artifact_id": str(artifact.uuid),
                "status": artifact.status,
                "version": artifact.current_version,
            },
            status=status.HTTP_201_CREATED,
        )


__all__ = (
    "ClinicalArtifactCreateAPIView",
    "ClinicalArtifactReviewAPIView",
    "LaboratoryOrderStatusAPIView",
    "ClinicalNoteCleanAPIView",
    "PrescriptionDraftAPIView",
)
