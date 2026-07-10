/**
 * Organization query keys.
 */

export const organizationKeys = {
  all: ["organizations"] as const,

  lists: () => [
    ...organizationKeys.all,
    "list",
  ] as const,

  list: (
    params?: Record<
      string,
      unknown
    >,
  ) =>
    [
      ...organizationKeys.lists(),
      params ?? {},
    ] as const,

  details: () => [
    ...organizationKeys.all,
    "detail",
  ] as const,

  detail: (
    id: number | string,
  ) =>
    [
      ...organizationKeys.details(),
      id,
    ] as const,
} as const;
