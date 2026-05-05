import { DeadlineList } from "@/components/DeadlineList";

export default function Home() {
  return (
    <div className="flex flex-1 flex-col items-center bg-zinc-50 px-4 py-12 dark:bg-black">
      <div className="w-full max-w-2xl space-y-6">
        <header className="text-center">
          <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
            Deadline Track
          </h1>
          <p className="mt-2 text-zinc-600 dark:text-zinc-400">
            Never miss an important date again.
          </p>
        </header>
        <DeadlineList />
      </div>
    </div>
  );
}
