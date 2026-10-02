import { API_BASE_URL } from "@/core/api/config";
import type { ReactNode } from "react";

export interface DatavionBootstrapEffective {
  modules: Record<string, boolean>;
  features: Record<string, boolean>;
  permissions: string[];
  roles: string[];
  departments: string[];
  facilities: string[];
  data_scopes?: Record<string, unknown>;
  ai_capabilities?: Record<string, boolean>;
  limits: Record<string, unknown>;
}

export interface DatavionBootstrapResponse {
  user: {
    id: string | null;
    [key: string]: unknown;
  };

  organization: {
    id: string | null;
    [key: string]: unknown;
  };

  tenant: {
    id: string | null;
    [key: string]: unknown;
  };

  subscription: {
    modules: Record<string, boolean>;
    features: Record<string, boolean>;
    limits: Record<string, unknown>;
    [key: string]: unknown;
  } | null;

  entitlements: {
    modules: Record<string, boolean>;
    features: Record<string, boolean>;
    limits: Record<string, unknown>;
    [key: string]: unknown;
  } | null;

  effective: DatavionBootstrapEffective;

  modules: Record<string, boolean>;
  features: Record<string, boolean>;
  permissions: string[];
  roles: string[];
  departments: string[];
  facilities: string[];
  limits: Record<string, unknown>;

  [key: string]: unknown;
}

const DEFAULT_BOOTSTRAP_PATH = "/datavionos/bootstrap/";

function getBootstrapUrl(): string {
  const base =
    API_BASE_URL?.replace(/\/+$/, "") ?? "";

  const path =
    process.env.NEXT_PUBLIC_DATAVION_BOOTSTRAP_PATH ??
    DEFAULT_BOOTSTRAP_PATH;

  if (/^https?:\/\//i.test(path)) {
    return path;
  }

  return `${base}${path.startsWith("/") ? path : `/${path}`}`;
}

export async function fetchDatavionBootstrap(): Promise<
  DatavionBootstrapResponse | null
> {
  const response = await fetch(getBootstrapUrl(), {
    method: "GET",
    credentials: "include",
    headers: {
      Accept: "application/json",
    },
    cache: "no-store",
  });

  if (response.status === 401 || response.status === 403) {
    return null;
  }

  if (!response.ok) {
    throw new Error(
      `DatavionOS bootstrap request failed with HTTP ${response.status}.`,
    );
  }

  return (await response.json()) as DatavionBootstrapResponse;
}
