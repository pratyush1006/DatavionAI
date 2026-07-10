/**
 * Authentication query keys.
 */

export const accountKeys = {
  all: ["accounts"] as const,

  me: () =>
    [...accountKeys.all, "me"] as const,
};
