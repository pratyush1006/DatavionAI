/**
 * API endpoint definitions.
 */

export const API_ENDPOINTS = {
  accounts: {
    login: "/accounts/login/",
    me: "/accounts/me/",
  },

  patients: {},

  appointments: {},

  encounters: {},

  diagnoses: {},

  allergies: {},

  vitals: {},

  medications: {},

  prescriptions: {},

  laboratories: {},

  radiology: {},

  billing: {},

  settings: {},
} as const;
