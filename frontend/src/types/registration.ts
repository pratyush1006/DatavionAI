export type OrganizationRegistrationPayload = {
  organization: Record<string, unknown>;
  administrator: Record<string, unknown>;
  subscription?: Record<string, unknown>;
};

export type OrganizationRegistrationResult = {
  [key: string]: unknown;
};
