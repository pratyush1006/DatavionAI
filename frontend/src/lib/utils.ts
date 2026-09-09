/**
 * =============================================================================
 * DatavionOS
 * File: src/lib/utils.ts
 * =============================================================================
 *
 * Shared frontend utility functions.
 *
 * This module contains small, framework-independent helpers used throughout
 * the presentation layer.
 *
 * Design Principles
 * -----------------
 * • Minimal
 * • Reusable
 * • Type Safe
 * • No business logic
 * • No API dependencies
 * • No authentication dependencies
 * • No feature dependencies
 * • Compatible with shadcn/ui
 * • Enterprise Ready
 * =============================================================================
 */

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merge conditional class names safely.
 *
 * Combines clsx's conditional class handling with Tailwind's conflict
 * resolution.
 *
 * Example:
 *
 * cn(
 *     "px-4 py-2",
 *     isActive && "bg-primary",
 *     className,
 * );
 */
export function cn(
    ...inputs: ClassValue[]
): string {
    return twMerge(
        clsx(inputs),
    );
}
