import { useCallback } from "react";
import { Trash2, Loader2 } from "lucide-react";
import { useTranslation } from "react-i18next";
import { BottomSheet } from "@/shared/ui";
import { useDeleteMedication } from "../model/use-delete-medication";

interface DeleteMedicationButtonProps {
  medicationId: number;
  medicationName: string;
  isOpen: boolean;
  onOpen: () => void;
  onClose: () => void;
}

export function DeleteMedicationButton({
  medicationId,
  medicationName,
  isOpen,
  onOpen,
  onClose,
}: DeleteMedicationButtonProps) {
  const { t } = useTranslation();
  const { mutate, isPending } = useDeleteMedication();

  const handleDelete = useCallback(() => {
    mutate(medicationId, {
      onSuccess: () => {
        onClose();
      },
    });
  }, [medicationId, mutate, onClose]);

  return (
    <>
      <button
        onClick={(e) => {
          e.stopPropagation();
          onOpen();
        }}
        className="p-2 rounded-xl text-text-hint hover:text-danger hover:bg-danger-soft transition-colors duration-150 cursor-pointer min-w-[44px] min-h-[44px] flex items-center justify-center"
        aria-label={t("medications.delete_medication")}
      >
        <Trash2 size={18} strokeWidth={1.8} />
      </button>

      <BottomSheet isOpen={isOpen} onClose={onClose}>
        <div className="px-5 pb-[calc(20px+env(safe-area-inset-bottom))]">
          <div className="flex flex-col items-center mb-5 pt-2">
            <div className="w-12 h-12 rounded-full bg-danger-soft flex items-center justify-center mb-3">
              <Trash2 size={22} className="text-danger" strokeWidth={1.8} />
            </div>
            <h2 className="text-[17px] text-text text-center font-bold leading-snug">
              {t("medications.confirm_delete", { name: medicationName })}
            </h2>
            <p className="text-sm text-text-secondary text-center mt-1.5">
              {t("medications.delete_description")}
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="flex-1 py-3 rounded-xl text-[15px] font-semibold text-text border border-border cursor-pointer transition-colors duration-150 active:bg-surface-muted"
            >
              {t("common.cancel")}
            </button>
            <button
              onClick={handleDelete}
              disabled={isPending}
              className="flex-1 py-3 rounded-xl text-[15px] font-semibold text-white bg-danger cursor-pointer transition-all duration-150 active:scale-[0.98] disabled:opacity-40 flex items-center justify-center gap-1.5"
            >
              {isPending && <Loader2 size={16} className="animate-spin" />}
              {t("common.confirm")}
            </button>
          </div>
        </div>
      </BottomSheet>
    </>
  );
}
