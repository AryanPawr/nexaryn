import type { Device } from "@/lib/types";
import { formatDateTime } from "@/lib/format";

export function DeviceContext({ device }: { device: Device | null }) {
  if (!device) {
    return (
      <div className="rounded-lg border border-line bg-white px-4 py-3 text-sm text-zinc-600">
        No active device
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-line bg-white px-4 py-3">
      <p className="text-xs font-semibold uppercase tracking-normal text-zinc-500">Active device</p>
      <p className="mt-1 text-sm font-semibold text-ink">{device.hostname}</p>
      <p className="mt-1 text-xs text-zinc-500">
        {device.os_name} {device.os_version} · last seen {formatDateTime(device.last_seen_at)}
      </p>
    </div>
  );
}
