"""AI REST API."""

from __future__ import annotations

from django.http import StreamingHttpResponse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.api.serializers import (
    ChatSerializer,
    RAGIndexSerializer,
    RAGSearchSerializer,
)
from apps.ai.models import AIApplication, AIModuleReference, KnowledgeBase
from apps.ai.permissions import AIAuthenticatedPermission
from apps.ai.production import production_config
from apps.ai.services.chat import generate
from apps.ai.services.rag import add_text_document, index_document, retrieve
from apps.ai.services.safety import validate_embedding_provider_selection


def enforce_production_provider(requested_provider):
    provider = str(requested_provider or production_config().provider).strip().lower()
    runtime = production_config()
    if provider == "mock" and not runtime.allow_mock:
        from rest_framework.exceptions import ValidationError

        raise ValidationError("Mock AI provider is disabled in production.")
    if provider != runtime.provider:
        from rest_framework.exceptions import ValidationError

        raise ValidationError(
            "Requested AI provider is not enabled for this deployment."
        )
    return provider


def resolve_scope(request):
    organization = getattr(request, "organization", None) or getattr(
        request.user, "organization", None
    )
    tenant = getattr(request, "tenant", None) or (
        getattr(organization, "tenant", None) if organization else None
    )
    return tenant, organization


class EmptyAPIViewSerializer(serializers.Serializer):
    """Schema placeholder for bodyless endpoints."""


class AIHealthAPIView(APIView):
    permission_classes = ()
    serializer_class = EmptyAPIViewSerializer

    def get(self, request):
        return Response({"status": "ok", "service": "ai"})


class AIApplicationsAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)
    required_ai_permission = "ai.view"
    serializer_class = EmptyAPIViewSerializer

    def get(self, request):
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        rows = AIApplication.objects.filter(
            tenant=tenant, organization=organization, status="active"
        ).values("uuid", "code", "name", "department", "description")
        return Response(list(rows))


class AIChatAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)
    required_ai_permission = "ai.create"
    serializer_class = ChatSerializer

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        application = AIApplication.objects.get(
            tenant=tenant,
            organization=organization,
            code=serializer.validated_data["application_code"],
            status="active",
        )
        data = dict(serializer.validated_data)
        module_reference, _ = AIModuleReference.objects.get_or_create(
            tenant=tenant,
            organization=organization,
            module_code=data.pop("module_code"),
            resource_type=data.pop("resource_type"),
            resource_id=data.pop("resource_id"),
        )
        provider_name = enforce_production_provider(data.pop("provider", None))
        data.setdefault("model", production_config().model)
        result = generate(
            application=application,
            tenant=tenant,
            organization=organization,
            module_reference=module_reference,
            provider_name=provider_name,
            **data,
        )
        return Response(
            {
                "content": result.content,
                "provider": result.provider,
                "model": result.model,
                "usage": {
                    "prompt_tokens": result.prompt_tokens,
                    "completion_tokens": result.completion_tokens,
                },
            }
        )


class AIChatStreamAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)
    required_ai_permission = "ai.create"
    serializer_class = ChatSerializer

    def post(self, request):
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        application = AIApplication.objects.get(
            tenant=tenant,
            organization=organization,
            code=serializer.validated_data["application_code"],
            status="active",
        )
        request_data = dict(serializer.validated_data)
        module_reference, _ = AIModuleReference.objects.get_or_create(
            tenant=tenant,
            organization=organization,
            module_code=request_data.pop("module_code"),
            resource_type=request_data.pop("resource_type"),
            resource_id=request_data.pop("resource_id"),
        )
        provider_name = enforce_production_provider(request_data.get("provider"))
        request_data.setdefault("model", production_config().model)
        from apps.ai.providers import ChatMessage, ChatRequest, get_chat_provider

        provider = get_chat_provider(provider_name)
        chat_request = ChatRequest(
            model=request_data["model"],
            messages=[
                ChatMessage(m["role"], m["content"]) for m in request_data["messages"]
            ],
            temperature=request_data["temperature"],
            max_tokens=request_data["max_tokens"],
        )
        response = StreamingHttpResponse(
            provider.stream(chat_request), content_type="text/plain"
        )
        response["X-AI-Application"] = application.code
        return response


class AIRAGIndexAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)
    required_ai_permission = "ai.update"
    serializer_class = RAGIndexSerializer

    def post(self, request):
        serializer = RAGIndexSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        kb = KnowledgeBase.objects.get(
            uuid=serializer.validated_data["knowledge_base_id"],
            tenant=tenant,
            organization=organization,
        )
        document = add_text_document(
            knowledge_base=kb,
            **{
                k: serializer.validated_data[k]
                for k in ("title", "content", "source_uri")
                if k in serializer.validated_data
            },
        )
        runtime = production_config()
        validate_embedding_provider_selection(runtime.embedding_provider)
        count = index_document(
            document=document,
            tenant=tenant,
            organization=organization,
            embedding_provider=runtime.embedding_provider,
            embedding_model=runtime.embedding_model,
        )
        return Response(
            {"document_id": str(document.uuid), "chunks": count}, status=201
        )


class AIRAGSearchAPIView(APIView):
    permission_classes = (AIAuthenticatedPermission,)
    required_ai_permission = "ai.view"
    serializer_class = RAGSearchSerializer

    def post(self, request):
        serializer = RAGSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant, organization = resolve_scope(request)
        if not tenant or not organization:
            return Response(
                {"detail": "Tenant and organization context are required."}, status=400
            )
        kb = KnowledgeBase.objects.get(
            uuid=serializer.validated_data["knowledge_base_id"],
            tenant=tenant,
            organization=organization,
        )
        runtime = production_config()
        validate_embedding_provider_selection(runtime.embedding_provider)
        return Response(
            retrieve(
                knowledge_base=kb,
                tenant=tenant,
                organization=organization,
                query=serializer.validated_data["query"],
                top_k=serializer.validated_data["top_k"],
                embedding_provider=runtime.embedding_provider,
                embedding_model=runtime.embedding_model,
            )
        )
