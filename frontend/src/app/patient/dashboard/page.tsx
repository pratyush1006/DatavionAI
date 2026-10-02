import type { Metadata } from "next";

import { PatientDashboard } from "@/features/patient-portal/patient-dashboard";

export const metadata: Metadata = {
  title: "Patient Dashboard | DatavionOS",
  manifest: "/patient-manifest.webmanifest",
};

export default function PatientDashboardPage() {
  return <PatientDashboard />;
}
