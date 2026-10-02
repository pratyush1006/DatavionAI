"""
DatavionOS lifecycle manager.
"""

from __future__ import annotations

from collections.abc import Iterable

from apps.datavionos.lifecycle.base import (
    LifecycleComponent,
)


class LifecycleManager:
    """
    Manages the lifecycle of registered
    DatavionOS components.
    """

    def __init__(
        self,
    ) -> None:
        """
        Initialize the lifecycle manager.
        """

        self._components: dict[
            str,
            LifecycleComponent,
        ] = {}

    def register(
        self,
        component: LifecycleComponent,
    ) -> None:
        """
        Register a lifecycle component.
        """

        self._components[component.component_id] = component

    def unregister(
        self,
        component_id: str,
    ) -> None:
        """
        Remove a registered component.
        """

        self._components.pop(
            component_id,
            None,
        )

    def get(
        self,
        component_id: str,
    ) -> LifecycleComponent | None:
        """
        Retrieve a registered component.
        """

        return self._components.get(
            component_id,
        )

    def contains(
        self,
        component_id: str,
    ) -> bool:
        """
        Determine whether a component
        is registered.
        """

        return component_id in self._components

    @property
    def component_count(
        self,
    ) -> int:
        """
        Number of registered components.
        """

        return len(
            self._components,
        )

    @property
    def components(
        self,
    ) -> tuple[LifecycleComponent, ...]:
        """
        Registered components.
        """

        return tuple(
            self._components.values(),
        )

    def __iter__(
        self,
    ) -> Iterable[LifecycleComponent]:
        """
        Iterate over components.
        """

        return iter(
            self._components.values(),
        )

    def start_all(
        self,
    ) -> None:
        """
        Start every registered component.
        """

        for component in self._components.values():
            component.start()

    def stop_all(
        self,
    ) -> None:
        """
        Stop every running component.
        """

        for component in self._components.values():
            if component.is_running:
                component.stop()

    def pause_all(
        self,
    ) -> None:
        """
        Pause every running component.
        """

        for component in self._components.values():
            if component.is_running:
                component.pause()

    def resume_all(
        self,
    ) -> None:
        """
        Resume every paused component.
        """

        for component in self._components.values():
            if component.state == "paused":
                component.resume()

    def restart_all(
        self,
    ) -> None:
        """
        Restart every registered component.
        """

        for component in self._components.values():
            component.restart()

    def health_summary(
        self,
    ) -> dict[str, bool]:
        """
        Return the health of every component.
        """

        return {
            component.component_id: component.health_check()
            for component in self._components.values()
        }

    def clear(
        self,
    ) -> None:
        """
        Remove all registered components.
        """

        self._components.clear()


__all__ = [
    "LifecycleManager",
]
