import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createElement } from "react";
import { medicationKeys, useMedications, useMedication } from "../queries";
import { apiClient } from "@/shared/api";
import type { Medication } from "../types";
import {
  createSuccessResponse,
  createErrorResponse,
  mockMedications,
} from "@/test/mocks/handlers";

vi.mock("@/shared/api", () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}));

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
      },
    },
  });

  return function Wrapper({ children }: { children: React.ReactNode }) {
    return createElement(QueryClientProvider, { client: queryClient }, children);
  };
}

describe("medicationKeys", () => {
  it("generates base key", () => {
    expect(medicationKeys.all).toEqual(["medications"]);
  });

  it("generates list key extending base", () => {
    expect(medicationKeys.list()).toEqual(["medications", "list"]);
  });

  it("generates detail key with id", () => {
    expect(medicationKeys.detail(42)).toEqual(["medications", "detail", 42]);
  });
});

describe("useMedications", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("fetches medications from /medications endpoint", async () => {
    vi.mocked(apiClient.get).mockResolvedValue(
      createSuccessResponse(mockMedications)
    );

    const { result } = renderHook(() => useMedications(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(apiClient.get).toHaveBeenCalledWith("/medications");
    expect(result.current.data).toEqual(mockMedications);
  });

  it("throws when response is not successful", async () => {
    vi.mocked(apiClient.get).mockResolvedValue(
      createErrorResponse("Server error")
    );

    const { result } = renderHook(() => useMedications(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error?.message).toBe("Server error");
  });

  it("throws fallback message when error is null", async () => {
    vi.mocked(apiClient.get).mockResolvedValue({
      success: false,
      data: null,
      error: null,
    });

    const { result } = renderHook(() => useMedications(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error?.message).toBe("Failed to fetch medications");
  });
});

describe("useMedication", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("fetches a single medication by id", async () => {
    const med: Medication = mockMedications[0];
    vi.mocked(apiClient.get).mockResolvedValue(createSuccessResponse(med));

    const { result } = renderHook(() => useMedication(1), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(apiClient.get).toHaveBeenCalledWith("/medications/1");
    expect(result.current.data).toEqual(med);
  });

  it("does not fetch when id is 0", () => {
    const { result } = renderHook(() => useMedication(0), {
      wrapper: createWrapper(),
    });

    expect(result.current.fetchStatus).toBe("idle");
    expect(apiClient.get).not.toHaveBeenCalled();
  });

  it("throws when single medication response fails", async () => {
    vi.mocked(apiClient.get).mockResolvedValue(
      createErrorResponse("Not found")
    );

    const { result } = renderHook(() => useMedication(999), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error?.message).toBe("Not found");
  });
});
