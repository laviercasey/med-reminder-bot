import { retrieveRawInitData } from "@telegram-apps/sdk-react";
import { API_URL } from "@/shared/config";
import type { ApiResponse } from "./types";

function getInitData(): string {
  try {
    return retrieveRawInitData() ?? "";
  } catch {
    return "";
  }
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const initData = getInitData();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(initData ? { Authorization: `tma ${initData}` } : {}),
    ...(options.headers as Record<string, string>),
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    return {
      success: false,
      data: null,
      error: errorBody?.error ?? `Request failed with status ${response.status}`,
    };
  }

  let body: unknown;
  try {
    body = await response.json();
  } catch {
    return { success: false, data: null, error: "Failed to parse server response" };
  }

  if (body && typeof body === "object" && "success" in body) {
    return body as ApiResponse<T>;
  }

  return { success: true, data: body as T, error: null };
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
