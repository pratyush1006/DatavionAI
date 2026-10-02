"use client";

import Link from "next/link";
import { ChevronRight, Home } from "lucide-react";
import { usePathname } from "next/navigation";

const LABELS: Record<string, string> = {
  dashboard: "Dashboard",
  clinical: "Clinical",
  appointments: "Appointments",
  patients: "Patients",
  employees: "Employees",
  organizations: "Organizations",
  documents: "Documents",
  notes: "Notes",
  transcription: "Transcription",
  laboratories: "Laboratories",
  radiology: "Radiology",
  encounters: "Encounters",
  billing: "Billing",
  settings: "Settings",
  modules: "Modules",
  access: "Access",
  ai: "AI",
};

function displayLabel(value: string): string {
  return (
    LABELS[value.toLowerCase()] ??
    value
      .replace(/[-_]+/g, " ")
      .replace(/\b\w/g, (character) => character.toUpperCase())
  );
}

export function WorkspaceBreadcrumbs() {
  const pathname = usePathname();
  const segments = pathname.split("/").filter(Boolean);

  const crumbs = segments.map((segment, index) => ({
    segment,
    href: `/${segments.slice(0, index + 1).join("/")}`,
  }));

  return (
    <nav aria-label="Breadcrumb">
      <ol className="breadcrumb mb-0 align-items-center small">
        <li className="breadcrumb-item">
          <Link
            href="/dashboard"
            className="text-decoration-none text-body-secondary d-inline-flex align-items-center"
            aria-label="Dashboard"
          >
            <Home size={15} aria-hidden="true" />
          </Link>
        </li>

        {crumbs.map((crumb, index) => {
          const last = index === crumbs.length - 1;

          return (
            <li
              className={`breadcrumb-item d-flex align-items-center ${
                last ? "active" : ""
              }`}
              aria-current={last ? "page" : undefined}
              key={crumb.href}
            >
              <ChevronRight
                className="mx-1 text-body-tertiary"
                size={14}
                aria-hidden="true"
              />

              {last ? (
                <span>{displayLabel(crumb.segment)}</span>
              ) : (
                <Link
                  href={crumb.href}
                  className="text-decoration-none text-body-secondary"
                >
                  {displayLabel(crumb.segment)}
                </Link>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
