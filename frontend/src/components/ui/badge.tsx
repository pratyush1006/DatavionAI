import { mergeProps } from "@base-ui/react/merge-props";
import { useRender } from "@base-ui/react/use-render";
import {
  cva,
  type VariantProps,
} from "class-variance-authority";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex h-6 w-fit shrink-0 items-center justify-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-medium whitespace-nowrap transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 [&>svg]:size-3",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-primary-foreground",

        secondary:
          "border-transparent bg-secondary text-secondary-foreground",

        success:
          "border-transparent bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400",

        warning:
          "border-transparent bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400",

        destructive:
          "border-transparent bg-destructive text-destructive-foreground",

        outline:
          "border-border bg-background text-foreground",

        ghost:
          "border-transparent bg-transparent text-foreground",

        info:
          "border-transparent bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400",
      },
    },

    defaultVariants: {
      variant: "default",
    },
  },
);

type BadgeProps =
  useRender.ComponentProps<"span"> &
    VariantProps<
      typeof badgeVariants
    >;

function Badge({
  className,
  variant,
  render,
  ...props
}: BadgeProps) {
  return useRender({
    defaultTagName: "span",

    props: mergeProps<"span">(
      {
        className: cn(
          badgeVariants({
            variant,
          }),
          className,
        ),
      },
      props,
    ),

    render,

    state: {
      slot: "badge",
      variant,
    },
  });
}

export {
  Badge,
  badgeVariants,
};
