from apps.core.workflows.registry import workflow_registry


def register_notes_workflows():
    workflows = (
        "notes.note.create",
        "notes.note.edit",
        "notes.note.submit_review",
        "notes.note.sign",
        "notes.note.cancel",
        "notes.note.amend",
        "notes.note.amend.accept",
    )
    for name in workflows:
        try:
            workflow_registry.register(name)
        except Exception:
            pass
