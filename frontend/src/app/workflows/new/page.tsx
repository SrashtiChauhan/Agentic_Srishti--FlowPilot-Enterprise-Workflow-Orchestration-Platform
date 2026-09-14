"use client";

import Link from "next/link";
import { useWorkflowStore } from "@/store/workflowStore";

export default function NewWorkflowPage() {
  const nodes = useWorkflowStore((state) => state.nodes);

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <header className="border-b border-slate-800 px-6 py-4">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div>
            <Link
              href="/"
              className="text-sm text-slate-400 hover:text-white"
            >
              ← Back to Dashboard
            </Link>

            <h1 className="mt-2 text-2xl font-bold">
              Create New Workflow
            </h1>
          </div>

          <button className="rounded-lg bg-sky-500 px-4 py-2 font-medium text-slate-950 hover:bg-sky-400">
            Save Workflow
          </button>
        </div>
      </header>

      <section className="mx-auto grid max-w-7xl grid-cols-[240px_1fr] gap-6 p-6">
        <aside className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <h2 className="mb-4 font-semibold">Node Palette</h2>

          <div className="space-y-3">
            <button className="w-full rounded-lg border border-slate-700 p-3 text-left hover:border-sky-400">
              Trigger
            </button>

            <button className="w-full rounded-lg border border-slate-700 p-3 text-left hover:border-sky-400">
              AI Agent
            </button>

            <button className="w-full rounded-lg border border-slate-700 p-3 text-left hover:border-sky-400">
              Condition
            </button>

            <button className="w-full rounded-lg border border-slate-700 p-3 text-left hover:border-sky-400">
              Action
            </button>
          </div>
        </aside>

        <div className="min-h-[600px] rounded-xl border border-slate-800 bg-slate-900 p-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h2 className="font-semibold">Workflow Canvas</h2>
              <p className="text-sm text-slate-400">
                Build your workflow by connecting nodes.
              </p>
            </div>

            <span className="text-sm text-slate-400">
              {nodes.length} nodes
            </span>
          </div>

          <div className="mt-6 flex min-h-[500px] items-center justify-center rounded-lg border border-dashed border-slate-700">
            <p className="text-center text-slate-500">
              React Flow canvas will be added here.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}