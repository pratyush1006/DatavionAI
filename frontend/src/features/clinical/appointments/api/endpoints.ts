export const appointmentEndpoints = {
  collection:
    "/appointments/",

  byId: (
    id: string | number,
  ) =>
    `/appointments/${String(id)}/`,

  reschedule: (
    id: string | number,
  ) =>
    `/appointments/${String(id)}/reschedule/`,

  depositCheckout: (id: string | number) =>
    `/appointments/${String(id)}/deposit/checkout/`,

  depositVerify: (id: string | number) =>
    `/appointments/${String(id)}/deposit/verify/`,

  checkIn: (id: string | number) =>
    `/appointments/${String(id)}/check-in/`,

  noShow: (id: string | number) =>
    `/appointments/${String(id)}/no-show/`,

  scribeTicket: (id: string | number) =>
    `/appointments/${String(id)}/scribe-ticket/`,

  tracking: (token: string) =>
    `/appointments/track/${encodeURIComponent(token)}/`,
} as const;
