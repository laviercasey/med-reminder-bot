import { renderHook, waitFor, act } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createElement } from "react";
import { useAddMedication } from "../use-add-medication";
import { apiClient } from "@/shared/api";
import { medicationKeys } from "@/entities/medication";
import { checklistKeys } from "@/entities/checklist";
import type { Medication, CreateMedicationPayload } from "@/entities/medication";
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

describe("useAddMedication", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  const newMedPayload: CreateMedicationPayload = {
    name: "Ibuprofen",
    schedule: "day",
    time: "14:00",
  };

  const newMedResponse: Medication = {
    id: 3,
    user_id: 123456789,
    name: "Ibuprofen",
    schedule: "day",
    time: "14:00",
    created_at: "2026-04-07T14:00:00Z",
  };

  it("calls POST to /medications with payload", async () => {
    vi.mocked(apiClient.post).mockResolvedValue(
      createSuccessResponse(newMedResponse)
    );

    const { wrapper } = createTestEnv();
    const { result } = renderHook(() => useAddMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(newMedPayload);
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(apiClient.post).toHaveBeenCalledWith("/medications", newMedPayload);
  });

  it("appends new medication to cached list on success", async () => {
    vi.mocked(apiClient.post).mockResolvedValue(
      createSuccessResponse(newMedResponse)
    );

    const { queryClient, wrapper } = createTestEnv(mockMedications);
    const { result } = renderHook(() => useAddMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(newMedPayload);
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    const cached = queryClient.getQueryData<Medication[]>(
      medicationKeys.list()
    );
    expect(cached).toHaveLength(3);
    expect(cached?.[2]).toEqual(newMedResponse);
  });

  it("creates list with new medication when cache is empty", async () => {
    vi.mocked(apiClient.post).mockResolvedValue(
      createSuccessResponse(newMedResponse)
    );

    const { queryClient, wrapper } = createTestEnv();
    queryClient.setQueryData(medicationKeys.list(), undefined);
    const { result } = renderHook(() => useAddMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(newMedPayload);
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    const cached = queryClient.getQueryData<Medication[]>(
      medicationKeys.list()
    );
    expect(cached).toEqual([newMedResponse]);
  });

  it("invalidates today checklist on success", async () => {
    vi.mocked(apiClient.post).mockResolvedValue(
      createSuccessResponse(newMedResponse)
    );

    const { queryClient, wrapper } = createTestEnv();
    const invalidateSpy = vi.spyOn(queryClient, "invalidateQueries");
    const { result } = renderHook(() => useAddMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(newMedPayload);
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(invalidateSpy).toHaveBeenCalledWith(
      expect.objectContaining({ queryKey: checklistKeys.today() })
    );
  });

  it("throws when response is not successful", async () => {
    vi.mocked(apiClient.post).mockResolvedValue(
      createErrorResponse("Limit reached")
    );

    const { wrapper } = createTestEnv();
    const { result } = renderHook(() => useAddMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(newMedPayload);
    });

    await waitFor(() => expect(result.current.isError).toBe(true));

    expect(result.current.error?.message).toBe("Limit reached");
  });

  it("returns the created medication as mutation data", async () => {
    vi.mocked(apiClient.post).mockResolvedValue(
      createSuccessResponse(newMedResponse)
    );

    const { wrapper } = createTestEnv();
    const { result } = renderHook(() => useAddMedication(), { wrapper });

    await act(async () => {
      result.current.mutate(newMedPayload);
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual(newMedResponse);
  });
});
