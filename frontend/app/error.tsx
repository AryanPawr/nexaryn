"use client";

import { ErrorState } from "@/components/ErrorState";

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="space-y-4">
      <ErrorState message={error.message} />
      <button className="rounded-md bg-accent px-4 py-2 text-sm font-semibold text-white hover:bg-teal-800" onClick={reset}>
        Retry
      </button>
    </div>
  );
}
