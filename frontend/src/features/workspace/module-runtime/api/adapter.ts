"use client";

import { apiClient, buildApiUrl } from "@/core/api";
import type { ModuleApiContract } from "./types";
import type {
  ModuleApiRequest,
  ModuleApiResult,
  ModuleListResponse,
} from "./adapter-types";

function buildQuery(
  query: ModuleApiRequest["query"],
): string {
  if (!query) {
    return "";
  }

  const params = new URLSearchParams();

  for (const [key, value] of Object.entries(query)) {
    if (value === undefined) {
      continue;
    }
    params.set(key, String(value));
  }

  const encoded = params.toString();
  return encoded ? `?${encoded}` : "";
}

function resolveRoute(
  contract: ModuleApiContract,
  route?: string,
): string {
  const candidate = (route ?? contract.prefix).trim();

  if (!candidate.startsWith("/")) {
    throw new Error("Module API routes must be absolute application paths.");
  }

  if (candidate.includes("<")) {
    throw new Error(
      "A concrete module API route is required for parameterized endpoints.",
    );
  }

  return candidate;
}

async function execute<T>(
  request: ModuleApiRequest,
): Promise<ModuleApiResult<T>> {
  let url: string;

  try {
    url = buildApiUrl(
      resolveRoute(
        request.contract,
        request.route,
      ) + buildQuery(request.query),
    );
  } catch (error) {
    return {
      ok: false,
      error: {
        status: 0,
        message:
          error instanceof Error
            ? error.message
            : "Invalid module API route.",
      },
    };
  }

  try {
    // Use the canonical transport so module workspaces receive the current
    // bearer token, tenant and active-organization headers just like every
    // feature-specific API request. Raw fetch caused authenticated module
    // tables to fail with 401 despite the user being signed in.
    const response = await apiClient.axios.get<unknown>(url, {
      signal: request.signal,
      headers: { Accept: "application/json" },
    });

    const body = response.data;

    return {
      ok: true,
      response: {
        data: body as T,
        status: response.status,
        // Module callers do not consume response headers today. Preserve the
        // Fetch-shaped adapter contract without leaking Axios's header type.
        headers: new Headers(),
      },
    };
  } catch (error) {
    const axiosError = error as {
      response?: { status?: number; data?: unknown };
      message?: string;
    };
    const body = axiosError.response?.data;
    const detail =
      body && typeof body === "object" && "detail" in body &&
      typeof (body as { detail?: unknown }).detail === "string"
        ? (body as { detail: string }).detail
        : undefined;

    return {
      ok: false,
      error: {
        status: axiosError.response?.status ?? 0,
        message: detail ?? axiosError.message ?? "Module API request failed.",
        body,
      },
    };
  }
}

export async function getModule<T = unknown>(
  request: ModuleApiRequest,
): Promise<ModuleApiResult<T>> {
  return execute<T>(request);
}

export async function listModule<T = unknown>(
  request: ModuleApiRequest,
): Promise<ModuleApiResult<ModuleListResponse<T>>> {
  const result = await execute<unknown>(request);

  if (!result.ok) {
    return result;
  }

  const body = result.response.data;

  if (Array.isArray(body)) {
    return {
      ok: true,
      response: {
        ...result.response,
        data: {
          results: body as readonly T[],
        },
      },
    };
  }

  if (
    body &&
    typeof body === "object" &&
    !Array.isArray(body)
  ) {
    const candidate = body as Record<string, unknown>;
    const rows =
      candidate.results ??
      candidate.data ??
      candidate.items ??
      candidate.rows;

    if (Array.isArray(rows)) {
      return {
        ok: true,
        response: {
          ...result.response,
          data: {
            results: rows as readonly T[],
            count:
              typeof candidate.count === "number"
                ? candidate.count
                : undefined,
            next:
              typeof candidate.next === "string"
                ? candidate.next
                : null,
            previous:
              typeof candidate.previous === "string"
                ? candidate.previous
                : null,
          },
        },
      };
    }
  }

  return {
    ok: true,
    response: {
      ...result.response,
      data: {
        results: [],
      },
    },
  };
}
