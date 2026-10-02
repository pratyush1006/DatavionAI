import Link from "next/link";

export function PublicSiteFooter() {
  return (
    <footer className="border-t">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-10 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="font-semibold">DatavionAI</p>
          <p className="mt-1 text-xs text-muted-foreground">
            DatavionOS — The AI Operating System for Healthcare.
          </p>
        </div>
        <div className="flex gap-5 text-sm text-muted-foreground">
          <Link href="/about">About</Link>
          <Link href="/support">Support</Link>
          <Link href="/pricing">Pricing</Link>
        </div>
      </div>
    </footer>
  );
}
