
import apiClient from "@/core/api/client";
import type { Device, TelemetryRecord } from "./types";

export async function listDevices(): Promise<Device[]> {
  const { data } = await apiClient.get("/api/device-platform/devices/");
  return data;
}

export async function registerDevice(payload: Record<string, unknown>): Promise<Device> {
  const { data } = await apiClient.post("/api/device-platform/devices/", payload);
  return data;
}

export async function pairDevice(deviceId: string): Promise<Device> {
  const { data } = await apiClient.post(`/api/device-platform/devices/${deviceId}/pair/`);
  return data;
}

export async function unpairDevice(deviceId: string): Promise<Device> {
  const { data } = await apiClient.post(`/api/device-platform/devices/${deviceId}/unpair/`);
  return data;
}

export async function retireDevice(deviceId: string): Promise<Device> {
  const { data } = await apiClient.post(`/api/device-platform/devices/${deviceId}/retire/`);
  return data;
}

export async function ingestTelemetry(payload: Record<string, unknown>): Promise<TelemetryRecord> {
  const { data } = await apiClient.post("/api/device-platform/telemetry/ingest/", payload);
  return data;
}
