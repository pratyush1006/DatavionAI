/** DatavionAI backend-authority capability helpers. */
export type EffectiveCapabilityContext = {
  organization?: { id?: string; type?: string };
  subscription?: { plan?: string };
  modules: Record<string, boolean>;
  features: Record<string, boolean>;
  permissions: string[];
  departments?: string[];
};

export function moduleEnabled(context: EffectiveCapabilityContext | null | undefined, key: string): boolean {
  return Boolean(context?.modules?.[key]);
}
export function featureEnabled(context: EffectiveCapabilityContext | null | undefined, key: string): boolean {
  return Boolean(context?.features?.[key]);
}
export function hasPermission(context: EffectiveCapabilityContext | null | undefined, permission: string): boolean {
  return Boolean(context?.permissions?.includes(permission));
}
export function hasAnyPermission(context: EffectiveCapabilityContext | null | undefined, permissions: readonly string[]): boolean {
  if (!permissions.length) return true;
  return permissions.some((permission) => hasPermission(context, permission));
}
