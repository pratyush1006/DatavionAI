import { redirect } from "next/navigation";

/**
 * Legacy entry point retained for existing bookmarks.
 *
 * The canonical dashboard is the only runtime surface: it consumes the
 * backend bootstrap contract for modules, navigation, permissions, and
 * organization context. Keeping a second capability screen here would allow
 * stale hard-coded module state to diverge from that authority.
 */
export default function DatavionRuntimePage() {
  redirect("/dashboard");
}
