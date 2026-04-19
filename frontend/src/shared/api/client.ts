import { API_URL } from "@/shared/config";
import {
  ensureFreshAccessToken,
  forceRefresh,
} from "@/shared/auth/refresh-coordinator";
import { clearTokens } from "@/shared/auth/token-store";
import type { ApiResponse } from "./types";

const REFRESHABLE_ERRORS = new Set(["token_expired", "invalid_token"]);

interface ParsedResponse<T> {
  ok: boolean;
  status: number;
  body: ApiResponse<T> | { error?: string } | null;
  parseFailed: boolean;
}

async function parseResponse<T>(response: Response): Promise<ParsedResponse<T>> {
  let body: ApiResponse<T> | { error?: string } | null = null;
  let parseFailed = false;
  try {
    body = (await response.json()) as ApiResponse<T> | { error?: string };
  } catch {
    parseFailed = true;
  }
  return { ok: response.ok, status: response.status, body, parseFailed };
}

function toEnvelope<T>(parsed: ParsedResponse<T>): ApiResponse<T> {
  if (!parsed.ok) {
    if (parsed.parseFailed || parsed.body === null) {
      return {
        success: false,
        data: null,
        error: `Request failed with status ${parsed.status}`,
      };
    }
    const errorField = (parsed.body as { error?: string }).error;
    return {
      success: false,
      data: null,
      error: errorField ?? `Request failed with status ${parsed.status}`,
    };
  }

  if (parsed.parseFailed) {
    return {
      success: false,
      data: null,
      error: "Failed to parse server response",
    };
  }

  if (
    parsed.body &&
    typeof parsed.body === "object" &&
    "success" in parsed.body
  ) {
    return parsed.body as ApiResponse<T>;
  }

  return { success: true, data: parsed.body as T, error: null };
}

function isRefreshable<T>(parsed: ParsedResponse<T>): boolean {
  if (parsed.status !== 401 || parsed.body === null) {
    return false;
  }
  const errorField = (parsed.body as { error?: string }).error;
  return errorField !== undefined && REFRESHABLE_ERRORS.has(errorField);
}

async function fetchWithToken(
  endpoint: string,
  options: RequestInit,
  accessToken: string
): Promise<Response> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${accessToken}`,
    ...(options.headers as Record<string, string> | undefined),
  };
  return fetch(`${API_URL}${endpoint}`, { ...options, headers });
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  let accessToken: string;
  try {
    accessToken = await ensureFreshAccessToken();
  } catch (error) {
    return {
      success: false,
      data: null,
      error:
        error instanceof Error ? error.message : "auth_unavailable",
    };
  }

  const firstResponse = await fetchWithToken(endpoint, options, accessToken);
  const firstParsed = await parseResponse<T>(firstResponse);

  if (!isRefreshable(firstParsed)) {
    return toEnvelope<T>(firstParsed);
  }

  let rotated: string;
  try {
    rotated = await forceRefresh();
  } catch {
    clearTokens();
    return toEnvelope<T>(firstParsed);
  }

  const secondResponse = await fetchWithToken(endpoint, options, rotated);
  const secondParsed = await parseResponse<T>(secondResponse);

  if (secondParsed.status === 401) {
    clearTokens();
  }

  return toEnvelope<T>(secondParsed);
}

export const apiClient = {
  get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return request<T>(endpoint, { method: "GET" });
  },

  post<T>(endpoint: string, body?: unknown): Promise<ApiResponse<T>> {
    return request<T>(endpoint, {
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    });
  },

  put<T>(endpoint: string, body?: unknown): Promise<ApiResponse<T>> {
    return request<T>(endpoint, {
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
    });
  },

  patch<T>(endpoint: string, body?: unknown): Promise<ApiResponse<T>> {
    return request<T>(endpoint, {
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
    });
  },

  delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return request<T>(endpoint, { method: "DELETE" });
  },
};
