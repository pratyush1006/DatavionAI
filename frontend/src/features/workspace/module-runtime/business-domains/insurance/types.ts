import type { ModuleRuntimeDefinition } from "../../domain/types";

export type InsuranceDomain = "overview"
  | "api"
  | "models";

export const INSURANCE_DOMAINS = [
  "overview",
  "api",
  "models"
] as const;

export type InsuranceDomainKey = typeof INSURANCE_DOMAINS[number];

export type InsuranceWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;
