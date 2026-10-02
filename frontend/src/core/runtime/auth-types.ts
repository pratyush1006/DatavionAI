export type AuthStatus =
  | "unknown"
  | "authenticated"
  | "unauthenticated"
  | "otp_required";

export type AuthIdentity = {
  id: string;
  email: string;
  displayName?: string;
};

export type AuthOrganization = {
  id: string;
  name: string;
  organizationType?: string;
};

export type AuthSession = {
  status: AuthStatus;
  identity: AuthIdentity | null;
  organization: AuthOrganization | null;
  accessToken: string | null;
};

export type LoginInput = {
  email: string;
  password: string;
};

export type OtpInput = {
  challengeId: string;
  code: string;
};

export type RegisterOrganizationInput = {
  organizationName: string;
  organizationType: string;
  planCode: string;
  ownerEmail: string;
  ownerName: string;
  password: string;
};

export type AuthRuntime = {
  session: AuthSession;
  login(input: LoginInput): Promise<void>;
  verifyOtp(input: OtpInput): Promise<void>;
  logout(): Promise<void>;
  registerOrganization(input: RegisterOrganizationInput): Promise<void>;
  refreshBootstrap(): Promise<void>;
};
