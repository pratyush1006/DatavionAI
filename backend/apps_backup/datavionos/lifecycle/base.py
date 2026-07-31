"""
DatavionOS lifecycle component base.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
)

from apps.datavionos.lifecycle.state import (
    LifecycleState,
)


class LifecycleComponent(ABC):
    """
    Base lifecycle component.

    Defines the contract implemented by every
    long-running DatavionOS component.
    """

    @property
    @abstractmethod
    def component_id(self) -> str:
        """
        Unique component identifier.
        """

    @property
    @abstractmethod
    def component_name(self) -> str:
        """
        Human readable component name.
        """

    @property
    @abstractmethod
    def state(self) -> LifecycleState:
        """
        Current lifecycle state.
        """

    @abstractmethod
    def start(self) -> None:
        """
        Start the component.
        """

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the component.
        """

    @abstractmethod
    def pause(self) -> None:
        """
        Pause the component.
        """

    @abstractmethod
    def resume(self) -> None:
        """
        Resume the component.
        """

    @abstractmethod
    def restart(self) -> None:
        """
        Restart the component.
        """

    @abstractmethod
    def health_check(self) -> bool:
        """
        Return component health.
        """

    @property
    def is_failed(self) -> bool:
        """
        Whether the component has failed.
        """

        return self._state is LifecycleState.FAILED

    @property
    def is_running(self) -> bool:
        """
        Whether the component is running.
        """

        return self.state is LifecycleState.RUNNING

    @property
    def is_stopped(self) -> bool:
        """
        Whether the component is stopped.
        """

        return self.state in {
            LifecycleState.STOPPED,
            LifecycleState.TERMINATED,
        }

    def supports(
        self,
        capability: Any,
    ) -> bool:
        """
        Determine whether the component
        supports the supplied capability.
        """

        return False


__all__ = [
    "LifecycleComponent",
]
