from django.db import models
class ParticipantType(models.TextChoices):
    PATIENT="patient","Patient"; PROVIDER="provider","Provider"; NURSE="nurse","Nurse"; INTERPRETER="interpreter","Interpreter"; OBSERVER="observer","Observer"
class ParticipantStatus(models.TextChoices):
    INVITED="invited","Invited"; ADMITTED="admitted","Admitted"; JOINED="joined","Joined"; LEFT="left","Left"; REMOVED="removed","Removed"
class ConnectionQuality(models.TextChoices):
    EXCELLENT="excellent","Excellent"; GOOD="good","Good"; FAIR="fair","Fair"; POOR="poor","Poor"; DISCONNECTED="disconnected","Disconnected"
class MediaPermission(models.TextChoices):
    PROMPT="prompt","Prompt"; GRANTED="granted","Granted"; DENIED="denied","Denied"; NOT_APPLICABLE="not_applicable","Not Applicable"
