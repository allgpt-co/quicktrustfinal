"use client";

import { FormEvent, Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowRight, Loader2, LockKeyhole, ShieldCheck } from "lucide-react";
import { useAuth } from "@/providers/auth-provider";
import { requestPasswordReset } from "@/lib/auth";

function safeReturnTo(value: string | null): string {
  return value && value.startsWith("/") && !value.startsWith("//")
    ? value
    : "/dashboard";
}

type Mode = "signin" | "register" | "forgot";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { authenticated, loading, signIn, register } = useAuth();
  const returnTo = safeReturnTo(searchParams.get("returnTo"));
  const invitationToken = returnTo.match(/^\/invite\/([^/?]+)/)?.[1];
  const [mode, setMode] = useState<Mode>("signin");
  const [email, setEmail] = useState(searchParams.get("email") || "");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && authenticated) router.replace(returnTo);
  }, [authenticated, loading, returnTo, router]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setNotice(null);
    setSubmitting(true);
    try {
      if (mode === "forgot") {
        await requestPasswordReset(email);
        setNotice("If an active account exists, we sent a secure password link.");
        return;
      }
      if (mode === "register") {
        if (password !== confirmPassword) {
          throw new Error("Passwords do not match");
        }
        await register({
          email,
          full_name: fullName,
          password,
          ...(invitationToken ? { invitation_token: invitationToken } : {}),
        });
        return;
      }
      await signIn(email, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to complete sign-in");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading || authenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-muted/30">
        <Loader2 className="h-6 w-6 animate-spin text-primary" aria-label="Loading" />
      </div>
    );
  }

  const title = mode === "signin" ? "Welcome back" : mode === "register" ? "Create your account" : "Reset your password";
  const description = mode === "signin"
    ? "Sign in to manage your compliance program."
    : mode === "register"
      ? invitationToken
        ? "Create an account to join your team in QuickTrust."
        : "Start a secure workspace for your organization."
      : "Enter your email and we’ll send a one-time password link.";

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden bg-background px-4 py-12">
      <div aria-hidden="true" className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,oklch(0.708_0.165_254.624_/_0.12),transparent_40%)]" />
      <div className="relative grid w-full max-w-4xl overflow-hidden rounded-2xl border bg-card shadow-2xl md:grid-cols-[0.9fr_1.1fr]">
        <section className="hidden bg-primary p-10 text-primary-foreground md:flex md:flex-col md:justify-between">
          <div>
            <div className="flex items-center gap-2 text-lg font-semibold">
              <ShieldCheck className="h-6 w-6" />
              QuickTrust
            </div>
            <h1 className="mt-12 text-3xl font-semibold leading-tight">
              Compliance operations, protected by your application.
            </h1>
            <p className="mt-4 text-sm leading-6 text-primary-foreground/75">
              Access controls, evidence, risk, policies, and audits remain scoped to your organization and role.
            </p>
          </div>
          <div className="flex items-center gap-2 text-xs text-primary-foreground/70">
            <LockKeyhole className="h-4 w-4" />
            Argon2id password protection · short-lived access tokens
          </div>
        </section>

        <section className="p-6 sm:p-10">
          <div className="mb-8 md:hidden">
            <div className="flex items-center gap-2 text-lg font-semibold">
              <ShieldCheck className="h-6 w-6 text-primary" /> QuickTrust
            </div>
          </div>
          <h2 className="text-2xl font-semibold tracking-tight">{title}</h2>
          <p className="mt-2 text-sm text-muted-foreground">{description}</p>

          {mode !== "forgot" && (
            <div className="mt-6 grid grid-cols-2 rounded-lg bg-muted p-1" aria-label="Authentication mode">
              <button
                type="button"
                onClick={() => { setMode("signin"); setError(null); setNotice(null); }}
                className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${mode === "signin" ? "bg-background shadow-sm" : "text-muted-foreground hover:text-foreground"}`}
              >
                Sign in
              </button>
              <button
                type="button"
                onClick={() => { setMode("register"); setError(null); setNotice(null); }}
                className={`rounded-md px-3 py-2 text-sm font-medium transition-colors ${mode === "register" ? "bg-background shadow-sm" : "text-muted-foreground hover:text-foreground"}`}
              >
                Create account
              </button>
            </div>
          )}

          <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
            {mode === "register" && (
              <div>
                <label htmlFor="full-name" className="text-sm font-medium">Full name</label>
                <input id="full-name" autoComplete="name" required maxLength={255} value={fullName} onChange={(event) => setFullName(event.target.value)} className="mt-1.5 h-10 w-full rounded-md border bg-background px-3 text-sm" />
              </div>
            )}
            <div>
              <label htmlFor="email" className="text-sm font-medium">Work email</label>
              <input id="email" type="email" inputMode="email" autoComplete="email" required value={email} onChange={(event) => setEmail(event.target.value)} className="mt-1.5 h-10 w-full rounded-md border bg-background px-3 text-sm" />
            </div>
            {mode !== "forgot" && (
              <div>
                <div className="flex items-center justify-between">
                  <label htmlFor="password" className="text-sm font-medium">Password</label>
                  {mode === "signin" && (
                    <button type="button" onClick={() => { setMode("forgot"); setError(null); setNotice(null); }} className="text-xs font-medium text-primary hover:underline">
                      Forgot password?
                    </button>
                  )}
                </div>
                <input id="password" type="password" autoComplete={mode === "signin" ? "current-password" : "new-password"} required minLength={mode === "register" ? 12 : 1} value={password} onChange={(event) => setPassword(event.target.value)} className="mt-1.5 h-10 w-full rounded-md border bg-background px-3 text-sm" />
                {mode === "register" && <p className="mt-1.5 text-xs text-muted-foreground">Use 12+ characters with upper/lowercase, a number, and a symbol.</p>}
              </div>
            )}
            {mode === "register" && (
              <div>
                <label htmlFor="confirm-password" className="text-sm font-medium">Confirm password</label>
                <input id="confirm-password" type="password" autoComplete="new-password" required minLength={12} value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} className="mt-1.5 h-10 w-full rounded-md border bg-background px-3 text-sm" />
              </div>
            )}

            {error && <div role="alert" className="rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-sm text-destructive">{error}</div>}
            {notice && <div role="status" className="rounded-md border border-green-600/30 bg-green-600/10 px-3 py-2 text-sm text-green-700 dark:text-green-300">{notice}</div>}

            <button type="submit" disabled={submitting} className="flex h-10 w-full items-center justify-center gap-2 rounded-md bg-primary px-4 text-sm font-medium text-primary-foreground shadow hover:bg-primary/90 disabled:opacity-50">
              {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : <ArrowRight className="h-4 w-4" />}
              {mode === "signin" ? "Sign in" : mode === "register" ? "Create account" : "Send password link"}
            </button>
          </form>

          {mode === "forgot" && (
            <button type="button" onClick={() => { setMode("signin"); setError(null); setNotice(null); }} className="mt-5 w-full text-center text-sm text-muted-foreground hover:text-foreground">
              Back to sign in
            </button>
          )}
        </section>
      </div>
    </main>
  );
}

export default function LoginPage() {
  return <Suspense fallback={<div className="flex min-h-screen items-center justify-center"><Loader2 className="h-6 w-6 animate-spin" /></div>}><LoginForm /></Suspense>;
}
