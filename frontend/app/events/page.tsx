import { DataTable } from "@/components/DataTable";
import { EmptyState } from "@/components/EmptyState";
import { ErrorState } from "@/components/ErrorState";
import { FilterBar, SelectFilter } from "@/components/FilterBar";
import { PageHeader } from "@/components/PageHeader";
import { SeverityPill } from "@/components/Pill";
import { getActiveDevice, getEvents } from "@/lib/api";
import { deviceName, formatDateTime, titleize } from "@/lib/format";
import type { Event } from "@/lib/types";

export const dynamic = "force-dynamic";

const pageSize = 25;

export default async function EventsPage({ searchParams }: { searchParams: Promise<{ severity?: string; category?: string; page?: string }> }) {
  const query = await searchParams;
  const currentPage = Number(query.page ?? "1") > 0 ? Number(query.page ?? "1") : 1;
  try {
    const activeDevice = await getActiveDevice();
    const events = await getEvents({
      device_id: activeDevice?.id,
      severity: query.severity,
      category: query.category,
      limit: pageSize,
      offset: (currentPage - 1) * pageSize
    });
    const devices = activeDevice ? [activeDevice] : [];

    return (
      <div className="space-y-6">
        <PageHeader title="Events" description="Telemetry received from registered agents." />
        <FilterBar>
          <SelectFilter label="Severity" name="severity" value={query.severity} options={["info", "low", "medium", "high", "critical"]} />
          <SelectFilter label="Category" name="category" value={query.category} options={["process", "network", "package", "container", "secret", "config", "system"]} />
        </FilterBar>
        {events.length === 0 ? (
          <EmptyState title="No events yet" detail="Try a different filter or wait for agent telemetry." />
        ) : (
          <DataTable headers={["Event type", "Category", "Severity", "Device", "Occurred"]}>
            {events.map((event: Event) => (
              <tr key={event.id} className="bg-white">
                <td className="px-4 py-3 font-medium text-ink">{titleize(event.event_type)}</td>
                <td className="px-4 py-3 text-zinc-600">{event.category}</td>
                <td className="px-4 py-3"><SeverityPill value={event.severity} /></td>
                <td className="px-4 py-3 text-zinc-600">{deviceName(event.device_id, devices)}</td>
                <td className="px-4 py-3 text-zinc-600">{formatDateTime(event.occurred_at)}</td>
              </tr>
            ))}
          </DataTable>
        )}
        <div className="flex justify-end gap-2">
          {currentPage > 1 ? <a className="rounded-md border border-line px-3 py-2 text-sm font-semibold" href={`?page=${currentPage - 1}`}>Previous</a> : null}
          {events.length === pageSize ? <a className="rounded-md border border-line px-3 py-2 text-sm font-semibold" href={`?page=${currentPage + 1}`}>Next</a> : null}
        </div>
      </div>
    );
  } catch (error) {
    return <ErrorState message={error instanceof Error ? error.message : "Events could not be loaded."} />;
  }
}
