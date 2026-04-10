import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/shared/api";
import type { ChecklistResponse } from "./types";
import { QUERY_STALE_TIME } from "@/shared/config";

export const checklistKeys = {
  all: ["checklist"] as const,
  today: () => [...checklistKeys.all, "today"] as const,
  byDate: (date: string) => [...checklistKeys.all, "date", date] as const,
};

export function useTodayChecklist() {
  return useQuery({
    queryKey: checklistKeys.today(),
    queryFn: async () => {
      const response = await apiClient.get<ChecklistResponse>("/checklist");
      if (!response.success || !response.data) {
        throw new Error(response.error ?? "Failed to fetch checklist");
      }
      return response.data;
    },
    staleTime: QUERY_STALE_TIME,
  });
}
