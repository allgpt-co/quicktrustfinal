'use client';

import { useMemo, useState } from 'react';

export default function ComplianceRoiCalculator() {
  const [investment, setInvestment] = useState(77400);
  const [blockedDeals, setBlockedDeals] = useState(3);
  const [acv, setAcv] = useState(120000);
  const [daysSaved, setDaysSaved] = useState(25);
  const [dealsPerYear, setDealsPerYear] = useState(15);
  const [insuranceSavings, setInsuranceSavings] = useState(12000);
  const impact = useMemo(() => blockedDeals * acv + acv * dealsPerYear * (daysSaved / 365) + insuranceSavings, [blockedDeals, acv, dealsPerYear, daysSaved, insuranceSavings]);
  const roi = investment > 0 ? ((impact - investment) / investment) * 100 : 0;
  const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

  const numberInput = (label: string, value: number, setValue: (value: number) => void, min = 0) => (
    <label className="block rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300">
      <span className="block font-medium">{label}</span>
      <input type="number" min={min} value={value} onChange={(event) => setValue(Math.max(min, Number(event.target.value) || 0))} className="mt-2 w-full rounded-lg border border-white/10 bg-slate-900 px-3 py-2 text-slate-100" />
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
        {numberInput('Sales-cycle days saved', daysSaved, setDaysSaved)}
        {numberInput('Enterprise deals per year', dealsPerYear, setDealsPerYear)}
        {numberInput('Estimated insurance savings', insuranceSavings, setInsuranceSavings)}
      </div>
      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-6"><p className="text-sm text-slate-400">Estimated annual impact</p><p className="mt-2 font-display text-3xl font-bold text-slate-50">{money.format(impact)}</p></div>
        <div className="rounded-2xl border border-teal-500/30 bg-teal-500/10 p-6"><p className="text-sm text-teal-300">Estimated ROI</p><p className="mt-2 font-display text-3xl font-bold text-slate-50">{roi.toFixed(0)}%</p></div>
      </div>
      <p className="mt-6 text-sm text-slate-500">The model includes blocked deals, sales-cycle acceleration, and insurance savings. Validate each assumption with your finance, sales, and security teams before using it for a budget decision.</p>
    </div>
  );
}
