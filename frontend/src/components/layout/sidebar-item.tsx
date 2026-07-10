/**
 * Sidebar navigation item.
 */

"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";

import type { NavigationItem } from "@/core/navigation";

type SidebarItemProps = Readonly<{
  item: NavigationItem;
}>;

export function SidebarItem({
  item,
}: SidebarItemProps) {
  const pathname = usePathname();

  const Icon = item.icon;

  const active =
    pathname === item.href ||
    pathname.startsWith(`${item.href}/`);

  return (
    <Link
      href={item.href}
      className={cn(
        "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
        active
          ? "bg-primary text-primary-foreground"
          : "text-muted-foreground hover:bg-muted hover:text-foreground",
      )}
    >
      <Icon className="h-5 w-5 shrink-0" />

      <span>{item.label}</span>
    </Link>
  );
}
