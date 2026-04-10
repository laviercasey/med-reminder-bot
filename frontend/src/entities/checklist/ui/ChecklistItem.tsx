import { useTranslation } from "react-i18next";
import { Sunrise, Sun, Moon, Clock, type LucideIcon } from "lucide-react";
import type { ChecklistEntry } from "../model/types";

interface ChecklistItemProps {
  entry: ChecklistEntry;
  after?: React.ReactNode;
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

export function ChecklistItem({ entry, after }: ChecklistItemProps) {
  const { t } = useTranslation();

  const Icon = SCHEDULE_ICONS[entry.schedule] ?? Clock;
  const colors = SCHEDULE_COLORS[entry.schedule] ?? SCHEDULE_COLORS.custom;

  return (
    <div
      className="rounded-2xl bg-white flex items-center"
      style={{ gap: 12, padding: "0 16px", height: 72, boxShadow: "0 1px 8px rgba(0,0,0,0.03)" }}
    >
      <div
        className="flex-shrink-0 w-11 h-11 rounded-[14px] flex items-center justify-center"
        style={{ backgroundColor: colors.bg }}
      >
        <Icon size={22} color={colors.icon} strokeWidth={1.8} />
      </div>

      <div className="flex-1 min-w-0">
        <p className="text-[15px] font-semibold leading-snug truncate" style={{ color: "#1C1917" }}>
          {entry.medication_name}
        </p>
        <p className="text-[12px]" style={{ color: "#A8A29E", marginTop: 2 }}>
          {entry.medication_time} &middot; {t(`medications.${entry.schedule}`)}
        </p>
      </div>

      {after && <div className="flex-shrink-0">{after}</div>}
    </div>
  );
}
