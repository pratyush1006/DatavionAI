/**
 * Statistic card.
 */

import type { LucideIcon } from "lucide-react";

import { DashboardCard } from "../cards/dashboard-card";

type StatCardProps = Readonly<{
  title: string;
  value: string;
  icon: LucideIcon;
}>;

export function StatCard({
  title,
  value,
  icon: Icon,
}: StatCardProps) {
  return (
    <DashboardCard>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-muted-foreground">
            {title}
          </p>

          <h2 className="mt-2 text-3xl font-bold">
            {value}
          </h2>
        </div>

        <Icon className="h-8 w-8 text-primary" />
      </div>
    </DashboardCard>
  );
}
