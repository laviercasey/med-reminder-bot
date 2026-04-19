import {
  setTokens,
  getAccessToken,
  getAccessExpiresAt,
  getRefreshToken,
  clearTokens,
  subscribe,
  REFRESH_TOKEN_STORAGE_KEY,
} from "../token-store";

beforeEach(() => {
  localStorage.clear();
  clearTokens();
});

afterEach(() => {
  localStorage.clear();
  clearTokens();
});

describe("token-store", () => {
  it("persists refresh token to localStorage under key 'mr.rt'", () => {
    setTokens({
      accessToken: "access-1",
      accessExpiresAt: 1000,
      refreshToken: "refresh-1",
    });

    expect(localStorage.getItem(REFRESH_TOKEN_STORAGE_KEY)).toBe("refresh-1");
    expect(REFRESH_TOKEN_STORAGE_KEY).toBe("mr.rt");
  });

  it("reads refresh token from localStorage on load", () => {
    localStorage.setItem(REFRESH_TOKEN_STORAGE_KEY, "stored-refresh");

    expect(getRefreshToken()).toBe("stored-refresh");
  });

  it("keeps access token in memory only, never in localStorage", () => {
    setTokens({
      accessToken: "access-2",
      accessExpiresAt: 2000,
      refreshToken: "refresh-2",
    });

    expect(getAccessToken()).toBe("access-2");
    expect(getAccessExpiresAt()).toBe(2000);
    expect(localStorage.getItem("mr.at")).toBeNull();
    const keys = Object.keys(localStorage);
    const accessLeak = keys.some((k) => localStorage.getItem(k) === "access-2");
    expect(accessLeak).toBe(false);
  });

  it("clears both memory and localStorage on clearTokens()", () => {
    setTokens({
      accessToken: "access-3",
      accessExpiresAt: 3000,
      refreshToken: "refresh-3",
    });

    clearTokens();

    expect(getAccessToken()).toBeNull();
    expect(getAccessExpiresAt()).toBeNull();
    expect(getRefreshToken()).toBeNull();
    expect(localStorage.getItem(REFRESH_TOKEN_STORAGE_KEY)).toBeNull();
  });

  it("emits change events to subscribers on setTokens", () => {
    const listener = vi.fn();
    const unsubscribe = subscribe(listener);

    setTokens({
      accessToken: "access-4",
      accessExpiresAt: 4000,
      refreshToken: "refresh-4",
    });

    expect(listener).toHaveBeenCalledTimes(1);
    unsubscribe();
  });

  it("emits change events on clearTokens", () => {
    setTokens({
      accessToken: "access-5",
      accessExpiresAt: 5000,
      refreshToken: "refresh-5",
    });
    const listener = vi.fn();
    const unsubscribe = subscribe(listener);

    clearTokens();

    expect(listener).toHaveBeenCalledTimes(1);
    unsubscribe();
  });

  it("stops emitting after unsubscribe", () => {
    const listener = vi.fn();
    const unsubscribe = subscribe(listener);
    unsubscribe();

    setTokens({
      accessToken: "access-6",
      accessExpiresAt: 6000,
      refreshToken: "refresh-6",
    });

    expect(listener).not.toHaveBeenCalled();
  });
});
