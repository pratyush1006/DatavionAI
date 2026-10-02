"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import { useBootstrap } from "@/core/bootstrap";
import { adaptBootstrapNavigation } from "@/core/navigation";

export function MobileWorkspaceMenu() {
  const [open, setOpen] = useState(false);

  const { bootstrap } = useBootstrap();

  const navigation = useMemo(() => {
    if (!bootstrap) {
      return [];
    }

    return adaptBootstrapNavigation({
      navigation: bootstrap.navigation,
      modules: bootstrap.modules,
      portal: "staff",
    });
  }, [bootstrap]);

  return (
    <>
      <button
        type="button"
        className="btn btn-outline-secondary d-lg-none d-inline-flex align-items-center justify-content-center"
        aria-label="Open workspace navigation"
        aria-expanded={open}
        onClick={() => setOpen(true)}
      >
        <Menu size={19} aria-hidden="true" />
      </button>

      {open ? (
        <div
          className="position-fixed top-0 start-0 w-100 h-100"
          style={{ zIndex: 1050 }}
          role="dialog"
          aria-modal="true"
          aria-label="Workspace navigation"
        >
          <button
            type="button"
            className="position-absolute top-0 start-0 w-100 h-100 border-0 bg-dark opacity-50"
            aria-label="Close workspace navigation"
            onClick={() => setOpen(false)}
          />

          <aside
            className="position-relative bg-body h-100 shadow-lg d-flex flex-column"
            style={{ width: "min(86vw, 360px)" }}
          >
            <div className="d-flex align-items-center justify-content-between p-3 border-bottom">
              <div className="fw-semibold">
                DatavionOS
              </div>

              <button
                type="button"
                className="btn btn-outline-secondary btn-sm"
                aria-label="Close workspace navigation"
                onClick={() => setOpen(false)}
              >
                <X size={18} aria-hidden="true" />
              </button>
            </div>

            <nav
              className="p-3 overflow-auto flex-grow-1"
              aria-label="Workspace"
            >
              {navigation.length === 0 ? (
                <div className="small text-body-secondary py-2">
                  No workspace navigation is currently available.
                </div>
              ) : (
                <div className="list-group list-group-flush">
                  {navigation.map((item) => (
                    <Link
                      key={item.id}
                      href={item.href}
                      className="list-group-item list-group-item-action border-0 rounded py-3"
                      onClick={() => setOpen(false)}
                    >
                      <span className="fw-medium">
                        {item.label}
                      </span>
                    </Link>
                  ))}
                </div>
              )}
            </nav>
          </aside>
        </div>
      ) : null}
    </>
  );
}
