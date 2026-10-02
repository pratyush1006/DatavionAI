import { ReactNode } from "react";
import { Header } from "./Header";
import { Footer } from "./Footer";

export function SiteShell({ children }: { children: ReactNode }) {
  return (
    <div className="site-shell">
      <Header />
      <main>{children}</main>
      <Footer />
    </div>
  );
}
