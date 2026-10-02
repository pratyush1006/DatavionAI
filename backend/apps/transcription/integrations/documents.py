"""Documents integration; lifecycle remains apps.documents."""


def build_document_payload(*, title, content, context):
    return {
        "title": title,
        "content": content,
        "context": context,
        "source": "transcription",
    }
