/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/domain/defaults.ts
 * =============================================================================
 */

import type {
  EmployeeFormValues,
} from "./schema";

export const employeeDefaults:
  EmployeeFormValues = {
    organization: "",
    user: "",
    employeeCode: "",
    designation: "",
    workEmail: "",
    phoneNumber: "",
    employmentType: "FULL_TIME",
    joiningDate: "",
  };
