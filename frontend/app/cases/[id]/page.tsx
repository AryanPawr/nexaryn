import Link from "next/link";
import { DataTable } from "@/components/DataTable";
import { EmptyState } from "@/components/EmptyState";
import { ErrorState } from "@/components/ErrorState";
import { PageHeader } from "@/components/PageHeader";
import { SeverityPill, StatusPill } from "@/components/Pill";
import { getCase } from "@/lib/api";
import { formatDateTime, titleize } from "@/lib/format";

export const dynamic = "force-dynamic";

export default async function CaseDetailPage({ params }: { params: Promise<{ id: string }> }) {
  try {
    const { id } = await params;
    const caseDetail = await getCase(id);
    return (
      <div className="space-y-6">
        <PageHeader
          title={caseDetail.title}
          description={`Opened ${formatDateTime(caseDetail.opened_at)}`}
          actions={<Link className="rounded-md border border-line px-3 py-2 text-sm font-semibold text-zinc-700 hover:bg-panel" href="/cases">Back to cases</Link>}
        />

        <section className="grid gap-4 lg:grid-cols-3">
          <div className="rounded-lg border border-line bg-white p-5 shadow-soft lg:col-span-2">
            <div className="flex flex-wrap gap-2">
              <SeverityPill value={caseDetail.severity} />
              <StatusPill value={caseDetail.status} />
            </div>
            <p className="mt-4 text-sm leading-6 text-zinc-700">{caseDetail.summary}</p>
          </div>
          <div className="space-y-4">
            <section className="rounded-lg border border-line bg-white p-5 shadow-soft">
              <p className="text-xs font-semibold uppercase tracking-normal text-zinc-500">AI summary</p>
              <p className="mt-2 text-sm text-zinc-600">Pending Week 2 reasoning pipeline</p>
            </section>
            <section className="rounded-lg border border-line bg-white p-5 shadow-soft">
              <p className="text-xs font-semibold uppercase tracking-normal text-zinc-500">Recommended action</p>
              <p className="mt-2 text-sm text-zinc-600">Pending action recommendation pipeline</p>
            </section>
          </div>
        </section>

        <section className="space-y-3">
          <h2 className="text-lg font-semibold text-ink">Associated findings</h2>
          {caseDetail.findings.length === 0 ? (
            <EmptyState title="No associated findings" />
          ) : (
            <DataTable headers={["Title", "Type", "Severity", "Status", "First seen"]}>
              {caseDetail.findings.map((finding) => (
                <tr key={finding.id} className="bg-white">
                  <td className="px-4 py-3 font-medium text-ink">{finding.title}</td>
                  <td className="px-4 py-3 text-zinc-600">{titleize(finding.finding_type)}</td>
                  <td className="px-4 py-3"><SeverityPill value={finding.severity} /></td>
                  <td className="px-4 py-3"><StatusPill value={finding.status} /></td>
                  <td className="px-4 py-3 text-zinc-600">{formatDateTime(finding.first_seen_at)}</td>
                </tr>
              ))}
            </DataTable>
          )}
        </section>
      </div>
    );
  } catch (error) {
    return <ErrorState message={error instanceof Error ? error.message : "Case detail could not be loaded."} />;
  }
}
