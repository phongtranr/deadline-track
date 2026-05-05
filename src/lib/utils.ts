export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function getDaysUntil(dateString: string): number {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  const target = new Date(dateString);
  target.setHours(0, 0, 0, 0);
  const diff = target.getTime() - now.getTime();
  return Math.ceil(diff / (1000 * 60 * 60 * 24));
}

export function getUrgencyClass(daysUntil: number, completed: boolean): string {
  if (completed) return "text-green-600";
  if (daysUntil < 0) return "text-red-600";
  if (daysUntil <= 3) return "text-orange-500";
  if (daysUntil <= 7) return "text-yellow-600";
  return "text-zinc-600";
}

export function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}
