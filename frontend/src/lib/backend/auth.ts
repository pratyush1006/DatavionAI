import { ENDPOINTS } from "./endpoints";
import {
  apiGet,
  apiPost,
  clearTokens,
  getRefreshToken,
  storeTokens,
} from "./http";

export type AuthUser = {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  name?: string;
};

export type LoginChallenge = {
  otp_id: string;
  requires_otp: boolean;
  expires_at?: string;
  resend_available_at?: string;
};

export type TokenPair = {
  access: string;
  refresh: string;
};

export async function requestLoginOtp(
  email: string,
  password: string,
): Promise<LoginChallenge> {
  const response = await apiPost<LoginChallenge>(ENDPOINTS.auth.login, {
    email,
    password,
  });
  return response.data;
}

export async function resendLoginOtp(otpId: string): Promise<LoginChallenge> {
  const response = await apiPost<LoginChallenge>(
    ENDPOINTS.auth.resendLoginOtp,
    { otp_id: otpId },
  );
  return response.data;
}

export async function verifyLoginOtp(
  otpId: string,
  otp: string,
): Promise<TokenPair> {
  const response = await apiPost<TokenPair>(
    ENDPOINTS.auth.verifyLoginOtp,
    { otp_id: otpId, otp },
  );
  storeTokens(response.data.access, response.data.refresh);
  return response.data;
}

export async function refreshAccessToken(): Promise<TokenPair> {
  const refresh = getRefreshToken();
  if (!refresh) throw new Error("No DatavionOS refresh token is available.");
  const response = await apiPost<TokenPair>(ENDPOINTS.auth.refresh, { refresh });
  storeTokens(response.data.access, response.data.refresh);
  return response.data;
}

export async function logout(): Promise<void> {
  const refresh = getRefreshToken();
  try {
    if (refresh) {
      await apiPost<null>(ENDPOINTS.auth.logout, { refresh });
    }
  } finally {
    clearTokens();
  }
}

export async function getCurrentUser(): Promise<AuthUser> {
  const response = await apiGet<AuthUser>(ENDPOINTS.auth.me);
  return response.data;
}

export async function requestPasswordReset(email: string): Promise<unknown> {
  const response = await apiPost<unknown>(ENDPOINTS.auth.forgotPassword, { email });
  return response.data;
}

export async function resetPassword(payload: Record<string, unknown>): Promise<unknown> {
  const response = await apiPost<unknown>(ENDPOINTS.auth.resetPassword, payload);
  return response.data;
}

export async function changePassword(payload: Record<string, unknown>): Promise<unknown> {
  const response = await apiPost<unknown>(ENDPOINTS.auth.changePassword, payload);
  return response.data;
}

export async function verifyEmail(payload: Record<string, unknown>): Promise<unknown> {
  const response = await apiPost<unknown>(ENDPOINTS.auth.verifyEmail, payload);
  return response.data;
}

export async function resendVerification(payload: Record<string, unknown>): Promise<unknown> {
  const response = await apiPost<unknown>(ENDPOINTS.auth.resendVerification, payload);
  return response.data;
}

export async function loginWithGoogle(token: string): Promise<TokenPair> {
  const response = await apiPost<TokenPair>(ENDPOINTS.auth.google, { token });
  storeTokens(response.data.access, response.data.refresh);
  return response.data;
}

export async function loginWithMicrosoft(token: string): Promise<TokenPair> {
  const response = await apiPost<TokenPair>(ENDPOINTS.auth.microsoft, { token });
  storeTokens(response.data.access, response.data.refresh);
  return response.data;
}
