import { API_BASE_URL } from "@/core/api/config";
import type {
  AuthRuntime,
  LoginInput,
  OtpInput,
  RegisterOrganizationInput,
} from "./auth-types";



async function request<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(init.headers ?? {}),
    },
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export function createAuthRuntime(
  refreshBootstrap: () => Promise<void>,
): AuthRuntime {
  let session: AuthRuntime["session"] = {
    status: "unknown",
    identity: null,
    organization: null,
    accessToken: null,
  };

  return {
    get session() {
      return session;
    },

    async login(input: LoginInput) {
      const result = await request<{
        status?: "authenticated" | "otp_required";
        challengeId?: string;
      }>("/auth/login/", {
        method: "POST",
        body: JSON.stringify(input),
      });

      if (result.status === "otp_required") {
        session = {
          ...session,
          status: "otp_required",
        };
        return;
      }

      session = {
        ...session,
        status: "authenticated",
      };
      await refreshBootstrap();
    },

    async verifyOtp(input: OtpInput) {
      await request("/auth/otp/verify/", {
        method: "POST",
        body: JSON.stringify(input),
      });

      session = {
        ...session,
        status: "authenticated",
      };
      await refreshBootstrap();
    },

    async logout() {
      await request("/auth/logout/", { method: "POST" });
      session = {
        status: "unauthenticated",
        identity: null,
        organization: null,
        accessToken: null,
      };
    },

    async registerOrganization(input: RegisterOrganizationInput) {
      await request("/organizations/register/", {
        method: "POST",
        body: JSON.stringify(input),
      });
      session = {
        ...session,
        status: "authenticated",
      };
      await refreshBootstrap();
    },

    async refreshBootstrap() {
      await refreshBootstrap();
    },
  };
}
