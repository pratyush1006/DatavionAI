"""
Architecture tests for the clinical transcription bounded context.
"""

from __future__ import annotations

from pathlib import Path

from django.test import SimpleTestCase


class TranscriptionArchitectureTests(SimpleTestCase):
    def test_canonical_patient_reference(self):
        package = Path(__file__).parents[1]
        sources = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                package.joinpath("models", "__init__.py"),
                package.joinpath("models_legacy.py"),
                package.joinpath("models", "live.py"),
            )
        )
        self.assertNotIn("apps.clinical." + "patients", sources)
        self.assertIn("patient_core.Patient", sources)

    def test_workflow_registry_contains_complete_mutation_surface(self):
        source = (
            Path(__file__)
            .parents[1]
            .joinpath(
                "workflow_registry.py",
            )
            .read_text(encoding="utf-8")
        )
        for name in (
            "transcription.job.create",
            "transcription.job.queue",
            "transcription.job.run",
            "transcription.job.cancel",
            "transcription.note.generate",
            "transcription.note.review",
            "transcription.note.sign",
        ):
            self.assertIn(name, source)

    def test_event_publication_is_after_commit(self):
        source = (
            Path(__file__)
            .parents[1]
            .joinpath(
                "services",
                "__init__.py",
            )
            .read_text(encoding="utf-8")
        )
        self.assertIn("publish_after_commit", source)
        self.assertNotIn("publisher.publish(", source)

    def test_provider_boundary_is_fail_closed(self):
        source = (
            Path(__file__)
            .parents[1]
            .joinpath(
                "integrations",
                "providers.py",
            )
            .read_text(encoding="utf-8")
        )
        self.assertIn("TRANSCRIPTION_SPEECH_PROVIDER", source)
        self.assertIn("TRANSCRIPTION_NOTE_PROVIDER", source)
