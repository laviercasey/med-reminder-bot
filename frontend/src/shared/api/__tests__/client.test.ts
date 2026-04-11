import { apiClient } from "../client";
import {
  createSuccessResponse,
  mockMedications,
} from "@/test/mocks/handlers";
import { API_URL } from "@/shared/config";

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn());
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe("apiClient", () => {
  describe("authorization header", () => {
    it("sends tma authorization header with initData", async () => {
      const mockResponse = createSuccessResponse(mockMedications);
      vi.mocked(fetch).mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      } as Response);

      await apiClient.get("/medications");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/medications`,
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: "tma test_init_data",
          }),
        })
      );
    });
  });

  describe("content-type header", () => {
    it("sends application/json content-type", async () => {
      vi.mocked(fetch).mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(createSuccessResponse(null)),
      } as Response);

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
      vi.mocked(fetch).mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(expected),
      } as Response);

      const result = await apiClient.get("/medications");

      expect(result).toEqual(expected);
    });
  });

  describe("error responses", () => {
    it("returns error response with server error message", async () => {
      vi.mocked(fetch).mockResolvedValue({
        ok: false,
        status: 400,
        json: () => Promise.resolve({ error: "Validation failed" }),
      } as Response);

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
  });

  describe("HTTP methods", () => {
    beforeEach(() => {
      vi.mocked(fetch).mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(createSuccessResponse(null)),
      } as Response);
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
      vi.mocked(fetch).mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(createSuccessResponse(null)),
      } as Response);

      await apiClient.get("/checklist/today");

      expect(fetch).toHaveBeenCalledWith(
        `${API_URL}/checklist/today`,
        expect.any(Object)
      );
    });
  });
});
