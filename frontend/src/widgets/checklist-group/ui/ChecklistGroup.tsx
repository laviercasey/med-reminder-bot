import { useTranslation } from "react-i18next";
import { PartyPopper, AlertCircle, ClipboardList } from "lucide-react";
import { ChecklistItem, useTodayChecklist } from "@/entities/checklist";
import { MarkTakenButton } from "@/features/mark-taken";
import { Spinner } from "@/shared/ui";

export function ChecklistGroup() {
  const { t } = useTranslation();
  const { data: entries, isLoading, isError } = useTodayChecklist();

  if (isLoading) return <Spinner />;

  if (isError) {
    return (
      <div className="flex flex-col items-center gap-4 py-16 text-center">
        <div className="w-16 h-16 rounded-full bg-danger-soft flex items-center justify-center">
          <AlertCircle size={32} className="text-danger" strokeWidth={1.5} />
        </div>
        <p className="text-text-secondary text-sm">{t("common.error")}</p>
      </div>
    );
  }

  const items = entries?.items ?? [];

  if (items.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 text-center" style={{ minHeight: "calc(100vh - 180px - 74px - 32px)" }}>
        <div className="w-20 h-20 rounded-3xl bg-white flex items-center justify-center" style={{ boxShadow: "0 1px 8px rgba(0,0,0,0.03)" }}>
          <ClipboardList size={36} color="#A8A29E" strokeWidth={1.5} />
        </div>
        <div>
          <p className="text-[15px] font-semibold mb-1" style={{ color: "#1C1917" }}>{t("checklist.no_medications_today")}</p>
          <p className="text-[13px]" style={{ color: "#A8A29E" }}>{t("checklist.no_medications_today")}</p>
        </div>
      </div>
    );
  }

  const takenCount = items.filter((e) => e.status).length;
  const allTaken = takenCount === items.length;
  const pct = Math.round((takenCount / items.length) * 100);

  return (
    <div className="flex flex-col" style={{ gap: 12 }}>
      <div
        className="bg-white rounded-[20px] flex items-center"
        style={{ padding: "16px 20px", gap: 16, boxShadow: "0 2px 12px rgba(0,0,0,0.04)" }}
      >
        <div style={{ position: "relative", width: 56, height: 56, flexShrink: 0 }}>
          <svg viewBox="0 0 36 36" style={{ width: 56, height: 56, transform: "rotate(-90deg)" }}>
            <circle cx="18" cy="18" r="15" fill="none" stroke="#E5E7EB" strokeWidth="4" />
            <circle
              cx="18" cy="18" r="15" fill="none"
              stroke="#059669"
              strokeWidth="4"
              strokeLinecap="round"
              strokeDasharray={`${pct * 0.942} 100`}
            />
          </svg>
          <span
            className="absolute inset-0 flex items-center justify-center text-[13px] font-bold"
            style={{ color: "#1C1917" }}
          >
            {pct}%
          </span>
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-[16px] font-bold" style={{ color: "#1C1917" }}>
            {t("checklist.progress_count", { taken: takenCount, total: items.length })}
          </p>
          <p className="text-[13px]" style={{ color: "#A8A29E", marginTop: 2 }}>
            {allTaken
              ? t("checklist.all_taken_congrats")
              : t("checklist.keep_going")}
          </p>
        </div>
        {allTaken && <PartyPopper size={24} color="#16A34A" style={{ flexShrink: 0, marginLeft: -8 }} />}
      </div>

      {items.map((entry) => (
        <ChecklistItem
          key={entry.id}
          entry={entry}
          after={
            <MarkTakenButton checklistId={entry.id} isTaken={entry.status} />
          }
        />
      ))}
    </div>
  );
}
