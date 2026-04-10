import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/api";
import { medicationKeys } from "@/entities/medication";
import type { Medication, UpdateMedicationPayload } from "@/entities/medication";
import { checklistKeys } from "@/entities/checklist";
import { hapticFeedback } from "@/shared/lib";

interface EditMedicationVariables {
  id: number;
  payload: UpdateMedicationPayload;
}

export function useEditMedication() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, payload }: EditMedicationVariables) => {
      const response = await apiClient.put<Medication>(
        `/medications/${id}`,
        payload
      );
      if (!response.success || !response.data) {
        throw new Error(response.error ?? "Failed to update medication");
      }
      return response.data;
    },
    onSuccess: (updated) => {
      queryClient.setQueryData<Medication[]>(medicationKeys.list(), (old) =>
        old
          ? old.map((m) => (m.id === updated.id ? updated : m))
          : [updated]
      );
      queryClient.invalidateQueries({ queryKey: checklistKeys.today() });
      hapticFeedback("notification", "success");
    },
    onError: () => {
      hapticFeedback("notification", "error");
    },
  });
}
