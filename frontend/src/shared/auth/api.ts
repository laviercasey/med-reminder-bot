import { API_URL } from "@/shared/config";
import type { ApiResponse } from "@/shared/api/types";
import { setTokens, type TokenPair } from "./token-store";

interface ServerTokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  expires_at: number;
  refresh_expires_at: number;
}

export class AuthApiError extends Error {
  status: number;
  error: string;

  constructor(status: number, error: string) {
    super(error);
    this.name = "AuthApiError";
    this.status = status;
    this.error = error;
  }
}

function toTokenPair(server: ServerTokenPair): TokenPair {
  return {
    accessToken: server.access_token,
    accessExpiresAt: server.expires_at,
    refreshToken: server.refresh_token,
  };
}

async function parseEnvelope<T>(
  response: Response
): Promise<ApiResponse<T>> {
  try {
    const body = (await response.json()) as ApiResponse<T>;
    return body;
  } catch {
    return {
      success: false,
      data: null,
      error: `Request failed with status ${response.status}`,
    };
  }
}

async function postJson(path: string, body: unknown, accessToken?: string): Promise<Response> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }
  return fetch(`${API_URL}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
}

export async function loginWithInitData(initData: string): Promise<TokenPair> {
  const response = await postJson("/auth/login", { init_data: initData });
  const envelope = await parseEnvelope<ServerTokenPair>(response);

  if (!response.ok || !envelope.success || !envelope.data) {
    throw new AuthApiError(response.status, envelope.error ?? "login_failed");
  }

  const pair = toTokenPair(envelope.data);
  setTokens(pair);
  return pair;
}

export async function refreshTokens(refreshToken: string): Promise<TokenPair> {
  const response = await postJson("/auth/refresh", { refresh_token: refreshToken });
  const envelope = await parseEnvelope<ServerTokenPair>(response);

  if (!response.ok || !envelope.success || !envelope.data) {
    throw new AuthApiError(response.status, envelope.error ?? "refresh_failed");
  }

  const pair = toTokenPair(envelope.data);
  setTokens(pair);
  return pair;
}

export async function logoutServer(
  refreshToken: string,
  accessToken: string
): Promise<void> {
  try {
    await postJson("/auth/logout", { refresh_token: refreshToken }, accessToken);
  } catch {
    void 0;
  }
}
