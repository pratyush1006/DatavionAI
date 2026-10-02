"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import type { EffectiveCapabilityContext } from "../types/capability";
import { resolveCapability } from "../lib/capability";
import {
  fetchEffectiveCapabilityContext,
} from "../lib/capability-client";
import { resolveNavigation } from "../lib/navigation";

type RuntimeShellContextValue = {
  context: EffectiveCapabilityContext | null;
  navigation: ReturnType<typeof resolveNavigation>;
  loading: boolean;
  error: string | null;
  hasCapability: (capability: string) => boolean;
  refresh: () => Promise<void>;
};

const RuntimeShellContext = createContext<RuntimeShellContextValue | null>(
  null,
);

type RuntimeShellProviderProps = {
  children: ReactNode;
};

function isNavigationItemAllowed(
  context: EffectiveCapabilityContext | null,
  item: unknown,
): boolean {
  if (!context || !item || typeof item !== "object") {
    return false;
  }

  const record = item as Record<string, unknown>;

  const capability =
    typeof record.capability === "string"
      ? record.capability
      : typeof record.requiredCapability === "string"
        ? record.requiredCapability
        : null;

  if (capability) {
    return resolveCapability(context, capability);
  }

  const moduleKey =
    typeof record.module === "string"
      ? record.module
      : typeof record.moduleKey === "string"
        ? record.moduleKey
        : null;

  if (moduleKey) {
    return context.modules?.[moduleKey] === true;
  }

  return true;
}

export function RuntimeShellProvider({
  children,
}: RuntimeShellProviderProps) {
  const [context, setContext] =
    useState<EffectiveCapabilityContext | null>(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async (): Promise<void> => {
    setLoading(true);
    setError(null);

    try {
      const result = await fetchEffectiveCapabilityContext();

      const normalizedContext: EffectiveCapabilityContext = {
        userId: result.user_id,
        organizationId: result.organization_id,
        tenantId: result.tenant_id,
        modules: result.modules ?? {},
        features: result.features ?? {},
        permissions: result.permissions ?? [],
        roles: result.roles ?? [],
        facilities: result.facilities ?? [],
        departments: result.departments ?? [],
        dataScopes: result.data_scopes ?? {},
        aiCapabilities: result.ai_capabilities ?? {},
        limits: result.limits ?? {},
      };

      setContext(normalizedContext);
    } catch (runtimeError) {
      setContext(null);

      setError(
        runtimeError instanceof Error
          ? runtimeError.message
          : "Unable to load effective capability context.",
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void refresh();
    }, 0);

    return () => {
      window.clearTimeout(timer);
    };
  }, [refresh]);

  const navigation = useMemo(() => {
    return resolveNavigation(
      [],
      (item) => isNavigationItemAllowed(context, item),
    );
  }, [context]);

  const value = useMemo<RuntimeShellContextValue>(() => {
    return {
      context,
      navigation,
      loading,
      error,
      hasCapability: (capability: string) =>
        resolveCapability(context, capability),
      refresh,
    };
  }, [context, navigation, loading, error, refresh]);

  return (
    <RuntimeShellContext.Provider value={value}>
      {children}
    </RuntimeShellContext.Provider>
  );
}

export function useRuntimeShell(): RuntimeShellContextValue {
  const context = useContext(RuntimeShellContext);

  if (!context) {
    throw new Error(
      "useRuntimeShell must be used inside RuntimeShellProvider.",
    );
  }

  return context;
}

export function useRuntimeCapability(): EffectiveCapabilityContext | null {
  return useRuntimeShell().context;
}

export function useRuntimeNavigation(): RuntimeShellContextValue["navigation"] {
  return useRuntimeShell().navigation;
}

export function useRuntimeLoading(): boolean {
  return useRuntimeShell().loading;
}

export function useRuntimeError(): string | null {
  return useRuntimeShell().error;
}

export function useRuntimeHasCapability(
  capability: string,
): boolean {
  return useRuntimeShell().hasCapability(capability);
}
