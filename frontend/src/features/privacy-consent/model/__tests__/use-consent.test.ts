import { renderHook, act } from "@testing-library/react";
import { useConsent } from "../use-consent";

describe("useConsent", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("returns false when no consent stored", () => {
    const { result } = renderHook(() => useConsent());
    expect(result.current.accepted).toBe(false);
  });

  it("returns true when consent already accepted", () => {
    localStorage.setItem("med_reminder_consent_accepted", "true");
    const { result } = renderHook(() => useConsent());
    expect(result.current.accepted).toBe(true);
  });

  it("accepts consent and persists to localStorage", () => {
    const { result } = renderHook(() => useConsent());

    act(() => {
      result.current.accept();
    });

    expect(result.current.accepted).toBe(true);
    expect(localStorage.getItem("med_reminder_consent_accepted")).toBe("true");
  });

  it("handles localStorage errors gracefully on read", () => {
    const spy = vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
      throw new Error("storage error");
    });

    const { result } = renderHook(() => useConsent());
    expect(result.current.accepted).toBe(false);

    spy.mockRestore();
  });

  it("handles localStorage errors gracefully on write", () => {
    const spy = vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw new Error("storage error");
    });

    const { result } = renderHook(() => useConsent());

    act(() => {
      result.current.accept();
    });

    expect(result.current.accepted).toBe(true);

    spy.mockRestore();
  });
});
