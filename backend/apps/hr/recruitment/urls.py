from django.urls import path

from .views import (
    CandidateDetail,
    CandidateList,
    InterviewDetail,
    InterviewList,
    JobDetail,
    JobList,
)

urlpatterns = [
    path("jobs/", JobList.as_view(), name="hr-job-list"),
    path("jobs/<int:pk>/", JobDetail.as_view(), name="hr-job-detail"),
    path("candidates/", CandidateList.as_view(), name="hr-candidate-list"),
    path("candidates/<int:pk>/", CandidateDetail.as_view(), name="hr-candidate-detail"),
    path("interviews/", InterviewList.as_view(), name="hr-interview-list"),
    path("interviews/<int:pk>/", InterviewDetail.as_view(), name="hr-interview-detail"),
]
