/**
 * DatavionOS responsive authenticated workspace header.
 *
 * Organization, notifications, search and user actions remain owned by
 * their existing feature components.
 *
 * Authorization is NOT implemented here.
 * Backend bootstrap remains authoritative.
 */

"use client";

import { MobileWorkspaceMenu } from "./mobile-workspace-menu";
import { NotificationMenu } from "./notification-menu";
import { OrganizationSwitcher } from "./organization-switcher";
import { SearchBar } from "./search-bar";
import { UserMenu } from "./user-menu";
import { WorkspaceBreadcrumbs } from "./workspace-breadcrumbs";

export function AppHeader() {
  return (
    <header className="sticky top-0 z-40 border-bottom bg-body">
      <div className="container-fluid px-3 px-lg-4">
        <div className="d-flex align-items-center justify-content-between gap-3 py-2">
          <div className="d-flex min-w-0 align-items-center gap-2 gap-lg-3">
            <MobileWorkspaceMenu />

            <div className="d-none d-md-block">
              <WorkspaceBreadcrumbs />
            </div>
          </div>

          <div className="d-flex align-items-center gap-2 gap-lg-3">
            <div className="d-none d-lg-block">
              <SearchBar />
            </div>

            <OrganizationSwitcher />

            <NotificationMenu />

            <UserMenu />
          </div>
        </div>

        <div className="d-md-none pb-2">
          <WorkspaceBreadcrumbs />
        </div>
      </div>
    </header>
  );
}
