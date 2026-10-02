"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  BarChart3,
  Building2,
  Cable,
  CreditCard,
  FileSearch,
  Home,
  Landmark,
  LockKeyhole,
  type LucideIcon,
  Settings2,
  ShieldCheck,
  Palette,
  SlidersHorizontal,
  Users,
} from "lucide-react";

import { useBootstrap } from "@/core/bootstrap";

const PLATFORM_NAVIGATION: ReadonlyArray<Readonly<{
  title: string;
  route: string;
  icon: LucideIcon;
}>> = [
  { title: "Overview", route: "/platform-admin", icon: Home },
  { title: "Organizations", route: "/organizations", icon: Building2 },
  { title: "Users", route: "/employees", icon: Users },
  { title: "Subscriptions", route: "/organization/subscription", icon: CreditCard },
  { title: "Analytics", route: "/platform-admin#activity", icon: BarChart3 },
  { title: "Billing", route: "/platform-admin#billing", icon: Landmark },
  { title: "System", route: "/settings/modules", icon: Activity },
  { title: "Integrations", route: "/settings/ai", icon: Cable },
  { title: "Security", route: "/settings/access", icon: LockKeyhole },
  { title: "Audit", route: "/platform-admin#activity", icon: FileSearch },
  { title: "Configuration", route: "/organization/settings", icon: Settings2 },
];

export function DynamicNavigation() {
  const pathname = usePathname();
  const { bootstrap, isLoading } = useBootstrap();

  if (isLoading && !bootstrap) {
    return (
      <nav className="p-3" aria-label="Workspace navigation" aria-busy="true">
        <div className="placeholder-glow">
          <span className="placeholder col-8 d-block mb-3" />
          <span className="placeholder col-10 d-block mb-3" />
          <span className="placeholder col-7 d-block" />
        </div>
      </nav>
    );
  }

  const items = (bootstrap?.navigation ?? [])
    .filter((item) => item.title.trim() && item.route.trim())
    .slice()
    .sort((left, right) => left.order - right.order);

  const isPlatformAdmin = Boolean(bootstrap?.user.is_platform_admin);
  const canManageOrganization = Boolean(
    bootstrap?.organization && (
      bootstrap.permissions.includes("organizations.update") ||
      bootstrap.organization_roles.some((role) => /organization admin|organization_admin|organization owner|organization_owner/i.test(role))
    )
  );

  if (isPlatformAdmin) {
    return (
      <nav className="p-3" aria-label="Platform navigation">
        <div className="small text-uppercase fw-semibold text-body-secondary px-3 mb-2" style={{ letterSpacing: ".08em" }}>
          Platform control
        </div>
        <div className="nav nav-pills flex-column gap-1">
          {PLATFORM_NAVIGATION.map(({ title, route, icon: Icon }) => {
            const routePath = route.split("#", 1)[0];
            // Anchor links target panels within the overview page. They must
            // not inherit the page pathname as their active state, otherwise
            // Overview, Analytics and Audit are highlighted together.
            const isAnchorLink = route.includes("#");
            const active = !isAnchorLink && (
              pathname === routePath || pathname.startsWith(`${routePath}/`)
            );
            return (
              <Link key={`${title}:${route}`} href={route} aria-current={active ? "page" : undefined} className={`nav-link d-flex align-items-center gap-2 ${active ? "active" : "text-body"}`}>
                <Icon size={17} aria-hidden="true" />
                {title}
              </Link>
            );
          })}
        </div>

        <div className="mt-4 pt-3 border-top">
          <div className="small text-uppercase fw-semibold text-body-secondary px-3 mb-2" style={{ letterSpacing: ".08em" }}>
            Product modules
          </div>
          <div className="nav nav-pills flex-column gap-1">
            {items.filter((item) => item.route !== "/dashboard").map((item) => {
              const active = pathname === item.route || pathname.startsWith(`${item.route}/`);
              return <Link key={`${item.route}:${item.title}`} href={item.route} aria-current={active ? "page" : undefined} className={`nav-link ${active ? "active" : "text-body"}`}>{item.title}</Link>;
            })}
          </div>
        </div>
      </nav>
    );
  }

  return (
    <nav className="p-3" aria-label="Workspace navigation">
      <div className="small text-uppercase fw-semibold text-body-secondary px-3 mb-2" style={{ letterSpacing: ".08em" }}>
        Enabled modules
      </div>
      <div className="nav nav-pills flex-column gap-1">
        <Link
          href="/dashboard"
          aria-current={pathname === "/dashboard" ? "page" : undefined}
          className={`nav-link d-flex align-items-center gap-2 ${pathname === "/dashboard" ? "active" : "text-body"}`}
        >
          <Home size={17} aria-hidden="true" />
          Dashboard
        </Link>

        {items
          .filter((item) => item.route !== "/dashboard")
          .map((item) => {
            const active = pathname === item.route || pathname.startsWith(`${item.route}/`);
            return (
              <Link
                key={`${item.route}:${item.title}`}
                href={item.route}
                aria-current={active ? "page" : undefined}
                className={`nav-link ${active ? "active" : "text-body"}`}
              >
                {item.title}
              </Link>
            );
          })}
      </div>

      {!items.length ? (
        <p className="small text-body-secondary px-3 mt-3 mb-0">
          No modules are available for your current role.
        </p>
      ) : null}

      {canManageOrganization ? (
        <div className="mt-4 pt-3 border-top">
          <div className="small text-uppercase fw-semibold text-body-secondary px-3 mb-2" style={{ letterSpacing: ".08em" }}>
            Organization administration
          </div>
          <div className="nav nav-pills flex-column gap-1">
            {[
              ["Organization settings", "/organization/settings", SlidersHorizontal],
              ["Branding", "/organization/branding", Palette],
              ["Organization structure", "/organization/hierarchy", Building2],
              ["Subscription", "/organization/subscription", CreditCard],
            ].map(([title, route, Icon]) => {
              const active = pathname === route || pathname.startsWith(`${route}/`);
              const NavigationIcon = Icon as LucideIcon;
              return <Link key={route as string} href={route as string} aria-current={active ? "page" : undefined} className={`nav-link d-flex align-items-center gap-2 ${active ? "active" : "text-body"}`}><NavigationIcon size={17} aria-hidden="true" />{title as string}</Link>;
            })}
          </div>
        </div>
      ) : null}

    </nav>
  );
}
