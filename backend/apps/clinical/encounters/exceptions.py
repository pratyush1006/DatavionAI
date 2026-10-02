class EncounterError(Exception):
    pass


class EncounterValidationError(EncounterError):
    pass


class EncounterTransitionError(EncounterError):
    pass
