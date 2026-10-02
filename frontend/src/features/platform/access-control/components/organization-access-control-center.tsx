"use client";

import { useEffect, useState } from "react";
import {
  assignDepartmentMember,
  createDepartment,
  createTeam,
  assignOrganizationRole,
  getOrganizationAccessControl,
  setDepartmentMemberActive,
  setOrganizationRoleActive,
} from "../api";
import type { OrganizationAccessSnapshot } from "../domain";

export function OrganizationAccessControlCenter() {
  const [data, setData] = useState<OrganizationAccessSnapshot | null>(null);
  const [tab, setTab] = useState<"roles" | "departments">("roles");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [departmentName, setDepartmentName] = useState("");
  const [departmentCode, setDepartmentCode] = useState("");
  const [departmentType, setDepartmentType] = useState("GENERAL");
  const [teamName, setTeamName] = useState("");
  const [teamCode, setTeamCode] = useState("");
  const [teamDepartmentId, setTeamDepartmentId] = useState("");
  const [teamType, setTeamType] = useState("CLINICAL");

  const load = async () => {
    try {
      setData(await getOrganizationAccessControl());
      setError("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unable to load access controls.");
    }
  };

  useEffect(() => {
    let cancelled = false;

    void getOrganizationAccessControl()
      .then((snapshot) => {
        if (cancelled) return;
        setData(snapshot);
        setError("");
      })
      .catch((e) => {
        if (cancelled) return;
        setError(e instanceof Error ? e.message : "Unable to load access controls.");
      });

    return () => {
      cancelled = true;
    };
  }, []);

  if (!data && !error) {
    return <div className="container-fluid py-4">Loading access controls...</div>;
  }
  if (!data) {
    return (
      <div className="container-fluid py-4">
        <div className="d-flex flex-wrap justify-content-between align-items-start gap-3 mb-4">
          <div>
            <div className="small text-body-secondary text-uppercase fw-semibold">Organization administration</div>
            <h1 className="h3 mb-1">Access control</h1>
            <p className="text-body-secondary mb-0">Users, organization roles, and department membership are managed by the backend.</p>
          </div>
        </div>
        <div className="alert alert-danger" role="alert">
          <div className="fw-semibold mb-1">Access controls could not be loaded</div>
          <div>{error}</div>
          <button type="button" className="btn btn-sm btn-outline-danger mt-3" onClick={() => void load()}>Try again</button>
        </div>
      </div>
    );
  }

  const activeEmployees = data.employees.filter((x) => x.is_active);
  const employeesWithAccounts = activeEmployees.filter((x) => x.user_id);
  const departmentTemplatesForType = data.department_templates.filter(
    (template) => template.department_type === departmentType,
  );
  const teamTemplatesForSelection = data.team_templates.filter(
    (template) => template.department_id === teamDepartmentId && template.team_type === teamType,
  );

  const roleToggle = async (id: string, active: boolean) => {
    setBusy(true);
    try { await setOrganizationRoleActive(id, active); await load(); }
    catch (e) { setError(e instanceof Error ? e.message : "Role update failed."); }
    finally { setBusy(false); }
  };

  const memberToggle = async (id: string, active: boolean) => {
    setBusy(true);
    try { await setDepartmentMemberActive(id, active); await load(); }
    catch (e) { setError(e instanceof Error ? e.message : "Membership update failed."); }
    finally { setBusy(false); }
  };

  return (
    <div className="container-fluid py-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h1 className="h3 mb-1">Organization Access Control</h1>
          <p className="text-secondary mb-0">{data.organization.name} · {data.organization.code}</p>
        </div>
        <span className="badge text-bg-light border">Backend-authoritative RBAC</span>
      </div>

      {error && <div className="alert alert-info">{error}</div>}

      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button type="button" className={`nav-link ${tab === "roles" ? "active" : ""}`} onClick={() => setTab("roles")}>
            Users & Roles
          </button>
        </li>
        <li className="nav-item">
          <button type="button" className={`nav-link ${tab === "departments" ? "active" : ""}`} onClick={() => setTab("departments")}>
            Departments
          </button>
        </li>
      </ul>

      {tab === "roles" && (
        <div className="row g-4">
          <div className="col-12 col-xl-8">
            <div className="card shadow-sm">
              <div className="card-header bg-white"><strong>Organization Role Assignments</strong></div>
              <div className="table-responsive">
                <table className="table table-hover align-middle mb-0">
                  <thead><tr><th>User</th><th>Role</th><th>Scope</th><th>Status</th><th /></tr></thead>
                  <tbody>
                    {data.organization_roles.map((x) => (
                      <tr key={x.id}>
                        <td><div className="fw-semibold">{x.user_name || x.user_email}</div><small className="text-secondary">{x.user_email}</small></td>
                        <td><div>{x.role_name}</div><small className="text-secondary">{x.role_code}</small></td>
                        <td>{x.role_scope}</td>
                        <td><span className={`badge ${x.is_active ? "text-bg-success" : "text-bg-secondary"}`}>{x.is_active ? "Active" : "Inactive"}</span></td>
                        <td className="text-end">
                          <button className="btn btn-sm btn-outline-secondary" disabled={busy || !data.can_manage_access} onClick={() => void roleToggle(x.id, !x.is_active)}>
                            {x.is_active ? "Disable" : "Enable"}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div className="col-12 col-xl-4">
            <div className="card shadow-sm">
              <div className="card-header bg-white"><strong>Role Assignment</strong></div>
              <div className="card-body">
                <label className="form-label">User</label>
                <select id="org-user" className="form-select mb-3" defaultValue="">
                  <option value="" disabled>Select user</option>
                  {employeesWithAccounts.map((x) => <option key={x.id} value={x.user_id!}>{x.name || x.email}</option>)}
                </select>
                <label className="form-label">Role</label>
                <select id="org-role" className="form-select mb-3" defaultValue="">
                  <option value="" disabled>Select role</option>
                  {data.available_roles.map((x) => <option key={x.id} value={x.id}>{x.name} ({x.code})</option>)}
                </select>
                <button
                  className="btn btn-primary w-100"
                  disabled={busy || !data.can_manage_access}
                  onClick={() => {
                    const user = (document.getElementById("org-user") as HTMLSelectElement).value;
                    const role = (document.getElementById("org-role") as HTMLSelectElement).value;
                    if (!user || !role) return;
                    setBusy(true);
                    void assignOrganizationRole({ user_id: user, role_id: role, is_active: true })
                      .then(load)
                      .catch((e) => setError(e instanceof Error ? e.message : "Role assignment failed."))
                      .finally(() => setBusy(false));
                  }}
                >
                  Assign Role
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {tab === "departments" && (
        <div className="row g-4">
          <div className="col-12">
            <div className="card shadow-sm"><div className="card-header bg-white"><strong>Create Department</strong></div><div className="card-body"><div className="row g-3 align-items-end"><div className="col-12 col-md-3"><label className="form-label" htmlFor="department-type">Department type</label><select id="department-type" className="form-select" value={departmentType} onChange={(event) => { setDepartmentType(event.target.value); setDepartmentName(""); setDepartmentCode(""); }}><option value="">Choose a type</option>{data.department_type_options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></div><div className="col-12 col-md-3"><label className="form-label" htmlFor="department-template">Department name</label><select id="department-template" className="form-select" value={departmentCode} disabled={!departmentType} onChange={(event) => { const template = departmentTemplatesForType.find((item) => item.code === event.target.value); setDepartmentName(template?.name || ""); setDepartmentCode(template?.code || ""); }}><option value="">Choose a department</option>{departmentTemplatesForType.map((template) => <option key={template.code} value={template.code}>{template.name}</option>)}</select></div><div className="col-12 col-md-3"><label className="form-label" htmlFor="department-code">Department code</label><input id="department-code" className="form-control bg-body-secondary" value={departmentCode} readOnly placeholder="Selected with department" aria-describedby="department-code-help" /><div id="department-code-help" className="form-text">Generated from the selected template.</div></div><div className="col-12 col-md-3"><button className="btn btn-primary w-100" disabled={busy || !data.can_manage_departments || !departmentName || !departmentCode} onClick={() => { setBusy(true); void createDepartment({ name: departmentName, code: departmentCode, department_type: departmentType }).then(() => { setDepartmentName(""); setDepartmentCode(""); return load(); }).catch((e) => setError(e instanceof Error ? e.message : "Department creation failed.")).finally(() => setBusy(false)); }}>{busy ? "Saving…" : "Create Department"}</button></div></div><p className="small text-secondary mb-0 mt-3">All values are selected from the backend catalogue. The department name and code are locked to the selected type.</p></div></div>
          </div>
          <div className="col-12">
            <div className="card shadow-sm"><div className="card-header bg-white"><strong>Create Team</strong></div><div className="card-body"><div className="row g-3 align-items-end"><div className="col-12 col-md-3"><label className="form-label" htmlFor="team-department">Department *</label><select id="team-department" className="form-select" value={teamDepartmentId} onChange={(event) => { setTeamDepartmentId(event.target.value); setTeamName(""); setTeamCode(""); }}><option value="">Choose a department</option>{data.departments.filter((department) => department.is_active).map((department) => <option key={department.id} value={department.id}>{department.name} ({department.code})</option>)}</select></div><div className="col-12 col-md-2"><label className="form-label" htmlFor="team-type">Team type</label><select id="team-type" className="form-select" value={teamType} onChange={(event) => { setTeamType(event.target.value); setTeamName(""); setTeamCode(""); }}><option value="">Choose a type</option>{data.team_type_options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></div><div className="col-12 col-md-3"><label className="form-label" htmlFor="team-template">Team name</label><select id="team-template" className="form-select" value={teamCode} disabled={!teamDepartmentId || !teamType} onChange={(event) => { const template = teamTemplatesForSelection.find((item) => item.code === event.target.value); setTeamName(template?.name || ""); setTeamCode(template?.code || ""); }}><option value="">Choose a team</option>{teamTemplatesForSelection.map((template) => <option key={template.code} value={template.code}>{template.name}</option>)}</select></div><div className="col-12 col-md-2"><label className="form-label" htmlFor="team-code">Team code</label><input id="team-code" className="form-control bg-body-secondary" value={teamCode} readOnly placeholder="Selected with team" aria-describedby="team-code-help" /><div id="team-code-help" className="form-text">Generated from the selected template.</div></div><div className="col-12 col-md-2"><button className="btn btn-primary w-100" disabled={busy || !data.can_manage_departments || !teamDepartmentId || !teamName || !teamCode} onClick={() => { setBusy(true); void createTeam({ department_id: teamDepartmentId, name: teamName, code: teamCode, team_type: teamType }).then(() => { setTeamName(""); setTeamCode(""); setTeamDepartmentId(""); return load(); }).catch((e) => setError(e instanceof Error ? e.message : "Team creation failed.")).finally(() => setBusy(false)); }}>{busy ? "Saving…" : "Create Team"}</button></div></div><p className="small text-secondary mb-0 mt-3">All team fields are selected from the backend catalogue for the chosen department and team type.</p></div></div>
          </div>
          <div className="col-12">
            <div className="card shadow-sm">
              <div className="card-header bg-white"><strong>Department Memberships</strong></div>
              <div className="table-responsive">
                <table className="table table-hover align-middle mb-0">
                  <thead><tr><th>Department</th><th>Employee</th><th>Department Role</th><th>Status</th><th /></tr></thead>
                  <tbody>
                    {data.department_memberships.length === 0 && (
                      <tr><td colSpan={5} className="py-4 text-center text-secondary">No employee department memberships have been assigned yet.</td></tr>
                    )}
                    {data.department_memberships.map((x) => (
                      <tr key={x.id}>
                        <td>{x.department_name}</td>
                        <td>{x.employee_name}</td>
                        <td>{x.role_name || "Not assigned"}</td>
                        <td><span className={`badge ${x.is_active ? "text-bg-success" : "text-bg-secondary"}`}>{x.is_active ? "Active" : "Inactive"}</span></td>
                        <td className="text-end">
                          <button className="btn btn-sm btn-outline-secondary" disabled={busy} onClick={() => void memberToggle(x.id, !x.is_active)}>
                            {x.is_active ? "Disable" : "Enable"}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div className="col-12">
            <div className="card shadow-sm">
              <div className="card-header bg-white"><strong>Assign Employee to Department</strong></div>
              <div className="table-responsive">
                <table className="table table-hover align-middle mb-0">
                  <thead><tr><th>Department</th><th>Employee</th><th className="text-end">Action</th></tr></thead>
                  <tbody>
                    {data.departments.length === 0 && <tr><td colSpan={3} className="py-4 text-center text-secondary">Create a department before assigning employees.</td></tr>}
                    {data.departments.map((department) => (
                      <tr key={department.id}>
                        <td><div className="fw-semibold">{department.name}</div><small className="text-secondary">{department.code}</small></td>
                        <td><select id={`employee-${department.id}`} className="form-select" defaultValue="" disabled={activeEmployees.length === 0}><option value="">{activeEmployees.length === 0 ? "No active employees available" : "Select employee"}</option>{activeEmployees.map((x) => <option key={x.id} value={x.id}>{x.name || x.email}</option>)}</select></td>
                        <td className="text-end"><button className="btn btn-outline-primary" disabled={busy || !data.can_manage_departments || activeEmployees.length === 0} onClick={() => { const employee = (document.getElementById(`employee-${department.id}`) as HTMLSelectElement).value; if (!employee) return; setBusy(true); void assignDepartmentMember({ department_id: department.id, employee_id: employee }).then(load).catch((e) => setError(e instanceof Error ? e.message : "Department assignment failed.")).finally(() => setBusy(false)); }}>Assign employee</button></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}

      {!data.can_manage_access && !data.can_manage_departments && (
        <div className="alert alert-warning mt-4">
          Your current RBAC context is read-only for this organization. A platform administrator does not automatically receive an organization role; select an organization where you have the required role, or assign an organization administrator through the platform workflow.
        </div>
      )}
    </div>
  );
}
