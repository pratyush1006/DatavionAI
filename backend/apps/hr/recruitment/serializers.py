from datetime import timedelta

from rest_framework import serializers

from apps.hr.recruitment.models import Candidate, Interview, JobOpening


class OrganizationSerializer(serializers.ModelSerializer):
    """Check both submitted and retained relationships on partial updates."""

    def validate(self, attrs):
        organization = attrs.get(
            "organization", getattr(self.instance, "organization", None)
        )
        for field in ("department", "job", "candidate", "interviewer"):
            relation = attrs.get(field, getattr(self.instance, field, None))
            if (
                relation
                and organization
                and relation.organization_id != organization.pk
            ):
                raise serializers.ValidationError(
                    {field: "Must belong to the selected organization."}
                )
        return attrs


class JobSerializer(OrganizationSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    vacancies = serializers.IntegerField(min_value=1, default=1)

    class Meta:
        model = JobOpening
        fields = (
            "id",
            "organization",
            "department",
            "department_name",
            "title",
            "description",
            "location",
            "vacancies",
            "priority",
            "status",
            "closing_date",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if (
            self.instance
            and attrs.get("vacancies", self.instance.vacancies)
            < self.instance.candidates.filter(status="hired").count()
        ):
            raise serializers.ValidationError(
                {"vacancies": "Cannot reduce vacancies below the number already hired."}
            )
        return attrs


class CandidateSerializer(OrganizationSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    employee_code = serializers.CharField(
        write_only=True, required=False, allow_blank=True, max_length=50
    )
    joining_date = serializers.DateField(write_only=True, required=False)

    class Meta:
        model = Candidate
        fields = (
            "id",
            "organization",
            "job",
            "job_title",
            "employee_code",
            "joining_date",
            "hired_employee",
            "full_name",
            "email",
            "phone",
            "resume_url",
            "notes",
            "status",
            "created_at",
        )
        read_only_fields = ("id", "created_at", "hired_employee")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        job = attrs.get("job", getattr(self.instance, "job", None))
        if job and (not self.instance or "job" in attrs) and job.status != "open":
            raise serializers.ValidationError(
                {"job": "Applications require an open job."}
            )
        transitions = {
            "applied": {"shortlisted", "rejected", "withdrawn"},
            "shortlisted": {"interviewing", "rejected", "withdrawn"},
            "interviewing": {"offered", "rejected", "withdrawn"},
            "offered": {"hired", "rejected", "withdrawn"},
            "hired": set(),
            "rejected": set(),
            "withdrawn": set(),
        }
        current = self.instance.status if self.instance else "applied"
        target = attrs.get("status", current)
        if (not self.instance and target != "applied") or (
            target != current and target not in transitions[current]
        ):
            raise serializers.ValidationError(
                {"status": "Invalid candidate stage transition."}
            )
        if (
            target == "offered"
            and target != current
            and not self.instance.interviews.filter(status="completed").exists()
        ):
            raise serializers.ValidationError(
                {"status": "Complete an interview before making an offer."}
            )
        if self.instance and "job" in attrs and job.pk != self.instance.job_id:
            raise serializers.ValidationError(
                {"job": "A submitted application cannot change jobs."}
            )
        if target == "hired" and current != "hired":
            if job.status != "open":
                raise serializers.ValidationError(
                    {"job": "Reopen the job before hiring."}
                )
            if job.candidates.filter(status="hired").count() >= job.vacancies:
                raise serializers.ValidationError(
                    {"status": "All vacancies have been filled."}
                )
            for field in ("employee_code", "joining_date"):
                if not attrs.get(field):
                    raise serializers.ValidationError(
                        {field: "Required when hiring a candidate."}
                    )
            request = self.context.get("request")
            if request:
                from apps.platform.rbac.engines import user_has_permission

                for permission in ("employees.create", "onboarding.create"):
                    if not user_has_permission(
                        user=request.user,
                        permission=permission,
                        organization=job.organization,
                    ):
                        raise serializers.ValidationError(
                            {
                                "status": "Employee creation and onboarding permission are required to hire."
                            }
                        )
        return attrs


class InterviewSerializer(OrganizationSerializer):
    candidate_name = serializers.CharField(source="candidate.full_name", read_only=True)
    interviewer_name = serializers.CharField(
        source="interviewer.full_name", read_only=True
    )
    duration_minutes = serializers.IntegerField(min_value=1, max_value=480, default=60)

    class Meta:
        model = Interview
        fields = (
            "id",
            "organization",
            "candidate",
            "candidate_name",
            "interviewer",
            "interviewer_name",
            "scheduled_at",
            "duration_minutes",
            "location",
            "feedback",
            "status",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        candidate = attrs.get("candidate", getattr(self.instance, "candidate", None))
        current = self.instance.status if self.instance else "scheduled"
        target = attrs.get("status", current)
        if (not self.instance and target != "scheduled") or (
            current != "scheduled" and target != current
        ):
            raise serializers.ValidationError(
                {"status": "Only scheduled interviews can be completed or cancelled."}
            )
        if (
            target == "completed"
            and not attrs.get(
                "feedback", getattr(self.instance, "feedback", "")
            ).strip()
        ):
            raise serializers.ValidationError(
                {"feedback": "Feedback is required to complete an interview."}
            )
        if target == "scheduled":
            if candidate and (
                candidate.status not in {"shortlisted", "interviewing"}
                or candidate.job.status != "open"
            ):
                raise serializers.ValidationError(
                    {
                        "candidate": "Select a shortlisted or interviewing candidate for an open job."
                    }
                )
            start = attrs.get(
                "scheduled_at", getattr(self.instance, "scheduled_at", None)
            )
            duration = attrs.get(
                "duration_minutes", getattr(self.instance, "duration_minutes", 60)
            )
            interviewer = attrs.get(
                "interviewer", getattr(self.instance, "interviewer", None)
            )
            if start and interviewer:
                meetings = Interview.objects.filter(
                    interviewer=interviewer,
                    status="scheduled",
                    scheduled_at__lt=start + timedelta(minutes=duration),
                )
                if self.instance:
                    meetings = meetings.exclude(pk=self.instance.pk)
                if any(
                    meeting.scheduled_at + timedelta(minutes=meeting.duration_minutes)
                    > start
                    for meeting in meetings
                ):
                    raise serializers.ValidationError(
                        {
                            "scheduled_at": "The interviewer already has an overlapping interview."
                        }
                    )
        return attrs
