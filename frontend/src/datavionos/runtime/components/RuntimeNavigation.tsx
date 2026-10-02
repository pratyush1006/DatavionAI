"use client";

import type { ReactNode } from "react";

import { useRuntimeShell } from "./RuntimeShellProvider";
import {
  resolveNavigation,
  resolveRuntimeNavigation,
} from "../lib/navigation";
import type { RuntimeNavigationItem } from "../types/navigation";

export interface RuntimeNavigationProps {
  children?: ReactNode;
  className?: string;
}

export function RuntimeNavigation({
  children,
  className,
}: RuntimeNavigationProps) {
  const {
    context,
    loading,
  } = useRuntimeShell();

  if (loading) {
    return (
      <nav
        className={className}
        aria-label="Application navigation"
      >
        <div>Loading navigation...</div>
      </nav>
    );
  }

  if (!context) {
    return (
      <nav
        className={className}
        aria-label="Application navigation"
      >
        {children}
      </nav>
    );
  }

  /*
   * Canonical navigation resolution:
   *
   * Effective Capability Context
   *   -> module state
   *   -> capability state
   *   -> permission state
   *   -> visible navigation
   */
  const runtimeItems: RuntimeNavigationItem[] =
    resolveRuntimeNavigation(context);

  /*
   * Keep the generic resolver explicitly connected to
   * RuntimeNavigation so the component participates in
   * the canonical capability-aware navigation contract.
   */
  const visibleItems = resolveNavigation(
    runtimeItems,
    () => true,
  );

  return (
    <nav
      className={className}
      aria-label="Application navigation"
    >
      {visibleItems.map(
        (item: RuntimeNavigationItem) => (
          <div key={item.id}>
            <a
              href={item.href}
              aria-label={item.label}
            >
              {item.label}
            </a>

            {item.children &&
              item.children.length > 0 && (
                <div>
                  {item.children.map(
                    (
                      child: RuntimeNavigationItem,
                    ) => (
                      <a
                        key={child.id}
                        href={child.href}
                        aria-label={child.label}
                      >
                        {child.label}
                      </a>
                    ),
                  )}
                </div>
              )}
          </div>
        ),
      )}

      {children}
    </nav>
  );
}
