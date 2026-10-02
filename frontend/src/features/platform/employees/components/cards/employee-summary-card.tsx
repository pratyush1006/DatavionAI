/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/components/cards/employee-summary-card.tsx
 * =============================================================================
 *
 * Employee summary presentation.
 * =============================================================================
 */

"use client";

import {
  BriefcaseBusiness,
  Building2,
  Mail,
  Phone,
  UserRound,
} from "lucide-react";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import type {
  Employee,
} from "../../domain";

import {
  EmployeeStatusBadge,
} from "../employee-status-badge";

export type EmployeeSummaryCardProps =
  Readonly<{
    employee: Employee;
  }>;

export function EmployeeSummaryCard({
  employee,
}: EmployeeSummaryCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
              <UserRound className="h-6 w-6 text-primary" />
            </div>

            <div>
              <CardTitle>
                {employee.fullName}
              </CardTitle>

              <p className="text-sm text-muted-foreground">
                {employee.employeeCode}
              </p>
            </div>
          </div>

          <EmployeeStatusBadge
            status={employee.status}
          />
        </div>
      </CardHeader>

      <CardContent>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div className="flex items-start gap-3">
            <BriefcaseBusiness className="mt-0.5 h-4 w-4 text-muted-foreground" />

            <div>
              <p className="text-xs text-muted-foreground">
                Designation
              </p>

              <p className="text-sm font-medium">
                {employee.designation ||
                  "Not specified"}
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Building2 className="mt-0.5 h-4 w-4 text-muted-foreground" />

            <div>
              <p className="text-xs text-muted-foreground">
                Organization
              </p>

              <p className="text-sm font-medium">
                {employee.organization?.name ||
                  "Not assigned"}
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Mail className="mt-0.5 h-4 w-4 text-muted-foreground" />

            <div>
              <p className="text-xs text-muted-foreground">
                Work Email
              </p>

              <p className="break-all text-sm font-medium">
                {employee.workEmail ||
                  "Not provided"}
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <Phone className="mt-0.5 h-4 w-4 text-muted-foreground" />

            <div>
              <p className="text-xs text-muted-foreground">
                Phone
              </p>

              <p className="text-sm font-medium">
                {employee.phoneNumber ||
                  "Not provided"}
              </p>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
