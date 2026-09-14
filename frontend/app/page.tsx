const workflows = [
  {
    name: "Customer Support Automation",
    status: "Active",
    updated: "2 minutes ago",
  },
  {
    name: "Invoice Approval Pipeline",
    status: "Draft",
    updated: "1 hour ago",
  },
  {
    name: "Lead Qualification Agent",
    status: "Active",
    updated: "Yesterday",
  },
];

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-8 text-slate-100 md:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="mb-10 flex flex-col gap-4 border-b border-slate-800 pb-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="mb-2 text-sm font-medium uppercase tracking-[0.25em] text-cyan-400">
              FlowPilot
            </p>
            <h1 className="text-3xl font-bold tracking-tight">
              Workflow Command Center
            </h1>
            <p className="mt-2 text-sm text-slate-400">
              Design, automate, and monitor intelligent workflows.
            </p>
          </div>

          <button className="rounded-lg bg-cyan-400 px-5 py-3 font-semibold text-slate-950 transition hover:bg-cyan-300">
            + Create Workflow
          </button>
        </header>

        <section className="grid gap-4 md:grid-cols-3">
          <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">Total Workflows</p>
            <p className="mt-3 text-3xl font-bold">12</p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">Active Executions</p>
            <p className="mt-3 text-3xl font-bold text-cyan-400">4</p>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
            <p className="text-sm text-slate-400">Success Rate</p>
            <p className="mt-3 text-3xl font-bold text-emerald-400">98.4%</p>
          </div>
        </section>

        <section className="mt-10">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold">Recent Workflows</h2>
              <p className="mt-1 text-sm text-slate-400">
                Your latest workflow activity.
              </p>
            </div>

            <button className="text-sm text-cyan-400 hover:text-cyan-300">
              View all
            </button>
          </div>

          <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900">
            {workflows.map((workflow) => (
              <div
                key={workflow.name}
                className="flex flex-col gap-3 border-b border-slate-800 p-5 last:border-b-0 sm:flex-row sm:items-center sm:justify-between"
              >
                <div>
                  <h3 className="font-medium">{workflow.name}</h3>
                  <p className="mt-1 text-sm text-slate-500">
                    Updated {workflow.updated}
                  </p>
                </div>

                <span
                  className={`w-fit rounded-full px-3 py-1 text-xs font-medium ${
                    workflow.status === "Active"
                      ? "bg-emerald-400/10 text-emerald-400"
                      : "bg-amber-400/10 text-amber-400"
                  }`}
                >
                  {workflow.status}
                </span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}