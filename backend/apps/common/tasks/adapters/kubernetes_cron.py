"""
Kubernetes CronJob adapter for DatavionOS.

Provides a Kubernetes CronJob integration contract without
coupling the task kernel to Kubernetes client libraries.

The Kubernetes manifests and cluster operations belong to
the deployment/infrastructure layer.
"""

from __future__ import annotations

from apps.common.tasks.adapters.base import (
    BaseSchedulerAdapter,
)
from apps.common.tasks.scheduler import (
    ScheduleDefinition,
)


class KubernetesCronJobAdapter(
    BaseSchedulerAdapter,
):
    """
    Kubernetes CronJob scheduler adapter.

    Responsible for translating DatavionOS schedule
    definitions into Kubernetes CronJob resources.

    No Kubernetes dependency is required inside the kernel.
    """

    name = "kubernetes_cronjob"

    def __init__(
        self,
    ) -> None:
        """
        Initialize adapter.
        """

        self._schedules: dict[
            str,
            ScheduleDefinition,
        ] = {}

    def register(
        self,
        definition: ScheduleDefinition,
    ) -> None:
        """
        Register a Kubernetes CronJob definition.

        Kubernetes resource generation is handled by
        infrastructure deployment tooling.
        """

        self._schedules[definition.schedule_id] = definition

    def unregister(
        self,
        schedule_id: str,
    ) -> None:
        """
        Remove Kubernetes CronJob definition.
        """

        self._schedules.pop(
            schedule_id,
            None,
        )

    def sync(
        self,
    ) -> None:
        """
        Synchronize schedules with Kubernetes.

        Deployment layer can generate:

        - CronJob YAML
        - Helm templates
        - Kubernetes API resources
        """

        return


__all__: tuple[str, ...] = ("KubernetesCronJobAdapter",)
