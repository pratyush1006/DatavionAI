export type AuthUser = {
  id?: string;
  uuid?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  name?: string;
};

export type AuthSession = {
  accessToken: string | null;
  refreshToken: string | null;
  user: AuthUser | null;
};

const ACCESS_TOKEN_KEY = "datavionos.access_token";
const REFRESH_TOKEN_KEY = "datavionos.refresh_token";
const USER_KEY = "datavionos.user";

function browserAvailable(): boolean {
  return typeof window !== "undefined";
}

export function getAccessToken(): string | null {
  if (!browserAvailable()) {
    return null;
  }

  return window.localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  if (!browserAvailable()) {
    return null;
  }

  return window.localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function getStoredUser(): AuthUser | null {
  if (!browserAvailable()) {
    return null;
  }

  const raw = window.localStorage.getItem(USER_KEY);

  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as AuthUser;
  } catch {
    return null;
  }
}

export function setSession(
  accessToken: string,
  refreshToken: string | null,
  user: AuthUser | null,
): void {
  if (!browserAvailable()) {
    return;
  }

  window.localStorage.setItem(
    ACCESS_TOKEN_KEY,
    accessToken,
  );

  if (refreshToken) {
    window.localStorage.setItem(
      REFRESH_TOKEN_KEY,
      refreshToken,
    );
  } else {
    window.localStorage.removeItem(REFRESH_TOKEN_KEY);
  }

  if (user) {
    window.localStorage.setItem(
      USER_KEY,
      JSON.stringify(user),
    );
  } else {
    window.localStorage.removeItem(USER_KEY);
  }
}

export function clearSession(): void {
  if (!browserAvailable()) {
    return;
  }

  window.localStorage.removeItem(ACCESS_TOKEN_KEY);
  window.localStorage.removeItem(REFRESH_TOKEN_KEY);
  window.localStorage.removeItem(USER_KEY);
}

export function getSession(): AuthSession {
  return {
    accessToken: getAccessToken(),
    refreshToken: getRefreshToken(),
    user: getStoredUser(),
  };
}

export function isAuthenticated(): boolean {
  return Boolean(getAccessToken());
}
