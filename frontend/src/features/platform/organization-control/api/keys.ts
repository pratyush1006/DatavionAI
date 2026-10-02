export const organizationControlKeys = {
  all: ["organization-control"] as const,
  snapshot: () =>
    [...organizationControlKeys.all, "snapshot"] as const,
} as const;
