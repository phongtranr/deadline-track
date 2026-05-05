"use client";

import { useState } from "react";
import { Deadline } from "@/lib/types";
import { generateId } from "@/lib/utils";
import { DeadlineForm } from "./DeadlineForm";
import { DeadlineItem } from "./DeadlineItem";

export function DeadlineList() {
  const [deadlines, setDeadlines] = useState<Deadline[]>([]);

  const addDeadline = (title: string, dueDate: string, description: string) => {
    const newDeadline: Deadline = {
      id: generateId(),
      title,
      dueDate,
      description: description || undefined,
      completed: false,
      createdAt: new Date().toISOString(),
    };
    setDeadlines((prev) => [...prev, newDeadline]);
  };

  const toggleDeadline = (id: string) => {
    setDeadlines((prev) =>
      prev.map((d) => (d.id === id ? { ...d, completed: !d.completed } : d))
    );
  };

  const deleteDeadline = (id: string) => {
    setDeadlines((prev) => prev.filter((d) => d.id !== id));
  };

  const sortedDeadlines = [...deadlines].sort((a, b) => {
    if (a.completed !== b.completed) return a.completed ? 1 : -1;
    return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
  });

  const activeCount = deadlines.filter((d) => !d.completed).length;

  return (
    <div className="space-y-6">
      <DeadlineForm onAdd={addDeadline} />

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">
            Your Deadlines
          </h2>
          {deadlines.length > 0 && (
            <span className="text-sm text-zinc-500 dark:text-zinc-400">
              {activeCount} active
            </span>
          )}
        </div>

        {sortedDeadlines.length === 0 ? (
          <p className="rounded-lg border border-dashed border-zinc-300 py-8 text-center text-sm text-zinc-500 dark:border-zinc-700 dark:text-zinc-400">
            No deadlines yet. Add one above to get started.
          </p>
        ) : (
          <div className="space-y-2">
            {sortedDeadlines.map((deadline) => (
              <DeadlineItem
                key={deadline.id}
                deadline={deadline}
                onToggle={toggleDeadline}
                onDelete={deleteDeadline}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
