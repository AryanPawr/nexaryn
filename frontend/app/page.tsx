import Link from "next/link";
import { DataTable } from "@/components/DataTable";
import { DeviceContext } from "@/components/DeviceContext";
import { EmptyState } from "@/components/EmptyState";
import { ErrorState } from "@/components/ErrorState";
import { PageHeader } from "@/components/PageHeader";
import { SeverityPill, StatusPill } from "@/components/Pill";
import { SummaryCard } from "@/components/SummaryCard";
import { getActiveDevice, getCases, getEvents, getFindings, getPostureScore } from "@/lib/api";
import { deviceName, formatDateTime, formatInteger, severityOrder, titleize } from "@/lib/format";
import type { Case, Device, Event, Finding, PostureScore, Severity } from "@/lib/types";

export const dynamic = "force-dynamic";

function openFindingCount(posture: PostureScore): number {
  return severityOrder.reduce((total, severity) => total + (posture.summary_counts.findings?.[severity] ?? 0), 0);
}

function openCaseCount(posture: PostureScore): number {
  return severityOrder.reduce((total, severity) => total + (posture.summary_counts.cases?.[severity] ?? 0), 0);
}

function SeverityBreakdown({ posture }: { posture: PostureScore }) {
  return (
    <div className="grid grid-cols-5 gap-2">
      {severityOrder.map((severity) => (
        <div key={severity} className="rounded-md border border-line bg-panel px-2 py-2 text-center">
          <p className="text-xs font-semibold capitalize text-zinc-500">{severity}</p>
          <p className="mt-1 text-lg font-semibold text-ink">{posture.summary_counts.findings?.[severity] ?? 0}</p>
        </div>
      ))}
    </div>
  );
}

function RecentEvents({ events, device }: { events: Event[]; device: Device | null }) {
  if (events.length === 0) {
    return <EmptyState title="No events yet" detail="Telemetry events will appear after an agent reports data." />;
  }

  const devices = device ? [device] : [];
  return (
    <DataTable headers={["Event", "Category", "Severity", "Device", "Occurred"]}>
      {events.map((event) => (
        <tr key={event.id} className="bg-white">
          <td className="px-4 py-3 font-medium text-ink">{titleize(event.event_type)}</td>
          <td className="px-4 py-3 text-zinc-600">{event.category}</td>
          <td className="px-4 py-3"><SeverityPill value={event.severity} /></td>
          <td className="px-4 py-3 text-zinc-600">{deviceName(event.device_id, devices)}</td>
          <td className="px-4 py-3 text-zinc-600">{formatDateTime(event.occurred_at)}</td>
        </tr>
      ))}
    </DataTable>
  );
}

export default async function DashboardPage() {
  try {
    const activeDevice = await getActiveDevice();
    const deviceId = activeDevice?.id;
    const [posture, events] = await Promise.all([
      getPostureScore(deviceId),
      getEvents({ device_id: deviceId, limit: 10 })
    ]);
    const findingsBySeverity = posture.summary_counts.findings ?? {};
    const openFindings = openFindingCount(posture);
    const openCases = openCaseCount(posture);

    return (
      <div className="space-y-6">
        <PageHeader title="Dashboard" description="Live posture, telemetry, and active work for the selected device." actions={<DeviceContext device={activeDevice} />} />

        <div className="grid gap-4 lg:grid-cols-3">
          <SummaryCard label="Posture score" value={posture.overall_score} detail={`Trend: ${posture.trend}`}>
            <div className="space-y-2 text-sm text-zinc-600">
              {posture.drivers.map((driver) => (
                <p key={driver}>{driver}</p>
              ))}
            </div>
          </SummaryCard>
          <SummaryCard label="Open findings" value={formatInteger(openFindings)} detail="Grouped by severity">
            <SeverityBreakdown posture={posture} />
          </SummaryCard>
          <SummaryCard label="Open cases" value={formatInteger(openCases)} detail={`Risk points: ${posture.summary_counts.risk_points ?? 0}`} />
        </div>

        <section className="space-y-3">
          <div className="flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold text-ink">Recent events</h2>
            <Link className="text-sm font-semibold text-accent hover:text-teal-800" href="/events">View all</Link>
          </div>
          <RecentEvents events={events} device={activeDevice} />
        </section>
      </div>
    );
  } catch (error) {
    return <ErrorState message={error instanceof Error ? error.message : "Dashboard data could not be loaded."} />;
  }
}
