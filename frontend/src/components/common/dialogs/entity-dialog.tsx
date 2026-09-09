/**
 * =============================================================================
 * DatavionOS
 * File: src/components/common/dialogs/entity-dialog.tsx
 * =============================================================================
 *
 * Standard entity dialog wrapper.
 *
 * Used for Create, Edit and View operations across DatavionOS.
 * =============================================================================
 */

"use client";

import type {
    ReactNode,
} from "react";

import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";

import {
    cn,
} from "@/lib/utils";

/* =============================================================================
 * Types
 * =============================================================================
 */

export type EntityDialogProps =
    Readonly<{
        open: boolean;

        onOpenChange:
            (open: boolean) => void;

        title: string;

        description?:
            ReactNode;

        children: ReactNode;

        footer?:
            ReactNode;

        size?:
            | "sm"
            | "md"
            | "lg"
            | "xl";

        className?:
            string;
    }>;

/* =============================================================================
 * Configuration
 * =============================================================================
 */

const SIZE_CLASSES = {
    sm: "sm:max-w-lg",
    md: "sm:max-w-3xl",
    lg: "sm:max-w-5xl",
    xl: "sm:max-w-7xl",
} as const;

/* =============================================================================
 * Component
 * =============================================================================
 */

export function EntityDialog({
    open,
    onOpenChange,
    title,
    description,
    children,
    footer,
    size = "lg",
    className,
}: EntityDialogProps) {
    return (
        <Dialog
            open={open}
            onOpenChange={onOpenChange}
        >
            <DialogContent
                className={cn(
                    "flex max-h-[92vh] flex-col overflow-hidden p-0",
                    SIZE_CLASSES[size],
                    className,
                )}
            >
                <DialogHeader className="px-8 pt-6">
                    <DialogTitle>
                        {title}
                    </DialogTitle>

                    {description && (
                        <DialogDescription
                            asChild
                        >
                            <div>
                                {description}
                            </div>
                        </DialogDescription>
                    )}
                </DialogHeader>

                <div className="flex-1 overflow-y-auto px-8 py-6">
                    {children}
                </div>

                {footer && (
                    <div className="border-t bg-muted/40 px-8 py-4">
                        {footer}
                    </div>
                )}
            </DialogContent>
        </Dialog>
    );
}
