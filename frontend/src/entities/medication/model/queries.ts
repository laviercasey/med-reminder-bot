import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/shared/api";
import type { Medication } from "./types";
import { QUERY_STALE_TIME } from "@/shared/config";

export const medicationKeys = {
  all: ["medications"] as const,
  list: () => [...medicationKeys.all, "list"] as const,
  detail: (id: number) => [...medicationKeys.all, "detail", id] as const,
};

interface MedicationListResponse {
  medications: Medication[];
  count: number;
}

export function useMedications() {
  return useQuery({
    queryKey: medicationKeys.list(),
    queryFn: async () => {
      const response = await apiClient.get<MedicationListResponse>("/medications");
      if (!response.success || !response.data) {
        throw new Error(response.error ?? "Failed to fetch medications");
      }
      return response.data.medications;
    },
    staleTime: QUERY_STALE_TIME,
  });
}

export function useMedication(id: number) {
  return useQuery({
    queryKey: medicationKeys.detail(id),
    queryFn: async () => {
      const response = await apiClient.get<Medication>(`/medications/${id}`);
      if (!response.success || !response.data) {
        throw new Error(response.error ?? "Failed to fetch medication");
      }
      return response.data;
    },
    staleTime: QUERY_STALE_TIME,
    enabled: id > 0,
  });
}
