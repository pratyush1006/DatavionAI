from apps.clinical.encounters.workflows import (
    EncounterCancelWorkflow,
    EncounterCompleteWorkflow,
    EncounterCreateWorkflow,
    EncounterDeleteWorkflow,
    EncounterStartWorkflow,
    EncounterUpdateWorkflow,
)

WORKFLOW_REGISTRY = {
    "encounter.create": EncounterCreateWorkflow,
    "encounter.update": EncounterUpdateWorkflow,
    "encounter.start": EncounterStartWorkflow,
    "encounter.complete": EncounterCompleteWorkflow,
    "encounter.cancel": EncounterCancelWorkflow,
    "encounter.delete": EncounterDeleteWorkflow,
}
