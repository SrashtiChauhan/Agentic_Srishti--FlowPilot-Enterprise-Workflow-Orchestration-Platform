"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { createAgent, getAgents, updateAgent, deleteAgent } from "@/lib/api";
import type { Agent, AgentInput } from "@/types/agent";



const emptyAgent: AgentInput = {
  name: "",
  description: "",
  provider: "ollama",
  model_name: "llama3.2",
  system_prompt: "",
  temperature: 0.2,
  tool_bindings: [],
  risk_score: "low",
};

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState<AgentInput>(emptyAgent);
  const [editingAgentId, setEditingAgentId] = useState<string | null>(null);

  const loadAgents = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const result = await getAgents();
      setAgents(result.agents);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load agents");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadAgents();
  }, [loadAgents]);

  async function handleCreate(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      if (editingAgentId) {
        await updateAgent(editingAgentId, form);
      } else {
        await createAgent(form);
      }

      setForm(emptyAgent);
      setEditingAgentId(null);
      setShowForm(false);
      await loadAgents();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save agent");
    } finally {
      setSaving(false);
    }
  }

  function handleEdit(agent: Agent) {
    setForm({
      name: agent.name,
      description: agent.description,
      provider: agent.provider,
      model_name: agent.model_name,
      system_prompt: agent.system_prompt,
      temperature: agent.temperature,
      tool_bindings: agent.tool_bindings,
      risk_score: agent.risk_score,
    });

    setEditingAgentId(agent.id);
    setShowForm(true);
    setError("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function handleDelete(agent: Agent) {
    const confirmed = window.confirm(
      `Delete "${agent.name}"? This action cannot be undone.`,
    );

    if (!confirmed) return;

    setError("");

    try {
      await deleteAgent(agent.id);
      await loadAgents();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete agent");
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-8 text-slate-100 md:px-10">
      <div className="mx-auto max-w-6xl">
        <header className="mb-10 flex flex-wrap items-center justify-between gap-4">
          <div>
            <Link
              href="/"
              className="mb-3 inline-block text-sm text-cyan-400 hover:text-cyan-300"
            >
              ← Back to dashboard
            </Link>
            <h1 className="text-3xl font-bold tracking-tight">Agent Studio</h1>
            <p className="mt-2 text-slate-400">
              Create and manage the AI agents used by your workflows.
            </p>
          </div>

          <button
            onClick={() => {
              if (showForm) {
                setShowForm(false);
                setEditingAgentId(null);
                setForm(emptyAgent);
              } else {
                setShowForm(true);
                setEditingAgentId(null);
                setForm(emptyAgent);
              }
            }}
            className="rounded-lg bg-cyan-500 px-4 py-2.5 font-semibold text-slate-950 hover:bg-cyan-400"
          >
            {showForm
              ? "Cancel"
              : editingAgentId
                ? "Edit Agent"
                : "+ Create Agent"}
          </button>
        </header>

        {error && (
          <div
            role="alert"
            className="mb-6 rounded-lg border border-rose-500/40 bg-rose-500/10 p-4 text-rose-300"
          >
            {error}
          </div>
        )}

        {showForm && (
          <form
            onSubmit={handleCreate}
            className="mb-8 grid gap-5 rounded-xl border border-slate-800 bg-slate-900/70 p-6 md:grid-cols-2"
          >
            <h2 className="text-lg font-semibold md:col-span-2">
              {editingAgentId ? "Edit Agent" : "Create New Agent"}
            </h2>
            <label className="grid gap-2 text-sm">
              Agent name
              <input
                required
                maxLength={100}
                value={form.name}
                onChange={(event) =>
                  setForm({ ...form, name: event.target.value })
                }
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5"
                placeholder="Security Analysis Agent"
              />
            </label>

            <label className="grid gap-2 text-sm">
              Description
              <input
                maxLength={500}
                value={form.description ?? ""}
                onChange={(event) =>
                  setForm({ ...form, description: event.target.value })
                }
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5"
                placeholder="What does this agent do?"
              />
            </label>

            <label className="grid gap-2 text-sm">
              Provider
              <select
                value={form.provider}
                onChange={(event) =>
                  setForm({
                    ...form,
                    provider: event.target.value as AgentInput["provider"],
                  })
                }
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5"
              >
                <option value="ollama">Ollama</option>
                <option value="huggingface">Hugging Face</option>
                <option value="mistral">Mistral</option>
              </select>
            </label>

            <label className="grid gap-2 text-sm">
              Model name
              <input
                required
                maxLength={200}
                value={form.model_name}
                onChange={(event) =>
                  setForm({ ...form, model_name: event.target.value })
                }
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5"
                placeholder="llama3.2"
              />
            </label>

            <label className="grid gap-2 text-sm md:col-span-2">
              System prompt
              <textarea
                required
                minLength={1}
                maxLength={10000}
                rows={5}
                value={form.system_prompt}
                onChange={(event) =>
                  setForm({ ...form, system_prompt: event.target.value })
                }
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5"
                placeholder="Define the agent's role, rules, and expected behavior..."
              />
            </label>

            <label className="grid gap-2 text-sm">
              Temperature: {form.temperature.toFixed(1)}
              <input
                type="range"
                min={0}
                max={1}
                step={0.1}
                value={form.temperature}
                onChange={(event) =>
                  setForm({
                    ...form,
                    temperature: Number(event.target.value),
                  })
                }
                className="accent-cyan-400"
              />
            </label>

            <label className="grid gap-2 text-sm">
              Risk score
              <select
                value={form.risk_score}
                onChange={(event) =>
                  setForm({
                    ...form,
                    risk_score: event.target.value as AgentInput["risk_score"],
                  })
                }
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2.5"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </label>

            <div className="md:col-span-2">
              <button
                type="submit"
                disabled={saving}
                className="rounded-lg bg-cyan-500 px-5 py-2.5 font-semibold text-slate-950 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {saving
                  ? "Saving..."
                  : editingAgentId
                    ? "Update Agent"
                    : "Save Agent"}
              </button>
            </div>
          </form>
        )}

        <section>
          <div className="mb-5 flex items-center justify-between">
            <h2 className="text-xl font-semibold">Your Agents</h2>
            <span className="text-sm text-slate-400">
              {agents.length} {agents.length === 1 ? "agent" : "agents"}
            </span>
          </div>

          {loading ? (
            <p className="text-slate-400">Loading agents...</p>
          ) : agents.length === 0 ? (
            <div className="rounded-xl border border-dashed border-slate-700 p-10 text-center">
              <p className="text-lg font-medium">No agents yet</p>
              <p className="mt-2 text-sm text-slate-400">
                Create your first agent to get started.
              </p>
            </div>
          ) : (
            <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
              {agents.map((agent) => (
                <article
                  key={agent.id}
                  className="rounded-xl border border-slate-800 bg-slate-900/70 p-5"
                >
                  <div className="mb-4 flex items-start justify-between gap-3">
                    <div>
                      <h3 className="font-semibold">{agent.name}</h3>
                      <p className="mt-1 text-xs text-slate-400">
                        {agent.provider} · {agent.model_name || "No model set"}
                      </p>
                    </div>
                    <span className="rounded-full border border-slate-700 px-2.5 py-1 text-xs capitalize">
                      {agent.risk_score}
                    </span>
                  </div>

                  <p className="mb-4 text-sm text-slate-300">
                    {agent.description || "No description provided."}
                  </p>

                  <p className="line-clamp-3 whitespace-pre-wrap text-xs text-slate-400">
                    {agent.system_prompt}
                  </p>

                  <div className="mt-5 border-t border-slate-800 pt-3">
                    <div className="mb-4 text-xs text-slate-500">
                      Temperature: {agent.temperature.toFixed(1)}
                      {" · "}
                      {agent.tool_bindings.length} tools
                    </div>

                    <div className="flex gap-3">
                      <button
                        type="button"
                        onClick={() => handleEdit(agent)}
                        className="flex-1 rounded-lg border border-cyan-500/40 px-3 py-2 text-sm text-cyan-300 hover:bg-cyan-500/10"
                      >
                        Edit
                      </button>

                      <button
                        type="button"
                        onClick={() => void handleDelete(agent)}
                        className="flex-1 rounded-lg border border-rose-500/40 px-3 py-2 text-sm text-rose-300 hover:bg-rose-500/10"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
