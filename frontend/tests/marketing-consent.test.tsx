import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";
import MarketingConsent from "@/components/marketing/MarketingConsent";
import {
  ANALYTICS_CONSENT_EVENT,
  getAnalyticsConsent,
  setAnalyticsConsent,
} from "@/lib/marketing-analytics";

vi.mock("@/lib/marketing-analytics", () => ({
  ANALYTICS_CONSENT_EVENT: "qt:analytics-consent",
  getAnalyticsConsent: vi.fn(),
  setAnalyticsConsent: vi.fn(),
}));

const mockedGetConsent = vi.mocked(getAnalyticsConsent);
const mockedSetConsent = vi.mocked(setAnalyticsConsent);

beforeEach(() => {
  mockedGetConsent.mockReturnValue(null);
  mockedSetConsent.mockReset();
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe("MarketingConsent", () => {
  test("shows equally available opt-in and decline controls with privacy link", () => {
    render(<MarketingConsent />);

    expect(screen.getByRole("heading", { name: /choose google analytics preferences/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /allow google analytics/i })).toBeVisible();
    expect(screen.getByRole("button", { name: /decline google analytics/i })).toBeVisible();
    expect(screen.getByRole("link", { name: /privacy policy/i })).toHaveAttribute("href", "/privacy-policy");
    expect(screen.getByText(/not enabled until you choose allow/i)).toBeVisible();
  });

  test("persists an allow choice, closes the panel, and focuses the reopen control", () => {
    render(<MarketingConsent />);
    fireEvent.click(screen.getByRole("button", { name: /allow google analytics/i }));

    expect(mockedSetConsent).toHaveBeenCalledWith("granted");
    expect(screen.getByRole("button", { name: /analytics preferences/i })).toHaveFocus();
    expect(screen.getByRole("status")).toHaveTextContent(/allowed/i);
  });

  test("persists decline and allows a visitor to reopen and change the choice", () => {
    render(<MarketingConsent />);
    fireEvent.click(screen.getByRole("button", { name: /decline google analytics/i }));

    expect(mockedSetConsent).toHaveBeenCalledWith("denied");
    const reopen = screen.getByRole("button", { name: /analytics preferences/i });
    expect(reopen).toHaveFocus();
    fireEvent.click(reopen);

    expect(screen.getByRole("heading", { name: /choose google analytics preferences/i })).toHaveFocus();
    fireEvent.click(screen.getByRole("button", { name: /allow google analytics/i }));
    expect(mockedSetConsent).toHaveBeenLastCalledWith("granted");
  });

  test("reflects an external consent decision without reimplementing storage", async () => {
    mockedGetConsent.mockReturnValueOnce(null).mockReturnValueOnce("granted");
    render(<MarketingConsent />);
    window.dispatchEvent(new Event(ANALYTICS_CONSENT_EVENT));

    await waitFor(() => expect(screen.getByText(/allowed/i)).toBeVisible());
    expect(screen.getByRole("button", { name: /analytics preferences/i })).toBeVisible();
  });
});
