from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from apps.hr.api import HrListCreateAPIView, HrRetrieveUpdateDestroyAPIView
from apps.hr.onboarding.services.lifecycle_process import start_lifecycle_process
from apps.hr.permissions import HrPermission
from apps.hr.recruitment.models import Candidate, Interview, JobOpening
from apps.hr.recruitment.serializers import (
    CandidateSerializer,
    InterviewSerializer,
    JobSerializer,
)
from apps.hr.scope import scope_queryset
from apps.organization.employees.models import Employee
from apps.organization.employees.services.employee import create_employee


class CanViewRecruitment(HrPermission):
    permission_code = "recruitment.view"


class CanCreateRecruitment(HrPermission):
    permission_code = "recruitment.create"


class CanUpdateRecruitment(HrPermission):
    permission_code = "recruitment.update"


class CanDeleteRecruitment(HrPermission):
    permission_code = "recruitment.delete"


@transaction.atomic
def save_record(*, validated_data, instance=None, model=None):
    data = dict(validated_data)
    if instance is not None:
        instance = type(instance).objects.select_for_update().get(pk=instance.pk)
        model = type(instance)
    if model is Candidate:
        job = data.get("job", getattr(instance, "job", None))
        job = JobOpening.objects.select_for_update().get(pk=job.pk)
        data["job"] = job
        CandidateSerializer(instance=instance).validate(data)
    elif model is Interview:
        candidate = data.get("candidate", getattr(instance, "candidate", None))
        candidate = Candidate.objects.select_for_update().get(pk=candidate.pk)
        data["candidate"] = candidate
        interviewer = data.get("interviewer", getattr(instance, "interviewer", None))
        Employee.objects.select_for_update().get(pk=interviewer.pk)
        InterviewSerializer(instance=instance).validate(data)
    employee_code = data.pop("employee_code", None)
    joining_date = data.pop("joining_date", None)
    if instance is None:
        instance = model.objects.create(**data)
    else:
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
    if (
        isinstance(instance, Candidate)
        and instance.status == "hired"
        and instance.hired_employee_id is None
    ):
        employee = create_employee(
            validated_data={
                "organization": instance.organization,
                "employee_code": employee_code,
                "designation": instance.job.title,
                "joining_date": joining_date,
                "work_email": instance.email,
                "phone_number": instance.phone,
                "metadata": {
                    "candidate_name": instance.full_name,
                    "recruitment_candidate_id": instance.pk,
                },
            }
        )
        instance.hired_employee = employee
        instance.save(update_fields=["hired_employee"])
        start_lifecycle_process(
            validated_data={
                "organization": instance.organization,
                "employee": employee,
                "process_type": "onboarding",
                "start_date": joining_date,
            }
        )
    if isinstance(instance, Interview) and instance.status == "scheduled":
        Candidate.objects.filter(pk=instance.candidate_id, status="shortlisted").update(
            status="interviewing"
        )
    return instance


def delete_record(*, instance):
    try:
        instance.delete()
    except ProtectedError:
        raise ValidationError(
            "This record has related applications or interviews. Close or cancel it instead."
        ) from None


class RecruitmentList(HrListCreateAPIView):
    create_success_message = "Recruitment record created."
    permission_classes_map = {
        "GET": (CanViewRecruitment,),
        "POST": (CanCreateRecruitment,),
    }
    ordering = ("-created_at",)

    def get_queryset(self):
        return scope_queryset(self.detail_serializer_class.Meta.model.objects.all())

    @staticmethod
    def create_service(*, validated_data):
        raise NotImplementedError


class RecruitmentDetail(HrRetrieveUpdateDestroyAPIView):
    update_success_message = "Recruitment record updated."
    permission_classes_map = {
        "GET": (CanViewRecruitment,),
        "PATCH": (CanUpdateRecruitment,),
        "PUT": (CanUpdateRecruitment,),
        "DELETE": (CanDeleteRecruitment,),
    }
    update_service = staticmethod(save_record)
    delete_service = staticmethod(delete_record)

    def get_queryset(self):
        return scope_queryset(self.detail_serializer_class.Meta.model.objects.all())

    def get_object(self):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])


class JobList(RecruitmentList):
    serializer_classes = {"GET": JobSerializer, "POST": JobSerializer}
    detail_serializer_class = JobSerializer
    search_fields = ("title", "description", "location")
    filterset_fields = ("status", "priority", "department")

    @staticmethod
    def create_service(*, validated_data):
        return save_record(model=JobOpening, validated_data=validated_data)


class JobDetail(RecruitmentDetail):
    serializer_classes = dict.fromkeys(("GET", "PUT", "PATCH"), JobSerializer)
    detail_serializer_class = JobSerializer


class CandidateList(RecruitmentList):
    serializer_classes = {"GET": CandidateSerializer, "POST": CandidateSerializer}
    detail_serializer_class = CandidateSerializer
    search_fields = ("full_name", "email", "job__title")
    filterset_fields = ("status", "job")

    @staticmethod
    def create_service(*, validated_data):
        return save_record(model=Candidate, validated_data=validated_data)


class CandidateDetail(RecruitmentDetail):
    serializer_classes = dict.fromkeys(("GET", "PUT", "PATCH"), CandidateSerializer)
    detail_serializer_class = CandidateSerializer


class InterviewList(RecruitmentList):
    serializer_classes = {"GET": InterviewSerializer, "POST": InterviewSerializer}
    detail_serializer_class = InterviewSerializer
    search_fields = ("candidate__full_name", "location")
    filterset_fields = ("status", "candidate", "interviewer")

    @staticmethod
    def create_service(*, validated_data):
        return save_record(model=Interview, validated_data=validated_data)


class InterviewDetail(RecruitmentDetail):
    serializer_classes = dict.fromkeys(("GET", "PUT", "PATCH"), InterviewSerializer)
    detail_serializer_class = InterviewSerializer
