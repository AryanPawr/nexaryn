interface ErrorStateProps {
  title?: string;
  message: string;
}

export function ErrorState({ title = "Unable to load data", message }: ErrorStateProps) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 px-5 py-4">
      <p className="text-sm font-semibold text-red-900">{title}</p>
      <p className="mt-1 text-sm text-red-700">{message}</p>
    </div>
  );
}
