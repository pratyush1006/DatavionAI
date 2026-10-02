export type OrganizationAccessSnapshot = {
  organization: { id: string; name: string; code: string; organization_type?: string | null };
  departments: DepartmentSummary[];
  teams: TeamSummary[];
  department_type_options: SelectOption[];
  department_templates: DepartmentTemplate[];
  team_type_options: SelectOption[];
  team_templates: TeamTemplate[];
  organization_roles: OrganizationRoleAssignment[];
  available_roles: AvailableRole[];
  employees: EmployeeSummary[];
  department_memberships: DepartmentMembership[];
  permissions: PermissionSummary[];
  ai_capabilities: Record<string, boolean>;
  can_manage_access: boolean;
  can_manage_departments: boolean;
};
export type DepartmentSummary = {
  id: string; name: string; code: string; slug?: string | null;
  department_type?: string | null; status?: string | null;
  is_active: boolean; parent_id?: string | null;
};
export type OrganizationRoleAssignment = {
  id: string; user_id: string; user_email: string; user_name: string;
  role_id: string; role_code: string; role_name: string;
  role_scope: string; role_type: string; is_primary: boolean; is_active: boolean;
};
export type AvailableRole = {
  id: string; code: string; name: string; description: string;
  role_type: string; scope: string; category: string; priority: number;
  is_system: boolean; is_default: boolean; is_active: boolean;
};
export type EmployeeSummary = {
  id: string; user_id?: string | null; name: string; email: string; code?: string | null; is_active: boolean;
};
export type SelectOption = { value: string; label: string };
export type DepartmentTemplate = { department_type: string; name: string; code: string };
export type TeamTemplate = { department_id: string; team_type: string; name: string; code: string };
export type TeamSummary = {
  id: string; name: string; code: string; department_id?: string | null;
};
export type DepartmentMembership = {
  id: string; department_id: string; department_name: string;
  employee_id: string; employee_name: string; role_id?: string | null;
  role_code?: string | null; role_name?: string | null; title: string;
  is_primary: boolean; is_active: boolean;
};
export type PermissionSummary = {
  id: string; code: string; name: string; module: string; action: string;
  scope: string; is_assignable: boolean; is_delegable: boolean;
};
