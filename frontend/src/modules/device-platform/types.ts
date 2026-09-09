
export type DeviceLifecycle =
  | "DISCOVERED" | "PAIRING" | "PAIRED" | "ASSOCIATED"
  | "ACTIVE" | "SUSPENDED" | "RETIRED";

export interface Device {
  device_id: string;
  organization: string;
  device_type: string;
  manufacturer: string;
  model_name: string;
  model_number: string;
  serial_number: string;
  firmware_version: string;
  hardware_revision: string;
  lifecycle: DeviceLifecycle;
  trust_state: string;
  metadata: Record<string, unknown>;
  last_seen_at: string | null;
  battery_percent: number | null;
  created_at: string;
  updated_at: string;
}

export interface TelemetryRecord {
  telemetry_id: string;
  patient: string;
  device: string;
  measurement_type: string;
  value: string | null;
  unit: string;
  measured_at: string;
  received_at: string;
  source: string;
  quality: string;
}
