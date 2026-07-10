/**
 * Command item.
 */

import {
  CommandItem,
} from "@/components/ui/command";

type AppCommandItemProps = Readonly<{
  title: string;

  onSelect: () => void;
}>;

export function AppCommandItem({
  title,
  onSelect,
}: AppCommandItemProps) {
  return (
    <CommandItem onSelect={onSelect}>
      {title}
    </CommandItem>
  );
}
