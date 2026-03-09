"use client";

import { useEffect } from "react";
import { useAuth } from "@/providers/auth-provider";

export default function LoginPage() {
  const { authenticated, loading, login } = useAuth();

  useEffect(() => {
    if (!loading && !authenticated) {
      login();
    }
  }, [loading, authenticated, login]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p className="text-muted-foreground">Redirecting to login...</p>
    </div>
  );
}
