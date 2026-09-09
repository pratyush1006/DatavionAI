/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/employee-status-badge.tsx
 * =============================================================================
 *
 * Employee employment-status presentation.
 * =============================================================================
 */

"use client";

import { Badge } from "@/components/ui/badge";

import {
  formatEmployeeEnumLabel,
  type EmploymentStatus,
} from "../domain";

export type EmployeeStatusBadgeProps =
  Readonly<{
    status: EmploymentStatus;
  }>;

export function EmployeeStatusBadge({
  status,
}: EmployeeStatusBadgeProps) {
  const variant =
    status === "ACTIVE"
      ? "default"
      : status === "TERMINATED" ||
          status === "RESIGNED"
        ? "destructive"
        : "secondary";

  return (
    <Badge variant={variant}>
      {formatEmployeeEnumLabel(status)}
    </Badge>
  );
}
