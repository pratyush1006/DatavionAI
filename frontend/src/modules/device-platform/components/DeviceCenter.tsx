
import { useEffect, useState } from "react";
import { listDevices, pairDevice } from "../api";
import type { Device } from "../types";
import { useBluetoothDevices } from "../hooks/useBluetoothDevices";

export function DeviceCenter() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [error, setError] = useState<string | null>(null);
  const { supported, requestDevice } = useBluetoothDevices();

  const refresh = async () => {
    try {
      setDevices(await listDevices());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load devices.");
    }
  };

  useEffect(() => {
    const timer = window.setTimeout(() => {
      void refresh();
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  const discover = async () => {
    try {
      await requestDevice();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Bluetooth discovery failed.");
    }
  };

  const pair = async (id: string) => {
    try {
      await pairDevice(id);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Pairing failed.");
    }
  };

  return (
    <section>
      <header>
        <h1>Device Center</h1>
        <button onClick={discover} disabled={!supported}>Scan Bluetooth</button>
      </header>
      {!supported && <p>Web Bluetooth is unavailable. Use the Datavion mobile/edge gateway for this device.</p>}
      {error && <p role="alert">{error}</p>}
      <ul>
        {devices.map((device) => (
          <li key={device.device_id}>
            <strong>{device.manufacturer} {device.model_name}</strong>
            <span> — {device.lifecycle}</span>
            {device.lifecycle === "DISCOVERED" && (
              <button onClick={() => void pair(device.device_id)}>Pair</button>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
