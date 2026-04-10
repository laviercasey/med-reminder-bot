import { useMemo } from "react";
import { useTranslation } from "react-i18next";
import { useNavigate, useLocation } from "react-router-dom";
import { ClipboardCheck, Pill, Settings, ShieldCheck, type LucideIcon } from "lucide-react";
import { useUserStore } from "@/entities/user";

interface NavItem {
  path: string;
  labelKey: string;
  icon: LucideIcon;
}

const BASE_ITEMS: NavItem[] = [
  { path: "/", labelKey: "nav.checklist", icon: ClipboardCheck },
  { path: "/medications", labelKey: "nav.medications", icon: Pill },
  { path: "/settings", labelKey: "nav.settings", icon: Settings },
];

const ADMIN_ITEM: NavItem = { path: "/admin", labelKey: "nav.admin", icon: ShieldCheck };

export function BottomNav() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const isAdmin = useUserStore((s) => s.isAdmin);

  const navItems = useMemo(
    () => (isAdmin ? [...BASE_ITEMS, ADMIN_ITEM] : BASE_ITEMS),
    [isAdmin]
  );

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-50 bg-white"
      style={{
        boxShadow: "0 -2px 12px rgba(0,0,0,0.04)",
        padding: "8px 16px calc(20px + env(safe-area-inset-bottom)) 16px",
      }}
    >
      <div className="flex items-center justify-around">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          const Icon = item.icon;

          return (
            <button
              key={item.path}
              onClick={() => navigate(item.path)}
              className="flex-1 flex flex-col items-center justify-center gap-[3px] h-[46px] cursor-pointer"
              aria-label={t(item.labelKey)}
              aria-current={isActive ? "page" : undefined}
            >
              <Icon
                size={22}
                strokeWidth={isActive ? 2.2 : 1.8}
                color={isActive ? "#059669" : "#A8A29E"}
              />
              <span
                className="text-[9px] uppercase leading-none"
                style={{
                  color: isActive ? "#059669" : "#A8A29E",
                  fontWeight: isActive ? 600 : 500,
                  letterSpacing: "0.5px",
                }}
              >
                {t(item.labelKey)}
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
