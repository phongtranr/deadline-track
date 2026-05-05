"use client";

import { Deadline } from "@/lib/types";
import { formatDate, getDaysUntil, getUrgencyClass } from "@/lib/utils";

interface DeadlineItemProps {
  deadline: Deadline;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
}

export function DeadlineItem({ deadline, onToggle, onDelete }: DeadlineItemProps) {
  const daysUntil = getDaysUntil(deadline.dueDate);
  const urgencyClass = getUrgencyClass(daysUntil, deadline.completed);

  const statusLabel = deadline.completed
    ? "Completed"
    : daysUntil < 0
      ? `${Math.abs(daysUntil)} day${Math.abs(daysUntil) !== 1 ? "s" : ""} overdue`
      : daysUntil === 0
        ? "Due today"
        : `${daysUntil} day${daysUntil !== 1 ? "s" : ""} left`;

  return (
    <div className={`flex items-center gap-4 rounded-lg border p-4 transition-colors ${deadline.completed ? "border-green-200 bg-green-50 dark:border-green-900 dark:bg-green-950/30" : "border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900"}`}>
      <button
        onClick={() => onToggle(deadline.id)}
        aria-label={deadline.completed ? "Mark incomplete" : "Mark complete"}
        className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full border-2 transition-colors ${deadline.completed ? "border-green-500 bg-green-500 text-white" : "border-zinc-300 hover:border-blue-500 dark:border-zinc-600"}`}
      >
        {deadline.completed && (
          <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        )}
      </button>
      <div className="min-w-0 flex-1">
        <p className={`text-sm font-medium ${deadline.completed ? "text-zinc-500 line-through dark:text-zinc-400" : "text-zinc-900 dark:text-zinc-100"}`}>
          {deadline.title}
        </p>
        {deadline.description && (
          <p className="mt-0.5 text-xs text-zinc-500 dark:text-zinc-400">
            {deadline.description}
          </p>
        )}
        <div className="mt-1 flex items-center gap-3 text-xs">
          <span className="text-zinc-500 dark:text-zinc-400">
            {formatDate(deadline.dueDate)}
          </span>
          <span className={`font-medium ${urgencyClass}`}>
            {statusLabel}
          </span>
        </div>
      </div>
      <button
        onClick={() => onDelete(deadline.id)}
        aria-label="Delete deadline"
        className="shrink-0 rounded-md p-1.5 text-zinc-400 transition-colors hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-950 dark:hover:text-red-400"
      >
        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>
  );
}
