import {
  getAccessToken,
  getAccessExpiresAt,
  getRefreshToken,
  clearTokens,
} from "./token-store";
import { refreshTokens } from "./api";

const REFRESH_LEEWAY_SECONDS = 60;

let inFlight: Promise<string> | null = null;

function nowSeconds(): number {
  return Math.floor(Date.now() / 1000);
}

function isAccessFresh(): boolean {
  const token = getAccessToken();
  const expiresAt = getAccessExpiresAt();
  if (!token || expiresAt === null) {
    return false;
  }
  return expiresAt - nowSeconds() > REFRESH_LEEWAY_SECONDS;
}

async function doRefresh(): Promise<string> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    clearTokens();
    throw new Error("missing_refresh_token");
  }
  try {
    const pair = await refreshTokens(refreshToken);
    return pair.accessToken;
  } catch (error) {
    clearTokens();
    throw error;
  }
}

export async function ensureFreshAccessToken(): Promise<string> {
  if (isAccessFresh()) {
    const token = getAccessToken();
    if (token) {
      return token;
    }
  }
  if (inFlight) {
    return inFlight;
  }
  inFlight = doRefresh().finally(() => {
    inFlight = null;
  });
  return inFlight;
}

export async function forceRefresh(): Promise<string> {
  if (inFlight) {
    return inFlight;
  }
  inFlight = doRefresh().finally(() => {
    inFlight = null;
  });
  return inFlight;
}

export function resetCoordinator(): void {
  inFlight = null;
}
