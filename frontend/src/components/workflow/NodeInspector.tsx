"use client";

import type { Node } from "@xyflow/react";
import type { WorkflowNodeConfig } from "@/types/workflow";

interface NodeInspectorProps {
  node: Node | null;
  onUpdateNode: (nodeId: string, updates: Record<string, unknown>) => void;
}
export default function NodeInspector({
  node,
  onUpdateNode,
}: NodeInspectorProps) {
  const config = node?.data.config as WorkflowNodeConfig | undefined;
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
          <p className="text-sm text-slate-400">No node selected</p>

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
          <label
            htmlFor="node-title"
            className="text-[10px] font-bold uppercase tracking-wider text-slate-500"
          >
            Title
          </label>

          <input
            id="node-title"
            type="text"
            value={String(node.data.title ?? "")}
            onChange={(event) => {
              onUpdateNode(node.id, {
                title: event.target.value,
              });
            }}
            className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-cyan-400/60"
          />
        </div>

        <div>
          <label
            htmlFor="node-subtitle"
            className="text-[10px] font-bold uppercase tracking-wider text-slate-500"
          >
            Subtitle
          </label>

          <input
            id="node-subtitle"
            type="text"
            value={String(node.data.subtitle ?? "")}
            onChange={(event) => {
              onUpdateNode(node.id, {
                subtitle: event.target.value,
              });
            }}
            className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-cyan-400/60"
          />
        </div>

        {node.data.type === "trigger" && (
  <div>
    <label
      htmlFor="trigger-type"
      className="text-[10px] font-bold uppercase tracking-wider text-slate-500"
    >
      Trigger Type
    </label>

    <select
      id="trigger-type"
      value={config?.triggerType ?? "manual"}
      onChange={(event) => {
        onUpdateNode(node.id, {
          config: {
            ...(node.data.config as Record<string, unknown>),
            triggerType: event.target.value,
          },
        });
      }}
      className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-amber-400/60"
    >
      <option value="manual">Manual</option>
      <option value="webhook">Webhook</option>
      <option value="schedule">Schedule</option>
      <option value="event">Event</option>
    </select>
  </div>
)}
{node.data.type === "agent" && (
  <div>
    <label
      htmlFor="agent-id"
      className="text-[10px] font-bold uppercase tracking-wider text-slate-500"
    >
      Agent ID
    </label>

    <input
      id="agent-id"
      type="text"
      value={config?.agentId ?? ""}
      onChange={(event) => {
        onUpdateNode(node.id, {
          config: {
            ...(node.data.config as Record<string, unknown>),
            agentId: event.target.value,
          },
        });
      }}
      placeholder="Enter agent ID"
      className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-cyan-400/60"
    />
  </div>
)}
{node.data.type === "agent" && (
  <div>
    <label
      htmlFor="agent-prompt"
      className="text-[10px] font-bold uppercase tracking-wider text-slate-500"
    >
      Prompt
    </label>

    <textarea
      id="agent-prompt"
      value={config?.prompt ?? ""}
      onChange={(event) => {
        onUpdateNode(node.id, {
          config: {
            ...(node.data.config as Record<string, unknown>),
            prompt: event.target.value,
          },
        });
      }}
      placeholder="Enter the agent prompt"
      rows={5}
      className="mt-2 w-full resize-y rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-cyan-400/60"
    />
  </div>
)}
{node.data.type === "agent" && (
  <div>
    <label
      htmlFor="agent-temperature"
      className="text-[10px] font-bold uppercase tracking-wider text-slate-500"
    >
      Temperature
    </label>

    <input
      id="agent-temperature"
      type="number"
      min="0"
      max="1"
      step="0.1"
      value={config?.temperature ?? 0.7}
      onChange={(event) => {
        onUpdateNode(node.id, {
          config: {
            ...(node.data.config as Record<string, unknown>),
            temperature: Number(event.target.value),
          },
        });
      }}
      className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-cyan-400/60"
    />

    <p className="mt-1 text-[10px] text-slate-600">
      Range: 0–1
    </p>
  </div>
)}
{node.data.type === "agent" && (
  <div>
    <label
      htmlFor="agent-risk-score"
      className="text-[10px] font-bold uppercase tracking-wider text-slate-500"
    >
      Risk Score
    </label>

    <select
      id="agent-risk-score"
      value={config?.riskScore ?? "low"}
      onChange={(event) => {
        onUpdateNode(node.id, {
          config: {
            ...(node.data.config as Record<string, unknown>),
            riskScore: event.target.value,
          },
        });
      }}
      className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-cyan-400/60"
    >
      <option value="low">Low</option>
      <option value="medium">Medium</option>
      <option value="high">High</option>
      <option value="critical">Critical</option>
    </select>
  </div>
)}
{node.data.type === "condition" && (
  <div>
    <label
      htmlFor="condition-logic"
      className="text-[10px] font-bold uppercase tracking-wider text-slate-500"
    >
      Condition Logic
    </label>

    <textarea
      id="condition-logic"
      value={config?.conditionLogic ?? ""}
      onChange={(event) => {
        onUpdateNode(node.id, {
          config: {
            ...(node.data.config as Record<string, unknown>),
            conditionLogic: event.target.value,
          },
        });
      }}
      placeholder="Example: revenue > 10000"
      rows={4}
      className="mt-2 w-full resize-y rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-purple-400/60"
    />

    <p className="mt-1 text-[10px] text-slate-600">
      Define the logic used to evaluate this condition.
    </p>
  </div>
)}
{node.data.type === "hitl" && (
  <div>
    <label
      htmlFor="approval-role"
      className="text-[10px] font-bold uppercase tracking-wider text-slate-500"
    >
      Required Approval Role
    </label>

    <input
      id="approval-role"
      type="text"
      value={config?.requireApprovalRole ?? ""}
      onChange={(event) => {
        onUpdateNode(node.id, {
          config: {
            ...(node.data.config as Record<string, unknown>),
            requireApprovalRole: event.target.value,
          },
        });
      }}
      placeholder="Example: manager"
      className="mt-2 w-full rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none transition focus:border-rose-400/60"
    />

    <p className="mt-1 text-[10px] text-slate-600">
      Role required to approve this workflow step.
    </p>
  </div>
)}
      </div>
    </aside>
  );
}
