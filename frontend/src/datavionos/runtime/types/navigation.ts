import type { EffectiveCapabilityContext } from "./capability";

export type RuntimeNavigationItem = {
  id: string;
  label: string;
  href: string;
  icon?: string;
  requiredCapability?: string;
  requiredModule?: string;
  requiredPermission?: string;
  children?: RuntimeNavigationItem[];
};

export type NavigationResolver = (
  context: EffectiveCapabilityContext,
) => RuntimeNavigationItem[];
