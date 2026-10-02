export function isHrManager(roles: readonly string[], requested: string | null): boolean {
  if (requested === "manager") return true;
  if (requested === "executive") return false;
  return roles.some((role) => role.toLowerCase().replaceAll(" ", "_") === "hr_manager");
}

export function hrLink(section: string, manager: boolean): string {
  return `/workspace/hr?section=${section}&view=${manager ? "manager" : "executive"}`;
}
