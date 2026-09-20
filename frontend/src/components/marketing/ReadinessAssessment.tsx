'use client';

import { useMemo, useState } from 'react';

const domains = [
  'Access control', 'Encryption', 'Monitoring and logging', 'Incident response',
  'Change management', 'Vendor management', 'Security policies', 'Business continuity',
];

export default function ReadinessAssessment() {
  const [scores, setScores] = useState<number[]>(Array.from({ length: 8 }, () => 0));
  const total = useMemo(() => scores.reduce((sum, value) => sum + value, 0), [scores]);
  const percentage = Math.round((total / 16) * 100);
  const band = total >= 14 ? 'Audit ready' : total >= 10 ? 'Nearly ready' : total >= 6 ? 'In progress' : 'Early stage';

  return (
    <div className="mx-auto max-w-4xl px-4 sm:px-6">
      <h2 className="font-display text-3xl font-bold text-slate-50">Score your eight control domains</h2>
      <p className="mt-3 text-slate-400">Choose 0 for not implemented, 1 for partially implemented, or 2 for fully implemented. This self-assessment is informational and is not an audit opinion.</p>
      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        {domains.map((domain, index) => (
          <label key={domain} className="rounded-xl border border-white/10 bg-white/5 p-4 text-slate-200">
            <span className="block font-medium">{domain}</span>
            <select
              value={scores[index]}
              onChange={(event) => setScores((current) => current.map((value, item) => item === index ? Number(event.target.value) : value))}
              className="mt-3 w-full rounded-lg border border-white/10 bg-slate-900 px-3 py-2 text-slate-200"
              aria-label={`${domain} score`}
            >
              <option value={0}>0 — Not implemented</option>
              <option value={1}>1 — Partially implemented</option>
              <option value={2}>2 — Fully implemented</option>
            </select>
          </label>
        ))}
      </div>
      <div className="mt-8 rounded-2xl border border-teal-500/30 bg-teal-500/10 p-6">
        <p className="text-sm uppercase tracking-wide text-teal-300">Current estimate</p>
        <p className="mt-2 font-display text-4xl font-bold text-slate-50">{total}/16 domain points</p>
        <p className="mt-2 text-slate-300">{percentage}% complete · {band}</p>
        <p className="mt-4 text-sm text-slate-400">Use the lowest-scoring domains to prioritize evidence collection and engineering remediation.</p>
      </div>
    </div>
  );
}
