import { API_BASE_URL } from "@/core/api/config";
import {
  clearSession,
  getAccessToken,
} from "./auth-runtime";



type ApiRequestOptions = RequestInit & {
  authenticated?: boolean;
};

async function request<T>(
  path: string,
  options: ApiRequestOptions = {},
): Promise<T> {
  const {
    authenticated = true,
    headers,
    ...requestOptions
  } = options;

  const accessToken = getAccessToken();

  const requestHeaders = new Headers(headers);

  requestHeaders.set(
    "Content-Type",
    "application/json",
  );

  if (authenticated && accessToken) {
    requestHeaders.set(
      "Authorization",
      `Bearer ${accessToken}`,
    );
  }

  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...requestOptions,
      headers: requestHeaders,
      credentials: "include",
    },
  );

  if (response.status === 401) {
    clearSession();
  }

  const contentType =
    response.headers.get("content-type") || "";

  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      typeof payload === "object" &&
      payload !== null &&
      "detail" in payload
        ? String(
            (payload as { detail?: unknown }).detail ||
            "Request failed.",
          )
        : "Request failed.";

    throw new Error(message);
  }

  return payload as T;
}

export function apiGet<T>(
  path: string,
): Promise<T> {
  return request<T>(path);
}

export function apiPost<T>(
  path: string,
  body: unknown,
  authenticated = false,
): Promise<T> {
  return request<T>(path, {
    method: "POST",
    body: JSON.stringify(body),
    authenticated,
  });
}

export function apiPut<T>(
  path: string,
  body: unknown,
): Promise<T> {
  return request<T>(path, {
    method: "PUT",
    body: JSON.stringify(body),
  });
}

export function apiPatch<T>(
  path: string,
  body: unknown,
): Promise<T> {
  return request<T>(path, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}
