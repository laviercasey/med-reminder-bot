import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./app";
import { AuthErrorScreen } from "./app/providers/auth-error";
import { bootstrapAuth, getBootstrapState } from "./shared/auth/bootstrap";
import "./app/providers/i18n";

async function start(): Promise<void> {
  const root = document.getElementById("root");
  if (!root) {
    return;
  }

  await bootstrapAuth();

  const state = getBootstrapState();

  if (state.status === "auth_expired") {
    createRoot(root).render(
      <StrictMode>
        <AuthErrorScreen />
      </StrictMode>
    );
    return;
  }

  createRoot(root).render(
    <StrictMode>
      <App />
    </StrictMode>
  );
}

void start();
