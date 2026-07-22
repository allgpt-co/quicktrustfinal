"use client";

import { FormEvent, Suspense, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { CheckCircle2, Loader2, ShieldCheck } from "lucide-react";
import { resetPassword } from "@/lib/auth";

function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token") || "";
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [complete, setComplete] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    if (!token) return setError("This password link is invalid.");
    if (password !== confirmPassword) return setError("Passwords do not match");
    setSubmitting(true);
    try {
      await resetPassword(token, password);
      setComplete(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to update password");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-muted/30 px-4">
      <section className="w-full max-w-md rounded-xl border bg-card p-8 shadow-xl">
        <div className="flex items-center gap-2 font-semibold"><ShieldCheck className="h-6 w-6 text-primary" /> QuickTrust</div>
        {complete ? (
          <div className="mt-8 text-center">
            <CheckCircle2 className="mx-auto h-10 w-10 text-green-600" />
            <h1 className="mt-4 text-2xl font-semibold">Password updated</h1>
            <p className="mt-2 text-sm text-muted-foreground">Your sessions were secured. Sign in with your new password.</p>
            <Link href="/login" className="mt-6 inline-flex h-10 items-center rounded-md bg-primary px-5 text-sm font-medium text-primary-foreground">Continue to sign in</Link>
          </div>
        ) : (
          <>
            <h1 className="mt-8 text-2xl font-semibold">Set your password</h1>
            <p className="mt-2 text-sm text-muted-foreground">Use 12+ characters with upper/lowercase, a number, and a symbol.</p>
            <form onSubmit={submit} className="mt-6 space-y-4">
              <div><label htmlFor="new-password" className="text-sm font-medium">New password</label><input id="new-password" type="password" autoComplete="new-password" minLength={12} required value={password} onChange={(event) => setPassword(event.target.value)} className="mt-1.5 h-10 w-full rounded-md border bg-background px-3 text-sm" /></div>
              <div><label htmlFor="confirm-new-password" className="text-sm font-medium">Confirm password</label><input id="confirm-new-password" type="password" autoComplete="new-password" minLength={12} required value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} className="mt-1.5 h-10 w-full rounded-md border bg-background px-3 text-sm" /></div>
              {error && <div role="alert" className="rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">{error}</div>}
              <button type="submit" disabled={submitting} className="flex h-10 w-full items-center justify-center gap-2 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground disabled:opacity-50">{submitting && <Loader2 className="h-4 w-4 animate-spin" />}Update password</button>
            </form>
          </>
        )}
      </section>
    </main>
  );
}

export default function ResetPasswordPage() {
  return <Suspense fallback={<div className="flex min-h-screen items-center justify-center"><Loader2 className="h-6 w-6 animate-spin" /></div>}><ResetPasswordForm /></Suspense>;
}
