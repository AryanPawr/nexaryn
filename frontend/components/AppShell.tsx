import Link from "next/link";
import type { ReactNode } from "react";

const navItems = [
  { href: "/", label: "Dashboard" },
  { href: "/events", label: "Events" },
  { href: "/findings", label: "Findings" },
  { href: "/cases", label: "Cases" },
  { href: "/actions", label: "Actions" }
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-white px-5 py-6 lg:block">
        <Link href="/" className="block">
          <p className="text-xl font-semibold tracking-normal text-ink">Nexaryn</p>
          <p className="mt-1 text-xs font-medium uppercase tracking-normal text-zinc-500">Control plane</p>
        </Link>
        <nav className="mt-8 grid gap-1">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href} className="rounded-md px-3 py-2 text-sm font-medium text-zinc-700 hover:bg-panel hover:text-ink">
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 border-b border-line bg-white/90 px-4 py-3 backdrop-blur lg:hidden">
          <div className="flex items-center justify-between gap-3">
            <Link href="/" className="text-lg font-semibold text-ink">Nexaryn</Link>
            <nav className="flex gap-2 overflow-x-auto text-sm text-zinc-600">
              {navItems.map((item) => (
                <Link key={item.href} href={item.href} className="rounded-md px-2 py-1 hover:bg-panel">
                  {item.label}
                </Link>
              ))}
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</main>
      </div>
    </div>
  );
}
