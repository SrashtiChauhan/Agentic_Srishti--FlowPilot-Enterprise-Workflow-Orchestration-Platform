
export type AgentProvider = "ollama" | "huggingface" | "mistral";

export type AgentRiskScore = "low" | "medium" | "high" | "critical";

export interface Agent {
  id: string;
  name: string;
  description: string;
  provider: AgentProvider;
  model_name: string;
  system_prompt: string;
  temperature: number;
  tool_bindings: string[];
  risk_score: AgentRiskScore;
}

export interface AgentInput {
  name: string;
  description?: string;
  provider: AgentProvider;
  model_name: string;
  system_prompt: string;
  temperature: number;
  tool_bindings: string[];
  risk_score: AgentRiskScore;
}
