export type HrRecord = Record<string, unknown>;
export type Field = {
  name: string; type?: string; required?: boolean; choices?: string[];
  lookup?: string; default?: string | boolean; nullable?: boolean;
};
export type Action = { route: string; label: string; permission: string; statuses?: string[]; note?: string };
export type Collection = {
  id: string; label: string; path: string; permission: string; columns: string[];
  fields: Field[]; organization?: boolean; updateFields?: string[]; actions?: Action[];
};
const f = (name: string, type = "text", required = false): Field => ({ name, type, required });
const choice = (name: string, choices: string[]): Field => ({ name, choices, default: choices[0] });
const bool = (name: string, value = false): Field => ({ name, type: "checkbox", default: value });
const ref = (name: string, lookup: string, required = true): Field => ({ name, lookup, required, nullable: !required });
const employee = ref("employee", "employees");
const notes = f("notes", "textarea");
const dates = [f("start_date", "date", true), f("end_date", "date", true)];
const category = () => choice("category", ["hr", "it", "facilities", "finance", "manager", "other"]);
const processType = () => choice("process_type", ["onboarding", "offboarding"]);
export const HR_COLLECTIONS: Collection[] = [
  { id: "recruitment", label: "Job openings", path: "/hr/recruitment/jobs/", permission: "recruitment", organization: true,
    columns: ["title", "department_name", "vacancies", "priority", "status", "closing_date"],
    fields: [f("title", "text", true), ref("department", "departments", false), f("description", "textarea"), f("location"), { ...f("vacancies", "number", true), default: "1" }, choice("priority", ["normal", "urgent"]), choice("status", ["draft", "open", "closed"]), { ...f("closing_date", "date"), nullable: true }] },
  { id: "candidates", label: "Candidates", path: "/hr/recruitment/candidates/", permission: "recruitment", organization: true,
    columns: ["full_name", "job_title", "email", "phone", "status"],
    fields: [ref("job", "recruitment"), f("full_name", "text", true), f("email", "email", true), f("phone"), f("resume_url", "url"), notes, choice("status", ["applied", "shortlisted", "interviewing", "offered", "hired", "rejected", "withdrawn"]), f("employee_code"), f("joining_date", "date")] },
  { id: "interviews", label: "Interviews", path: "/hr/recruitment/interviews/", permission: "recruitment", organization: true,
    columns: ["candidate_name", "interviewer_name", "scheduled_at", "duration_minutes", "status"],
    fields: [ref("candidate", "candidates"), ref("interviewer", "employees"), f("scheduled_at", "datetime-local", true), { ...f("duration_minutes", "number", true), default: "60" }, f("location"), f("feedback", "textarea"), choice("status", ["scheduled", "completed", "cancelled"])] },
  { id: "attendance", label: "Attendance", path: "/hr/attendance/", permission: "attendance", organization: true,
    columns: ["employee_name", "work_date", "check_in", "check_out", "hours_worked", "status"],
    fields: [employee, f("work_date", "date", true), { ...f("check_in", "time"), nullable: true }, { ...f("check_out", "time"), nullable: true }, choice("status", ["present", "absent", "half_day", "late", "on_leave", "holiday", "week_off"]), notes] },
  { id: "requests", label: "Leave requests", path: "/hr/leave/requests/", permission: "leave", organization: true,
    columns: ["employee_name", "leave_type", "start_date", "end_date", "number_of_days", "status"],
    fields: [employee, ref("leave_type", "types"), ...dates, f("number_of_days", "number", true), f("reason", "textarea")],
    actions: [
      { route: "approve", label: "Approve", permission: "leave.approve", statuses: ["pending"], note: "decision_notes" },
      { route: "reject", label: "Reject", permission: "leave.approve", statuses: ["pending"], note: "decision_notes" },
      { route: "cancel", label: "Cancel leave", permission: "leave.approve", statuses: ["pending", "approved"] },
    ] },
  { id: "balances", label: "Leave balances", path: "/hr/leave/balances/", permission: "leave",
    columns: ["employee_name", "leave_type", "year", "allocated_days", "used_days", "remaining_days"],
    fields: [employee, ref("leave_type", "types"), f("year", "number", true), f("allocated_days", "number", true), f("used_days", "number"), f("carried_forward_days", "number")] },
  { id: "types", label: "Leave types", path: "/hr/leave/types/", permission: "leave", organization: true,
    columns: ["name", "code", "is_paid", "max_days_per_year", "is_active"],
    fields: [f("name", "text", true), f("code", "text", true), f("description", "textarea"), bool("is_paid", true), bool("requires_approval", true), f("max_days_per_year", "number"), bool("allow_carry_forward"), bool("is_active", true)] },
  { id: "shifts", label: "Shifts", path: "/hr/shifts/", permission: "shifts", organization: true,
    columns: ["name", "code", "start_time", "end_time", "is_night_shift", "is_active"],
    fields: [f("name", "text", true), f("code", "text", true), f("start_time", "time", true), f("end_time", "time", true), f("break_minutes", "number"), bool("is_night_shift"), bool("is_active", true)] },
  { id: "assignments", label: "Shift assignments", path: "/hr/shifts/assignments/", permission: "shifts", organization: true,
    columns: ["employee_name", "shift", "work_date", "status"],
    fields: [employee, ref("shift", "shifts"), f("work_date", "date", true), choice("status", ["scheduled", "completed", "absent", "swapped", "cancelled"]), notes] },
  { id: "holidays", label: "Holidays", path: "/hr/holidays/", permission: "holidays", organization: true,
    columns: ["name", "date", "holiday_type", "is_recurring_yearly"],
    fields: [f("name", "text", true), f("date", "date", true), choice("holiday_type", ["mandatory", "optional"]), f("description", "textarea"), bool("is_recurring_yearly")],
    actions: [{ route: "apply-to-attendance", label: "Apply to attendance", permission: "holidays.update" }] },
  { id: "salaries", label: "Salary structures", path: "/hr/payroll/salary-structures/", permission: "payroll", organization: true,
    columns: ["employee_name", "basic_salary", "gross_salary", "currency", "effective_from", "is_active"],
    fields: [employee, f("basic_salary", "number", true), f("house_rent_allowance", "number"), f("other_allowances", "number"), { ...f("currency"), default: "INR" }, f("effective_from", "date", true), { ...f("effective_to", "date"), nullable: true }, bool("is_active", true)] },
  { id: "payslips", label: "Payslips", path: "/hr/payroll/payslips/", permission: "payroll", organization: true,
    columns: ["employee_name", "pay_period_start", "pay_period_end", "net_pay", "currency", "status"],
    fields: [employee, f("pay_period_start", "date", true), f("pay_period_end", "date", true), f("basic_salary", "number", true), f("total_allowances", "number"), { ...f("currency"), default: "INR" }, notes, f("line_items", "line-items")],
    actions: [{ route: "process", label: "Process", permission: "payroll.verify", statuses: ["draft"] }, { route: "mark-paid", label: "Mark paid", permission: "payroll.release", statuses: ["processed"] }] },
  { id: "processes", label: "Onboarding / offboarding", path: "/hr/onboarding/processes/", permission: "onboarding", organization: true,
    columns: ["employee_name", "process_type", "start_date", "target_completion_date", "completion_percentage", "status"],
    fields: [employee, processType(), f("start_date", "date", true), { ...f("target_completion_date", "date"), nullable: true }, notes], updateFields: ["target_completion_date", "notes"],
    actions: [{ route: "complete", label: "Complete", permission: "onboarding.update", statuses: ["in_progress"] }, { route: "cancel", label: "Cancel process", permission: "onboarding.update", statuses: ["in_progress"] }] },
  { id: "tasks", label: "Lifecycle tasks", path: "/hr/onboarding/tasks/", permission: "onboarding",
    columns: ["title", "process", "assigned_to_name", "due_date", "is_mandatory", "status"],
    fields: [ref("process", "processes"), f("title", "text", true), f("description", "textarea"), category(), bool("is_mandatory", true), ref("assigned_to", "employees", false), choice("status", ["pending", "in_progress", "completed", "skipped"]), { ...f("due_date", "date"), nullable: true }, f("order", "number"), notes] },
  { id: "templates", label: "Task templates", path: "/hr/onboarding/task-templates/", permission: "onboarding", organization: true,
    columns: ["title", "process_type", "category", "is_mandatory", "order", "is_active"],
    fields: [processType(), f("title", "text", true), f("description", "textarea"), category(), bool("is_mandatory", true), f("order", "number"), bool("is_active", true)] },
  { id: "cycles", label: "Review cycles", path: "/hr/performance/cycles/", permission: "performance", organization: true,
    columns: ["name", "start_date", "end_date", "status"],
    fields: [f("name", "text", true), ...dates, choice("status", ["upcoming", "active", "closed"])] },
  { id: "reviews", label: "Performance reviews", path: "/hr/performance/reviews/", permission: "performance",
    columns: ["employee_name", "cycle", "reviewer", "overall_rating", "status"],
    fields: [ref("cycle", "cycles"), employee, ref("reviewer", "employees", false), { ...f("overall_rating", "number"), nullable: true }, f("strengths", "textarea"), f("areas_for_improvement", "textarea"), f("reviewer_comments", "textarea")],
    actions: [{ route: "submit", label: "Submit", permission: "performance.update", statuses: ["draft"] }, { route: "acknowledge", label: "Acknowledge", permission: "performance.update", statuses: ["submitted"], note: "employee_comments" }, { route: "complete", label: "Complete", permission: "performance.update", statuses: ["acknowledged"] }] },
  { id: "goals", label: "Performance goals", path: "/hr/performance/goals/", permission: "performance",
    columns: ["title", "review", "weight", "target_date", "rating", "status"],
    fields: [ref("review", "reviews"), f("title", "text", true), f("description", "textarea"), f("weight", "number"), { ...f("target_date", "date"), nullable: true }, choice("status", ["not_started", "in_progress", "completed", "deferred"]), { ...f("rating", "number"), nullable: true }] },
];
export const label = (value: string) => value.replaceAll("_", " ").replace(/^./, (c) => c.toUpperCase());
