import { apiClient } from "@/core/api";
import type { OrganizationAccessSnapshot } from "../domain";

// Keep this aligned with backend/config/urls.py.  This feature used a stale
// route name, so every request was returning 404 before the screen could load.
const BASE = "/organization-access/";

// React development mode intentionally mounts effects more than once.  Without
// request de-duplication that behavior also made the access-control screen and
// employee dialog issue identical heavyweight snapshot requests in parallel.
// This is only an in-flight cache: every subsequent completed action still
// fetches fresh, backend-authoritative data.
let activeSnapshotRequest: Promise<OrganizationAccessSnapshot> | null = null;

export async function getOrganizationAccessControl() {
  if (!activeSnapshotRequest) {
    activeSnapshotRequest = apiClient
      .get<OrganizationAccessSnapshot>(BASE)
      .then((response) => response.data)
      .finally(() => {
        activeSnapshotRequest = null;
      });
  }
  return activeSnapshotRequest;
}
export async function assignOrganizationRole(input: {
  user_id: string; role_id: string; is_primary?: boolean; is_active?: boolean;
}) {
  const response = await apiClient.post(BASE + "roles/assign/", input);
  return response.data;
}
export async function setOrganizationRoleActive(id: string, is_active: boolean) {
  const response = await apiClient.patch(`${BASE}roles/${id}/lifecycle/`, { is_active });
  return response.data;
}
export async function assignDepartmentMember(input: {
  department_id: string; employee_id: string; role_id?: string | null;
  title?: string; is_primary?: boolean;
}) {
  const response = await apiClient.post(BASE + "department-members/assign/", input);
  return response.data;
}
export async function setDepartmentMemberActive(id: string, is_active: boolean) {
  const response = await apiClient.patch(
    `${BASE}department-members/${id}/lifecycle/`, { is_active },
  );
  return response.data;
}
export async function createDepartment(input: { name: string; code: string; department_type?: string }) {
  const response = await apiClient.post(BASE + "departments/", input);
  return response.data;
}
export async function createTeam(input: { name: string; code: string; department_id: string; team_type?: string }) {
  const response = await apiClient.post(BASE + "teams/", input);
  return response.data;
}

export async function onboardOrganizationMember(input: {
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  temporary_password: string;
  role_id: string;
  designation: string;
  employee_code?: string;
  employment_type?: string;
  joining_date?: string;
  department_id?: string | null;
  team_id?: string | null;
  supervisor_id?: string | null;
}) {
  const response = await apiClient.post<{
    user_id: string;
    employee_id: string;
    role_assignment_id: string;
    role_name: string;
  }>(BASE + "members/onboard/", input);
  return response.data;
}
