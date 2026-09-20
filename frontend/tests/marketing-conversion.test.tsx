import { cleanup, fireEvent, render, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import BookingModal from "@/components/marketing/homepage/BookingModal";
import ContactForm from "@/components/marketing/homepage/ContactForm";
import LeadCapture from "@/components/marketing/homepage/LeadCapture";
import { trackMarketingLead } from "@/lib/marketing-analytics";

vi.mock("@/lib/marketing-analytics", () => ({
  trackMarketingLead: vi.fn(),
}));

const mockedTrack = vi.mocked(trackMarketingLead);
const fetchMock = vi.fn();

function submit(container: HTMLElement): void {
  const form = container.querySelector("form");
  if (!form) throw new Error("Expected a form");
  fireEvent.submit(form);
}

function successResponse() {
  return { ok: true, json: async () => ({ success: true }) };
}

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  vi.restoreAllMocks();
});

beforeEach(() => {
  vi.stubGlobal("fetch", fetchMock);
  fetchMock.mockReset();
  vi.spyOn(console, "error").mockImplementation(() => {});
});

describe("marketing conversion events", () => {
  test.each([
    ["contact", () => render(<ContactForm />)],
    ["booking", () => render(<BookingModal isOpen onClose={vi.fn()} />)],
    ["readiness", () => render(<LeadCapture />)],
  ] as const)("emits the PII-free event after a successful %s submission", async (formType, renderForm) => {
    fetchMock.mockResolvedValue(successResponse());
    const { container } = renderForm();

    submit(container);

    await waitFor(() => expect(mockedTrack).toHaveBeenCalledWith(formType));
    expect(mockedTrack).toHaveBeenCalledTimes(1);
    expect(JSON.stringify(mockedTrack.mock.calls[0])).not.toMatch(/@|email|phone|company|message/i);
  });

  test("does not emit when the API rejects the contact submission", async () => {
    fetchMock.mockResolvedValue({ ok: false, status: 502, statusText: "Bad Gateway", json: async () => ({ error: "Unavailable" }) });
    const { container } = render(<ContactForm />);

    submit(container);

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    expect(mockedTrack).not.toHaveBeenCalled();
  });

  test("does not emit when a 200 response does not explicitly confirm success", async () => {
    fetchMock.mockResolvedValue({ ok: true, json: async () => ({ success: false }) });
    const { container } = render(<LeadCapture />);

    submit(container);

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1));
    expect(mockedTrack).not.toHaveBeenCalled();
  });
});
