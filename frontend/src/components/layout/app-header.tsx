/**
 * Enterprise application header.
 */

import { NotificationMenu } from "./notification-menu";
import { OrganizationSwitcher } from "./organization-switcher";
import { SearchBar } from "./search-bar";
import { UserMenu } from "./user-menu";

export function AppHeader() {
  return (
    <header className="sticky top-0 z-40 flex h-16 items-center justify-between border-b bg-background px-6">
      <SearchBar />

      <div className="flex items-center gap-3">
        <OrganizationSwitcher />

        <NotificationMenu />

        <UserMenu />
      </div>
    </header>
  );
}
