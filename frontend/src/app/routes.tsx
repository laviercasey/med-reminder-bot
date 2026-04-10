import { Routes, Route, Navigate } from "react-router-dom";
import { ChecklistPage } from "@/pages/checklist";
import { MedicationsPage } from "@/pages/medications";
import { SettingsPage } from "@/pages/settings";
import { AdminPage } from "@/pages/admin";
import { useUserStore } from "@/entities/user";

function AdminGuard({ children }: { children: React.ReactNode }) {
  const isAdmin = useUserStore((s) => s.isAdmin);
  if (!isAdmin) {
    return <Navigate to="/" replace />;
  }
  return <>{children}</>;
}

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<ChecklistPage />} />
      <Route path="/medications" element={<MedicationsPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route
        path="/admin"
        element={
          <AdminGuard>
            <AdminPage />
          </AdminGuard>
        }
      />
    </Routes>
  );
}
