import { DataTable } from "@/components/DataTable";
import { EmptyState } from "@/components/EmptyState";
import { ErrorState } from "@/components/ErrorState";
import { FilterBar, SelectFilter } from "@/components/FilterBar";
import { PageHeader } from "@/components/PageHeader";
import { SeverityPill, StatusPill } from "@/components/Pill";
import { getActiveDevice, getFindings } from "@/lib/api";
import { deviceName, formatDateTime, titleize } from "@/lib/format";
import type { Finding } from "@/lib/types";

export const dynamic = "force-dynamic";

export default async function FindingsPage({ searchParams }: { searchParams: Promise<{ severity?: string; status?: string }> }) {
  const query = await searchParams;
  try {
    const activeDevice = await getActiveDevice();
    const findings = await getFindings({
      device_id: activeDevice?.id,
      severity: query.severity,
      status: query.status
    });
    const devices = activeDevice ? [activeDevice] : [];

    return (
      <div className="space-y-6">
        <PageHeader title="Findings" description="Rule-based finding candidates generated from telemetry." />
        <FilterBar>
          <SelectFilter label="Severity" name="severity" value={query.severity} options={["info", "low", "medium", "high", "critical"]} />
          <SelectFilter label="Status" name="status" value={query.status} options={["open", "triaged", "resolved", "ignored"]} />
        </FilterBar>
        {findings.length === 0 ? (
          <EmptyState title="No findings yet" detail="Findings will appear after ingest processing creates candidates." />
        ) : (
          <DataTable headers={["Title", "Type", "Severity", "Status", "Device", "First seen"]}>
            {findings.map((finding: Finding) => (
              <tr key={finding.id} className="bg-white">
                <td className="px-4 py-3 font-medium text-ink">{finding.title}</td>
                <td className="px-4 py-3 text-zinc-600">{titleize(finding.finding_type)}</td>
                <td className="px-4 py-3"><SeverityPill value={finding.severity} /></td>
                <td className="px-4 py-3"><StatusPill value={finding.status} /></td>
                <td className="px-4 py-3 text-zinc-600">{deviceName(finding.device_id, devices)}</td>
                <td className="px-4 py-3 text-zinc-600">{formatDateTime(finding.first_seen_at)}</td>
              </tr>
            ))}
          </DataTable>
        )}
      </div>
    );
  } catch (error) {
    return <ErrorState message={error instanceof Error ? error.message : "Findings could not be loaded."} />;
  }
}
