import { useState, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { Plus } from "lucide-react";
import { useMedications } from "@/entities/medication";
import type { Medication } from "@/entities/medication";
import { MedicationList } from "@/widgets/medication-list";
import { AddMedicationForm } from "@/features/add-medication";
import { EditMedicationModal } from "@/features/edit-medication";
import { DeleteConfirmModal } from "./DeleteConfirmModal";

export function MedicationsPage() {
  const { t } = useTranslation();
  const { data: medications } = useMedications();

  const [addOpen, setAddOpen] = useState(false);
  const [editTarget, setEditTarget] = useState<Medication | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Medication | null>(null);

  const activeCount = medications?.length ?? 0;

  const handleEdit = useCallback((medication: Medication) => {
    setEditTarget(medication);
  }, []);

  const handleDelete = useCallback((medication: Medication) => {
    setDeleteTarget(medication);
  }, []);

  const handleEditClose = useCallback(() => {
    setEditTarget(null);
  }, []);

  const handleDeleteFromEdit = useCallback(() => {
    if (editTarget) {
      setDeleteTarget(editTarget);
      setEditTarget(null);
    }
  }, [editTarget]);

  return (
    <div className="flex flex-col min-h-full" style={{ paddingBottom: "calc(74px + 68px + env(safe-area-inset-bottom))" }}>
      <div
        className="rounded-b-[28px] flex flex-col justify-center gap-1 flex-shrink-0"
        style={{
          background: "linear-gradient(160deg, #059669 0%, #0D9488 100%)",
          height: 160,
          padding: "52px 20px 24px 20px",
        }}
      >
        <h1 className="text-white text-[26px] font-bold leading-tight">
          {t("medications.my_medications")}
        </h1>
        <p className="text-[#D1FAE5] text-[13px] font-medium">
          {t("medications.active_count", { count: activeCount })}
        </p>
      </div>

      <div className="flex-1" style={{ padding: "16px 16px 0 16px" }}>
        <MedicationList onEdit={handleEdit} onDelete={handleDelete} />
      </div>

      <div
        className="fixed left-0 right-0 z-40"
        style={{ bottom: "calc(74px + env(safe-area-inset-bottom))", padding: "0 16px 12px 16px" }}
      >
        <button
          onClick={() => setAddOpen(true)}
          className="w-full h-[52px] rounded-2xl text-[15px] font-semibold text-white cursor-pointer transition-all duration-150 active:scale-[0.98] flex items-center justify-center gap-2"
          style={{
            backgroundColor: "#059669",
            boxShadow: "0 4px 16px rgba(5,150,105,0.2)",
          }}
        >
          <Plus size={20} strokeWidth={2.5} />
          {t("medications.add_medication")}
        </button>
      </div>

      <AddMedicationForm
        key={addOpen ? "open" : "closed"}
        isOpen={addOpen}
        onClose={() => setAddOpen(false)}
      />

      {editTarget && (
        <EditMedicationModal
          key={editTarget.id}
          medication={editTarget}
          isOpen={!!editTarget}
          onClose={handleEditClose}
          onDelete={handleDeleteFromEdit}
        />
      )}

      {deleteTarget && (
        <DeleteConfirmModal
          medication={deleteTarget}
          isOpen={!!deleteTarget}
          onClose={() => setDeleteTarget(null)}
        />
      )}
    </div>
  );
}
