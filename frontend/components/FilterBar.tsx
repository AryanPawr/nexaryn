import type { ReactNode } from "react";

interface FilterBarProps {
  children: ReactNode;
}

export function FilterBar({ children }: FilterBarProps) {
  return (
    <form className="flex flex-wrap items-end gap-3 rounded-lg border border-line bg-white p-4 shadow-soft">
      {children}
      <button className="h-10 rounded-md bg-accent px-4 text-sm font-semibold text-white hover:bg-teal-800" type="submit">
        Apply
      </button>
      <a className="flex h-10 items-center rounded-md border border-line px-4 text-sm font-semibold text-zinc-700 hover:bg-panel" href="?">
        Reset
      </a>
    </form>
  );
}

export function SelectFilter({
  label,
  name,
  value,
  options
}: {
  label: string;
  name: string;
  value?: string;
  options: string[];
}) {
  return (
    <label className="grid gap-1 text-sm text-zinc-600">
      <span className="font-medium">{label}</span>
      <select name={name} defaultValue={value ?? ""} className="h-10 rounded-md border border-line bg-white px-3 text-sm text-ink">
        <option value="">All</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option.replace(/_/g, " ")}
          </option>
        ))}
      </select>
    </label>
  );
}
