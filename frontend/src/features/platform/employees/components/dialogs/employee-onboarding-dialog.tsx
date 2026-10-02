/** Create a login-enabled employee in the active organization. */

"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";

import { EntityDialog } from "@/components/common/dialogs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  getOrganizationAccessControl,
  onboardOrganizationMember,
} from "@/features/platform/access-control/api/service";
import type {
  AvailableRole,
  DepartmentSummary,
  EmployeeSummary,
  TeamSummary,
} from "@/features/platform/access-control/domain";

const today = () => new Date().toISOString().slice(0, 10);

export function EmployeeOnboardingDialog() {
  const [open, setOpen] = useState(false);
  const [roles, setRoles] = useState<AvailableRole[]>([]);
  const [departments, setDepartments] = useState<DepartmentSummary[]>([]);
  const [teams, setTeams] = useState<TeamSummary[]>([]);
  const [supervisors, setSupervisors] = useState<EmployeeSummary[]>([]);
  const [loadingRoles, setLoadingRoles] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({
    firstName: "", lastName: "", email: "", phone: "", temporaryPassword: "",
    roleId: "", designation: "", employeeCode: "", employmentType: "FULL_TIME",
    joiningDate: today(), departmentId: "", teamId: "", supervisorId: "",
  });

  useEffect(() => {
    if (!open) return;
    setLoadingRoles(true);
    getOrganizationAccessControl()
      .then((snapshot) => {
        const assignable = snapshot.available_roles.filter((role) => role.is_active);
        setRoles(assignable);
        setDepartments(snapshot.departments.filter((department) => department.is_active));
        setTeams(snapshot.teams);
        setSupervisors(snapshot.employees.filter((employee) => employee.is_active));
        setForm((current) => ({ ...current, roleId: current.roleId || assignable[0]?.id || "" }));
      })
      .catch(() => toast.error("Unable to load roles for the active organization."))
      .finally(() => setLoadingRoles(false));
  }, [open]);

  function update(name: keyof typeof form, value: string) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit() {
    if (!form.roleId) {
      toast.error("Select the access role this employee needs.");
      return;
    }
    setSubmitting(true);
    try {
      const member = await onboardOrganizationMember({
        email: form.email.trim(), first_name: form.firstName.trim(), last_name: form.lastName.trim(),
        phone: form.phone.trim(), temporary_password: form.temporaryPassword, role_id: form.roleId,
        designation: form.designation.trim(), employee_code: form.employeeCode.trim(),
        employment_type: form.employmentType, joining_date: form.joiningDate,
        department_id: form.departmentId || null,
        team_id: form.teamId || null,
        supervisor_id: form.supervisorId || null,
      });
      toast.success(`Created employee access with the ${member.role_name} role.`);
      setOpen(false);
      setForm({
        firstName: "", lastName: "", email: "", phone: "", temporaryPassword: "",
        roleId: "", designation: "", employeeCode: "", employmentType: "FULL_TIME",
        joiningDate: today(), departmentId: "", teamId: "", supervisorId: "",
      });
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Unable to onboard the employee.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <Button type="button" onClick={() => setOpen(true)}>Onboard Employee</Button>
      <EntityDialog
        open={open}
        onOpenChange={setOpen}
        title="Onboard employee"
        description="Creates their login and employee record, then assigns one pre-seeded least-privilege RBAC role in the active organization."
        size="xl"
      >
        <div className="space-y-5">
          <div className="grid gap-4 md:grid-cols-2">
            <Field label="First name" value={form.firstName} onChange={(value) => update("firstName", value)} required />
            <Field label="Last name" value={form.lastName} onChange={(value) => update("lastName", value)} required />
            <Field label="Work email" type="email" value={form.email} onChange={(value) => update("email", value)} required />
            <Field label="Phone" value={form.phone} onChange={(value) => update("phone", value)} />
            <Field label="Temporary password" type="password" value={form.temporaryPassword} onChange={(value) => update("temporaryPassword", value)} required />
            <Field label="Designation" value={form.designation} onChange={(value) => update("designation", value)} placeholder="Doctor, Nurse, Billing Officer" required />
            <Field label="Employee code" value={form.employeeCode} onChange={(value) => update("employeeCode", value)} placeholder="Optional — generated automatically" />
            <Field label="Joining date" type="date" value={form.joiningDate} onChange={(value) => update("joiningDate", value)} required />
          </div>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="space-y-2">
              <Label htmlFor="member-department">Department</Label>
              <select id="member-department" className="border-input bg-background h-9 w-full rounded-md border px-3 text-sm" value={form.departmentId} onChange={(event) => { update("departmentId", event.target.value); update("teamId", ""); }}>
                <option value="">No department assignment</option>
                {departments.map((department) => <option key={department.id} value={department.id}>{department.name}</option>)}
              </select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="member-team">Team</Label>
              <select id="member-team" className="border-input bg-background h-9 w-full rounded-md border px-3 text-sm" value={form.teamId} disabled={!form.departmentId} onChange={(event) => update("teamId", event.target.value)}>
                <option value="">No team assignment</option>
                {teams.filter((team) => team.department_id === form.departmentId).map((team) => <option key={team.id} value={team.id}>{team.name}</option>)}
              </select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="member-supervisor">Supervisor</Label>
              <select id="member-supervisor" className="border-input bg-background h-9 w-full rounded-md border px-3 text-sm" value={form.supervisorId} onChange={(event) => update("supervisorId", event.target.value)}>
                <option value="">No supervisor assigned</option>
                {supervisors.map((employee) => <option key={employee.id} value={employee.id}>{employee.name || employee.email}</option>)}
              </select>
            </div>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="member-role">Job role / access preset *</Label>
              <select id="member-role" className="border-input bg-background h-9 w-full rounded-md border px-3 text-sm" value={form.roleId} disabled={loadingRoles} onChange={(event) => update("roleId", event.target.value)}>
                <option value="">{loadingRoles ? "Loading roles…" : "Choose the required role"}</option>
                {roles.map((role) => <option key={role.id} value={role.id}>{role.name}</option>)}
              </select>
              <p className="text-muted-foreground text-xs">Roles and permissions are seeded and controlled by the backend. The selected preset determines the employee's modules and allowed actions after sign-in.</p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="employment-type">Employment type</Label>
              <select id="employment-type" className="border-input bg-background h-9 w-full rounded-md border px-3 text-sm" value={form.employmentType} onChange={(event) => update("employmentType", event.target.value)}>
                <option value="FULL_TIME">Full time</option><option value="PART_TIME">Part time</option><option value="CONTRACT">Contract</option><option value="CONSULTANT">Consultant</option>
              </select>
            </div>
          </div>
          <p className="text-muted-foreground text-sm">The temporary password is never displayed again. Give it to the employee through an approved secure channel and instruct them to change it after their first sign-in.</p>
          <div className="flex justify-end gap-3">
            <Button type="button" variant="outline" onClick={() => setOpen(false)} disabled={submitting}>Cancel</Button>
            <Button type="button" onClick={handleSubmit} disabled={submitting || loadingRoles || !form.firstName.trim() || !form.lastName.trim() || !form.email.trim() || !form.temporaryPassword || !form.designation.trim()}>
              {submitting ? "Creating…" : "Create employee access"}
            </Button>
          </div>
        </div>
      </EntityDialog>
    </>
  );
}

function Field({ label, value, onChange, type = "text", placeholder, required = false }: { label: string; value: string; onChange: (value: string) => void; type?: string; placeholder?: string; required?: boolean }) {
  const id = `member-${label.toLowerCase().replaceAll(" ", "-")}`;
  return <div className="space-y-2"><Label htmlFor={id}>{label}{required ? " *" : ""}</Label><Input id={id} type={type} value={value} placeholder={placeholder} onChange={(event) => onChange(event.target.value)} /></div>;
}
