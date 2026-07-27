import Link from "next/link";

import { Button } from "@/components/ui/button";

export default function NotFoundPage() {
  return (
    <main className="flex min-h-screen items-center justify-center p-6">
      <section className="max-w-md space-y-4 text-center">
        <h1 className="text-2xl font-semibold">
          Page not found
        </h1>

        <p className="text-sm text-muted-foreground">
          The requested workspace page does not exist or is not available to
          your account.
        </p>

        <Button asChild>
          <Link href="/dashboard">
            Return to dashboard
          </Link>
        </Button>
      </section>
    </main>
  );
}
