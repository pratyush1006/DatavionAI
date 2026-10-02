/**
 * Sidebar navigation group.
 */

import type { ReactNode } from "react";

type SidebarGroupProps = Readonly<{
  title: string;
  children: ReactNode;
}>;

export function SidebarGroup({
  title,
  children,
}: SidebarGroupProps) {
  return (
    <section className="mb-6">
      <h2 className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        {title}
      </h2>

      <div className="space-y-1">
        {children}
      </div>
    </section>
  );
}
