import { retrieveRawInitData } from "@telegram-apps/sdk-react";
import {
  getRefreshToken,
  getAccessExpiresAt,
  clearTokens,
  subscribe,
} from "./token-store";
import { loginWithInitData, refreshTokens, AuthApiError } from "./api";

const PREEMPTIVE_LEEWAY_SECONDS = 60;

export type BootstrapStatus = "idle" | "ready" | "auth_expired";

export interface BootstrapState {
  status: BootstrapStatus;
  error: string | null;
}

let state: BootstrapState = { status: "idle", error: null };
let preemptiveTimer: ReturnType<typeof setTimeout> | null = null;
let unsubscribeStore: (() => void) | null = null;

function getInitDataSafe(): string {
  try {
    return retrieveRawInitData() ?? "";
  } catch {
    return "";
  }
}

export function getBootstrapState(): BootstrapState {
  return state;
}

export function cancelPreemptiveRefresh(): void {
  if (preemptiveTimer !== null) {
    clearTimeout(preemptiveTimer);
    preemptiveTimer = null;
  }
}

function schedulePreemptive(): void {
  cancelPreemptiveRefresh();
  const expiresAt = getAccessExpiresAt();
  if (expiresAt === null) {
    return;
  }
  const nowSec = Math.floor(Date.now() / 1000);
  const delaySec = expiresAt - nowSec - PREEMPTIVE_LEEWAY_SECONDS;
  const delayMs = Math.max(delaySec, 0) * 1000;
  preemptiveTimer = setTimeout(() => {
    void runPreemptiveRefresh();
  }, delayMs);
}

async function runPreemptiveRefresh(): Promise<void> {
  const rt = getRefreshToken();
  if (!rt) {
    return;
  }
  try {
    await refreshTokens(rt);
  } catch {
    clearTokens();
  }
}

function attachStoreSubscription(): void {
  if (unsubscribeStore !== null) {
    return;
  }
  unsubscribeStore = subscribe(() => {
    if (state.status !== "ready") {
      return;
    }
    schedulePreemptive();
  });
}

function setReady(): void {
  state = { status: "ready", error: null };
  attachStoreSubscription();
  schedulePreemptive();
}

function setAuthExpired(error: string): void {
  cancelPreemptiveRefresh();
  state = { status: "auth_expired", error };
}

async function tryRefreshFlow(): Promise<boolean> {
  const stored = getRefreshToken();
  if (!stored) {
    return false;
  }
  try {
    await refreshTokens(stored);
    return true;
  } catch {
    clearTokens();
    return false;
  }
}

async function tryLoginFlow(): Promise<boolean> {
  const initData = getInitDataSafe();
  if (!initData) {
    setAuthExpired("missing_init_data");
    return false;
  }
  try {
    await loginWithInitData(initData);
    return true;
  } catch (error) {
    const code =
      error instanceof AuthApiError ? error.error : "login_failed";
    setAuthExpired(code);
    return false;
  }
}

export async function bootstrapAuth(): Promise<void> {
  cancelPreemptiveRefresh();
  state = { status: "idle", error: null };

  const refreshed = await tryRefreshFlow();
  if (refreshed) {
    setReady();
    return;
  }

  const loggedIn = await tryLoginFlow();
  if (loggedIn) {
    setReady();
  }
}

export function resetBootstrap(): void {
  cancelPreemptiveRefresh();
  if (unsubscribeStore !== null) {
    unsubscribeStore();
    unsubscribeStore = null;
  }
  state = { status: "idle", error: null };
}
