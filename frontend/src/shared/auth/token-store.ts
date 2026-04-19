export const REFRESH_TOKEN_STORAGE_KEY = "mr.rt";

export interface TokenPair {
  accessToken: string;
  accessExpiresAt: number;
  refreshToken: string;
}

interface TokenState {
  accessToken: string | null;
  accessExpiresAt: number | null;
  refreshToken: string | null;
}

type Listener = () => void;

const state: TokenState = {
  accessToken: null,
  accessExpiresAt: null,
  refreshToken: null,
};

const listeners = new Set<Listener>();

function emit(): void {
  for (const listener of Array.from(listeners)) {
    listener();
  }
}

function readRefreshFromStorage(): string | null {
  try {
    return localStorage.getItem(REFRESH_TOKEN_STORAGE_KEY);
  } catch {
    return null;
  }
}

function writeRefreshToStorage(value: string | null): void {
  try {
    if (value === null) {
      localStorage.removeItem(REFRESH_TOKEN_STORAGE_KEY);
      return;
    }
    localStorage.setItem(REFRESH_TOKEN_STORAGE_KEY, value);
  } catch {
    void 0;
  }
}

export function setTokens(pair: TokenPair): void {
  state.accessToken = pair.accessToken;
  state.accessExpiresAt = pair.accessExpiresAt;
  state.refreshToken = pair.refreshToken;
  writeRefreshToStorage(pair.refreshToken);
  emit();
}

export function getAccessToken(): string | null {
  return state.accessToken;
}

export function getAccessExpiresAt(): number | null {
  return state.accessExpiresAt;
}

export function getRefreshToken(): string | null {
  if (state.refreshToken !== null) {
    return state.refreshToken;
  }
  const stored = readRefreshFromStorage();
  if (stored !== null) {
    state.refreshToken = stored;
  }
  return stored;
}

export function clearTokens(): void {
  state.accessToken = null;
  state.accessExpiresAt = null;
  state.refreshToken = null;
  writeRefreshToStorage(null);
  emit();
}

export function subscribe(listener: Listener): () => void {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}
