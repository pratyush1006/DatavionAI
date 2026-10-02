"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  EffectiveCapabilityContext,
  EffectiveCapabilityResponse,
  getEffectiveCapabilityEndpoint,
  hasAnyPermission,
  hasPermission,
  isAIEnabled,
  isFeatureEnabled,
  isModuleEnabled,
  normalizeEffectiveCapability,
} from "@/lib/datavionos/effective-capability";

interface CapabilityProviderValue {
  context: EffectiveCapabilityContext | null;

  loading: boolean;
  error: string | null;

  refresh: () => Promise<void>;

  moduleEnabled: (name: string) => boolean;
  featureEnabled: (name: string) => boolean;
  aiEnabled: (name: string) => boolean;

  can: (permission: string) => boolean;
  canAny: (permissions: string[]) => boolean;
}

const CapabilityContext =
  createContext<CapabilityProviderValue | null>(null);

export function DatavionOSCapabilityProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [context, setContext] =
    useState<EffectiveCapabilityContext | null>(null);

  const [loading, setLoading] =
    useState<boolean>(true);

  const [error, setError] =
    useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        getEffectiveCapabilityEndpoint(),
        {
          method: "GET",

          credentials: "include",

          headers: {
            Accept: "application/json",
          },

          cache: "no-store",
        },
      );

      const payload =
        (await response.json()) as EffectiveCapabilityResponse;

      if (
        !response.ok ||
        payload.success === false
      ) {
        throw new Error(
          payload.error?.message ??
            "Unable to load effective organization capabilities.",
        );
      }

      setContext(
        normalizeEffectiveCapability(
          payload,
        ),
      );
    } catch (exception) {
      setContext(null);

      setError(
        exception instanceof Error
          ? exception.message
          : "Unable to load organization capabilities.",
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

  const value =
    useMemo<CapabilityProviderValue>(
      () => ({
        context,

        loading,

        error,

        refresh,

        moduleEnabled: (name) =>
          isModuleEnabled(
            context,
            name,
          ),

        featureEnabled: (name) =>
          isFeatureEnabled(
            context,
            name,
          ),

        aiEnabled: (name) =>
          isAIEnabled(
            context,
            name,
          ),

        can: (permission) =>
          hasPermission(
            context,
            permission,
          ),

        canAny: (permissions) =>
          hasAnyPermission(
            context,
            permissions,
          ),
      }),
      [
        context,
        loading,
        error,
        refresh,
      ],
    );

  return (
    <CapabilityContext.Provider
      value={value}
    >
      {children}
    </CapabilityContext.Provider>
  );
}

export function useDatavionOSCapabilities() {
  const value =
    useContext(
      CapabilityContext,
    );

  if (!value) {
    throw new Error(
      "useDatavionOSCapabilities must be used inside DatavionOSCapabilityProvider.",
    );
  }

  return value;
}

export function CapabilityGate({
  capability,
  children,
  fallback = null,
}: {
  capability: string;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}) {
  const {
    loading,
    moduleEnabled,
    featureEnabled,
    aiEnabled,
  } =
    useDatavionOSCapabilities();

  if (loading) {
    return null;
  }

  const enabled =
    moduleEnabled(capability) ||
    featureEnabled(capability) ||
    aiEnabled(capability);

  return enabled
    ? children
    : fallback;
}
