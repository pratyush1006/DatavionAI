import { useCallback, useState } from "react";

export interface BrowserBluetoothDevice {
  id: string;
  name?: string;
}

interface BluetoothDeviceLike {
  id: string;
  name?: string;
}

interface BluetoothRequestOptions {
  acceptAllDevices: boolean;
  optionalServices: string[];
}

interface BluetoothLike {
  requestDevice(options: BluetoothRequestOptions): Promise<BluetoothDeviceLike>;
}

interface NavigatorWithBluetooth extends Navigator {
  bluetooth?: BluetoothLike;
}

const getBluetoothSupport = (): boolean =>
  typeof navigator !== "undefined" &&
  "bluetooth" in navigator &&
  Boolean((navigator as NavigatorWithBluetooth).bluetooth);

export function useBluetoothDevices() {
  const [devices, setDevices] = useState<BrowserBluetoothDevice[]>([]);
  const supported = getBluetoothSupport();

  const requestDevice = useCallback(async () => {
    if (!supported) {
      throw new Error("Web Bluetooth is not supported by this browser.");
    }

    const bluetooth = (navigator as NavigatorWithBluetooth).bluetooth;
    if (!bluetooth) {
      throw new Error("Web Bluetooth is not available in this browser.");
    }

    const device = await bluetooth.requestDevice({
      acceptAllDevices: true,
      optionalServices: [],
    });

    const result: BrowserBluetoothDevice = {
      id: device.id,
      name: device.name,
    };

    setDevices((current) => [
      ...current.filter((item) => item.id !== result.id),
      result,
    ]);

    return result;
  }, [supported]);

  return { devices, supported, requestDevice };
}
