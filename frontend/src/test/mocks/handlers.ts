import type { ApiResponse } from "@/shared/api/types";
import type { Medication } from "@/entities/medication/model/types";
import type { ChecklistEntry } from "@/entities/checklist/model/types";

export const mockMedications: Medication[] = [
  {
    id: 1,
    user_id: 123456789,
    name: "Aspirin",
    schedule: "morning",
    time: "08:00",
    created_at: "2026-01-01T00:00:00Z",
  },
  {
    id: 2,
    user_id: 123456789,
    name: "Vitamin D",
    schedule: "evening",
    time: "20:00",
    created_at: "2026-01-02T00:00:00Z",
  },
];

export const mockChecklistEntries: ChecklistEntry[] = [
  {
    id: 10,
    date: "2026-04-07",
    medication_id: 1,
    status: false,
    updated_at: "2026-04-07T00:00:00Z",
    medication_name: "Aspirin",
    medication_time: "08:00",
    schedule: "morning",
  },
  {
    id: 11,
    date: "2026-04-07",
    medication_id: 2,
    status: true,
    updated_at: "2026-04-07T12:00:00Z",
    medication_name: "Vitamin D",
    medication_time: "20:00",
    schedule: "evening",
  },
];

export function createSuccessResponse<T>(data: T): ApiResponse<T> {
  return { success: true, data, error: null };
}

export function createErrorResponse(error: string): ApiResponse<null> {
  return { success: false, data: null, error };
}
