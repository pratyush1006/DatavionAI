
import { useCallback, useEffect, useState } from "react";

export interface BrowserBluetoothDevice {
  id: string;
  name?: string;
}

export function useBluetoothDevices() {
  const [devices, setDevices] = useState<BrowserBluetoothDevice[]>([]);
  const [supported, setSupported] = useState(false);

  useEffect(() => {
    setSupported(typeof navigator !== "undefined" && "bluetooth" in navigator);
  }, []);

  const requestDevice = useCallback(async () => {
    if (!supported) throw new Error("Web Bluetooth is not supported by this browser.");
    const bluetooth = (navigator as Navigator & { bluetooth?: any }).bluetooth;
    const device = await bluetooth.requestDevice({
      acceptAllDevices: true,
      optionalServices: [],
    });
    const result = { id: device.id, name: device.name };
    setDevices((current) => [...current.filter((item) => item.id !== result.id), result]);
    return result;
  }, [supported]);

  return { devices, supported, requestDevice };
}
