import type { AutoFillJob } from "@/hooks/use-api";

export function AutoFillStatus({ job, error }: { job?: AutoFillJob | null; error?: string }) {
  if (error) return <p role="alert" className="rounded-md border border-destructive p-4 text-sm text-destructive">{error}</p>;
  if (!job) return null;
  const active = job.status === "pending" || job.status === "running";
  const completed = Math.min(job.current_step, job.total_steps);
  return (
    <section aria-label="Auto-fill progress" aria-live="polite" role={job.status === "failed" ? "alert" : "status"}
      className="space-y-2 rounded-md border bg-muted/40 p-4 text-sm">
      <p className="font-medium">
        {job.status === "pending" ? "Auto-fill is queued" : job.status === "running" ? "Generating answers" :
          job.status === "completed" ? "Auto-fill complete" : "Auto-fill could not finish"}
      </p>
      {active ? <>
        <p className="text-muted-foreground">You can leave this page and return to check progress.</p>
        <progress aria-label="Questions processed" value={completed} max={Math.max(job.total_steps, 1)} className="h-2 w-full accent-primary" />
        <p>{completed} of {job.total_steps} questions processed</p>
      </> : job.status === "completed" ?
        <p>{job.output_data?.filled_count ?? 0} new answers saved. Review them below.</p> :
        <p>{job.error_message || "Saved answers are retained. Retry Auto-fill to continue."}</p>}
    </section>
  );
}
