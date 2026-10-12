import { render, screen, cleanup } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { AutoFillStatus } from "@/components/questionnaires/auto-fill-status";
import type { AutoFillJob } from "@/hooks/use-api";

afterEach(cleanup);
const job: AutoFillJob = {
  id: "job", status: "pending", current_step: 0, total_steps: 41,
  step_name: "Queued", output_data: null, error_message: null,
};

describe("Auto-fill feedback", () => {
  it("announces queued and running progress accessibly", () => {
    const { rerender } = render(<AutoFillStatus job={job} />);
    expect(screen.getByRole("status")).toHaveTextContent("Auto-fill is queued");
    rerender(<AutoFillStatus job={{ ...job, status: "running", current_step: 20 }} />);
    expect(screen.getByRole("status")).toHaveTextContent("20 of 41 questions processed");
    expect(screen.getByRole("progressbar", { name: "Questions processed" })).toHaveAttribute("value", "20");
  });
  it("shows completed answer count", () => {
    render(<AutoFillStatus job={{ ...job, status: "completed", output_data: { filled_count: 12 } }} />);
    expect(screen.getByRole("status")).toHaveTextContent("12 new answers saved");
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument();
  });
  it("announces failures and connection errors", () => {
    const { rerender } = render(<AutoFillStatus job={{ ...job, status: "failed" }} />);
    expect(screen.getByRole("alert")).toHaveTextContent("Retry Auto-fill");
    rerender(<AutoFillStatus job={job} error="Could not refresh status. Reconnecting…" />);
    expect(screen.getByRole("alert")).toHaveTextContent("Reconnecting");
  });
});
