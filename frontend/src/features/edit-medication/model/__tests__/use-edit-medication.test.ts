import { renderHook, waitFor, act } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createElement } from "react";
import { useEditMedication } from "../use-edit-medication";
import { apiClient } from "@/shared/api";
import {
  createSuccessResponse,
  createErrorResponse,
} from "@/test/mocks/handlers";
import type { Medication } from "@/entities/medication";

vi.mock("@/shared/api", () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

vi.mock("@/shared/lib", () => ({
  hapticFeedback: vi.fn(),
}));

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false, gcTime: 0 } },
  });
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return createElement(QueryClientProvider, { client: queryClient }, children);
  };
}

const mockMedication: Medication = {
  id: 1,
  user_id: 123456789,
  name: "Updated Aspirin",
  schedule: "morning",
  time: "09:00",
  created_at: "2026-01-01T00:00:00Z",
};

describe("useEditMedication", () => {
  afterEach(() => vi.clearAllMocks());

  it("updates medication via PUT", async () => {
    vi.mocked(apiClient.put).mockResolvedValue(
      createSuccessResponse(mockMedication)
    );

    const { result } = renderHook(() => useEditMedication(), {
      wrapper: createWrapper(),
    });

    await act(async () => {
      result.current.mutate({
        id: 1,
        payload: { name: "Updated Aspirin", schedule: "morning", time: "09:00" },
      });
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(apiClient.put).toHaveBeenCalledWith("/medications/1", {
      name: "Updated Aspirin",
      schedule: "morning",
      time: "09:00",
    });
    expect(result.current.data).toEqual(mockMedication);
  });

  it("throws when response is not successful", async () => {
    vi.mocked(apiClient.put).mockResolvedValue(
      createErrorResponse("Not found")
    );

    const { result } = renderHook(() => useEditMedication(), {
      wrapper: createWrapper(),
    });

    await act(async () => {
      result.current.mutate({
        id: 999,
        payload: { name: "Invalid", schedule: "morning", time: "08:00" },
      });
    });

    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error?.message).toBe("Not found");
  });
});
