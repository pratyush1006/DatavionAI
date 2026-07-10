/**
 * Global command palette.
 */

"use client";

import { useEffect, useState } from "react";

import {
  CommandDialog,
  CommandEmpty,
  CommandInput,
  CommandList,
} from "@/components/ui/command";

type CommandPaletteProps = Readonly<{
  children: React.ReactNode;
}>;

export function CommandPalette({
  children,
}: CommandPaletteProps) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const down = (event: KeyboardEvent) => {
      if (
        event.key === "k" &&
        (event.metaKey || event.ctrlKey)
      ) {
        event.preventDefault();

        setOpen((previous) => !previous);
      }
    };

    document.addEventListener("keydown", down);

    return () =>
      document.removeEventListener(
        "keydown",
        down,
      );
  }, []);

  return (
    <>
      {children}

      <CommandDialog
        open={open}
        onOpenChange={setOpen}
      >
        <CommandInput placeholder="Search anything..." />

        <CommandList>
          <CommandEmpty>
            No results found.
          </CommandEmpty>
        </CommandList>
      </CommandDialog>
    </>
  );
}
