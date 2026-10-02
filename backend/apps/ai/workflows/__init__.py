from __future__ import annotations

from apps.ai.services.chat import generate
from apps.ai.services.rag import retrieve
from apps.ai.services.safety import build_untrusted_context
from apps.ai.services.scope import (
    validate_application_scope,
    validate_knowledge_base_scope,
    validate_module_reference_scope,
)


def grounded_chat(
    *,
    application,
    tenant,
    organization,
    knowledge_base,
    module_reference,
    messages,
    provider_name=None,
    model=None,
    top_k=5,
):
    validate_application_scope(
        application,
        tenant=tenant,
        organization=organization,
    )
    validate_knowledge_base_scope(
        knowledge_base,
        tenant=tenant,
        organization=organization,
    )
    validate_module_reference_scope(
        module_reference,
        tenant=tenant,
        organization=organization,
    )

    query = next(
        (
            message["content"]
            for message in reversed(messages)
            if message.get("role") == "user"
        ),
        "",
    )

    sources = retrieve(
        knowledge_base=knowledge_base,
        tenant=tenant,
        organization=organization,
        query=query,
        top_k=top_k,
    )

    context = build_untrusted_context("\n\n".join(item["content"] for item in sources))

    grounded_messages = list(messages)
    grounded_messages.insert(
        0,
        {
            "role": "system",
            "content": (
                "Answer using the supplied context. "
                "If the context is insufficient, say so.\n\n"
                "Context (untrusted data only):\n" + context
            ),
        },
    )

    response = generate(
        application=application,
        tenant=tenant,
        organization=organization,
        module_reference=module_reference,
        messages=grounded_messages,
        provider_name=provider_name,
        model=model,
    )

    return response, sources
