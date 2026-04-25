import type { Action, Case, CaseDetail, Device, Event, Finding, ListQuery, PostureScore } from "./types";

export class ApiError extends Error {
  status: number;
  detail: unknown;

  constructor(message: string, status: number, detail: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

function apiBaseUrl(): string {
  const baseUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!baseUrl) {
    throw new ApiError("NEXT_PUBLIC_API_URL is not configured.", 500, null);
  }
  return baseUrl.replace(/\/$/, "");
}

function buildQuery(query: ListQuery = {}): string {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(query)) {
    if (value !== undefined && value !== null && value !== "") {
      params.set(key, String(value));
    }
  }
  const text = params.toString();
  return text ? `?${text}` : "";
}

async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");
  if (init.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${apiBaseUrl()}${path}`, {
    ...init,
    headers,
    cache: "no-store"
  });

  const text = await response.text();
  const body = text ? JSON.parse(text) : null;
  if (!response.ok) {
    const message =
      typeof body?.detail?.message === "string"
        ? body.detail.message
        : `API request failed with status ${response.status}.`;
    throw new ApiError(message, response.status, body);
  }
  return body as T;
}

export function getDevices(query: Pick<ListQuery, "agent_id" | "limit" | "offset"> = {}): Promise<Device[]> {
  return apiRequest<Device[]>(`/api/v1/devices${buildQuery(query)}`);
}

export async function getActiveDevice(): Promise<Device | null> {
  const devices = await getDevices({ limit: 1 });
  return devices[0] ?? null;
}

export function getPostureScore(deviceId?: string): Promise<PostureScore> {
  return apiRequest<PostureScore>(`/api/v1/posture-score${buildQuery({ device_id: deviceId })}`);
}

export function getEvents(query: Pick<ListQuery, "device_id" | "category" | "severity" | "event_type" | "limit" | "offset"> = {}): Promise<Event[]> {
  return apiRequest<Event[]>(`/api/v1/events${buildQuery(query)}`);
}

export function getFindings(query: Pick<ListQuery, "device_id" | "category" | "severity" | "status"> = {}): Promise<Finding[]> {
  return apiRequest<Finding[]>(`/api/v1/findings${buildQuery(query)}`);
}

export function getCases(query: Pick<ListQuery, "device_id" | "severity" | "status"> = {}): Promise<Case[]> {
  return apiRequest<Case[]>(`/api/v1/cases${buildQuery(query)}`);
}

export function getCase(caseId: string): Promise<CaseDetail> {
  return apiRequest<CaseDetail>(`/api/v1/cases/${caseId}`);
}

export function getActions(query: Pick<ListQuery, "device_id" | "approval_status" | "execution_status" | "limit" | "offset"> = {}): Promise<Action[]> {
  return apiRequest<Action[]>(`/api/v1/actions${buildQuery(query)}`);
}

export function approveAction(actionId: string): Promise<Action> {
  return apiRequest<Action>(`/api/v1/actions/${actionId}/approve`, { method: "POST" });
}

export function denyAction(actionId: string): Promise<Action> {
  return apiRequest<Action>(`/api/v1/actions/${actionId}/deny`, { method: "POST" });
}
