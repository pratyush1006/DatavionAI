import type { ModuleRuntimeDefinition } from "../../domain/types";

export type DevicePlatformDomain = "overview"
  | "alerts"
  | "api"
  | "bluetooth"
  | "consent"
  | "events"
  | "gateways"
  | "integrations"
  | "measurements"
  | "models"
  | "permissions"
  | "selectors"
  | "services"
  | "telemetry"
  | "workflows";

export const DEVICE_PLATFORM_DOMAINS = [
  "overview",
  "alerts",
  "api",
  "bluetooth",
  "consent",
  "events",
  "gateways",
  "integrations",
  "measurements",
  "models",
  "permissions",
  "selectors",
  "services",
  "telemetry",
  "workflows"
] as const;

export type DevicePlatformDomainKey = typeof DEVICE_PLATFORM_DOMAINS[number];

export type DevicePlatformWorkspaceProps = Readonly<{
  module: ModuleRuntimeDefinition;
}>;
