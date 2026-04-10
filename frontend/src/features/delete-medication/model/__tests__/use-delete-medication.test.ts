import { renderHook, waitFor, act } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createElement } from "react";
import { useDeleteMedication } from "../use-delete-medication";
import { apiClient } from "@/shared/api";
import { medicationKeys } from "@/entities/medication";
import { checklistKeys } from "@/entities/checklist";
import type { Medication } from "@/entities/medication";
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

vi.mock("@/shared/lib", () => ({
  hapticFeedback: vi.fn(),
}));

function createTestEnv(initialMedications?: Medication[]) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: Infinity },
      mutations: { retry: false },
    },
  });

  if (initialMedications) {
    queryClient.setQueryData(medicationKeys.list(), initialMedications);
  }

  const wrapper = ({ children }: { children: React.ReactNode }) =>
    createElement(QueryClientProvider, { client: queryClient }, children);

  return { queryClient, wrapper };
}

describe("useDeleteMedication", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("calls DELETE to /medications/:id", async () => {
    vi.mocked(apiClient.delete).mockResolvedValue(
      createSuccessResponse(null)
    );

    const { wrapper } = createTestEnv(mockMedications);
    const { result } = renderHook(() => useDeleteMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(1);
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(apiClient.delete).toHaveBeenCalledWith("/medications/1");
  });

  it("optimistically removes medication from cached list", async () => {
    let resolveDelete: (value: unknown) => void;
    const deletePromise = new Promise((resolve) => {
      resolveDelete = resolve;
    });
    vi.mocked(apiClient.delete).mockReturnValue(deletePromise as ReturnType<typeof apiClient.delete>);

    const { queryClient, wrapper } = createTestEnv(mockMedications);
    const { result } = renderHook(() => useDeleteMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(1);
    });

    await waitFor(() => {
      const cached = queryClient.getQueryData<Medication[]>(
        medicationKeys.list()
      );
      expect(cached).toHaveLength(1);
      expect(cached?.[0].id).toBe(2);
    });

    resolveDelete!(createSuccessResponse(null));
  });

  it("reverts optimistic update on error", async () => {
    vi.mocked(apiClient.delete).mockResolvedValue(
      createErrorResponse("Cannot delete")
    );

    const { queryClient, wrapper } = createTestEnv(mockMedications);
    const { result } = renderHook(() => useDeleteMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(1);
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    await waitFor(() => {
      const cached = queryClient.getQueryData<Medication[]>(
        medicationKeys.list()
      );
      expect(cached).toHaveLength(2);
      expect(cached?.find((m) => m.id === 1)).toBeDefined();
    });
  });

  it("invalidates medications list on settle", async () => {
    vi.mocked(apiClient.delete).mockResolvedValue(
      createSuccessResponse(null)
    );

    const { queryClient, wrapper } = createTestEnv(mockMedications);
    const invalidateSpy = vi.spyOn(queryClient, "invalidateQueries");
    const { result } = renderHook(() => useDeleteMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(1);
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(invalidateSpy).toHaveBeenCalledWith(
      expect.objectContaining({ queryKey: medicationKeys.list() })
    );
  });

  it("invalidates today checklist on settle", async () => {
    vi.mocked(apiClient.delete).mockResolvedValue(
      createSuccessResponse(null)
    );

    const { queryClient, wrapper } = createTestEnv(mockMedications);
    const invalidateSpy = vi.spyOn(queryClient, "invalidateQueries");
    const { result } = renderHook(() => useDeleteMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(1);
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(invalidateSpy).toHaveBeenCalledWith(
      expect.objectContaining({ queryKey: checklistKeys.today() })
    );
  });

  it("returns the deleted medication id", async () => {
    vi.mocked(apiClient.delete).mockResolvedValue(
      createSuccessResponse(null)
    );

    const { wrapper } = createTestEnv(mockMedications);
    const { result } = renderHook(() => useDeleteMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(2);
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toBe(2);
  });

  it("throws when delete response is not successful", async () => {
    vi.mocked(apiClient.delete).mockResolvedValue(
      createErrorResponse("Forbidden")
    );

    const { wrapper } = createTestEnv(mockMedications);
    const { result } = renderHook(() => useDeleteMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(1);
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error?.message).toBe("Forbidden");
  });
});
