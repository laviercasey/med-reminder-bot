import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import { ChecklistGroup } from "@/widgets/checklist-group";

function formatHeaderDate(locale: string): string {
  const now = new Date();
  return now.toLocaleDateString(locale === "ru" ? "ru-RU" : "en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });
}

export function ChecklistPage() {
  const { t, i18n } = useTranslation();
  const dateStr = useMemo(() => formatHeaderDate(i18n.language), [i18n.language]);

  return (
    <div className="min-h-full" style={{ paddingBottom: "calc(74px + 16px + env(safe-area-inset-bottom))" }}>
      <div
        className="rounded-b-[28px] flex flex-col justify-center gap-1"
        style={{
          background: "linear-gradient(160deg, #059669 0%, #0D9488 100%)",
          height: 180,
          padding: "52px 20px 24px 20px",
        }}
      >
        <p className="text-[#A7F3D0] text-[11px] font-semibold tracking-[1.5px] uppercase">
          MedReminder
        </p>
        <h1 className="text-white text-[26px] font-bold leading-tight">
          {t("checklist.today_checklist")}
        </h1>
        <p className="text-[#D1FAE5] text-[13px] font-medium">{dateStr}</p>
      </div>
      <div style={{ padding: "16px 16px 0 16px" }}>
        <ChecklistGroup />
      </div>
    </div>
  );
}
