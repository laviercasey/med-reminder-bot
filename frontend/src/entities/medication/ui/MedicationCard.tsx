import { useTranslation } from "react-i18next";
import { Sunrise, Sun, Moon, Clock, Pencil, Trash2, type LucideIcon } from "lucide-react";
import type { Medication } from "../model/types";

interface MedicationCardProps {
  medication: Medication;
  after?: React.ReactNode;
  onEdit?: () => void;
  onDelete?: () => void;
  onClick?: () => void;
}

const SCHEDULE_ICONS: Record<string, LucideIcon> = {
  morning: Sunrise,
  day: Sun,
  evening: Moon,
  custom: Clock,
};

const SCHEDULE_COLORS: Record<string, { icon: string; bg: string }> = {
  morning: { icon: "#D97706", bg: "#FEF3C7" },
  day: { icon: "#EA580C", bg: "#FFEDD5" },
  evening: { icon: "#7C3AED", bg: "#EDE9FE" },
  custom: { icon: "#059669", bg: "#ECFDF5" },
};

export function MedicationCard({ medication, after, onEdit, onDelete }: MedicationCardProps) {
  const { t } = useTranslation();

  const scheduleLabel = t(`medications.${medication.schedule}`);
  const Icon = SCHEDULE_ICONS[medication.schedule] ?? Clock;
  const colors = SCHEDULE_COLORS[medication.schedule] ?? SCHEDULE_COLORS.custom;

  return (
    <div
      className="flex items-center rounded-2xl bg-white"
      style={{ gap: 12, padding: "0 16px", height: 80, boxShadow: "0 1px 8px rgba(0,0,0,0.03)" }}
    >
      <div
        className="flex-shrink-0 w-12 h-12 rounded-[14px] flex items-center justify-center"
        style={{ backgroundColor: colors.bg }}
      >
        <Icon size={24} strokeWidth={1.8} color={colors.icon} />
      </div>

      <div className="flex-1 min-w-0">
        <p className="text-[16px] font-semibold leading-snug truncate" style={{ color: "#1C1917" }}>
          {medication.name}
        </p>
        <p className="text-[12px] mt-0.5" style={{ color: "#A8A29E" }}>
          {scheduleLabel} &middot; {medication.time}
        </p>
      </div>

      {after && (
        <div className="flex-shrink-0 flex items-center gap-3" onClick={(e) => e.stopPropagation()}>
          {after}
        </div>
      )}

      {!after && (onEdit || onDelete) && (
        <div className="flex-shrink-0 flex items-center gap-3">
          {onEdit && (
            <button onClick={onEdit} className="cursor-pointer p-1">
              <Pencil size={20} color="#A8A29E" strokeWidth={1.8} />
            </button>
          )}
          {onDelete && (
            <button onClick={onDelete} className="cursor-pointer p-1">
              <Trash2 size={20} color="#D6D3D1" strokeWidth={1.8} />
            </button>
          )}
        </div>
      )}
    </div>
  );
}
