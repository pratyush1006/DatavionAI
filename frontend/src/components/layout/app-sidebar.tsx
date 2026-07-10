/**
 * Enterprise application sidebar.
 */

"use client";

import { AppLogo } from "./app-logo";
import { SidebarGroup } from "./sidebar-group";
import { SidebarItem } from "./sidebar-item";

import {
  NavigationBuilder,
  SIDEBAR_GROUPS,
} from "@/core/navigation";

const navigation = NavigationBuilder.build({
  portal: "staff",
  enabledModules: [
    "dashboard",
    "organizations",
    "patients",
    "appointments",
    "encounters",
    "laboratories",
    "radiology",
    "billing",
    "settings",
  ],
  permissions: [
    "dashboard.view",
    "organization.view",
    "patient.view",
    "appointment.view",
    "encounter.view",
    "laboratory.view",
    "radiology.view",
    "billing.view",
    "settings.view",
  ],
});

export function AppSidebar() {
  return (
    <aside className="flex h-screen w-72 flex-col border-r bg-background">
      <div className="border-b p-6">
        <AppLogo />
      </div>

      <nav className="flex-1 overflow-y-auto p-4">
        {SIDEBAR_GROUPS.map((group) => {
          const items = navigation.filter(
            (item) => item.group === group,
          );

          if (items.length === 0) {
            return null;
          }

          return (
            <SidebarGroup
              key={group}
              title={group}
            >
              {items.map((item) => (
                <SidebarItem
                  key={item.id}
                  item={item}
                />
              ))}
            </SidebarGroup>
          );
        })}
      </nav>
    </aside>
  );
}
