import { apiClient } from "../client";
import { createSuccessResponse, mockMedications } from "@/test/mocks/handlers";
import { API_URL } from "@/shared/config";
import {
  setTokens,
  clearTokens,
  getAccessToken,
  getRefreshToken,
} from "@/shared/auth/token-store";
import { resetCoordinator } from "@/shared/auth/refresh-coordinator";

vi.mock("@/shared/auth/api", () => ({
  refreshTokens: vi.fn(),
  loginWithInitData: vi.fn(),
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

import { refreshTokens } from "@/shared/auth/api";

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(1700000000 * 1000));
  vi.stubGlobal("fetch", vi.fn());
  localStorage.clear();
  clearTokens();
  resetCoordinator();
  vi.mocked(refreshTokens).mockReset();
  setTokens({
    accessToken: "test-access",
    accessExpiresAt: 1700000000 + 900,
    refreshToken: "test-refresh",
  });
});

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  localStorage.clear();
  clearTokens();
  resetCoordinator();
});

function jsonOk(body: unknown): Response {
  return {
    ok: true,
    status: 200,
    json: () => Promise.resolve(body),
  } as Response;
}

function jsonErr(status: number, body: unknown): Response {
  return {
    ok: false,
    status,
    json: () => Promise.resolve(body),
  } as Response;
}

describe("apiClient", () => {
  describe("authorization header", () => {
    it("attaches Authorization: Bearer <access_token>", async () => {
      vi.mocked(fetch).mockResolvedValue(
        jsonOk(createSuccessResponse(mockMedications))
      );

      await apiClient.get("/medications");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/medications`,
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: "Bearer test-access",
          }),
        })
      );
    });

    it("does not send tma authorization scheme", async () => {
      vi.mocked(fetch).mockResolvedValue(
        jsonOk(createSuccessResponse(mockMedications))
      );

      await apiClient.get("/medications");

      const call = vi.mocked(fetch).mock.calls[0];
      const init = call[1] as RequestInit;
      const headers = init.headers as Record<string, string>;
      expect(headers.Authorization?.startsWith("tma ")).toBe(false);
    });
  });

  describe("content-type header", () => {
    it("sends application/json content-type", async () => {
      vi.mocked(fetch).mockResolvedValue(jsonOk(createSuccessResponse(null)));

      await apiClient.get("/test");

      expect(fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            "Content-Type": "application/json",
          }),
        })
      );
    });
  });

  describe("successful responses", () => {
    it("returns parsed json on success", async () => {
      const expected = createSuccessResponse(mockMedications);
      vi.mocked(fetch).mockResolvedValue(jsonOk(expected));

      const result = await apiClient.get("/medications");

      expect(result).toEqual(expected);
    });
  });

  describe("error responses", () => {
    it("returns error response with server error message", async () => {
      vi.mocked(fetch).mockResolvedValue(
        jsonErr(400, { error: "Validation failed" })
      );

      const result = await apiClient.get("/medications");

      expect(result).toEqual({
        success: false,
        data: null,
        error: "Validation failed",
      });
    });

    it("returns fallback error message when body is not json", async () => {
      vi.mocked(fetch).mockResolvedValue({
        ok: false,
        status: 500,
        json: () => Promise.reject(new Error("not json")),
      } as Response);

      const result = await apiClient.get("/test");

      expect(result).toEqual({
        success: false,
        data: null,
        error: "Request failed with status 500",
      });
    });

    it("non-401 errors are not retried", async () => {
      vi.mocked(fetch).mockResolvedValue(jsonErr(403, { error: "forbidden" }));

      await apiClient.get("/medications");

      expect(fetch).toHaveBeenCalledTimes(1);
      expect(refreshTokens).not.toHaveBeenCalled();
    });
  });

  describe("401 interceptor", () => {
    it("on 401 token_expired, refreshes and retries once", async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce(jsonErr(401, { error: "token_expired" }))
        .mockResolvedValueOnce(jsonOk(createSuccessResponse(mockMedications)));
      vi.mocked(refreshTokens).mockImplementation(async () => {
        const pair = {
          accessToken: "rotated-access",
          accessExpiresAt: 1700000000 + 1800,
          refreshToken: "rotated-rt",
        };
        setTokens(pair);
        return pair;
      });

      const result = await apiClient.get("/medications");

      expect(refreshTokens).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledTimes(2);
      const secondCall = vi.mocked(fetch).mock.calls[1];
      const init = secondCall[1] as RequestInit;
      const headers = init.headers as Record<string, string>;
      expect(headers.Authorization).toBe("Bearer rotated-access");
      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockMedications);
    });

    it("on 401 invalid_token, also refreshes and retries", async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce(jsonErr(401, { error: "invalid_token" }))
        .mockResolvedValueOnce(jsonOk(createSuccessResponse(null)));
      vi.mocked(refreshTokens).mockImplementation(async () => {
        const pair = {
          accessToken: "fresh-access",
          accessExpiresAt: 1700000000 + 1800,
          refreshToken: "fresh-rt",
        };
        setTokens(pair);
        return pair;
      });

      const result = await apiClient.get("/test");

      expect(refreshTokens).toHaveBeenCalledTimes(1);
      expect(result.success).toBe(true);
    });

    it("on second 401 after refresh, propagates error and clears tokens", async () => {
      vi.mocked(fetch)
        .mockResolvedValueOnce(jsonErr(401, { error: "token_expired" }))
        .mockResolvedValueOnce(jsonErr(401, { error: "token_expired" }));
      vi.mocked(refreshTokens).mockImplementation(async () => {
        const pair = {
          accessToken: "rotated-access",
          accessExpiresAt: 1700000000 + 1800,
          refreshToken: "rotated-rt",
        };
        setTokens(pair);
        return pair;
      });

      const result = await apiClient.get("/medications");

      expect(result.success).toBe(false);
      expect(result.error).toBe("token_expired");
      expect(getAccessToken()).toBeNull();
      expect(getRefreshToken()).toBeNull();
    });

    it("does not retry when 401 has unrelated error code", async () => {
      vi.mocked(fetch).mockResolvedValue(
        jsonErr(401, { error: "user_blocked" })
      );

      const result = await apiClient.get("/medications");

      expect(fetch).toHaveBeenCalledTimes(1);
      expect(refreshTokens).not.toHaveBeenCalled();
      expect(result.success).toBe(false);
      expect(result.error).toBe("user_blocked");
    });

    it("concurrent requests during refresh only trigger one refresh call", async () => {
      setTokens({
        accessToken: "expiring-access",
        accessExpiresAt: 1700000000 + 10,
        refreshToken: "rt-shared",
      });

      let resolveRefresh!: () => void;
      vi.mocked(refreshTokens).mockImplementation(
        () =>
          new Promise((resolve) => {
            resolveRefresh = () => {
              const pair = {
                accessToken: "shared-rotated",
                accessExpiresAt: 1700000000 + 1800,
                refreshToken: "shared-rotated-rt",
              };
              setTokens(pair);
              resolve(pair);
            };
          })
      );

      vi.mocked(fetch).mockResolvedValue(jsonOk(createSuccessResponse(null)));

      const p1 = apiClient.get("/a");
      const p2 = apiClient.get("/b");
      const p3 = apiClient.get("/c");

      await Promise.resolve();
      await Promise.resolve();

      expect(refreshTokens).toHaveBeenCalledTimes(1);

      resolveRefresh();

      await Promise.all([p1, p2, p3]);

      expect(refreshTokens).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledTimes(3);
      for (const call of vi.mocked(fetch).mock.calls) {
        const init = call[1] as RequestInit;
        const headers = init.headers as Record<string, string>;
        expect(headers.Authorization).toBe("Bearer shared-rotated");
      }
    });
  });

  describe("HTTP methods", () => {
    beforeEach(() => {
      vi.mocked(fetch).mockResolvedValue(jsonOk(createSuccessResponse(null)));
    });

    it("sends GET request", async () => {
      await apiClient.get("/medications");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/medications`,
        expect.objectContaining({ method: "GET" })
      );
    });

    it("sends POST request with body", async () => {
      const payload = { name: "Aspirin", schedule: "morning", time: "08:00" };
      await apiClient.post("/medications", payload);

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/medications`,
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify(payload),
        })
      );
    });

    it("sends POST request without body", async () => {
      await apiClient.post("/checklist/10/mark-taken");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/checklist/10/mark-taken`,
        expect.objectContaining({
          method: "POST",
          body: undefined,
        })
      );
    });

    it("sends PUT request with body", async () => {
      const payload = { name: "Updated Med" };
      await apiClient.put("/medications/1", payload);

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/medications/1`,
        expect.objectContaining({
          method: "PUT",
          body: JSON.stringify(payload),
        })
      );
    });

    it("sends PATCH request with body", async () => {
      const payload = { name: "Patched Med" };
      await apiClient.patch("/medications/1", payload);

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/medications/1`,
        expect.objectContaining({
          method: "PATCH",
          body: JSON.stringify(payload),
        })
      );
    });

    it("sends DELETE request", async () => {
      await apiClient.delete("/medications/1");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/medications/1`,
        expect.objectContaining({ method: "DELETE" })
      );
    });
  });

  describe("request URL construction", () => {
    it("prepends API_URL to the endpoint", async () => {
      vi.mocked(fetch).mockResolvedValue(jsonOk(createSuccessResponse(null)));

      await apiClient.get("/checklist/today");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/checklist/today`,
        expect.any(Object)
      );
    });
  });
});
