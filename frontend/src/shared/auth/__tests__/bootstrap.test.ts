import {
  bootstrapAuth,
  cancelPreemptiveRefresh,
  getBootstrapState,
  resetBootstrap,
} from "../bootstrap";
import {
  setTokens,
  clearTokens,
  getAccessToken,
  REFRESH_TOKEN_STORAGE_KEY,
} from "../token-store";
import { resetCoordinator } from "../refresh-coordinator";

vi.mock("@telegram-apps/sdk-react", () => ({
  retrieveRawInitData: vi.fn(() => "test_init_data_xyz"),
}));

vi.mock("../api", () => ({
  loginWithInitData: vi.fn(),
  refreshTokens: vi.fn(),
  logoutServer: vi.fn(),
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

import { loginWithInitData, refreshTokens, AuthApiError } from "../api";
import { retrieveRawInitData } from "@telegram-apps/sdk-react";

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(1700000000 * 1000));
  localStorage.clear();
  clearTokens();
  resetCoordinator();
  resetBootstrap();
  vi.mocked(loginWithInitData).mockReset();
  vi.mocked(refreshTokens).mockReset();
  vi.mocked(retrieveRawInitData).mockReset();
  vi.mocked(retrieveRawInitData).mockReturnValue("test_init_data_xyz");
});

afterEach(() => {
  cancelPreemptiveRefresh();
  vi.useRealTimers();
  vi.restoreAllMocks();
  localStorage.clear();
  clearTokens();
  resetCoordinator();
  resetBootstrap();
});

describe("bootstrapAuth", () => {
  it("calls /refresh first when a refresh token exists in localStorage", async () => {
    localStorage.setItem(REFRESH_TOKEN_STORAGE_KEY, "stored-rt");
    vi.mocked(refreshTokens).mockImplementation(async () => {
      const pair = {
        accessToken: "boot-access",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "boot-rt",
      };
      setTokens(pair);
      return pair;
    });

    await bootstrapAuth();

    expect(refreshTokens).toHaveBeenCalledTimes(1);
    expect(refreshTokens).toHaveBeenCalledWith("stored-rt");
    expect(loginWithInitData).not.toHaveBeenCalled();
    expect(getAccessToken()).toBe("boot-access");
    expect(getBootstrapState().status).toBe("ready");
  });

  it("falls back to /login with initData when no refresh token exists", async () => {
    vi.mocked(loginWithInitData).mockImplementation(async () => {
      const pair = {
        accessToken: "login-access",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "login-rt",
      };
      setTokens(pair);
      return pair;
    });

    await bootstrapAuth();

    expect(loginWithInitData).toHaveBeenCalledTimes(1);
    expect(loginWithInitData).toHaveBeenCalledWith("test_init_data_xyz");
    expect(refreshTokens).not.toHaveBeenCalled();
    expect(getAccessToken()).toBe("login-access");
    expect(getBootstrapState().status).toBe("ready");
  });

  it("falls back to /login when /refresh fails with 401", async () => {
    localStorage.setItem(REFRESH_TOKEN_STORAGE_KEY, "expired-rt");
    vi.mocked(refreshTokens).mockRejectedValue(
      new AuthApiError(401, "refresh_token_expired")
    );
    vi.mocked(loginWithInitData).mockImplementation(async () => {
      const pair = {
        accessToken: "after-login",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "after-rt",
      };
      setTokens(pair);
      return pair;
    });

    await bootstrapAuth();

    expect(refreshTokens).toHaveBeenCalledTimes(1);
    expect(loginWithInitData).toHaveBeenCalledTimes(1);
    expect(getBootstrapState().status).toBe("ready");
  });

  it("sets bootstrap state to 'auth_expired' when /login fails with auth_data_expired", async () => {
    vi.mocked(loginWithInitData).mockRejectedValue(
      new AuthApiError(401, "auth_data_expired")
    );

    await bootstrapAuth();

    const state = getBootstrapState();
    expect(state.status).toBe("auth_expired");
    expect(state.error).toBe("auth_data_expired");
  });

  it("sets bootstrap state to 'auth_expired' on any /login failure", async () => {
    vi.mocked(loginWithInitData).mockRejectedValue(
      new AuthApiError(401, "invalid_hash")
    );

    await bootstrapAuth();

    expect(getBootstrapState().status).toBe("auth_expired");
  });

  it("schedules pre-emptive refresh at expires_at - 60s", async () => {
    vi.mocked(loginWithInitData).mockImplementation(async () => {
      const pair = {
        accessToken: "boot-access",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "boot-rt",
      };
      setTokens(pair);
      return pair;
    });
    vi.mocked(refreshTokens).mockImplementation(async () => {
      const pair = {
        accessToken: "preemptive-access",
        accessExpiresAt: 1700000000 + 1800,
        refreshToken: "preemptive-rt",
      };
      setTokens(pair);
      return pair;
    });

    await bootstrapAuth();

    expect(refreshTokens).not.toHaveBeenCalled();

    await vi.advanceTimersByTimeAsync(840 * 1000);

    expect(refreshTokens).toHaveBeenCalledTimes(1);
  });

  it("cancels prior pre-emptive timer on cancelPreemptiveRefresh", async () => {
    vi.mocked(loginWithInitData).mockImplementation(async () => {
      const pair = {
        accessToken: "boot-access",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "boot-rt",
      };
      setTokens(pair);
      return pair;
    });

    await bootstrapAuth();
    cancelPreemptiveRefresh();

    await vi.advanceTimersByTimeAsync(900 * 1000);

    expect(refreshTokens).not.toHaveBeenCalled();
  });

  it("re-bootstrapping cancels any prior timer", async () => {
    vi.mocked(loginWithInitData).mockImplementation(async () => {
      const pair = {
        accessToken: "boot-access",
        accessExpiresAt: 1700000000 + 900,
        refreshToken: "boot-rt",
      };
      setTokens(pair);
      return pair;
    });
    vi.mocked(refreshTokens).mockImplementation(async () => {
      const pair = {
        accessToken: "preemptive-access-1",
        accessExpiresAt: 1700000000 + 5000,
        refreshToken: "preemptive-rt-1",
      };
      setTokens(pair);
      return pair;
    });

    await bootstrapAuth();
    expect(refreshTokens).not.toHaveBeenCalled();

    vi.mocked(loginWithInitData).mockImplementation(async () => {
      const pair = {
        accessToken: "boot-access-2",
        accessExpiresAt: 1700000000 + 300,
        refreshToken: "boot-rt-2",
      };
      setTokens(pair);
      return pair;
    });
    localStorage.removeItem(REFRESH_TOKEN_STORAGE_KEY);
    clearTokens();
    await bootstrapAuth();

    await vi.advanceTimersByTimeAsync(240 * 1000);

    expect(refreshTokens).toHaveBeenCalledTimes(1);
  });
});
