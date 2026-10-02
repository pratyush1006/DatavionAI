import Link from "next/link";
import { ArrowRight } from "lucide-react";

const items = [
  ["/about", "About"],
  ["/case-studies", "Case Studies"],
  ["/pricing", "Pricing"],
  ["/careers", "Careers"],
  ["/support", "Support"],
] as const;

export function PublicSiteHeader() {
  return (
    <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <Link href="/" className="font-semibold tracking-tight">DatavionAI</Link>
        <nav className="hidden items-center gap-6 md:flex">
          {items.map(([href, label]) => (
            <Link key={href} href={href} className="text-sm text-muted-foreground hover:text-foreground">
              {label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <Link href="/login" className="rounded-lg px-3 py-2 text-sm font-medium">Login</Link>
          <Link href="/register" className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground">
            Register <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </div>
    </header>
  );
}
