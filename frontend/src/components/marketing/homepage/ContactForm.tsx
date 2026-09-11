"use client";
import { useState, type FormEvent } from "react";

export default function ContactForm() {
  const [submitting, setSubmitting] = useState(false);
  const [status, setStatus] = useState<"success" | "error" | null>(null);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    setSubmitting(true);
    setStatus(null);
    try {
      const response = await fetch("/api/contact", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
      });
      if (!response.ok || !(await response.json()).success) throw new Error("Submit failed");
      form.reset();
      setStatus("success");
    } catch { setStatus("error"); }
    finally { setSubmitting(false); }
  }
  return (
              <form onSubmit={submit} className="space-y-4">
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-slate-300 mb-1">
                    Full Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="fullName"
                    required
                    autoComplete="name"
                    className="w-full bg-slate-900 border border-white/10 rounded-lg px-4 py-2.5 text-slate-100 placeholder:text-slate-500 focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 focus:outline-none"
                    placeholder="Your name"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-1">
                    Work Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    autoComplete="email"
                    className="w-full bg-slate-900 border border-white/10 rounded-lg px-4 py-2.5 text-slate-100 placeholder:text-slate-500 focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 focus:outline-none"
                    placeholder="you@company.com"
                  />
                </div>

                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-slate-300 mb-1">
                    Company Name
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    required
                    autoComplete="organization"
                    className="w-full bg-slate-900 border border-white/10 rounded-lg px-4 py-2.5 text-slate-100 placeholder:text-slate-500 focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 focus:outline-none"
                    placeholder="Your company"
                  />
                </div>

                <div>
                  <label htmlFor="framework" className="block text-sm font-medium text-slate-300 mb-1">
                    Framework of Interest
                  </label>
                  <select
                    id="framework"
                    name="framework"
                    className="w-full bg-slate-900 border border-white/10 rounded-lg px-4 py-2.5 text-slate-100 focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 focus:outline-none"
                  >
                    <option value="">Select a framework</option>
                    <option value="soc2">SOC 2</option>
                    <option value="iso27001">ISO 27001</option>
                    <option value="hipaa">HIPAA</option>
                    <option value="hitrust">HITRUST</option>
                    <option value="pci-dss">PCI DSS</option>
                    <option value="gdpr">GDPR</option>
                    <option value="iso42001">ISO 42001</option>
                    <option value="multiple">Multiple Frameworks</option>
                    <option value="other">Other / Not Sure</option>
                  </select>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-slate-300 mb-1">
                    Message
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    rows={4}
                    className="w-full bg-slate-900 border border-white/10 rounded-lg px-4 py-2.5 text-slate-100 placeholder:text-slate-500 focus:border-teal-500/50 focus:ring-1 focus:ring-teal-500/50 focus:outline-none"
                    placeholder="Tell us about your compliance needs..."
                  />
                </div>

                <button
                  type="submit" disabled={submitting}
                  className="w-full py-3 px-6 rounded-xl font-display font-semibold bg-gradient-to-r from-teal-400 to-teal-500 text-slate-950 shadow-[0_4px_20px_rgba(45,212,191,0.4)] hover:-translate-y-0.5 hover:shadow-[0_8px_30px_rgba(45,212,191,0.5)] transition-all"
                >
                  {submitting ? "Sending…" : "Send Message"}
                </button>

                <p className="text-xs text-slate-500 mt-2">
                  We respond within one business day. No spam, ever.
                </p>
              {status && <p role={status === "success" ? "status" : "alert"} className="mt-4 text-sm text-slate-200">{status === "success" ? "Thank you. We received your message and will be in touch." : "We could not send your message. Please check your details and try again."}</p>}
              </form>
  );
}
