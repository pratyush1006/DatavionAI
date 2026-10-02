import Link from "next/link";
import { ReactNode } from "react";

type Props = {
  href: string;
  children: ReactNode;
  variant?: "primary" | "secondary" | "light" | "outline" | "outline-light";
};

export function Button({
  href,
  children,
  variant = "primary",
}: Props) {
  return (
    <Link href={href} className={`site-button site-button-${variant}`}>
      {children}
    </Link>
  );
}
