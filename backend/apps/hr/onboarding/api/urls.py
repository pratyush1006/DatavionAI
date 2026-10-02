from django.urls import path

from apps.hr.onboarding.api.views import (
    LifecycleProcessCancelAPIView,
    LifecycleProcessCompleteAPIView,
    LifecycleProcessListCreateAPIView,
    LifecycleProcessRetrieveUpdateDestroyAPIView,
    LifecycleTaskListCreateAPIView,
    LifecycleTaskRetrieveUpdateDestroyAPIView,
    LifecycleTaskTemplateListCreateAPIView,
    LifecycleTaskTemplateRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "task-templates/",
        LifecycleTaskTemplateListCreateAPIView.as_view(),
        name="task-template-list-create",
    ),
    path(
        "task-templates/<int:task_template_id>/",
        LifecycleTaskTemplateRetrieveUpdateDestroyAPIView.as_view(),
        name="task-template-detail",
    ),
    path(
        "processes/",
        LifecycleProcessListCreateAPIView.as_view(),
        name="lifecycle-process-list-create",
    ),
    path(
        "processes/<int:lifecycle_process_id>/",
        LifecycleProcessRetrieveUpdateDestroyAPIView.as_view(),
        name="lifecycle-process-detail",
    ),
    path(
        "processes/<int:lifecycle_process_id>/complete/",
        LifecycleProcessCompleteAPIView.as_view(),
        name="lifecycle-process-complete",
    ),
    path(
        "processes/<int:lifecycle_process_id>/cancel/",
        LifecycleProcessCancelAPIView.as_view(),
        name="lifecycle-process-cancel",
    ),
    path(
        "tasks/",
        LifecycleTaskListCreateAPIView.as_view(),
        name="lifecycle-task-list-create",
    ),
    path(
        "tasks/<int:lifecycle_task_id>/",
        LifecycleTaskRetrieveUpdateDestroyAPIView.as_view(),
        name="lifecycle-task-detail",
    ),
]
