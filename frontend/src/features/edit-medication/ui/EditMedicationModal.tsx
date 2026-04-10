import { useState, useCallback } from "react";
import { useTranslation } from "react-i18next";
import {
  Sunrise,
  Sun,
  Moon,
  Clock,
  Check,
  Loader2,
  X,
  Trash2,
  Pencil,
  type LucideIcon,
} from "lucide-react";
import type { Medication, MedicationSchedule } from "@/entities/medication";
import { EditTimeModal } from "@/features/edit-time";
import { BottomSheet } from "@/shared/ui";
import { useEditMedication } from "../model/use-edit-medication";

interface EditMedicationModalProps {
  medication: Medication;
  isOpen: boolean;
  onClose: () => void;
  onDelete: () => void;
}

const SCHEDULES: MedicationSchedule[] = ["morning", "day", "evening", "custom"];

const DEFAULT_TIMES: Record<MedicationSchedule, string> = {
  morning: "08:00",
  day: "13:00",
  evening: "20:00",
  custom: "12:00",
};

const SCHEDULE_ICONS: Record<MedicationSchedule, LucideIcon> = {
  morning: Sunrise,
  day: Sun,
  evening: Moon,
  custom: Clock,
};

export function EditMedicationModal({
  medication,
  isOpen,
  onClose,
  onDelete,
}: EditMedicationModalProps) {
  const { t } = useTranslation();
  const { mutate, isPending } = useEditMedication();

  const [name, setName] = useState(medication.name);
  const [schedule, setSchedule] = useState<MedicationSchedule>(medication.schedule);
  const [times, setTimes] = useState<Record<MedicationSchedule, string>>({
    ...DEFAULT_TIMES,
    [medication.schedule]: medication.time,
  });
  const [editingTimeFor, setEditingTimeFor] = useState<MedicationSchedule | null>(null);

  const handleScheduleChange = useCallback((newSchedule: MedicationSchedule) => {
    setSchedule(newSchedule);
  }, []);

  const handleTimeSave = useCallback((newTime: string) => {
    if (editingTimeFor) {
      setTimes((prev) => ({ ...prev, [editingTimeFor]: newTime }));
    }
    setEditingTimeFor(null);
  }, [editingTimeFor]);

  const handleSubmit = useCallback(() => {
    if (!name.trim()) return;
    mutate(
      { id: medication.id, payload: { name: name.trim(), schedule, time: times[schedule] } },
      { onSuccess: onClose }
    );
  }, [name, schedule, times, medication.id, mutate, onClose]);

  const isValid = name.trim().length > 0 && name.trim().length <= 100;

  return (
    <>
      <BottomSheet isOpen={isOpen && !editingTimeFor} onClose={onClose}>
        <div style={{ padding: "8px 20px calc(24px + env(safe-area-inset-bottom)) 20px" }}>
          <div className="flex items-center justify-between h-12 mb-2">
            <h2 className="text-[18px] font-bold" style={{ color: "#1C1917" }}>
              {t("medications.edit_medication")}
            </h2>
            <button onClick={onClose} className="cursor-pointer p-1">
              <X size={20} color="#A8A29E" strokeWidth={2} />
            </button>
          </div>

          <div className="flex flex-col gap-4">
            <div>
              <p
                className="text-[11px] font-semibold uppercase"
                style={{ color: "#A8A29E", letterSpacing: "1px", marginBottom: 8 }}
              >
                {t("medications.medication_name_prompt")}
              </p>
              <div
                className="flex items-center rounded-xl"
                style={{ backgroundColor: "#F5F5F4", padding: "0 14px", height: 48 }}
              >
                <input
                  id="edit-med-name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  maxLength={100}
                  className="w-full text-[15px] bg-transparent outline-none"
                  style={{ color: "#1C1917" }}
                />
              </div>
            </div>

            <div>
              <p
                className="text-[11px] font-semibold uppercase"
                style={{ color: "#A8A29E", letterSpacing: "1px", marginBottom: 8 }}
              >
                {t("medications.select_schedule")}
              </p>
              <div className="rounded-xl overflow-hidden" style={{ backgroundColor: "#F5F5F4" }}>
                {SCHEDULES.map((s, idx) => {
                  const isSelected = schedule === s;
                  const Icon = SCHEDULE_ICONS[s];
                  return (
                    <div key={s}>
                      {idx > 0 && <div style={{ height: 1, backgroundColor: "#E7E5E4" }} />}
                      <div className="flex items-center w-full" style={{ height: 48, padding: "0 14px" }}>
                        <button
                          onClick={() => handleScheduleChange(s)}
                          className="flex items-center gap-2 flex-1 h-full cursor-pointer min-w-0"
                        >
                          <Icon
                            size={16}
                            strokeWidth={1.8}
                            color={isSelected ? "#059669" : "#A8A29E"}
                          />
                          <span
                            className="text-[15px] truncate"
                            style={{
                              color: isSelected ? "#1C1917" : "#57534E",
                              fontWeight: isSelected ? 600 : 400,
                            }}
                          >
                            {t(`medications.${s}`)} &middot; {times[s]}
                          </span>
                        </button>
                        <div className="flex items-center gap-2 flex-shrink-0">
                          {isSelected && (
                            <div
                              className="w-5 h-5 rounded-full"
                              style={{ backgroundColor: "#059669" }}
                            />
                          )}
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setEditingTimeFor(s);
                            }}
                            className="cursor-pointer p-1"
                          >
                            <Pencil size={14} color="#A8A29E" strokeWidth={1.8} />
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <button
              disabled={!isValid || isPending}
              onClick={handleSubmit}
              className="w-full h-12 rounded-[14px] text-[15px] font-semibold text-white cursor-pointer transition-all duration-150 active:scale-[0.98] disabled:opacity-35 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              style={{ backgroundColor: "#059669" }}
            >
              {isPending ? (
                <Loader2 size={18} className="animate-spin" />
              ) : (
                <Check size={18} strokeWidth={2.5} />
              )}
              {t("medications.save_changes")}
            </button>

            <button
              onClick={onDelete}
              className="w-full h-10 text-[13px] font-medium cursor-pointer flex items-center justify-center gap-1.5"
              style={{ color: "#E11D48" }}
            >
              <Trash2 size={15} color="#E11D48" strokeWidth={1.8} />
              {t("medications.delete_medication")}
            </button>
          </div>
        </div>
      </BottomSheet>

      {editingTimeFor && (
        <EditTimeModal
          key={editingTimeFor}
          isOpen={!!editingTimeFor}
          onClose={() => setEditingTimeFor(null)}
          scheduleLabel={t(`medications.${editingTimeFor}`)}
          defaultTime={DEFAULT_TIMES[editingTimeFor]}
          currentTime={times[editingTimeFor]}
          onSave={handleTimeSave}
        />
      )}
    </>
  );
}
