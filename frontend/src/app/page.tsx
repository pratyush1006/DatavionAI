"use client";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center">
      <DropdownMenu>
        <DropdownMenuTrigger className="rounded border px-4 py-2">
          Open Menu
        </DropdownMenuTrigger>

        <DropdownMenuContent>
          <DropdownMenuItem>
            Item 1
          </DropdownMenuItem>

          <DropdownMenuItem>
            Item 2
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </main>
  );
}
