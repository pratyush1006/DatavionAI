/**
 * Notification menu.
 */

import { Bell } from "lucide-react";

import { Button } from "@/components/ui/button";

export function NotificationMenu() {
  return (
    <Button
      size="icon"
      variant="ghost"
    >
      <Bell className="h-5 w-5" />
    </Button>
  );
}
