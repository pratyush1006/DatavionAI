export const appointmentEndpoints = {
  collection:
    "/appointments/",

  byId: (
    id: string | number,
  ) =>
    `/appointments/${String(id)}/`,
} as const;
