import { ensureFreshAccessToken, forceRefresh, resetCoordinator } from "../refresh-coordinator";
import {
  setTokens,
  clearTokens,
  getAccessToken,
  getRefreshToken,
} from "../token-store";

vi.mock("../api", () => ({
  refreshTokens: vi.fn(),
  AuthApiError: class AuthApiError extends Error {
    status: number;
    error: string;
    constructor(status: number, err: string) {
      super(err);
      this.status = status;
      this.error = err;
    }
  },
}));

import { refreshTokens } from "../api";

beforeEach(() => {
  localStorage.clear();
  clearTokens();
  resetCoordinator();
  vi.useFakeTimers();
  vi.setSystemTime(new Date(1700000000 * 1000));
  vi.mocked(refreshTokens).mockReset();
});

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  localStorage.clear();
  clearTokens();
  resetCoordinator();
});

describe("refresh-coordinator", () => {
  it("returns current access token when more than 60s of TTL remain", async () => {
    setTokens({
      accessToken: "fresh-access",
      accessExpiresAt: 1700000000 + 600,
      refreshToken: "rt",
    });

    const token = await ensureFreshAccessToken();

    expect(token).toBe("fresh-access");
    expect(refreshTokens).not.toHaveBeenCalled();
  });

  it("triggers refresh when TTL is less than 60s", async () => {
    setTokens({
      accessToken: "expiring-access",
      accessExpiresAt: 1700000000 + 30,
      refreshToken: "old-rt",
    });
    vi.mocked(refreshTokens).mockImplementation(async () => {
      setTokens({
        accessToken: "rotated-access",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "new-rt",
      });
      return {
        accessToken: "rotated-access",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "new-rt",
      };
    });

    const token = await ensureFreshAccessToken();

    expect(token).toBe("rotated-access");
    expect(refreshTokens).toHaveBeenCalledTimes(1);
    expect(refreshTokens).toHaveBeenCalledWith("old-rt");
  });

  it("single concurrent refresh — N callers share one in-flight promise", async () => {
    setTokens({
      accessToken: "stale",
      accessExpiresAt: 1700000000 + 10,
      refreshToken: "shared-rt",
    });
    let resolveRefresh!: (pair: { accessToken: string; accessExpiresAt: number; refreshToken: string }) => void;
    vi.mocked(refreshTokens).mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveRefresh = (pair) => {
            setTokens(pair);
            resolve(pair);
          };
        })
    );

    const p1 = ensureFreshAccessToken();
    const p2 = ensureFreshAccessToken();
    const p3 = ensureFreshAccessToken();

    expect(refreshTokens).toHaveBeenCalledTimes(1);

    resolveRefresh({
      accessToken: "shared-new",
      accessExpiresAt: 1700000000 + 900,
      refreshToken: "shared-new-rt",
    });

    const [t1, t2, t3] = await Promise.all([p1, p2, p3]);
    expect(t1).toBe("shared-new");
    expect(t2).toBe("shared-new");
    expect(t3).toBe("shared-new");
    expect(refreshTokens).toHaveBeenCalledTimes(1);
  });

  it("successful refresh updates the token store", async () => {
    setTokens({
      accessToken: "old",
      accessExpiresAt: 1700000000,
      refreshToken: "rt",
    });
    vi.mocked(refreshTokens).mockImplementation(async () => {
      const pair = {
        accessToken: "new-stored",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "new-rt-stored",
      };
      setTokens(pair);
      return pair;
    });

    await ensureFreshAccessToken();

    expect(getAccessToken()).toBe("new-stored");
    expect(getRefreshToken()).toBe("new-rt-stored");
  });

  it("failed refresh clears tokens and rethrows", async () => {
    setTokens({
      accessToken: "old",
      accessExpiresAt: 1700000000,
      refreshToken: "rt",
    });
    const err = new Error("refresh_token_expired");
    vi.mocked(refreshTokens).mockRejectedValue(err);

    await expect(ensureFreshAccessToken()).rejects.toBe(err);
    expect(getAccessToken()).toBeNull();
    expect(getRefreshToken()).toBeNull();
  });

  it("two sequential calls after completion each create their own refresh", async () => {
    setTokens({
      accessToken: "a1",
      accessExpiresAt: 1700000000 + 5,
      refreshToken: "rt1",
    });
    vi.mocked(refreshTokens).mockImplementation(async () => {
      const pair = {
        accessToken: "a2",
        accessExpiresAt: 1700000000 + 10,
        refreshToken: "rt2",
      };
      setTokens(pair);
      return pair;
    });

    await ensureFreshAccessToken();
    expect(refreshTokens).toHaveBeenCalledTimes(1);

    vi.mocked(refreshTokens).mockImplementation(async () => {
      const pair = {
        accessToken: "a3",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "rt3",
      };
      setTokens(pair);
      return pair;
    });

    await ensureFreshAccessToken();
    expect(refreshTokens).toHaveBeenCalledTimes(2);
  });

  it("forceRefresh always triggers a refresh even if the access token is fresh", async () => {
    setTokens({
      accessToken: "still-good",
      accessExpiresAt: 1700000000 + 600,
      refreshToken: "rt-x",
    });
    vi.mocked(refreshTokens).mockImplementation(async () => {
      const pair = {
        accessToken: "forced",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "rt-y",
      };
      setTokens(pair);
      return pair;
    });

    const token = await forceRefresh();

    expect(token).toBe("forced");
    expect(refreshTokens).toHaveBeenCalledTimes(1);
  });

  it("throws when there is no refresh token at all", async () => {
    await expect(ensureFreshAccessToken()).rejects.toThrow();
  });
});
