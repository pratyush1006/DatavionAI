/**
 * Login page.
 */

"use client";

import { useRouter } from "next/navigation";
import { toast } from "sonner";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

import { LoginForm } from "../components/forms/login-form";
import type { LoginFormValues } from "../domain/schema";
import { useLoginMutation } from "../hooks/use-login-mutation";

export function LoginPage() {
  const router = useRouter();

  const loginMutation = useLoginMutation();

  async function handleSubmit(
  values: LoginFormValues,
) {
  console.log("LOGIN SUBMIT");
  console.log(values);

    try {
    await loginMutation.mutateAsync(values);

    console.log("LOGIN SUCCESS");

    toast.success("Welcome to Datavion AI.");

    router.replace("/dashboard");
  } catch (error) {
    console.error("LOGIN ERROR", error);

    toast.error("Invalid email or password.");
  }
}

  return (
    <main className="flex min-h-screen items-center justify-center bg-muted/30 p-6">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>
            Sign in
          </CardTitle>
        </CardHeader>

        <CardContent>
          <LoginForm
            isSubmitting={loginMutation.isPending}
            onSubmit={handleSubmit}
          />
        </CardContent>
      </Card>
    </main>
  );
}
