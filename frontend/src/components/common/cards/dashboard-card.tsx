/**
 * Dashboard card.
 */

import type { ReactNode } from "react";

import { Card } from "@/components/ui/card";

type DashboardCardProps = Readonly<{
  children: ReactNode;
}>;

export function DashboardCard({
  children,
}: DashboardCardProps) {
  return (
    <Card className="p-6">
      {children}
    </Card>
  );
}
