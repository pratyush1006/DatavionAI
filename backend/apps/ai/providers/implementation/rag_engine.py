"""
Retrieval-Augmented Generation engine.

Combines embedding, vector search, prompt rendering, and chat completion
into a single generate workflow.
"""

from __future__ import annotations

from apps.datavionos.ai.chat import (
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ChatRole,
)
from apps.datavionos.ai.embeddings import EmbeddingRequest
from apps.datavionos.ai.prompt import PromptTemplate
from apps.datavionos.ai.rag import (
    RAGDocument,
    RAGRequest,
    RAGResponse,
)


class SimpleRAGEngine:
    """
    Default RAG engine.

    Embeds the query, retrieves similar chunks, renders a grounded prompt
    and asks the chat model to answer using only the retrieved context.
    """

    SYSTEM_PROMPT = (
        "You are a clinical assistant. Use ONLY the provided context to "
        "answer. If the context does not contain the answer, say you do "
        "not know. Never invent clinical facts."
    )

    def __init__(
        self,
        *,
        chat,
        embeddings,
        vector_store,
        prompts=None,
        template_name: str = "rag_answer",
    ) -> None:
        self._chat = chat
        self._embeddings = embeddings
        self._vector_store = vector_store
        self._prompts = prompts
        self._template_name = template_name

    async def generate(
        self,
        request: RAGRequest,
    ) -> RAGResponse:
        """Execute a retrieval-augmented generation workflow."""

        embedded = await self._embeddings.embed(
            EmbeddingRequest(input=(request.query,)),
        )

        query_vector = embedded.embeddings[0].vector

        search_response = await self._vector_store.search(
            type(
                "Req",
                (),
                {
                    "vector": query_vector,
                    "limit": request.limit,
                    "namespace": request.namespace,
                    "metadata": {},
                },
            )(),
        )

        documents = tuple(
            RAGDocument(
                identifier=result.document.id,
                content=result.document.content,
                score=result.score,
                metadata=result.document.metadata,
            )
            for result in search_response.results
        )

        context = "\n\n".join(
            f"[doc {index + 1}] {doc.content}" for index, doc in enumerate(documents)
        )

        if self._prompts is not None:
            rendered = await self._prompts.render(
                type(
                    "PR",
                    (),
                    {
                        "template": PromptTemplate(
                            name=self._template_name,
                            template=(
                                "Context:\n{{ context }}\n\n"
                                "Question: {{ question }}\n\nAnswer:"
                            ),
                        ),
                        "variables": {
                            "context": context,
                            "question": request.query,
                        },
                    },
                )(),
            )
            user_prompt = rendered.prompt
        else:
            user_prompt = f"Context:\n{context}\n\nQuestion: {request.query}"

        chat_response: ChatResponse = await self._chat.complete(
            ChatRequest(
                messages=(
                    ChatMessage(role=ChatRole.SYSTEM, content=self.SYSTEM_PROMPT),
                    ChatMessage(role=ChatRole.USER, content=user_prompt),
                ),
            )
        )

        return RAGResponse(
            response=chat_response,
            documents=documents,
            metadata={"context_tokens": len(context)},
        )


__all__ = [
    "SimpleRAGEngine",
]
