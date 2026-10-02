from __future__ import annotations
import uuid
from django.core.exceptions import ValidationError
from django.db import models
from apps.clinical.providers.models import Provider
from apps.core.models import BaseManager, BaseModel
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization
from apps.telemedicine.constants import DEFAULT_SESSION_STATUS, SessionStatus, SessionType
class TelemedicineSession(BaseModel):
    objects=BaseManager()
    organization=models.ForeignKey(Organization,on_delete=models.CASCADE,related_name="telemedicine_sessions")
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="telemedicine_sessions")
    provider=models.ForeignKey(Provider,on_delete=models.PROTECT,related_name="telemedicine_sessions")
    appointment=models.OneToOneField("appointments.Appointment",on_delete=models.SET_NULL,related_name="telemedicine_session",null=True,blank=True)
    session_id=models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    scheduled_start=models.DateTimeField(); scheduled_end=models.DateTimeField(); actual_start=models.DateTimeField(null=True,blank=True); actual_end=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=20,choices=SessionStatus.choices,default=DEFAULT_SESSION_STATUS,db_index=True)
    session_type=models.CharField(max_length=20,choices=SessionType.choices,default=SessionType.VIDEO)
    connection_url=models.URLField(blank=True); connection_id=models.CharField(max_length=128,blank=True); provider_name=models.CharField(max_length=100,blank=True)
    recording_consent=models.BooleanField(default=False); cancellation_reason=models.TextField(blank=True); failure_reason=models.TextField(blank=True); notes=models.TextField(blank=True)
    class Meta:
        db_table="telemedicine_sessions"; ordering=("-scheduled_start",)
        indexes=[models.Index(fields=["organization","status"],name="tele_sess_org_status_idx"),models.Index(fields=["patient","scheduled_start"],name="tele_sess_pat_start_idx"),models.Index(fields=["provider","scheduled_start"],name="tele_sess_prov_start_idx"),models.Index(fields=["appointment"],name="tele_sess_appt_idx")]
    def clean(self):
        super().clean()
        if self.scheduled_end<=self.scheduled_start: raise ValidationError({"scheduled_end":"Session end must be after session start."})
        for field,label in (("appointment","Appointment"),("provider","Provider"),("patient","Patient")):
            obj_id=getattr(self,field+"_id",None)
            if obj_id:
                obj=type(getattr(self,field)).objects.filter(pk=obj_id).values_list("organization_id",flat=True).first()
                if obj and obj!=self.organization_id: raise ValidationError({field:f"{label} belongs to another organization."})
    def __str__(self): return f"{self.session_id} | {self.status}"
