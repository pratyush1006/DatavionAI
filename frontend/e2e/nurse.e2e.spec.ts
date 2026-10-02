import { expect, test } from "@playwright/test";

const organization = "00000000-0000-4000-8000-000000000010";
const patient = "00000000-0000-4000-8000-000000000011";
const user = { id: "00000000-0000-4000-8000-000000000012", email: "priya@example.test", first_name: "Priya", last_name: "Nair", is_verified: true, is_active: true, is_platform_admin: false };
const envelope = (data: unknown) => ({ success: true, message: "Success", data, meta: {} });

test.beforeEach(async ({ page }) => {
  await page.addInitScript(({ user }) => {
    for (const [key, value] of Object.entries({ access_token: "nurse-test-token", refresh_token: "nurse-test-refresh", current_user: user })) {
      const entry = JSON.stringify({ value, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() });
      localStorage.setItem(`datavion:v1:${key}`, entry);
      sessionStorage.setItem(`datavion:v1:${key}`, entry);
    }
  }, { user });
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let data: unknown = [];
    if (path.endsWith("/auth/me/")) data = user;
    else if (path.endsWith("/bootstrap/")) data = {
      user, tenant: { id: organization, name: "ABC Healthcare", tenant_type: "hospital", status: "ACTIVE" },
      organization: { id: organization, name: "ABC Healthcare" }, employee: null,
      access_context: { organization_id: organization, department_id: null, team_id: null },
      permissions: ["nursing.view", "nursing.create", "nursing.update", "patients.view", "vitals.view", "prescriptions.view", "notes.view"], organization_roles: ["nurse"], platform_roles: [],
      modules: [], navigation: [], dashboard: [], branding: {}, feature_flags: {}, subscription: null, preferences: {},
    };
    else if (path.endsWith("/patient-management/patients/")) data = [{ id: patient, mrn: "MRN-100", display_name: "Patient A", phone: "555-0100", status: "active", is_active: true }];
    else if (path.endsWith("/vitals/")) data = [{ id: "vital-1", patient, recorded_at: new Date().toISOString(), oxygen_saturation: 89, pulse: 125, temperature: 39.2, systolic_bp: 185 }];
    else if (path.endsWith("/prescriptions/")) data = [{ id: "rx-1", patient, status: "active", is_active: true, dosage: "10", dosage_unit: "mg", frequency: "twice daily" }];
    else if (path.endsWith("/notes/")) data = [{ note_id: "note-1", patient, title: "Shift note" }];
    else if (path.endsWith("/nursing/assignments/")) data = [{ id: "assignment-1", patient, patient_name: "Patient A", nurse_name: "Priya Nair", ward_name: "Ward A", started_at: "2026-10-01T08:00:00Z", status: "active" }];
    else if (path.endsWith("/nursing/tasks/")) data = [{ id: "task-1", patient, patient_name: "Patient A", title: "Record vitals", priority: "urgent", due_at: "2026-10-01T10:30:00Z", status: "pending" }];
    else if (path.endsWith("/nursing/medication-administrations/")) data = [{ id: "mar-1", patient, patient_name: "Patient A", dose: "10 mg", scheduled_at: "2026-10-01T10:00:00Z", status: "scheduled" }];
    else if (path.endsWith("/nursing/alerts/")) data = [{ id: "alert-1", patient, patient_name: "Patient A", title: "Low oxygen", severity: "critical", status: "open" }];
    else if (path.endsWith("/nursing/schedules/")) data = [{ id: "shift-1", ward_name: "Ward A", shift_type: "morning", status: "active" }];
    else if (path.endsWith("/providers/")) data = [{ id: user.id, display_name: "Priya Nair" }];
    else if (path.endsWith("/hospital-operations/units/")) data = [{ uuid: "00000000-0000-4000-8000-000000000013", name: "Ward A" }];
    await route.fulfill({ json: envelope(data) });
  });
});

test("nurse can create and start a persistent task", async ({ page }) => {
  await page.goto("/nurse?section=tasks", { waitUntil: "domcontentloaded" });
  await page.getByRole("button", { name: "Create" }).click();
  await page.getByLabel("Patient *").selectOption(patient);
  await page.getByLabel("Assigned nurse *").selectOption(user.id);
  await page.getByLabel("Task *").fill("Recheck oxygen");
  await page.getByLabel("Type *").selectOption("vitals");
  await page.getByLabel("Priority *").selectOption("urgent");
  await page.getByLabel("Due at *").fill("2026-10-02T10:30");
  const created = page.waitForRequest((request) => request.method() === "POST" && request.url().endsWith("/nursing/tasks/"));
  await page.getByRole("button", { name: "Save record" }).click();
  expect((await created).postDataJSON()).toMatchObject({ patient, assigned_nurse: user.id, title: "Recheck oxygen", task_type: "vitals", priority: "urgent" });
  const started = page.waitForRequest((request) => request.method() === "POST" && request.url().includes("/nursing/tasks/task-1/start/"));
  await page.getByRole("button", { name: "start", exact: true }).click();
  await started;
});

test("nurse dashboard shows live care workload and critical alerts", async ({ page }) => {
  await page.goto("/nurse", { waitUntil: "domcontentloaded" });
  await expect(page.getByRole("heading", { name: /Priya/ })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Patient Care" })).toBeVisible();
  await expect(page.getByRole("cell", { name: "Patient A" })).toBeVisible();
  await expect(page.getByText("Patient A").first()).toBeVisible();
  await expect(page.getByText("Record vitals")).toBeVisible();
  await expect(page.getByText("Low oxygen")).toBeVisible();
  await expect(page.getByRole("link", { name: /Medication Schedule/ })).toBeVisible();
});
