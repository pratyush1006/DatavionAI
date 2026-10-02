/**
 * =============================================================================
 * DatavionOS
 * File: src/features/platform/employees/domain/types.ts
 * =============================================================================
 *
 * Employee domain types.
 *
 * The Employee aggregate is the primary frontend representation. Assignment
 * and contract lifecycle operations remain separate domain payloads.
 * =============================================================================
 */

import type {
  EmploymentStatus,
  EmploymentType,
} from "./constants";

/**
 * Lightweight organization reference returned by the Employee API.
 */
export interface EmployeeOrganization {
  readonly id: string;
  readonly name: string;
  readonly code: string | null;
}

/**
 * Lightweight linked user reference.
 */
export interface EmployeeUser {
  readonly id: string;
  readonly email: string;
  readonly name: string;
}

/**
 * Lightweight reporting manager reference.
 */
export interface EmployeeManager {
  readonly id: string;
  readonly employeeCode: string;
  readonly name: string;
}

/**
 * Employee list representation.
 */
export interface Employee {
  readonly id: string;
  readonly organization?: EmployeeOrganization | null;
  readonly user?: EmployeeUser | null;
  readonly employeeCode: string;
  readonly fullName: string;
  readonly designation: string;
  readonly workEmail: string | null;
  readonly phoneNumber: string | null;
  readonly employmentType: EmploymentType;
  readonly status: EmploymentStatus;
  readonly joiningDate: string;
  readonly confirmationDate: string | null;
  readonly terminationDate: string | null;
  readonly manager: EmployeeManager | null;
  readonly metadata: Record<string, unknown>;
  readonly isActiveEmployee: boolean;
  readonly isTerminated: boolean;
  readonly createdAt: string;
  readonly updatedAt: string;
}

/**
 * Create employee payload.
 */
export interface CreateEmployeePayload {
  readonly organization: string;
  readonly user?: string | null;
  readonly employeeCode: string;
  readonly designation: string;
  readonly workEmail?: string | null;
  readonly phoneNumber?: string | null;
  readonly employmentType: EmploymentType;
  readonly joiningDate: string;
}

/**
 * Update employee payload.
 *
 * These fields intentionally match the backend update serializer.
 */
export interface UpdateEmployeePayload {
  readonly designation: string;
  readonly workEmail?: string | null;
  readonly phoneNumber?: string | null;
  readonly employmentType: EmploymentType;
  readonly confirmationDate?: string | null;
  readonly metadata: Record<string, unknown>;
}

/**
 * Assignment action payload.
 */
export interface EmployeeAssignmentPayload {
  readonly departmentId?: string | null;
  readonly teamId?: string | null;
  readonly supervisorId?: string | null;
  readonly effectiveFrom?: string | null;
}

/**
 * Contract action payload.
 */
export interface EmployeeContractPayload {
  readonly contractData: Record<string, unknown>;
}

/**
 * Employee onboarding payload.
 */
export interface EmployeeOnboardingPayload {
  readonly organizationId: string;
  readonly employeeData: Record<string, unknown>;
  readonly contractData?: Record<string, unknown> | null;
  readonly assignmentData?: Record<string, unknown> | null;
}

/**
 * Employee offboarding payload.
 */
export interface EmployeeOffboardingPayload {
  readonly terminationDate?: string | null;
}

/**
 * Generic lifecycle result.
 */
export interface EmployeeLifecycleResult {
  readonly employeeId: string;
  readonly eventId?: string | null;
  readonly activated?: boolean;
  readonly deactivated?: boolean;
  readonly offboarded?: boolean;
}
