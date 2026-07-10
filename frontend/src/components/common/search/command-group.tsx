/**
 * Command group wrapper.
 */

import {
  CommandGroup,
  CommandGroupHeading,
} from "@/components/ui/command";

type AppCommandGroupProps = Readonly<{
  heading: string;
  children: React.ReactNode;
}>;

export function AppCommandGroup({
  heading,
  children,
}: AppCommandGroupProps) {
  return (
    <CommandGroup>
      <CommandGroupHeading>
        {heading}
      </CommandGroupHeading>

      {children}
    </CommandGroup>
  );
}
