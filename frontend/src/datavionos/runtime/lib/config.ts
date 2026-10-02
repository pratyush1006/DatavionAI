export const DATAVION_RUNTIME_CONFIG = {
  capabilityEndpoint:
    process.env.NEXT_PUBLIC_DATAVIONOS_CAPABILITY_ENDPOINT ??
    "/api/datavionos/effective-capability",

  moduleStateEndpoint:
    process.env.NEXT_PUBLIC_DATAVIONOS_MODULE_STATE_ENDPOINT ??
    "/api/datavionos/module-state",

  requestTimeoutMs: 15000,
} as const;
