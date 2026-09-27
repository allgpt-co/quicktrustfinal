'use client';

import { useMemo, useState } from 'react';

export default function ComplianceRoiCalculator() {
  const [investment, setInvestment] = useState(77400);
  const [blockedDeals, setBlockedDeals] = useState(3);
  const [acv, setAcv] = useState(120000);
  const [daysSaved, setDaysSaved] = useState(25);
  const [dealsPerYear, setDealsPerYear] = useState(15);
  const [insuranceSavings, setInsuranceSavings] = useState(12000);
  // Timing of existing revenue is not incremental revenue; show it separately.
  const impact = useMemo(() => blockedDeals * acv + insuranceSavings, [blockedDeals, acv, insuranceSavings]);
  const timing = acv * dealsPerYear * (daysSaved / 365);
  const roi = investment > 0 ? ((impact - investment) / investment) * 100 : 0;
  const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

  const numberInput = (label: string, value: number, setValue: (value: number) => void, min = 0, max = 1_000_000_000) => (
    <label className="block rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300">
      <span className="block font-medium">{label}</span>
      <input type="number" min={min} max={max} value={value} onChange={(event) => setValue(Math.min(max, Math.max(min, Number(event.target.value) || 0)))} className="mt-2 w-full rounded-lg border border-white/10 bg-slate-900 px-3 py-2 text-slate-100" />
    </label>
  );

  return (
    <div className="mx-auto max-w-5xl px-4 sm:px-6">
      <h2 className="font-display text-3xl font-bold text-slate-50">Model your first-year business case</h2>
      <p className="mt-3 text-slate-400">Replace the example assumptions with your own numbers. The result is an estimate, not a revenue guarantee.</p>
      <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {numberInput('Year-one compliance investment', investment, setInvestment, 1)}
        {numberInput('Compliance-blocked deals', blockedDeals, setBlockedDeals)}
        {numberInput('Average enterprise ACV', acv, setAcv)}
        {numberInput('Sales-cycle days saved', daysSaved, setDaysSaved, 0, 365)}
        {numberInput('Enterprise deals per year', dealsPerYear, setDealsPerYear)}
        {numberInput('Estimated insurance savings', insuranceSavings, setInsuranceSavings)}
      </div>
      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-6"><p className="text-sm text-slate-400">Hypothetical incremental benefit</p><p className="mt-2 font-display text-3xl font-bold text-slate-50">{money.format(impact)}</p></div>
        <div className="rounded-2xl border border-teal-500/30 bg-teal-500/10 p-6"><p className="text-sm text-teal-300">Simple scenario return</p><p className="mt-2 font-display text-3xl font-bold text-slate-50">{roi.toFixed(0)}%</p></div>
      </div>
      <p className="mt-6 text-sm text-slate-400">Annualized sales timing illustration: {money.format(timing)}. Excluded from the return calculation because earlier revenue is not additional revenue.</p>
      <p className="mt-3 text-sm text-slate-500">Contract value is not profit. This model excludes delivery costs, probabilities and discounting. Validate assumptions with finance, sales and security, and avoid counting the same deal more than once.</p>
    </div>
  );
}
