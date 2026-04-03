from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
import tiktoken
class CostRequest(BaseModel):
    model: str = Field(..., description="Model id, e.g. gpt-4, gpt-3.5, claude")
    input_tokens_per_request: int = Field(..., ge=0)
    output_tokens_per_request: int = Field(..., ge=0)
    requests_per_day: int = Field(..., ge=0)
    days_per_month: int = Field(..., ge=0, le=31)
    budget_limit: float = Field(..., ge=0)
    multi_model_usage: bool = False
    summarization_enabled: bool = False
    quality: int = 80


class ModelCost(BaseModel):
    name: str
    input_cost: float
    output_cost: float
    total_cost: float


class SavingsSuggestion(BaseModel):
    description: str
    monthly_saving: float


class CostResponse(BaseModel):
    total_monthly_cost: float
    cost_per_request: float
    models: list[ModelCost]
    savings_opportunities: list[SavingsSuggestion]
    within_budget: bool


class Scenario1Request(BaseModel):
    users_per_day: int = Field(..., ge=0)
    messages_per_user: int = Field(..., ge=0)
    chatbot_type: str = Field(
        ...,
        pattern="^(simple_faq|standard_assistant|advanced_assistant|custom|none)$",
    )
    avg_input_tokens_per_message: int = Field(..., ge=0)
    avg_output_tokens_per_response: int = Field(..., ge=0)
    selected_models: list[str] = Field(default_factory=list)
    days_per_month: int = Field(..., ge=0, le=31)
    quality_preference: str = Field("balanced", pattern="^(low_cost|balanced|high_quality)$")


class Scenario1UsageBreakdown(BaseModel):
    requests: int
    tokens_per_request: int


class Scenario1ComparisonRow(BaseModel):
    model: str
    monthly_cost: float
    quality: str
    score: int = Field(..., ge=1, le=5)
    label: str


class Scenario1HybridStrategy(BaseModel):
    allocations: dict[str, int] = Field(..., description="model -> percent")
    new_cost: float
    savings: float


class Scenario1Response(BaseModel):
    monthly_cost: float
    cost_per_conversation: float
    usage_breakdown: Scenario1UsageBreakdown
    insight: str
    comparison_table: list[Scenario1ComparisonRow]
    recommendation: str
    hybrid_strategy: Scenario1HybridStrategy | None = None


class Scenario2Request(BaseModel):
    users_per_day: int = Field(..., ge=0)
    messages_per_user: int = Field(..., ge=0)
    avg_input_tokens_per_message: int = Field(..., ge=0)
    avg_output_tokens_per_response: int = Field(..., ge=0)
    days_per_month: int = Field(..., ge=0, le=31)
    retry_rate: float = Field(..., ge=0, le=100)
    extra_output_growth: float = Field(..., ge=0, le=100)
    memory_multiplier: float = Field(..., ge=1)
    system_prompt_size: int = Field(..., ge=0)


class Scenario2Response(BaseModel):
    base_cost: float
    hidden_costs: float
    total_cost: float
    hidden_cost_sources: dict[str, float]
    alert: str
    suggestions: list[str]
    optimization_preview: dict[str, float]


class Scenario3Request(BaseModel):
    content_type: str = Field(..., pattern="^(blog|ads|email|product_description)$")
    number_of_outputs: int = Field(..., ge=0)
    words_per_output: int = Field(..., ge=0)
    avg_input_tokens_per_message: int = Field(..., ge=0)
    avg_output_tokens_per_response: int = Field(..., ge=0)
    selected_models: list[str] = Field(default_factory=list)
    days_per_month: int = Field(..., ge=0, le=31)
    quality_preference: str = Field("balanced", pattern="^(low_cost|balanced|high_quality)$")


class Scenario3Response(BaseModel):
    total_campaign_cost: float
    cost_per_content: float
    model_costs: dict[str, float]
    suggestions: list[str]
    scenario_planning: dict[str, float]
    scaling_insight: str


class Scenario4Request(BaseModel):
    users_per_day: int = Field(..., ge=0)
    messages_per_user: int = Field(..., ge=0)
    days_per_month: int = Field(..., ge=0, le=31)
    avg_input_tokens_per_message: int = Field(..., ge=0)
    avg_output_tokens_per_response: int = Field(..., ge=0)
    selected_models: list[str] = Field(default_factory=list)
    quality_preference: str = Field("balanced", pattern="^(low_cost|balanced|high_quality)$")
    revenue_per_conversion: float = Field(..., ge=0)
    conversion_rate: float = Field(..., ge=0, le=100)
    subscription_price: float = Field(..., ge=0)
    cost_budget: float = Field(..., ge=0)


class Scenario4Response(BaseModel):
    revenue: float
    cost: float
    profit: float
    roi_percent: float
    business_insight: str
    risk_alert: str | None = None
    recommendation: list[str]
    simulation: dict[str, float]


class Scenario5Request(BaseModel):
    revenue_per_request: float = Field(..., ge=0)
    conversion_rate: float = Field(..., ge=0, le=100)
    cost_budget: float = Field(..., ge=0)


class TokenizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Input text to tokenize")
    model: str = Field(
        default="gpt-4o",
        description="Model name (gpt-4o, gpt-4, gpt-3.5)",
    )
    mode: Literal["text", "ids", "both"] = Field(
        default="both",
        description="Return decoded tokens, token IDs, or both",
    )
    include_colors: bool = Field(
        default=True,
        description="Include color mapping for UI",
    )

# -----------------------------
# Response Model
# -----------------------------
class TokenItem(BaseModel):
    text: Optional[str] = None
    token_id: Optional[int] = None
    color: Optional[str] = None


class TokenizeResponse(BaseModel):
    token_count: int
    char_count: int
    tokens: List[TokenItem]



app = FastAPI(title="AI Cost Optimizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/api/tokenize", response_model=TokenizeResponse)
def tokenize_text(payload: TokenizeRequest) -> TokenizeResponse:
    """
    Simple tokenization endpoint for UI.
    Uses tiktoken to approximate tokenization for the selected model.
    """
    try:
        enc = tiktoken.encoding_for_model(payload.model)
    except Exception:
        # Fallback to a generic encoding if model-specific not available
        enc = tiktoken.get_encoding("cl100k_base")

    ids = enc.encode(payload.text)
    decoded = enc.decode_tokens_bytes(ids)

    colors_palette = [
        "#22c55e",
        "#0ea5e9",
        "#a855f7",
        "#f97316",
        "#eab308",
        "#ec4899",
    ]

    tokens: List[TokenItem] = []
    for idx, (raw, tok_id) in enumerate(zip(decoded, ids)):
        text = raw.decode("utf-8", errors="ignore")
        color = None
        if payload.include_colors:
            color = colors_palette[idx % len(colors_palette)]
        item = TokenItem(
            text=text if payload.mode in ("text", "both") else None,
            token_id=tok_id if payload.mode in ("ids", "both") else None,
            color=color,
        )
        tokens.append(item)

    return TokenizeResponse(
        token_count=len(ids),
        char_count=len(payload.text),
        tokens=tokens,
    )


@app.post("/api/calculate", response_model=CostResponse)
def calculate_cost(payload: CostRequest) -> CostResponse:
    # Simple example pricing assumptions (USD per 1K tokens)
    pricing = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-3.5": {"input": 0.001, "output": 0.002},
        "claude": {"input": 0.008, "output": 0.024},
    }

    selected = pricing.get(payload.model, pricing["gpt-4"])

    requests_per_month = payload.requests_per_day * payload.days_per_month
    total_input_tokens = payload.input_tokens_per_request * requests_per_month
    total_output_tokens = payload.output_tokens_per_request * requests_per_month

    def token_cost(rate_per_1k: float, tokens: int) -> float:
        return (tokens / 1000.0) * rate_per_1k

    gpt4_input_cost = token_cost(pricing["gpt-4"]["input"], total_input_tokens)
    gpt4_output_cost = token_cost(pricing["gpt-4"]["output"], total_output_tokens)
    gpt4_total = gpt4_input_cost + gpt4_output_cost

    gpt35_input_cost = token_cost(pricing["gpt-3.5"]["input"], total_input_tokens)
    gpt35_output_cost = token_cost(pricing["gpt-3.5"]["output"], total_output_tokens)
    gpt35_total = gpt35_input_cost + gpt35_output_cost

    total_monthly_cost = gpt4_total

    # Example savings estimations
    switch_half_to_35_saving = (gpt4_total - ((gpt4_total + gpt35_total) / 2.0))
    reduce_output_tokens_saving = token_cost(
        pricing["gpt-4"]["output"],
        (payload.output_tokens_per_request - 1000) * requests_per_month
        if payload.output_tokens_per_request > 1000
        else 0,
    )

    models = [
        ModelCost(
            name="GPT-4",
            input_cost=round(gpt4_input_cost, 2),
            output_cost=round(gpt4_output_cost, 2),
            total_cost=round(gpt4_total, 2),
        ),
        ModelCost(
            name="GPT-3.5",
            input_cost=round(gpt35_input_cost, 2),
            output_cost=round(gpt35_output_cost, 2),
            total_cost=round(gpt35_total, 2),
        ),
    ]

    savings = [
        SavingsSuggestion(
            description="Switch 50% of GPT-4 tasks to GPT-3.5",
            monthly_saving=round(max(switch_half_to_35_saving, 0.0), 2),
        ),
        SavingsSuggestion(
            description="Reduce average output tokens from 1500 to 1000",
            monthly_saving=round(max(reduce_output_tokens_saving, 0.0), 2),
        ),
    ]

    return CostResponse(
        total_monthly_cost=round(total_monthly_cost, 2),
        cost_per_request=round(total_monthly_cost / requests_per_month, 4)
        if requests_per_month > 0
        else 0.0,
        models=models,
        savings_opportunities=savings,
        within_budget=total_monthly_cost <= payload.budget_limit,
    )


def _pricing():
    return {
        "gpt-4": {"input": 0.03, "output": 0.06, "quality": (5, "Best Quality")},
        "claude": {"input": 0.008, "output": 0.024, "quality": (4, "Best Value")},
        "gemini": {"input": 0.004, "output": 0.012, "quality": (3, "Balanced")},
        "gpt-3.5": {"input": 0.001, "output": 0.002, "quality": (2, "Cheapest")},
    }


def _token_cost(rate_per_1k: float, tokens: int) -> float:
    return (tokens / 1000.0) * rate_per_1k


@app.post("/api/scenario1/estimate-chatbot-cost", response_model=Scenario1Response)
def scenario1_estimate_chatbot_cost(payload: Scenario1Request) -> Scenario1Response:
    pricing = _pricing()

    presets = {
        "simple_faq": (50, 150),
        "standard_assistant": (100, 300),
        "advanced_assistant": (200, 800),
    }

    # Requests ~= users * messages * days
    requests = payload.users_per_day * payload.messages_per_user * payload.days_per_month

    input_tokens = payload.avg_input_tokens_per_message
    output_tokens = payload.avg_output_tokens_per_response
    tokens_per_request = input_tokens + output_tokens

    selected_models = payload.selected_models or ["gpt-4"]

    comparison: list[Scenario1ComparisonRow] = []
    for mid in selected_models:
        if mid not in pricing:
            continue
        rates = pricing[mid]
        monthly_input_cost = _token_cost(rates["input"], input_tokens * requests)
        monthly_output_cost = _token_cost(rates["output"], output_tokens * requests)
        monthly_cost = monthly_input_cost + monthly_output_cost
        score, label = rates["quality"]
        quality = "High" if score >= 5 else "Medium" if score >= 3 else "Low"
        comparison.append(
            Scenario1ComparisonRow(
                model=mid.upper(),
                monthly_cost=round(monthly_cost, 2),
                quality=quality,
                score=score,
                label=label,
            )
        )

    # Pick best value recommendation: prefer Claude if present, else cheapest
    recommendation = ""
    if any(r.model == "CLAUDE" for r in comparison):
        base = next((r for r in comparison if r.model == "GPT-4"), None)
        claude = next((r for r in comparison if r.model == "CLAUDE"), None)
        if base and claude:
            recommendation = (
                f"Use Claude for most requests → Save ${round(base.monthly_cost - claude.monthly_cost,2)}/month "
                "→ Minimal quality loss. Use GPT-4 only for complex queries."
            )
    if not recommendation and comparison:
        cheapest = sorted(comparison, key=lambda r: r.monthly_cost)[0]
        recommendation = f"Start with {cheapest.model} to minimize cost, then upgrade selective flows for quality."

    # Hybrid strategy (only if Claude + GPT-4 both selected)
    hybrid = None
    gpt4 = next((r for r in comparison if r.model == "GPT-4"), None)
    claude = next((r for r in comparison if r.model == "CLAUDE"), None)
    if gpt4 and claude:
        new_cost = (0.7 * claude.monthly_cost) + (0.3 * gpt4.monthly_cost)
        best_current = min(gpt4.monthly_cost, claude.monthly_cost)
        savings_amt = max(gpt4.monthly_cost - new_cost, 0.0)
        hybrid = Scenario1HybridStrategy(
            allocations={"CLAUDE": 70, "GPT-4": 30},
            new_cost=round(new_cost, 2),
            savings=round(savings_amt, 2),
        )

    # Use first model as "current" for summary cost (fallback GPT-4)
    summary_cost = comparison[0].monthly_cost if comparison else 0.0
    cost_per_conversation = (summary_cost / requests) if requests else 0.0

    chatbot_note = ""
    if payload.chatbot_type in presets and payload.chatbot_type != "custom":
        preset_in, preset_out = presets[payload.chatbot_type]
        chatbot_note = (
            f"Preset selected: {payload.chatbot_type.replace('_',' ').title()} "
            f"({preset_in} in / {preset_out} out tokens per message)"
        )
    if payload.chatbot_type == "none":
        chatbot_note = "No chatbot preset selected. Using your custom token inputs."

    return Scenario1Response(
        monthly_cost=round(summary_cost, 2),
        cost_per_conversation=round(cost_per_conversation, 4),
        usage_breakdown=Scenario1UsageBreakdown(
            requests=requests,
            tokens_per_request=tokens_per_request,
        ),
        insight=(
            f"Your chatbot costs ~${round(cost_per_conversation,2)} per conversation. "
            + (chatbot_note if chatbot_note else "")
        ).strip(),
        comparison_table=sorted(comparison, key=lambda r: r.monthly_cost, reverse=True),
        recommendation=recommendation,
        hybrid_strategy=hybrid,
    )


@app.post("/api/scenario2/hidden-costs", response_model=Scenario2Response)
def scenario2_hidden_costs(payload: Scenario2Request) -> Scenario2Response:
    pricing = _pricing()["gpt-4"]
    requests = payload.users_per_day * payload.messages_per_user * payload.days_per_month
    base_input = payload.avg_input_tokens_per_message * requests
    base_output = payload.avg_output_tokens_per_response * requests
    base_cost = _token_cost(pricing["input"], base_input) + _token_cost(pricing["output"], base_output)

    retry_multiplier = 1 + (payload.retry_rate / 100.0)
    growth_multiplier = 1 + (payload.extra_output_growth / 100.0)
    memory_multiplier = payload.memory_multiplier
    system_prompt_tokens = payload.system_prompt_size * requests

    hidden_retry = base_cost * (retry_multiplier - 1)
    hidden_growth = _token_cost(pricing["output"], int(base_output * (growth_multiplier - 1)))
    hidden_memory = base_cost * (memory_multiplier - 1)
    hidden_prompt = _token_cost(pricing["input"], system_prompt_tokens)

    hidden_total = hidden_retry + hidden_growth + hidden_memory + hidden_prompt
    total = base_cost + hidden_total

    suggestions = [
        "Reduce retry rate by improving timeouts and validation (aim for 3%).",
        "Limit response length with hard caps and structured outputs.",
        "Trim conversation memory window (summarize older context).",
        "Shrink system prompts; move policy text to server-side tooling.",
    ]

    optimized_total = base_cost + (hidden_total * 0.25)
    return Scenario2Response(
        base_cost=round(base_cost, 2),
        hidden_costs=round(hidden_total, 2),
        total_cost=round(total, 2),
        hidden_cost_sources={
            "Retries": round(hidden_retry, 2),
            "Long Responses": round(hidden_growth, 2),
            "Memory Growth": round(hidden_memory, 2),
            "System Prompts": round(hidden_prompt, 2),
        },
        alert=f"You are losing {round((hidden_total / total) * 100, 1) if total else 0}% extra cost due to inefficiencies.",
        suggestions=suggestions,
        optimization_preview={
            "new_cost": round(optimized_total, 2),
            "savings": round(total - optimized_total, 2),
        },
    )


@app.post("/api/scenario3/bulk-usage", response_model=Scenario3Response)
def scenario3_bulk_usage(payload: Scenario3Request) -> Scenario3Response:
    pricing = _pricing()
    selected = payload.selected_models or ["claude"]
    # rough estimate tokens from words
    output_tokens = int(payload.words_per_output * 1.3)
    input_tokens = payload.avg_input_tokens_per_message
    requests = payload.number_of_outputs

    model_costs: dict[str, float] = {}
    for mid in selected:
        if mid not in pricing:
            continue
        rates = pricing[mid]
        cost = _token_cost(rates["input"], input_tokens * requests) + _token_cost(
            rates["output"], output_tokens * requests
        )
        model_costs[mid.upper()] = round(cost, 2)

    total = model_costs[sorted(model_costs.keys())[0]] if model_costs else 0.0
    cost_per = (total / requests) if requests else 0.0

    reduced_words_tokens = int((payload.words_per_output * 0.75) * 1.3)  # 800->600 style
    reduced_cost = _token_cost(pricing["claude"]["input"], input_tokens * requests) + _token_cost(
        pricing["claude"]["output"], reduced_words_tokens * requests
    )

    return Scenario3Response(
        total_campaign_cost=round(total, 2),
        cost_per_content=round(cost_per, 4),
        model_costs=model_costs,
        suggestions=[
            "Switch to Claude for most bulk content.",
            "Reduce word count for non-premium content.",
            "Use GPT-4 only for premium / high-impact outputs.",
        ],
        scenario_planning={"new_cost": round(reduced_cost, 2), "savings": round(total - reduced_cost, 2)},
        scaling_insight=f"Generating 50,000 outputs will cost ≈ ${round(cost_per * 50000,2)}",
    )


@app.post("/api/scenario4/roi", response_model=Scenario4Response)
def scenario4_roi(payload: Scenario4Request) -> Scenario4Response:
    pricing = _pricing()
    selected = payload.selected_models or ["claude"]
    # approximate requests
    requests = payload.users_per_day * payload.messages_per_user * payload.days_per_month
    input_tokens = payload.avg_input_tokens_per_message
    output_tokens = payload.avg_output_tokens_per_response

    # choose cheapest selected model for cost
    costs = []
    for mid in selected:
        if mid not in pricing:
            continue
        rates = pricing[mid]
        cost = _token_cost(rates["input"], input_tokens * requests) + _token_cost(
            rates["output"], output_tokens * requests
        )
        costs.append(cost)
    cost = min(costs) if costs else 0.0

    conversions = requests * (payload.conversion_rate / 100.0)
    revenue = conversions * payload.revenue_per_conversion
    # include subscription revenue (rough: conversions become subscribers)
    revenue += conversions * payload.subscription_price

    profit = revenue - cost
    roi = (profit / cost * 100.0) if cost else 0.0

    risk = None
    if payload.conversion_rate <= 2:
        risk = "If conversion drops further, profitability may turn negative."

    # simulate doubling users
    sim_requests = (payload.users_per_day * 2) * payload.messages_per_user * payload.days_per_month
    sim_cost = min(costs) * 2 if costs else 0.0
    sim_conversions = sim_requests * (payload.conversion_rate / 100.0)
    sim_revenue = sim_conversions * (payload.revenue_per_conversion + payload.subscription_price)
    sim_profit = sim_revenue - sim_cost

    return Scenario4Response(
        revenue=round(revenue, 2),
        cost=round(cost, 2),
        profit=round(profit, 2),
        roi_percent=round(roi, 1),
        business_insight="✅ Your AI feature is highly profitable" if profit > 0 else "❌ Your AI feature is not profitable yet",
        risk_alert=risk,
        recommendation=[
            "Scale usage if ROI remains positive.",
            "Invest in acquisition only after stabilizing conversion.",
        ],
        simulation={
            "users_per_day": payload.users_per_day * 2,
            "revenue": round(sim_revenue, 2),
            "cost": round(sim_cost, 2),
            "profit": round(sim_profit, 2),
        },
    )


