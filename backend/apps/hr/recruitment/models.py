from django.db import models

from apps.core.models import TimeStampedModel


class JobOpening(TimeStampedModel):
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    department = models.ForeignKey(
        "departments.Department", on_delete=models.PROTECT, null=True, blank=True
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    vacancies = models.PositiveIntegerField(default=1)
    priority = models.CharField(
        max_length=20,
        choices=[("normal", "Normal"), ("urgent", "Urgent")],
        default="normal",
    )
    status = models.CharField(
        max_length=20,
        choices=[("draft", "Draft"), ("open", "Open"), ("closed", "Closed")],
        default="draft",
    )
    closing_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(vacancies__gte=1), name="hr_job_positive_vacancies"
            )
        ]

    def __str__(self) -> str:
        return str(self.title)


class Candidate(TimeStampedModel):
    hired_employee = models.OneToOneField(
        "employees.Employee",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="recruitment_application",
    )
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        JobOpening, on_delete=models.PROTECT, related_name="candidates"
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    resume_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            (value, value.title())
            for value in (
                "applied",
                "shortlisted",
                "interviewing",
                "offered",
                "hired",
                "rejected",
                "withdrawn",
            )
        ],
        default="applied",
    )

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["job", "email"], name="hr_candidate_unique_application"
            )
        ]

    def __str__(self) -> str:
        return str(self.full_name)


class Interview(TimeStampedModel):
    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE
    )
    candidate = models.ForeignKey(
        Candidate, on_delete=models.PROTECT, related_name="interviews"
    )
    interviewer = models.ForeignKey("employees.Employee", on_delete=models.PROTECT)
    scheduled_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    location = models.CharField(max_length=200, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("scheduled", "Scheduled"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="scheduled",
    )

    class Meta:
        ordering = ["scheduled_at", "id"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(duration_minutes__gte=1),
                name="hr_interview_positive_duration",
            )
        ]
