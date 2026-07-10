/**
 * Dashboard grid layout.
 */

import type { ReactNode } from "react";

type DashboardGridProps = Readonly<{
  children: ReactNode;
}>;

export function DashboardGrid({
  children,
}: DashboardGridProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
      {children}
    </div>
  );
}
