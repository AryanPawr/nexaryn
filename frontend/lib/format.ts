import type { Device, Severity } from "./types";

export const severityOrder: Severity[] = ["critical", "high", "medium", "low", "info"];

export function formatDateTime(value: string | null | undefined): string {
  if (!value) {
    return "Not recorded";
  }
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  }).format(new Date(value));
}

export function formatInteger(value: number | undefined): string {
  return new Intl.NumberFormat("en").format(value ?? 0);
}

export function deviceName(deviceId: string, devices: Device[]): string {
  const device = devices.find((item) => item.id === deviceId);
  return device ? device.hostname : deviceId.slice(0, 8);
}

export function titleize(value: string): string {
  return value.replace(/_/g, " ");
}
