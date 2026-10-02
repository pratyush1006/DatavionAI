export interface DatavionRuntimeModule {
  key: string;
  label: string;
  path: string;
  icon?: string;
}

export const DATAVION_RUNTIME_MODULES: DatavionRuntimeModule[] = [
  {
    key: "patients",
    label: "Patients",
    path: "/workspace/patients",
  },
  {
    key: "appointments",
    label: "Appointments",
    path: "/workspace/appointments",
  },
  {
    key: "pharmacy",
    label: "Pharmacy",
    path: "/workspace/pharmacy",
  },
  {
    key: "laboratory",
    label: "Laboratory",
    path: "/workspace/laboratory",
  },
  {
    key: "imaging",
    label: "Imaging",
    path: "/workspace/imaging",
  },
];
