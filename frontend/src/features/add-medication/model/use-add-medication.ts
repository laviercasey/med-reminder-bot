import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/api";
import { medicationKeys } from "@/entities/medication";
import type { Medication, CreateMedicationPayload } from "@/entities/medication";
import { checklistKeys } from "@/entities/checklist";
import { hapticFeedback } from "@/shared/lib";

export function useAddMedication() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: CreateMedicationPayload) => {
      const response = await apiClient.post<Medication>("/medications", payload);
      if (!response.success || !response.data) {
        throw new Error(response.error ?? "Failed to add medication");
      }
      return response.data;
    },
    onSuccess: (newMedication) => {
      queryClient.setQueryData<Medication[]>(
        medicationKeys.list(),
        (old) => (old ? [...old, newMedication] : [newMedication])
      );
      queryClient.invalidateQueries({ queryKey: checklistKeys.today() });
      hapticFeedback("notification", "success");
    },
    onError: () => {
      hapticFeedback("notification", "error");
    },
  });
}
