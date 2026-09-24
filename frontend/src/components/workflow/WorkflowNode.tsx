"use client";

import {
  Handle,
  NodeResizer,
  Position,
  type Node,
  type NodeProps,
} from "@xyflow/react";

type WorkflowNodeData = {
  title: string;
  subtitle?: string;
  type: string;
  status:
    | "idle"
    | "running"
    | "completed"
    | "failed"
    | "waiting_approval";
};

type WorkflowNodeType = Node<WorkflowNodeData>;



const nodeStyles: Record<string, string> = {
  trigger: "border-amber-400/60 shadow-amber-500/10",
  agent: "border-cyan-400/60 shadow-cyan-500/10",
  condition: "border-purple-400/60 shadow-purple-500/10",
  hitl: "border-rose-400/60 shadow-rose-500/10",
  action: "border-emerald-400/60 shadow-emerald-500/10",
};

const badgeStyles: Record<string, string> = {
  trigger: "bg-amber-400/10 text-amber-400",
  agent: "bg-cyan-400/10 text-cyan-400",
  condition: "bg-purple-400/10 text-purple-400",
  hitl: "bg-rose-400/10 text-rose-400",
  action: "bg-emerald-400/10 text-emerald-400",
};

export default function WorkflowNode({
  data,
  selected,
}: NodeProps<WorkflowNodeType>) {
  const nodeType = data.type ?? "action";

  return (
    <>
      <NodeResizer
        minWidth={220}
        minHeight={140}
        isVisible={selected}
        lineClassName="!border-cyan-400/50"
        handleClassName="!h-2 !w-2 !border-cyan-400 !bg-slate-950"
      />

      <div
        className={`h-full min-w-56 rounded-xl border bg-slate-900/95 p-4 shadow-lg backdrop-blur-md ${
          nodeStyles[nodeType] ?? nodeStyles.action
        }`}
      >
        <Handle
          type="target"
          position={Position.Top}
          className="!h-2 !w-2 !border-0 !bg-slate-400"
        />

        <div
          className={`mb-3 inline-flex rounded-md px-2 py-1 text-[10px] font-bold uppercase tracking-wider ${
            badgeStyles[nodeType] ?? badgeStyles.action
          }`}
        >
          {nodeType}
        </div>

        <h3 className="text-sm font-semibold text-slate-100">
          {data.title}
        </h3>

        <p className="mt-1 text-xs text-slate-400">
          {data.subtitle ?? "Workflow node"}
        </p>

        <div className="mt-3 border-t border-slate-800 pt-3">
          <span className="font-mono text-[11px] text-slate-500">
            Status: Idle
          </span>
        </div>

        <Handle
          type="source"
          position={Position.Bottom}
          className="!h-2 !w-2 !border-0 !bg-slate-400"
        />
      </div>
    </>
  );
}