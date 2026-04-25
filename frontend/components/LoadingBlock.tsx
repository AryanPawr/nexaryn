export function LoadingBlock() {
  return (
    <div className="space-y-3">
      <div className="h-8 w-48 animate-pulse rounded bg-zinc-200" />
      <div className="grid gap-3 md:grid-cols-3">
        <div className="h-28 animate-pulse rounded-lg bg-zinc-200" />
        <div className="h-28 animate-pulse rounded-lg bg-zinc-200" />
        <div className="h-28 animate-pulse rounded-lg bg-zinc-200" />
      </div>
      <div className="h-72 animate-pulse rounded-lg bg-zinc-200" />
    </div>
  );
}
