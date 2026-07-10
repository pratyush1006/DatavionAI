/**
 * Reusable enterprise list page layout.
 */

"use client";

import type { ReactNode } from "react";

import { PageContainer } from "@/components/layout/page-container";
import { PageHeader } from "@/components/layout/page-header";

import { cn } from "@/lib/utils";

export type ListPageProps = Readonly<{
  title: string;

  description?: string;

  actions?: ReactNode;

  toolbar?: ReactNode;

  filters?: ReactNode;

  children: ReactNode;

  footer?: ReactNode;

  className?: string;
}>;

export function ListPage({
  title,
  description,
  actions,
  toolbar,
  filters,
  children,
  footer,
  className,
}: ListPageProps) {
  return (
    <PageContainer
      className={cn(
        "space-y-6",
        className,
      )}
    >
      <PageHeader
        title={title}
        description={description}
        actions={actions}
      />

      {(toolbar || filters) && (
        <section className="space-y-4">
          {toolbar}

          {filters}
        </section>
      )}

      <main className="space-y-6">
        {children}
      </main>

      {footer && (
        <footer>
          {footer}
        </footer>
      )}
    </PageContainer>
  );
}
