import Link from "next/link";
import { DataTable } from "@/components/DataTable";
import { EmptyState } from "@/components/EmptyState";
import { ErrorState } from "@/components/ErrorState";
import { PageHeader } from "@/components/PageHeader";
import { SeverityPill, StatusPill } from "@/components/Pill";
import { getActiveDevice, getCases } from "@/lib/api";
import { deviceName, formatDateTime } from "@/lib/format";
import type { Case } from "@/lib/types";

export const dynamic = "force-dynamic";

export default async function CasesPage() {
  try {
    const activeDevice = await getActiveDevice();
    const cases = await getCases({ device_id: activeDevice?.id });
    const devices = activeDevice ? [activeDevice] : [];

    return (
      <div className="space-y-6">
        <PageHeader title="Cases" description="Investigation work grouped by device and severity." />
        {cases.length === 0 ? (
          <EmptyState title="No cases yet" detail="Cases will appear when findings are grouped for investigation." />
        ) : (
          <DataTable headers={["Title", "Severity", "Status", "Device", "Opened"]}>
            {cases.map((caseItem: Case) => (
              <tr key={caseItem.id} className="bg-white">
                <td className="px-4 py-3 font-medium text-ink">
                  <Link className="text-accent hover:text-teal-800" href={`/cases/${caseItem.id}`}>{caseItem.title}</Link>
                </td>
                <td className="px-4 py-3"><SeverityPill value={caseItem.severity} /></td>
                <td className="px-4 py-3"><StatusPill value={caseItem.status} /></td>
                <td className="px-4 py-3 text-zinc-600">{deviceName(caseItem.device_id, devices)}</td>
                <td className="px-4 py-3 text-zinc-600">{formatDateTime(caseItem.opened_at)}</td>
              </tr>
            ))}
          </DataTable>
        )}
      </div>
    );
  } catch (error) {
    return <ErrorState message={error instanceof Error ? error.message : "Cases could not be loaded."} />;
  }
}
