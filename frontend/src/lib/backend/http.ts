import type { ApiEnvelope } from "./contracts";
import { API_BASE_URL } from "@/core/api/config";

const ACCESS_TOKEN_KEY =
  "datavion_access_token";

const REFRESH_TOKEN_KEY =
  "datavion_refresh_token";

function buildUrl(
  path: string,
): string {
  if (
    /^https?:\/\//i.test(path)
  ) {
    return path;
  }

  return `${API_BASE_URL}${
    path.startsWith("/")
      ? path
      : `/${path}`
  }`;
}

export function getAccessToken(): string | null {
  if (
    typeof window === "undefined"
  ) {
    return null;
  }

  return window.localStorage.getItem(
    ACCESS_TOKEN_KEY,
  );
}

export function getRefreshToken(): string | null {
  if (
    typeof window === "undefined"
  ) {
    return null;
  }

  return window.localStorage.getItem(
    REFRESH_TOKEN_KEY,
  );
}

export function storeTokens(
  access: string,
  refresh: string,
): void {
  if (
    typeof window === "undefined"
  ) {
    return;
  }

  window.localStorage.setItem(
    ACCESS_TOKEN_KEY,
    access,
  );

  window.localStorage.setItem(
    REFRESH_TOKEN_KEY,
    refresh,
  );
}

export function clearTokens(): void {
  if (
    typeof window === "undefined"
  ) {
    return;
  }

  window.localStorage.removeItem(
    ACCESS_TOKEN_KEY,
  );

  window.localStorage.removeItem(
    REFRESH_TOKEN_KEY,
  );
}

function getErrorMessage(
  body: unknown,
  fallback: string,
): string {
  if (
    !body ||
    typeof body !== "object"
  ) {
    return fallback;
  }

  const value =
    body as Record<string, unknown>;

  const error = value.error;

  if (
    error &&
    typeof error === "object"
  ) {
    const record =
      error as Record<string, unknown>;

    if (
      typeof record.message ===
      "string"
    ) {
      return record.message;
    }

    if (
      typeof record.details ===
      "string"
    ) {
      return record.details;
    }
  }

  if (
    typeof value.detail ===
    "string"
  ) {
    return value.detail;
  }

  if (
    typeof value.message ===
    "string"
  ) {
    return value.message;
  }

  return fallback;
}

async function parseResponse(
  response: Response,
): Promise<unknown> {
  const contentType =
    response.headers.get(
      "content-type",
    ) || "";

  if (
    contentType.includes(
      "application/json",
    )
  ) {
    return response.json();
  }

  return response.text();
}

export async function apiRequest<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const headers =
    new Headers(init.headers);

  headers.set(
    "Accept",
    "application/json",
  );

  if (
    init.body &&
    !headers.has("Content-Type")
  ) {
    headers.set(
      "Content-Type",
      "application/json",
    );
  }

  const accessToken =
    getAccessToken();

  if (
    accessToken &&
    !headers.has(
      "Authorization",
    )
  ) {
    headers.set(
      "Authorization",
      `Bearer ${accessToken}`,
    );
  }

  const response = await fetch(
    buildUrl(path),
    {
      ...init,
      headers,
      credentials: "include",
      cache: "no-store",
    },
  );

  const body =
    await parseResponse(
      response,
    );

  if (!response.ok) {
    throw new Error(
      getErrorMessage(
        body,
        `DatavionOS API request failed (${response.status})`,
      ),
    );
  }

  return body as T;
}

export async function apiEnvelope<T>(
  path: string,
  init: RequestInit = {},
): Promise<ApiEnvelope<T>> {
  const result =
    await apiRequest<
      ApiEnvelope<T>
    >(
      path,
      init,
    );

  if (
    !result ||
    result.success !== true
  ) {
    throw new Error(
      getErrorMessage(
        result,
        "DatavionOS API returned an unsuccessful response.",
      ),
    );
  }

  return result;
}

// Anonymous request boundary for public self-service flows.
export async function apiPublicRequest<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const headers =
    new Headers(init.headers);

  headers.set(
    "Accept",
    "application/json",
  );

  if (
    init.body &&
    !headers.has("Content-Type")
  ) {
    headers.set(
      "Content-Type",
      "application/json",
    );
  }

  headers.delete(
    "Authorization",
  );

  const publicResponse =
    await fetch(
      buildUrl(path),
      {
        ...init,
        headers,
        credentials: "omit",
        cache: "no-store",
      },
    );

  const body =
    await parseResponse(
      publicResponse,
    );

  if (!publicResponse.ok) {
    let detail =
      `DatavionOS public API request failed (${publicResponse.status})`;

    if (
      body &&
      typeof body === "object"
    ) {
      const record =
        body as Record<
          string,
          unknown
        >;

      if (
        typeof record.detail ===
        "string"
      ) {
        detail =
          record.detail;
      } else if (
        typeof record.message ===
        "string"
      ) {
        detail =
          record.message;
      } else if (
        record.error &&
        typeof record.error ===
          "object"
      ) {
        const error =
          record.error as Record<
            string,
            unknown
          >;

        if (
          typeof error.message ===
          "string"
        ) {
          detail =
            error.message;
        } else if (
          typeof error.details ===
          "string"
        ) {
          detail =
            error.details;
        }
      }
    }

    throw new Error(detail);
  }

  return body as T;
}

export async function apiPublicEnvelope<T>(
  path: string,
  init: RequestInit = {},
): Promise<{
  success: true;
  data: T;
  [key: string]: unknown;
}> {
  const result =
    await apiPublicRequest<{
      success?: boolean;
      data?: T;
      [key: string]: unknown;
    }>(
      path,
      init,
    );

  if (
    !result ||
    result.success !== true
  ) {
    const record =
      result &&
      typeof result === "object"
        ? result
        : {};

    const detail =
      typeof record.message ===
      "string"
        ? record.message
        : typeof record.detail ===
            "string"
          ? record.detail
          : "DatavionOS public API returned an unsuccessful response.";

    throw new Error(detail);
  }

  return result as {
    success: true;
    data: T;
    [key: string]: unknown;
  };
}

export const apiPublicGet =
  <T>(path: string) =>
    apiPublicEnvelope<T>(
      path,
      {
        method: "GET",
      },
    );

export const apiPublicPost =
  <T>(
    path: string,
    initOrBody: unknown,
  ) => {
    if (
      initOrBody &&
      typeof initOrBody ===
        "object" &&
      !Array.isArray(
        initOrBody,
      )
    ) {
      const candidate =
        initOrBody as Record<
          string,
          unknown
        >;

      if (
        "method" in candidate ||
        "headers" in candidate ||
        "body" in candidate
      ) {
        return apiPublicEnvelope<T>(
          path,
          candidate as RequestInit,
        );
      }
    }

    return apiPublicEnvelope<T>(
      path,
      {
        method: "POST",
        body: JSON.stringify(
          initOrBody,
        ),
      },
    );
  };

export const apiGet =
  <T>(path: string) =>
    apiEnvelope<T>(
      path,
      {
        method: "GET",
      },
    );

export const apiPost =
  <T>(
    path: string,
    body: unknown,
  ) =>
    apiEnvelope<T>(
      path,
      {
        method: "POST",
        body: JSON.stringify(body),
      },
    );

export const apiPatch =
  <T>(
    path: string,
    body: unknown,
  ) =>
    apiRequest<T>(
      path,
      {
        method: "PATCH",
        body: JSON.stringify(body),
      },
    );
