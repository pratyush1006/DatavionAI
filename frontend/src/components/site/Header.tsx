"use client";

import Link from "next/link";
import { useState } from "react";

const navigationLinks = [
  ["/features", "Platform"],
  ["/solutions", "Solutions"],
  ["/pricing", "Pricing"],
  ["/about", "About"],
  ["/support", "Contact"],
] as const;

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);

  function closeAll() {
    setMobileOpen(false);
  }

  return (
    <header className="site-header">
      <div className="container">
        <nav className="site-nav" aria-label="Primary navigation">
          <Link href="/" className="site-brand" onClick={closeAll}>
            <span className="site-brand-mark">D</span>
            <span className="site-brand-name">
              Datavion<span>AI</span>
            </span>
          </Link>

          <button
            type="button"
            className="nav-mobile-toggle"
            aria-label="Toggle navigation"
            aria-expanded={mobileOpen}
            onClick={() => setMobileOpen((value) => !value)}
          >
            <span />
            <span />
            <span />
          </button>

          <div className={`site-nav-links ${mobileOpen ? "is-open" : ""}`}>
            {navigationLinks.map(([href, label]) => (
              <Link
                href={href}
                className="site-nav-link"
                key={href}
                onClick={closeAll}
              >
                {label}
              </Link>
            ))}

            <div className="site-mobile-actions">
              <Link href="/login" className="site-login" onClick={closeAll}>
                Log in
              </Link>
              <Link
                href="/organization/register"
                className="site-button site-button-primary"
                onClick={closeAll}
              >
                Register organization
              </Link>
            </div>
          </div>

          <div className="site-nav-actions">
            <Link href="/login" className="site-login" onClick={closeAll}>
              Log in
            </Link>

            <Link
              href="/organization/register"
              className="site-button site-button-primary"
              onClick={closeAll}
            >
              Register organization
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
}
