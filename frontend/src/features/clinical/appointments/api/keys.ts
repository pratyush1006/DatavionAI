export const appointmentKeys = {
  all:
    ["appointments"] as const,

  lists: () =>
    [
      ...appointmentKeys.all,
      "list",
    ] as const,

  detail: (
    id: string | number,
  ) =>
    [
      ...appointmentKeys.all,
      "detail",
      String(id),
    ] as const,
} as const;
