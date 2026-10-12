import { act, cleanup, renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { afterEach, expect, it, vi } from "vitest";
import type { ReactNode } from "react";
import api from "@/lib/api";
import { useAutoFillQuestionnaire, useAutoFillStatus, type AutoFillJob } from "@/hooks/use-api";

vi.mock("@/lib/api", () => ({ default: { get: vi.fn(), post: vi.fn() } }));
afterEach(() => { cleanup(); vi.resetAllMocks(); });

it("polls a persisted job, refreshes answers on completion, and stops polling", async () => {
  const pending: AutoFillJob = { id: "job", status: "pending", current_step: 0, total_steps: 2,
    step_name: "Queued", output_data: null, error_message: null };
  let current: AutoFillJob | null = null;
  vi.mocked(api.get).mockImplementation(async () => current as never);
  vi.mocked(api.post).mockImplementation(async () => { current = pending; return pending as never; });
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const invalidate = vi.spyOn(qc, "invalidateQueries");
  const wrapper = ({ children }: { children: ReactNode }) => <QueryClientProvider client={qc}>{children}</QueryClientProvider>;
  const { result, unmount } = renderHook(() => ({
    status: useAutoFillStatus("org", "questionnaire"),
    start: useAutoFillQuestionnaire("org"),
  }), { wrapper });
  await waitFor(() => expect(result.current.status.isSuccess).toBe(true));
  await act(async () => { await result.current.start.mutateAsync("questionnaire"); });
  await waitFor(() => expect(result.current.status.data?.status).toBe("pending"));
  current = { ...pending, status: "completed", current_step: 2, output_data: { filled_count: 2 } };
  await waitFor(() => expect(result.current.status.data?.status).toBe("completed"), { timeout: 4000 });
  expect(invalidate).toHaveBeenCalledWith({ queryKey: ["questionnaires", "org"] });
  const calls = vi.mocked(api.get).mock.calls.length;
  await act(async () => { await new Promise(resolve => setTimeout(resolve, 1700)); });
  expect(vi.mocked(api.get).mock.calls.length).toBe(calls);
  unmount();
  qc.clear();
});
