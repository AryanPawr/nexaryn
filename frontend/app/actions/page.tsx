import { DataTable } from "@/components/DataTable";
import { EmptyState } from "@/components/EmptyState";
import { ErrorState } from "@/components/ErrorState";
import { PageHeader } from "@/components/PageHeader";
import { StatusPill } from "@/components/Pill";
import { getActions, getDevices } from "@/lib/api";
import { formatDateTime, titleize } from "@/lib/format";
import type { Action, Device } from "@/lib/types";
import { approveActionForm, denyActionForm } from "./mutations";

export const dynamic = "force-dynamic";

function deviceLabel(deviceId: string, devices: Device[]): string {
  return devices.find((device) => device.id === deviceId)?.hostname ?? deviceId.slice(0, 8);
}

function DecisionButtons({ action }: { action: Action }) {
  const disabled = action.approval_status !== "pending";
  return (
    <div className="flex flex-wrap gap-2">
      <form action={approveActionForm}>
        <input name="action_id" type="hidden" value={action.id} />
        <button
          className="rounded-md bg-accent px-3 py-1.5 text-xs font-semibold text-white hover:bg-teal-800 disabled:cursor-not-allowed disabled:bg-zinc-300"
          data-testid={`approve-action-${action.id}`}
          disabled={disabled}
          type="submit"
        >
          Approve
        </button>
      </form>
      <form action={denyActionForm}>
        <input name="action_id" type="hidden" value={action.id} />
        <button
          className="rounded-md border border-line px-3 py-1.5 text-xs font-semibold text-zinc-700 hover:bg-panel disabled:cursor-not-allowed disabled:text-zinc-300"
          data-testid={`deny-action-${action.id}`}
          disabled={disabled}
          type="submit"
        >
          Deny
        </button>
      </form>
    </div>
  );
}

export default async function ActionsPage() {
  try {
    const [actions, devices] = await Promise.all([
      getActions({ limit: 100 }),
      getDevices({ limit: 500 })
    ]);

    return (
      <div className="space-y-6">
        <PageHeader title="Actions" description="Operator approval queue for agent-executed actions." />
        {actions.length === 0 ? (
          <EmptyState title="No actions yet" detail="Actions will appear when cases request operator approval." />
        ) : (
          <DataTable headers={["Action", "Device", "Approval", "Execution", "Requested", "Decision"]}>
            {actions.map((action: Action) => (
              <tr key={action.id} className="bg-white">
                <td className="px-4 py-3 font-medium text-ink">{titleize(action.action_type)}</td>
                <td className="px-4 py-3 text-zinc-600">{deviceLabel(action.device_id, devices)}</td>
                <td className="px-4 py-3"><StatusPill value={action.approval_status} /></td>
                <td className="px-4 py-3"><StatusPill value={action.execution_status} /></td>
                <td className="px-4 py-3 text-zinc-600">{formatDateTime(action.requested_at)}</td>
                <td className="px-4 py-3"><DecisionButtons action={action} /></td>
              </tr>
            ))}
          </DataTable>
        )}
      </div>
    );
  } catch (error) {
    return <ErrorState message={error instanceof Error ? error.message : "Actions could not be loaded."} />;
  }
}
