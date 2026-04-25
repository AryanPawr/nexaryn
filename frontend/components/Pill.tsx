import type { ActionApprovalStatus, CaseStatus, FindingStatus, Severity } from "@/lib/types";

const severityClasses: Record<Severity, string> = {
  critical: "bg-red-100 text-red-800 border-red-200",
  high: "bg-orange-100 text-orange-800 border-orange-200",
  medium: "bg-amber-100 text-amber-800 border-amber-200",
  low: "bg-teal-100 text-teal-800 border-teal-200",
  info: "bg-sky-100 text-sky-800 border-sky-200"
};

const statusClasses: Record<string, string> = {
  open: "bg-red-50 text-red-800 border-red-200",
  investigating: "bg-amber-50 text-amber-800 border-amber-200",
  contained: "bg-sky-50 text-sky-800 border-sky-200",
  resolved: "bg-emerald-50 text-emerald-800 border-emerald-200",
  closed: "bg-zinc-100 text-zinc-700 border-zinc-200",
  ignored: "bg-zinc-100 text-zinc-700 border-zinc-200",
  triaged: "bg-blue-50 text-blue-800 border-blue-200",
  pending: "bg-amber-50 text-amber-800 border-amber-200",
  approved: "bg-emerald-50 text-emerald-800 border-emerald-200",
  denied: "bg-zinc-100 text-zinc-700 border-zinc-200",
  rejected: "bg-zinc-100 text-zinc-700 border-zinc-200"
};

function PillBase({ value, className }: { value: string; className: string }) {
  return (
    <span className={`inline-flex h-6 items-center rounded-full border px-2 text-xs font-medium capitalize ${className}`}>
      {value.replace(/_/g, " ")}
    </span>
  );
}

export function SeverityPill({ value }: { value: Severity }) {
  return <PillBase value={value} className={severityClasses[value]} />;
}

export function StatusPill({ value }: { value: FindingStatus | CaseStatus | ActionApprovalStatus | string }) {
  return <PillBase value={value} className={statusClasses[value] ?? "bg-zinc-100 text-zinc-700 border-zinc-200"} />;
}
