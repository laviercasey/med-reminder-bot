import { renderHook, waitFor, act } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createElement } from "react";
import { useMarkTaken } from "../use-mark-taken";
import { apiClient } from "@/shared/api";
import { checklistKeys } from "@/entities/checklist";
import type { ChecklistResponse } from "@/entities/checklist";
import {
  createSuccessResponse,
  createErrorResponse,
  mockChecklistEntries,
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

vi.mock("@/shared/lib", () => ({
  hapticFeedback: vi.fn(),
}));

const mockChecklistResponse: ChecklistResponse = {
  items: mockChecklistEntries,
  date: "2026-04-07",
  total: 2,
  taken: 1,
};

function createTestEnv(initialChecklist?: ChecklistResponse) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: Infinity },
      mutations: { retry: false },
    },
  });

  if (initialChecklist) {
    queryClient.setQueryData(checklistKeys.today(), initialChecklist);
  }

  const wrapper = ({ children }: { children: React.ReactNode }) =>
    createElement(QueryClientProvider, { client: queryClient }, children);

  return { queryClient, wrapper };
}

describe("useMarkTaken", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("calls PATCH to /checklist/:id with status", async () => {
    vi.mocked(apiClient.patch).mockResolvedValue(
      createSuccessResponse(null)
    );

    const { wrapper } = createTestEnv(mockChecklistResponse);
    const { result } = renderHook(() => useMarkTaken(), { wrapper });

    await act(async () => {
      result.current.mutate({ checklistId: 10, status: true });
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(apiClient.patch).toHaveBeenCalledWith("/checklist/10", { status: true });
  });

  it("optimistically updates checklist entry status to true", async () => {
    let resolvePatch: (value: unknown) => void;
    const patchPromise = new Promise((resolve) => {
      resolvePatch = resolve;
    });
    vi.mocked(apiClient.patch).mockReturnValue(patchPromise as ReturnType<typeof apiClient.patch>);

    const { queryClient, wrapper } = createTestEnv(mockChecklistResponse);
    const { result } = renderHook(() => useMarkTaken(), { wrapper });

    await act(async () => {
      result.current.mutate({ checklistId: 10, status: true });
    });

    await waitFor(() => {
      const cached = queryClient.getQueryData<ChecklistResponse>(
        checklistKeys.today()
      );
      expect(cached?.items.find((e) => e.id === 10)?.status).toBe(true);
    });

    resolvePatch!(createSuccessResponse(null));
  });

  it("reverts optimistic update on error", async () => {
    vi.mocked(apiClient.patch).mockResolvedValue(
      createErrorResponse("Server error")
    );

    const { queryClient, wrapper } = createTestEnv(mockChecklistResponse);
    const { result } = renderHook(() => useMarkTaken(), { wrapper });

    await act(async () => {
      result.current.mutate({ checklistId: 10, status: true });
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    await waitFor(() => {
      const cached = queryClient.getQueryData<ChecklistResponse>(
        checklistKeys.today()
      );
      expect(cached?.items.find((e) => e.id === 10)?.status).toBe(false);
    });
  });

  it("invalidates today checklist on settle", async () => {
    vi.mocked(apiClient.patch).mockResolvedValue(
      createSuccessResponse(null)
    );

    const { queryClient, wrapper } = createTestEnv(mockChecklistResponse);
    const invalidateSpy = vi.spyOn(queryClient, "invalidateQueries");
    const { result } = renderHook(() => useMarkTaken(), { wrapper });

    await act(async () => {
      result.current.mutate({ checklistId: 10, status: true });
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(invalidateSpy).toHaveBeenCalledWith(
      expect.objectContaining({ queryKey: checklistKeys.today() })
    );
  });

  it("preserves other entries during optimistic update", async () => {
    vi.mocked(apiClient.patch).mockResolvedValue(
      createSuccessResponse(null)
    );

    const { queryClient, wrapper } = createTestEnv(mockChecklistResponse);
    const { result } = renderHook(() => useMarkTaken(), { wrapper });

    await act(async () => {
      result.current.mutate({ checklistId: 10, status: true });
    });

    await waitFor(() => {
      const cached = queryClient.getQueryData<ChecklistResponse>(
        checklistKeys.today()
      );
      const untouched = cached?.items.find((e) => e.id === 11);
      expect(untouched?.status).toBe(true);
      expect(untouched?.medication_name).toBe("Vitamin D");
    });
  });
});
