import { loginWithInitData, refreshTokens, logoutServer } from "../api";
import {
  getAccessToken,
  getRefreshToken,
  getAccessExpiresAt,
  clearTokens,
} from "../token-store";
import { API_URL } from "@/shared/config";

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn());
  localStorage.clear();
  clearTokens();
});

afterEach(() => {
  vi.restoreAllMocks();
  localStorage.clear();
  clearTokens();
});

function mockJsonResponse(body: unknown, ok = true, status = 200): Response {
  return {
    ok,
    status,
    json: () => Promise.resolve(body),
  } as Response;
}

describe("auth/api", () => {
  describe("loginWithInitData", () => {
    it("posts init_data to /auth/login and stores returned token pair", async () => {
      const serverPair = {
        access_token: "srv-access",
        refresh_token: "srv-refresh",
        token_type: "Bearer",
        expires_in: 900,
        expires_at: 1700000900,
        refresh_expires_at: 1700604800,
      };
      vi.mocked(fetch).mockResolvedValue(
        mockJsonResponse({ success: true, data: serverPair, error: null })
      );

      const pair = await loginWithInitData("raw=initdata&hash=abc");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/auth/login`,
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ init_data: "raw=initdata&hash=abc" }),
          headers: expect.objectContaining({
            "Content-Type": "application/json",
          }),
        })
      );
      expect(pair.accessToken).toBe("srv-access");
      expect(pair.refreshToken).toBe("srv-refresh");
      expect(pair.accessExpiresAt).toBe(1700000900);
      expect(getAccessToken()).toBe("srv-access");
      expect(getRefreshToken()).toBe("srv-refresh");
      expect(getAccessExpiresAt()).toBe(1700000900);
    });

    it("does NOT include Authorization header on /auth/login", async () => {
      vi.mocked(fetch).mockResolvedValue(
        mockJsonResponse({
          success: true,
          data: {
            access_token: "a",
            refresh_token: "r",
            token_type: "Bearer",
            expires_in: 900,
            expires_at: 1,
            refresh_expires_at: 2,
          },
          error: null,
        })
      );

      await loginWithInitData("init");

      const call = vi.mocked(fetch).mock.calls[0];
      const init = call[1] as RequestInit;
      const headers = init.headers as Record<string, string>;
      expect(headers.Authorization).toBeUndefined();
    });

    it("propagates error envelope on failure", async () => {
      vi.mocked(fetch).mockResolvedValue(
        mockJsonResponse(
          { success: false, data: null, error: "auth_data_expired" },
          false,
          401
        )
      );

      await expect(loginWithInitData("init")).rejects.toMatchObject({
        status: 401,
        error: "auth_data_expired",
      });
    });
  });

  describe("refreshTokens", () => {
    it("posts refresh_token to /auth/refresh and rotates the stored pair", async () => {
      const serverPair = {
        access_token: "new-access",
        refresh_token: "new-refresh",
        token_type: "Bearer",
        expires_in: 900,
        expires_at: 1700001800,
        refresh_expires_at: 1700604800,
      };
      vi.mocked(fetch).mockResolvedValue(
        mockJsonResponse({ success: true, data: serverPair, error: null })
      );

      const pair = await refreshTokens("old-refresh");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/auth/refresh`,
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ refresh_token: "old-refresh" }),
        })
      );
      expect(pair.accessToken).toBe("new-access");
      expect(pair.refreshToken).toBe("new-refresh");
      expect(getRefreshToken()).toBe("new-refresh");
      expect(getAccessToken()).toBe("new-access");
    });

    it("rejects with envelope error on 401", async () => {
      vi.mocked(fetch).mockResolvedValue(
        mockJsonResponse(
          { success: false, data: null, error: "refresh_token_expired" },
          false,
          401
        )
      );

      await expect(refreshTokens("dead")).rejects.toMatchObject({
        status: 401,
        error: "refresh_token_expired",
      });
    });
  });

  describe("logoutServer", () => {
    it("posts refresh_token with bearer access token", async () => {
      vi.mocked(fetch).mockResolvedValue(
        mockJsonResponse({ success: true, data: { revoked: true }, error: null })
      );

      await logoutServer("rt", "at");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/auth/logout`,
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ refresh_token: "rt" }),
          headers: expect.objectContaining({
            Authorization: "Bearer at",
            "Content-Type": "application/json",
          }),
        })
      );
    });

    it("does not throw on server error (best effort)", async () => {
      vi.mocked(fetch).mockRejectedValue(new TypeError("network down"));

      await expect(logoutServer("rt", "at")).resolves.toBeUndefined();
    });

    it("does not throw on non-2xx response", async () => {
      vi.mocked(fetch).mockResolvedValue(
        mockJsonResponse({ success: false, error: "x" }, false, 500)
      );

      await expect(logoutServer("rt", "at")).resolves.toBeUndefined();
    });
  });
});
