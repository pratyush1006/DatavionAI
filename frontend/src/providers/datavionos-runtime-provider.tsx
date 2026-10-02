"use client";

import {
  DatavionOSAuthProvider,
} from "./datavionos-auth-provider";

import {
  DatavionOSCapabilityProvider,
} from "./datavionos-capability-provider";

export function DatavionOSRuntimeProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <DatavionOSAuthProvider>
      <DatavionOSCapabilityProvider>
        {children}
      </DatavionOSCapabilityProvider>
    </DatavionOSAuthProvider>
  );
}
