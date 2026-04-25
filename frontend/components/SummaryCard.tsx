import type { ReactNode } from "react";

interface SummaryCardProps {
  label: string;
  value: string | number;
  detail?: string;
  children?: ReactNode;
}

export function SummaryCard({ label, value, detail, children }: SummaryCardProps) {
  return (
    <section className="rounded-lg border border-line bg-white p-5 shadow-soft">
      <p className="text-xs font-semibold uppercase tracking-normal text-zinc-500">{label}</p>
      <p className="mt-2 text-3xl font-semibold tracking-normal text-ink">{value}</p>
      {detail ? <p className="mt-1 text-sm text-zinc-500">{detail}</p> : null}
      {children ? <div className="mt-4">{children}</div> : null}
    </section>
  );
}
