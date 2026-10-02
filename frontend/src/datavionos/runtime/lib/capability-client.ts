"use client";
import { API_BASE_URL } from "@/core/api/config";
export type EffectiveCapabilityResponse = {
  user_id: string | null;
  organization_id: string | null;
  tenant_id: string | null;

  modules: Record<string, boolean>;
  module_state?: Record<string, boolean>;

  features: Record<string, boolean>;

  permissions: string[];
  roles: string[];

  facilities: string[];
  departments: string[];

  data_scopes: Record<string, unknown>;

  ai_capabilities: Record<string, boolean>;

  limits: Record<string, unknown>;

  capabilities?: {
    effective_capabilities?: string[];
  };

  effective_capabilities?: string[];
};



const CAPABILITY_ENDPOINT =
  "/platform/context/effective/";

const STORAGE_KEYS = [
  "datavion_access_token",
  "datavion_accessToken",
  "access_token",
  "accessToken",
  "auth_token",
  "authToken",
] as const;

function normalizeToken(
  value: unknown,
): string | null {
  if (typeof value !== "string") {
    return null;
  }

  const token = value.trim();

  if (!token) {
    return null;
  }

  if (
    token
      .toLowerCase()
      .startsWith("bearer ")
  ) {
    return (
      token
        .slice(7)
        .trim() || null
    );
  }

  return token;
}

function readBrowserToken(): string | null {
  if (typeof window === "undefined") {
    return null;
  }

  for (
    const key of STORAGE_KEYS
  ) {
    try {
      const value =
        window.localStorage.getItem(
          key,
        );

      const token =
        normalizeToken(value);

      if (token) {
        return token;
      }
    } catch {
      // Continue.
    }

    try {
      const value =
        window.sessionStorage.getItem(
          key,
        );

      const token =
        normalizeToken(value);

      if (token) {
        return token;
      }
    } catch {
      // Continue.
    }
  }

  return null;
}

function readRuntimeToken(): string | null {
  if (
    typeof window === "undefined"
  ) {
    return null;
  }

  const runtime = (
    window as Window & {
      datavionAuthRuntime?: {
        getAccessToken?: () =>
          | string
          | null
          | undefined;

        accessToken?:
          | string
          | null;

        token?:
          | string
          | null;
      };
    }
  ).datavionAuthRuntime;

  if (!runtime) {
    return null;
  }

  if (
    typeof runtime.getAccessToken ===
    "function"
  ) {
    const token =
      normalizeToken(
        runtime.getAccessToken(),
      );

    if (token) {
      return token;
    }
  }

  return (
    normalizeToken(
      runtime.accessToken,
    ) ??
    normalizeToken(
      runtime.token,
    )
  );
}

function normalizeStoredAccessToken(
  value: unknown,
): string | null {
  if (typeof value !== "string") {
    return null;
  }

  const trimmed = value.trim();

  if (!trimmed) {
    return null;
  }

  try {
    const parsed: unknown = JSON.parse(trimmed);

    if (
      typeof parsed === "string" &&
      parsed.trim()
    ) {
      return parsed.trim();
    }

    if (
      typeof parsed === "object" &&
      parsed !== null &&
      "value" in parsed
    ) {
      const candidate = (
        parsed as {
          value?: unknown;
        }
      ).value;

      if (
        typeof candidate === "string" &&
        candidate.trim()
      ) {
        return candidate.trim();
      }
    }
  } catch {
    return trimmed;
  }

  return trimmed;
}

function resolveAuthRuntimeAccessToken():
  | string
  | null {
  if (typeof window === "undefined") {
    return null;
  }

  const runtime = (
    window as Window & {
      authRuntime?: {
        tokenStorage?: {
          getAccessToken?: () =>
            | string
            | null
            | Promise<string | null>;
        };
      };

      datavionAuthRuntime?: {
        tokenStorage?: {
          getAccessToken?: () =>
            | string
            | null
            | Promise<string | null>;
        };

        getAccessToken?: () =>
          | string
          | null;

        accessToken?: string | null;
      };
    }
  );

  const canonicalRuntime =
    runtime.authRuntime;

  const canonicalGetter =
    canonicalRuntime
      ?.tokenStorage
      ?.getAccessToken;

  if (typeof canonicalGetter === "function") {
    try {
      const value =
        canonicalGetter.call(
          canonicalRuntime?.tokenStorage,
        );

      if (
        typeof value === "string" &&
        value.trim()
      ) {
        return value.trim();
      }
    } catch {
      // Continue to the compatibility runtime.
    }
  }

  const compatibilityRuntime =
    runtime.datavionAuthRuntime;

  const compatibilityGetter =
    compatibilityRuntime
      ?.tokenStorage
      ?.getAccessToken;

  if (
    typeof compatibilityGetter ===
    "function"
  ) {
    try {
      const value =
        compatibilityGetter.call(
          compatibilityRuntime?.tokenStorage,
        );

      if (
        typeof value === "string" &&
        value.trim()
      ) {
        return value.trim();
      }
    } catch {
      // Continue to the existing compatibility paths.
    }
  }

  if (
    typeof compatibilityRuntime
      ?.getAccessToken === "function"
  ) {
    try {
      const value =
        compatibilityRuntime.getAccessToken();

      if (
        typeof value === "string" &&
        value.trim()
      ) {
        return value.trim();
      }
    } catch {
      // Continue to the existing compatibility paths.
    }
  }

  return normalizeStoredAccessToken(
    compatibilityRuntime?.accessToken,
  );
}

function resolveAccessToken():
  string | null {
  const runtimeToken =
    resolveAuthRuntimeAccessToken();

  if (runtimeToken) {
    return runtimeToken;
  }

  if (typeof window === "undefined") {
    return null;
  }

  const storageKeys = [
    "datavion:v1:access_token",
    "datavion_access_token",
    "access_token",
  ];

  for (const key of storageKeys) {
    try {
      const stored =
        window.localStorage.getItem(key);

      const token =
        normalizeStoredAccessToken(
          stored,
        );

      if (token) {
        return token;
      }
    } catch {
      continue;
    }
  }

  return null;
}

export function getCapabilityAccessToken():
  | string
  | null {
  return resolveAccessToken();
}

export async function fetchEffectiveCapability(
  signal?: AbortSignal,
): Promise<EffectiveCapabilityResponse> {
  const token =
    resolveAccessToken();

  if (!token) {
    throw new Error(
      "DATAVION_AUTH_REQUIRED: No authenticated access token is available.",
    );
  }

  const response =
    await fetch(
      `${API_BASE_URL}${CAPABILITY_ENDPOINT}`,
      {
        method: "GET",

        headers: {
          Accept:
            "application/json",

          Authorization:
            `Bearer ${token}`,
        },

        credentials: "include",

        cache: "no-store",

        signal,
      },
    );

  if (
    response.status === 401
  ) {
    throw new Error(
      "DATAVION_AUTH_UNAUTHORIZED: Effective capability request returned HTTP 401.",
    );
  }

  if (!response.ok) {
    const body =
      await response
        .text()
        .catch(
          () => "",
        );

    throw new Error(
      `DATAVION_CAPABILITY_REQUEST_FAILED: HTTP ${response.status}${body ? ` - ${body}` : ""}`,
    );
  }

  return (
    (await response.json()) as EffectiveCapabilityResponse
  );
}

/**
 * Backward-compatible canonical context fetcher.
 *
 * Existing runtime callers use this name while the canonical implementation
 * remains fetchEffectiveCapability.
 */
export async function fetchEffectiveCapabilityContext(
  ...args: Parameters<typeof fetchEffectiveCapability>
): ReturnType<typeof fetchEffectiveCapability> {
  return fetchEffectiveCapability(...args);
}

/**
 * Organization module-state compatibility boundary.
 *
 * The effective-capability API is the authoritative read path. This
 * compatibility function intentionally does not invent a backend mutation
 * contract when one is not already exposed by the canonical client.
 *
 * Consumers may use the function only when an explicit organization-module
 * mutation endpoint is supplied by the existing client contract.
 */
export async function updateOrganizationModuleState(
  moduleKey: string,
  input: { enabled: boolean },
): Promise<EffectiveCapabilityResponse> {
  const token = resolveAccessToken();

  if (!token) {
    throw new Error(
      "DATAVION_AUTH_REQUIRED: No authenticated access token is available.",
    );
  }

  const response = await fetch(
    `${API_BASE_URL}/platform/context/effective/`,
    {
      method: "POST",

      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },

      credentials: "include",
      cache: "no-store",

      body: JSON.stringify({
        module_key: moduleKey,
        enabled: input.enabled,
      }),
    },
  );

  if (response.status === 401) {
    throw new Error(
      "DATAVION_AUTH_UNAUTHORIZED: Organization module-state request returned HTTP 401.",
    );
  }

  if (!response.ok) {
    const body = await response.text().catch(() => "");

    throw new Error(
      `DATAVION_MODULE_STATE_UPDATE_FAILED: HTTP ${response.status}${
        body ? ` - ${body}` : ""
      }`,
    );
  }

  return (await response.json()) as EffectiveCapabilityResponse;
}
