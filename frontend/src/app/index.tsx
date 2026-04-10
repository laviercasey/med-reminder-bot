import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { TelegramProvider, QueryProvider, AppRouterProvider } from "./providers";
import { AppRoutes } from "./routes";
import { BottomNav } from "@/widgets/navigation";
import { ErrorBoundary } from "@/shared/ui";
import { useConsent, PrivacyConsentScreen } from "@/features/privacy-consent";
import { useCurrentUser, useUserStore } from "@/entities/user";
import "./styles/global.css";

function ProfileLoader() {
  const { data: profile } = useCurrentUser();
  const setIsAdmin = useUserStore((s) => s.setIsAdmin);
  const setLanguage = useUserStore((s) => s.setLanguage);
  const { i18n } = useTranslation();

  useEffect(() => {
    if (!profile) return;
    setIsAdmin(profile.is_admin === true);
    if (profile.language && profile.language !== i18n.language) {
      setLanguage(profile.language);
      i18n.changeLanguage(profile.language);
    }
  }, [profile, setIsAdmin, setLanguage, i18n]);

  return null;
}

function AppContent() {
  const { accepted, accept } = useConsent();

  if (!accepted) {
    return <PrivacyConsentScreen onAccept={accept} />;
  }

  return (
    <>
      <ProfileLoader />
      <AppRoutes />
      <BottomNav />
    </>
  );
}

export function App() {
  return (
    <ErrorBoundary>
      <QueryProvider>
        <AppRouterProvider>
          <TelegramProvider>
            <AppContent />
          </TelegramProvider>
        </AppRouterProvider>
      </QueryProvider>
    </ErrorBoundary>
  );
}
