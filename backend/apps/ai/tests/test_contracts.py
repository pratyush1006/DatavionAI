"""AI platform contract tests."""

from __future__ import annotations

from apps.ai.providers import ChatMessage, ChatRequest, get_chat_provider
from apps.ai.services.prompts import render
from apps.ai.services.rag import chunk_text


def test_mock_provider_contract():
    provider = get_chat_provider("mock")
    response = provider.complete(
        ChatRequest(model="test", messages=[ChatMessage("user", "hello")])
    )
    assert response.provider == "mock"
    assert "hello" in response.content


def test_stream_contract():
    provider = get_chat_provider("mock")
    chunks = list(
        provider.stream(
            ChatRequest(model="test", messages=[ChatMessage("user", "hello")])
        )
    )
    assert chunks


def test_prompt_rendering():
    assert render("Hello {name}", {"name": "World"}) == "Hello World"


def test_chunking():
    chunks = chunk_text(
        "one two three four five six seven eight nine ten", chunk_size=25, overlap=5
    )
    assert chunks
