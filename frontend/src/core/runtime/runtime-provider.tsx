"use client";

import React, {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  fetchDatavionBootstrap,
  type DatavionBootstrapResponse,
} from "./runtime-api";

export interface DatavionRuntimeContextValue {
  loading: boolean;
  authenticated: boolean;
  error: string | null;

  user: DatavionBootstrapResponse["user"] | null;
  organization: DatavionBootstrapResponse["organization"] | null;
  tenant: DatavionBootstrapResponse["tenant"] | null;

  subscription: DatavionBootstrapResponse["subscription"] | null;
  entitlements: DatavionBootstrapResponse["entitlements"] | null;

  effective: DatavionBootstrapResponse["effective"] | null;

  modules: Record<string, boolean>;
  features: Record<string, boolean>;
  permissions: string[];
  roles: string[];
  departments: string[];
  facilities: string[];
  limits: Record<string, unknown>;

  bootstrap: DatavionBootstrapResponse | null;

  refresh: () => Promise<void>;
}

const DatavionRuntimeContext = createContext<
  DatavionRuntimeContextValue | undefined
>(undefined);

export function DatavionRuntimeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [bootstrap, setBootstrap] =
    useState<DatavionBootstrapResponse | null>(null);

  const refresh = useCallback(async (): Promise<void> => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetchDatavionBootstrap();

      if (!response) {
        setAuthenticated(false);
        setBootstrap(null);
        return;
      }

      setBootstrap(response);
      setAuthenticated(true);
    } catch (exc) {
      setAuthenticated(false);
      setBootstrap(null);

      const message =
        exc instanceof Error
          ? exc.message
          : "Unable to load DatavionOS runtime.";

      setError(message);
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

  const value = useMemo<DatavionRuntimeContextValue>(() => {
    const effective = bootstrap?.effective ?? null;

    return {
      loading,
      authenticated,
      error,

      user: bootstrap?.user ?? null,
      organization: bootstrap?.organization ?? null,
      tenant: bootstrap?.tenant ?? null,

      subscription: bootstrap?.subscription ?? null,
      entitlements: bootstrap?.entitlements ?? null,

      effective,

      modules: effective?.modules ?? bootstrap?.modules ?? {},
      features: effective?.features ?? bootstrap?.features ?? {},

      permissions:
        effective?.permissions ?? bootstrap?.permissions ?? [],

      roles: effective?.roles ?? bootstrap?.roles ?? [],

      departments:
        effective?.departments ?? bootstrap?.departments ?? [],

      facilities:
        effective?.facilities ?? bootstrap?.facilities ?? [],

      limits: effective?.limits ?? bootstrap?.limits ?? {},

      bootstrap,

      refresh,
    };
  }, [authenticated, bootstrap, error, loading, refresh]);

  return (
    <DatavionRuntimeContext.Provider value={value}>
      {children}
    </DatavionRuntimeContext.Provider>
  );
}

/**
 * Compatibility export retained for existing layout.tsx consumers.
 */
export const DatavionOSRuntimeProvider = DatavionRuntimeProvider;

export function useDatavionRuntime(): DatavionRuntimeContextValue {
  const context = React.useContext(DatavionRuntimeContext);

  if (!context) {
    throw new Error(
      "useDatavionRuntime must be used inside DatavionRuntimeProvider.",
    );
  }

  return context;
}

export function useDatavionBootstrap(): DatavionBootstrapResponse | null {
  return useDatavionRuntime().bootstrap;
}
