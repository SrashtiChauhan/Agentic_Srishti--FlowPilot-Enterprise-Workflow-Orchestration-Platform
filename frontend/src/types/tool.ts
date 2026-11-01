export type ToolCategory =
  | "security"
  | "cloud"
  | "communication";

export type ToolMode = "simulated";

export interface ToolPropertySchema {
  type: string;
  description?: string;
  enum?: string[];
  minimum?: number;
  maximum?: number;
  items?: ToolPropertySchema;
}

export interface ToolSchema {
  type: "object";
  properties: Record<string, ToolPropertySchema>;
  required: string[];
  additionalProperties: boolean;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  category: ToolCategory;
  mode: ToolMode;
  input_schema: ToolSchema;
  output_schema: ToolSchema;
}

export interface ToolsResponse {
  tools: Tool[];
}