import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Bell, BellOff, Timer, Check, Pencil, X } from "lucide-react";
import { BottomSheet } from "@/shared/ui";
import { LanguageSelector } from "@/features/change-language";
import { useUserSettings, userKeys } from "@/entities/user";
import type { UserSettings } from "@/entities/user";
import { apiClient } from "@/shared/api";
import { Spinner } from "@/shared/ui";
import { hapticFeedback } from "@/shared/lib";

const REPEAT_OPTIONS = [5, 15, 30];

function CustomIntervalModal({ isOpen, currentValue, onClose, onSave }: {
  isOpen: boolean;
  currentValue: number;
  onClose: () => void;
  onSave: (minutes: number) => void;
}) {
  const { t } = useTranslation();
  const [value, setValue] = useState(String(currentValue || 10));

  useEffect(() => {
    if (isOpen) {
      setValue(String(currentValue || 10));
    }
  }, [isOpen, currentValue]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace" || e.key === "Delete" || e.key === "Tab") return;
    if (e.key === "Enter") { e.preventDefault(); return; }
    if (!/^\d$/.test(e.key)) { e.preventDefault(); return; }
    e.preventDefault();
    setValue((prev) => {
      const next = (prev.slice(-1) + e.key).slice(-2);
      const n = parseInt(next, 10);
      if (n > 60) return e.key;
      if (n < 1) return "1";
      return String(n);
    });
  }, []);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = e.target.value.replace(/\D/g, "");
    if (raw === "") { setValue("1"); return; }
    const n = Math.min(parseInt(raw, 10), 60);
    setValue(String(Math.max(n, 1)));
  }, []);

  const handleSave = useCallback(() => {
    const n = parseInt(value, 10);
    if (!isNaN(n) && n >= 1 && n <= 60) {
      onSave(n);
      onClose();
    }
  }, [value, onSave, onClose]);

  return (
    <BottomSheet isOpen={isOpen} onClose={onClose}>
      <div style={{ padding: "8px 20px calc(32px + env(safe-area-inset-bottom)) 20px" }}>
        <div className="flex items-center justify-between" style={{ height: 48 }}>
          <h2 className="text-[18px] font-bold" style={{ color: "#1C1917" }}>
            {t("settings.custom_interval")}
          </h2>
          <button onClick={onClose} className="cursor-pointer p-1">
            <X size={20} color="#A8A29E" strokeWidth={2} />
          </button>
        </div>

        <div className="flex flex-col items-center" style={{ gap: 16, paddingTop: 16 }}>
          <p className="text-[13px]" style={{ color: "#A8A29E" }}>
            {t("settings.custom_interval_hint")}
          </p>

          <div
            className="rounded-2xl flex items-center justify-center"
            style={{
              width: 120,
              height: 72,
              backgroundColor: "#ECFDF5",
              boxShadow: "0 0 0 2px #059669",
            }}
          >
            <input
              type="text"
              inputMode="numeric"
              pattern="[0-9]*"
              value={value}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              onKeyUp={(e) => e.key === "Enter" && handleSave()}
              autoFocus
              className="text-[32px] font-bold text-center bg-transparent outline-none"
              style={{ color: "#059669", width: 60, caretColor: "transparent" }}
              maxLength={2}
            />
          </div>

          <p className="text-[12px]" style={{ color: "#A8A29E" }}>
            1 — 60 {t("settings.minutes")}
          </p>

          <button
            onClick={handleSave}
            disabled={!value || parseInt(value, 10) < 1}
            className="w-full flex items-center justify-center cursor-pointer transition-all duration-150 active:scale-[0.98] disabled:opacity-35 disabled:cursor-not-allowed"
            style={{ height: 48, borderRadius: 14, backgroundColor: "#059669", gap: 8 }}
          >
            <Check size={18} color="#FFFFFF" strokeWidth={2.5} />
            <span className="text-[15px] font-semibold text-white">{t("common.save")}</span>
          </button>
        </div>
      </div>
    </BottomSheet>
  );
}

export function SettingsPage() {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const { data: settings, isLoading } = useUserSettings();
  const [customModalOpen, setCustomModalOpen] = useState(false);
  const [lastCustom, setLastCustom] = useState<number | null>(null);

  useEffect(() => {
    if (settings?.reminder_repeat_minutes && !REPEAT_OPTIONS.includes(settings.reminder_repeat_minutes)) {
      setLastCustom(settings.reminder_repeat_minutes);
    }
  }, [settings?.reminder_repeat_minutes]);

  const updateSettings = useMutation({
    mutationFn: async (payload: Partial<UserSettings>) => {
      const response = await apiClient.patch<UserSettings>("/settings", payload);
      if (!response.success || !response.data) {
        throw new Error(response.error ?? "Failed to update settings");
      }
      return response.data;
    },
    onMutate: async (payload) => {
      await queryClient.cancelQueries({ queryKey: userKeys.settings() });
      const previous = queryClient.getQueryData<UserSettings>(userKeys.settings());

      queryClient.setQueryData<UserSettings>(
        userKeys.settings(),
        (old) => (old ? { ...old, ...payload } : old)
      );

      hapticFeedback("selection_change");
      return { previous };
    },
    onError: (_err, _payload, context) => {
      if (context?.previous) {
        queryClient.setQueryData(userKeys.settings(), context.previous);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: userKeys.settings() });
    },
  });

  const handleToggleReminders = useCallback(() => {
    if (!settings) return;
    updateSettings.mutate({
      reminders_enabled: !settings.reminders_enabled,
    });
  }, [settings, updateSettings]);

  const handleRepeatChange = useCallback(
    (minutes: number) => {
      updateSettings.mutate({ reminder_repeat_minutes: minutes });
    },
    [updateSettings]
  );

  if (isLoading) {
    return <Spinner />;
  }

  return (
    <div className="min-h-full" style={{ paddingBottom: "calc(74px + 16px + env(safe-area-inset-bottom))" }}>
      <header
        className="rounded-b-[28px] flex flex-col justify-center gap-1"
        style={{
          background: "linear-gradient(160deg, #059669 0%, #0D9488 100%)",
          height: 140,
          padding: "52px 20px 24px 20px",
        }}
      >
        <h1 className="text-[26px] font-bold text-white leading-tight">
          {t("settings.settings")}
        </h1>
      </header>

      <div className="flex flex-col gap-3" style={{ padding: "16px 16px 0 16px" }}>
        <LanguageSelector />

        <div
          className="rounded-2xl overflow-hidden"
          style={{ backgroundColor: "#FFFFFF", boxShadow: "0 1px 8px rgba(0,0,0,0.03)" }}
        >
          <div className="flex items-center" style={{ height: 40, padding: "0 16px", backgroundColor: "#F5F5F4" }}>
            <span
              className="text-[11px] font-semibold uppercase"
              style={{ color: "#A8A29E", letterSpacing: "1px" }}
            >
              {t("settings.reminders_settings")}
            </span>
          </div>

          <button
            onClick={handleToggleReminders}
            role="switch"
            aria-checked={settings?.reminders_enabled ?? false}
            className="flex items-center w-full cursor-pointer"
            style={{ gap: 12, padding: "0 16px", height: 56 }}
          >
            <div
              className="flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center"
              style={{
                backgroundColor: settings?.reminders_enabled ? "#ECFDF5" : "#F5F5F4",
              }}
            >
              {settings?.reminders_enabled
                ? <Bell size={20} strokeWidth={1.8} color="#059669" />
                : <BellOff size={20} strokeWidth={1.8} color="#A8A29E" />
              }
            </div>
            <span className="flex-1 text-left text-[15px] font-medium" style={{ color: "#1C1917" }}>
              {settings?.reminders_enabled
                ? t("settings.reminders_enabled")
                : t("settings.reminders_disabled")}
            </span>
            <div
              className="w-[46px] h-[28px] rounded-full relative flex-shrink-0 transition-colors duration-200"
              style={{ backgroundColor: settings?.reminders_enabled ? "#059669" : "#E7E5E4" }}
            >
              <div
                className="absolute top-[3px] w-[22px] h-[22px] rounded-full bg-white transition-transform duration-200"
                style={{
                  transform: settings?.reminders_enabled ? "translateX(21px)" : "translateX(3px)",
                  boxShadow: "0 1px 4px rgba(0,0,0,0.13)",
                }}
              />
            </div>
          </button>
        </div>

        {settings?.reminders_enabled && (
          <div
            className="rounded-2xl overflow-hidden animate-fade-in"
            style={{ backgroundColor: "#FFFFFF", boxShadow: "0 1px 8px rgba(0,0,0,0.03)" }}
          >
            <div className="flex items-center" style={{ height: 40, padding: "0 16px", backgroundColor: "#F5F5F4" }}>
              <span
                className="text-[11px] font-semibold uppercase"
                style={{ color: "#A8A29E", letterSpacing: "1px" }}
              >
                {t("settings.select_repeat_interval")}
              </span>
            </div>
            {REPEAT_OPTIONS.map((minutes, idx) => {
              const isSelected = settings?.reminder_repeat_minutes === minutes;
              return (
                <div key={minutes}>
                  {idx > 0 && <div style={{ height: 1, backgroundColor: "#F5F5F4" }} />}
                  <button
                    onClick={() => handleRepeatChange(minutes)}
                    className="flex items-center w-full cursor-pointer"
                    style={{ gap: 12, padding: "0 16px", height: 48 }}
                  >
                    <div
                      className="flex-shrink-0 w-9 h-9 rounded-[10px] flex items-center justify-center"
                      style={{
                        backgroundColor: isSelected ? "#ECFDF5" : "#F5F5F4",
                      }}
                    >
                      <Timer size={18} strokeWidth={1.8} color={isSelected ? "#059669" : "#A8A29E"} />
                    </div>
                    <span
                      className="flex-1 text-left text-[15px]"
                      style={{
                        color: isSelected ? "#1C1917" : "#57534E",
                        fontWeight: isSelected ? 600 : 400,
                      }}
                    >
                      {minutes} {t("settings.minutes")}
                    </span>
                    {isSelected && <Check size={18} color="#059669" strokeWidth={2.5} />}
                  </button>
                </div>
              );
            })}
            <div style={{ height: 1, backgroundColor: "#F5F5F4" }} />
            {(() => {
              const isCustomSelected = !REPEAT_OPTIONS.includes(settings?.reminder_repeat_minutes ?? 5);
              const hasCustom = lastCustom !== null;
              return (
                <div
                  className="flex items-center w-full"
                  style={{ padding: "0 16px", height: 48 }}
                >
                  <button
                    onClick={() => {
                      if (hasCustom) {
                        handleRepeatChange(lastCustom);
                      } else {
                        setCustomModalOpen(true);
                      }
                    }}
                    className="flex items-center flex-1 h-full cursor-pointer min-w-0"
                    style={{ gap: 12 }}
                  >
                    <div
                      className="flex-shrink-0 w-9 h-9 rounded-[10px] flex items-center justify-center"
                      style={{ backgroundColor: isCustomSelected ? "#ECFDF5" : "#F5F5F4" }}
                    >
                      <Timer size={18} strokeWidth={1.8} color={isCustomSelected ? "#059669" : "#A8A29E"} />
                    </div>
                    <span
                      className="flex-1 text-left text-[15px] truncate"
                      style={{
                        color: isCustomSelected ? "#1C1917" : "#57534E",
                        fontWeight: isCustomSelected ? 600 : 400,
                      }}
                    >
                      {hasCustom
                        ? `${lastCustom} ${t("settings.minutes")}`
                        : "Custom..."}
                    </span>
                  </button>
                  {isCustomSelected && <Check size={18} color="#059669" strokeWidth={2.5} style={{ flexShrink: 0 }} />}
                  {hasCustom && (
                    <button
                      onClick={() => setCustomModalOpen(true)}
                      className="cursor-pointer p-1 flex-shrink-0"
                      style={{ marginLeft: 8 }}
                    >
                      <Pencil size={14} color="#A8A29E" strokeWidth={1.8} />
                    </button>
                  )}
                  {!hasCustom && <span className="text-[11px] flex-shrink-0" style={{ color: "#A8A29E" }}>1-60</span>}
                </div>
              );
            })()}
          </div>
        )}

      </div>

      <CustomIntervalModal
        isOpen={customModalOpen}
        currentValue={lastCustom ?? 10}
        onClose={() => setCustomModalOpen(false)}
        onSave={(minutes) => {
          setLastCustom(minutes);
          handleRepeatChange(minutes);
        }}
      />
    </div>
  );
}
