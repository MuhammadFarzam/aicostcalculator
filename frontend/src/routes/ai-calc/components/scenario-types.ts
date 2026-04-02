import type { TokenUnit, ModelId } from "./types";

export function unitMultiplier(unit: TokenUnit) {
  if (unit === "K") return 1_000;
  if (unit === "M") return 1_000_000;
  if (unit === "B") return 1_000_000_000;
  return 1;
}

export function tokensValue(base: number, unit: TokenUnit) {
  return Math.max(0, Math.floor(Number(base) * unitMultiplier(unit)));
}

export type Scenario1Request = {
  users_per_day: number;
  messages_per_user: number;
  chatbot_type: "simple_faq" | "standard_assistant" | "advanced_assistant" | "custom" | "none";
  avg_input_tokens_per_message: number;
  avg_output_tokens_per_response: number;
  selected_models: ModelId[];
  days_per_month: number;
  quality_preference: "low_cost" | "balanced" | "high_quality";
};

export type Scenario1Response = {
  monthly_cost: number;
  cost_per_conversation: number;
  usage_breakdown: { requests: number; tokens_per_request: number };
  insight: string;
  comparison_table: { model: string; monthly_cost: number; quality: string; score: number; label: string }[];
  recommendation: string;
  hybrid_strategy: null | { allocations: Record<string, number>; new_cost: number; savings: number };
};

export type Scenario2Request = {
  users_per_day: number;
  messages_per_user: number;
  avg_input_tokens_per_message: number;
  avg_output_tokens_per_response: number;
  days_per_month: number;
  retry_rate: number;
  extra_output_growth: number;
  memory_multiplier: number;
  system_prompt_size: number;
};

export type Scenario2Response = {
  base_cost: number;
  hidden_costs: number;
  total_cost: number;
  hidden_cost_sources: Record<string, number>;
  alert: string;
  suggestions: string[];
  optimization_preview: { new_cost: number; savings: number };
};

export type Scenario3Request = {
  content_type: "blog" | "ads" | "email" | "product_description";
  number_of_outputs: number;
  words_per_output: number;
  avg_input_tokens_per_message: number;
  avg_output_tokens_per_response: number;
  selected_models: ModelId[];
  days_per_month: number;
  quality_preference: "low_cost" | "balanced" | "high_quality";
};

export type Scenario3Response = {
  total_campaign_cost: number;
  cost_per_content: number;
  model_costs: Record<string, number>;
  suggestions: string[];
  scenario_planning: { new_cost: number; savings: number };
  scaling_insight: string;
};

export type Scenario4Request = {
  users_per_day: number;
  messages_per_user: number;
  days_per_month: number;
  avg_input_tokens_per_message: number;
  avg_output_tokens_per_response: number;
  selected_models: ModelId[];
  quality_preference: "low_cost" | "balanced" | "high_quality";
  revenue_per_conversion: number;
  conversion_rate: number;
  subscription_price: number;
  cost_budget: number;
};

export type Scenario4Response = {
  revenue: number;
  cost: number;
  profit: number;
  roi_percent: number;
  business_insight: string;
  risk_alert: string | null;
  recommendation: string[];
  simulation: Record<string, number>;
};

