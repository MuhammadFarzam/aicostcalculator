from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class CostRequest(BaseModel):
    model: str
    input_tokens_per_request: int
    output_tokens_per_request: int
    requests_per_day: int
    days_per_month: int
    budget_limit: float
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
    models: list[ModelCost]
    savings_opportunities: list[SavingsSuggestion]
    within_budget: bool


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
        models=models,
        savings_opportunities=savings,
        within_budget=total_monthly_cost <= payload.budget_limit,
    )