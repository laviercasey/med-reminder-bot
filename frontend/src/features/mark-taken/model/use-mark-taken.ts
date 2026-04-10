import { useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/shared/api";
import { checklistKeys } from "@/entities/checklist";
import type { ChecklistResponse } from "@/entities/checklist";
import { hapticFeedback } from "@/shared/lib";

export function useMarkTaken() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      checklistId,
      status,
    }: {
      checklistId: number;
      status: boolean;
    }) => {
      const response = await apiClient.patch<null>(
        `/checklist/${checklistId}`,
        { status }
      );
      if (!response.success) {
        throw new Error(response.error ?? "Failed to update status");
      }
    },
    onMutate: async ({ checklistId, status }) => {
      await queryClient.cancelQueries({ queryKey: checklistKeys.today() });

      const previous = queryClient.getQueryData<ChecklistResponse>(
        checklistKeys.today()
      );

      queryClient.setQueryData<ChecklistResponse>(
        checklistKeys.today(),
        (old) => {
          if (!old) return old;
          const items = old.items.map((entry) =>
            entry.id === checklistId
              ? { ...entry, status, updated_at: new Date().toISOString() }
              : entry
          );
          const taken = items.filter((i) => i.status).length;
          return { ...old, items, taken };
        }
      );

      hapticFeedback("notification", "success");

      return { previous };
    },
    onError: (_err, _vars, context) => {
      if (context?.previous) {
        queryClient.setQueryData(checklistKeys.today(), context.previous);
      }
      hapticFeedback("notification", "error");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: checklistKeys.today() });
    },
  });
}
