def can_acquire(*, procedure, assessment):
    if getattr(procedure, "cect", False):
        return (
            assessment is not None
            and str(getattr(assessment, "status", "")) == "administered"
        )
    return True
