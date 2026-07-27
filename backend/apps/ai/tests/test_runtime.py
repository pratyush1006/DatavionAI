"""
Smoke tests for the AI runtime and transcription service (offline mode).
"""

from __future__ import annotations

import asyncio

from apps.ai.models import KnowledgeDocument
from apps.common.tests.base import BaseTestCase
from apps.datavionos.ai.implementation.chat import OpenAIChatModel
from apps.datavionos.ai.implementation.embeddings import OpenAIEmbeddingModel
from apps.datavionos.ai.implementation.rag_engine import SimpleRAGEngine
from apps.datavionos.ai.implementation.vector_store import PostgresVectorStore
from apps.transcription.constants import TranscriptionStatus
from apps.transcription.models import TranscriptionJob
from apps.transcription.services import TranscriptionService


class AIRuntimeTestCase(BaseTestCase):
    """
    Verify the AI runtime works without external API keys.
    """

    def test_offline_chat(self) -> None:
        chat = OpenAIChatModel()

        response = asyncio.run(
            chat.complete(
                type(
                    "Req",
                    (),
                    {
                        "messages": (
                            type(
                                "M",
                                (),
                                {
                                    "role": __import__(
                                        "apps.datavionos.ai.chat",
                                        fromlist=["ChatRole"],
                                    ).ChatRole.USER,
                                    "content": "Hello",
                                    "metadata": {},
                                },
                            )(),
                        ),
                        "temperature": 0.7,
                        "max_tokens": None,
                        "metadata": {},
                    },
                )()
            )
        )

        self.assertIsNotNone(response.message.content)

    def test_offline_embeddings_dimension(self) -> None:
        embeddings = OpenAIEmbeddingModel(dimension=64)

        response = asyncio.run(
            embeddings.embed(
                type(
                    "Req",
                    (),
                    {"input": ("a", "b"), "metadata": {}},
                )()
            )
        )

        self.assertEqual(len(response.embeddings), 2)
        self.assertEqual(len(response.embeddings[0].vector), 64)

    def test_rag_over_postgres_store(self) -> None:
        document = KnowledgeDocument.objects.create(
            organization=self.organization,
            title="Guideline",
            content="Aspirin is used for fever.",
        )

        store = PostgresVectorStore(organization_id=self.organization.id)
        embeddings = OpenAIEmbeddingModel(dimension=64)

        asyncio.run(
            store.upsert(
                (
                    type(
                        "VD",
                        (),
                        {
                            "id": str(document.id),
                            "vector": [0.0] * 64,
                            "content": document.content,
                            "metadata": {},
                        },
                    )(),
                )
            )
        )

        rag = SimpleRAGEngine(
            chat=OpenAIChatModel(),
            embeddings=embeddings,
            vector_store=store,
        )

        response = asyncio.run(
            rag.generate(
                type(
                    "R",
                    (),
                    {
                        "query": "aspirin",
                        "limit": 1,
                        "namespace": None,
                        "metadata": {},
                    },
                )()
            )
        )

        self.assertEqual(len(response.documents), 1)


class TranscriptionServiceTestCase(BaseTestCase):
    """
    Verify transcription jobs run in offline mode.
    """

    def test_transcribe_offline(self) -> None:
        from apps.transcription.constants import TranscriptionProvider

        job = TranscriptionJob.objects.create(
            organization=self.organization,
            provider=TranscriptionProvider.LOCAL,
            audio_path="/tmp/sample.wav",
        )

        TranscriptionService.transcribe(job=job)

        job.refresh_from_db()
        self.assertEqual(job.status, TranscriptionStatus.COMPLETED)
        self.assertTrue(job.transcript)
