import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/api";
import { medicationKeys } from "@/entities/medication";
import type { Medication } from "@/entities/medication";
import { checklistKeys } from "@/entities/checklist";
import { hapticFeedback } from "@/shared/lib";

export function useDeleteMedication() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (medicationId: number) => {
      const response = await apiClient.delete<void>(`/medications/${medicationId}`);
      if (!response.success) {
        throw new Error(response.error ?? "Failed to delete medication");
      }
      return medicationId;
    },
    onMutate: async (medicationId) => {
      await queryClient.cancelQueries({ queryKey: medicationKeys.list() });

      const previous = queryClient.getQueryData<Medication[]>(
        medicationKeys.list()
      );

      queryClient.setQueryData<Medication[]>(
        medicationKeys.list(),
        (old) => old?.filter((m) => m.id !== medicationId)
      );

      hapticFeedback("impact", "medium");

      return { previous };
    },
    onError: (_err, _id, context) => {
      if (context?.previous) {
        queryClient.setQueryData(medicationKeys.list(), context.previous);
      }
      hapticFeedback("notification", "error");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: medicationKeys.list() });
      queryClient.invalidateQueries({ queryKey: checklistKeys.today() });
    },
  });
}
