"use client";

import type { Node } from "@xyflow/react";

interface NodeInspectorProps {
  node: Node | null;
}
export default function NodeInspector({ node }: NodeInspectorProps) {
  if (!node) {
    return (
      <aside className="w-80 shrink-0 border-l border-slate-800 bg-slate-900/80 p-5 backdrop-blur-md">
        <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
          Node Inspector
        </p>

        <p className="mt-2 text-xs text-slate-500">
          Select a node to inspect its configuration.
        </p>

        <div className="mt-8 rounded-xl border border-dashed border-slate-700 p-5 text-center">
          <p className="text-sm text-slate-400">
            No node selected
          </p>

          <p className="mt-2 text-xs text-slate-600">
            Click a workflow node to view its details.
          </p>
        </div>
      </aside>
    );
  }

  return (
    <aside className="w-80 shrink-0 border-l border-slate-800 bg-slate-900/80 p-5 backdrop-blur-md">
      <p className="text-xs font-bold uppercase tracking-wider text-slate-400">
        Node Inspector
      </p>

      <p className="mt-2 text-xs text-slate-500">
        Inspect the selected workflow node.
      </p>

      <div className="mt-6 space-y-5">
        <div>
          <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
            Type
          </p>

          <p className="mt-1 text-sm font-semibold uppercase text-cyan-400">
            {String(node.data.type)}
          </p>
        </div>

        <div>
          <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
            Title
          </p>

          <p className="mt-1 text-sm font-semibold text-slate-100">
            {String(node.data.title)}
          </p>
        </div>

        <div>
          <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
            Subtitle
          </p>

          <p className="mt-1 text-sm text-slate-400">
            {String(node.data.subtitle ?? "No subtitle")}
          </p>
        </div>

        <div>
          <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
            Status
          </p>

          <p className="mt-1 font-mono text-xs uppercase text-slate-400">
            {String(node.data.status)}
          </p>
        </div>
      </div>
    </aside>
  );
}