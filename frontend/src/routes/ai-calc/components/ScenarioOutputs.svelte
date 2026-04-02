<script lang="ts">
  import type {
    Scenario1Response,
    Scenario2Response,
    Scenario3Response,
    Scenario4Response,
  } from "./scenario-types";

  const props = $props<{
    scenario: 1 | 2 | 3 | 4;
    loading?: boolean;
    error?: string | null;
    s1?: Scenario1Response | null;
    s2?: Scenario2Response | null;
    s3?: Scenario3Response | null;
    s4?: Scenario4Response | null;
  }>();

  function stars(score: number) {
    return "⭐".repeat(Math.max(0, Math.min(5, score)));
  }
</script>

<section class="outputs">
  <div class="card">
    <h2>Results</h2>
    {#if props.error}
      <p class="error-text">{props.error}</p>
    {:else if props.loading}
      <p class="placeholder-text">Calculating…</p>
    {:else if props.scenario === 1 && props.s1}
      <div class="result-block">
        <div class="result-title">💰 1. Monthly Cost</div>
        <div class="result-value">
          $ {props.s1.monthly_cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}
        </div>
      </div>

      <div class="result-block">
        <div class="result-title">📊 Usage Breakdown</div>
        <ul class="result-list">
          <li><strong>Requests:</strong> {props.s1.usage_breakdown.requests.toLocaleString()}</li>
          <li><strong>Tokens per request:</strong> {props.s1.usage_breakdown.tokens_per_request.toLocaleString()}</li>
        </ul>
      </div>

      <div class="result-block">
        <div class="result-title">💡 2. Insight</div>
        <div class="result-text">{props.s1.insight}</div>
      </div>

      <div class="result-block">
        <div class="result-title">3. Comparison Table</div>
        <div class="table">
          <div class="table-row table-header">
            <div>Model</div>
            <div>Monthly Cost</div>
            <div>Quality</div>
            <div>Score</div>
          </div>
          {#each props.s1.comparison_table as row}
            <div class="table-row">
              <div>{row.model}</div>
              <div>$ {row.monthly_cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}</div>
              <div>{row.quality}</div>
              <div>{stars(row.score)} <span class="muted-text">({row.label})</span></div>
            </div>
          {/each}
        </div>
      </div>

      <div class="result-block highlight">
        <div class="result-title">🏆 4. Smart Recommendation</div>
        <div class="result-text">{props.s1.recommendation}</div>
      </div>

      {#if props.s1.hybrid_strategy}
        <div class="result-block">
          <div class="result-title">🔄 5. Hybrid Strategy</div>
          <ul class="result-list">
            {#each Object.entries(props.s1.hybrid_strategy.allocations) as [model, pct]}
              <li><strong>{pct}%</strong> requests → {model}</li>
            {/each}
            <li>
              <strong>New Cost:</strong>
              $ {props.s1.hybrid_strategy.new_cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}
            </li>
            <li>
              <strong>Savings:</strong>
              <span class="good-text">
                $ {props.s1.hybrid_strategy.savings.toLocaleString(undefined, { maximumFractionDigits: 2 })}/month
              </span>
            </li>
          </ul>
          <button type="button" class="secondary-button">Apply Optimization</button>
        </div>
      {/if}
    {:else if props.scenario === 2 && props.s2}
      <div class="result-block">
        <div class="result-title">💰 1. Cost Breakdown</div>
        <ul class="result-list">
          <li><strong>Base Cost:</strong> $ {props.s2.base_cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          <li><strong>Hidden Costs:</strong> $ {props.s2.hidden_costs.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          <li><strong>Total Cost:</strong> $ {props.s2.total_cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
        </ul>
      </div>

      <div class="result-block">
        <div class="result-title">🔍 2. Detailed Breakdown</div>
        <ul class="result-list">
          {#each Object.entries(props.s2.hidden_cost_sources) as [k, v]}
            <li><strong>{k}:</strong> $ {v.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          {/each}
        </ul>
      </div>

      <div class="result-block warning">
        <div class="result-title">⚠️ 3. Alert</div>
        <div class="result-text">{props.s2.alert}</div>
      </div>

      <div class="result-block highlight">
        <div class="result-title">💡 4. Actionable Suggestions</div>
        <ul class="result-list">
          {#each props.s2.suggestions as sug}
            <li>{sug}</li>
          {/each}
        </ul>
      </div>

      <div class="result-block">
        <div class="result-title">📉 5. Optimization Preview</div>
        <ul class="result-list">
          <li><strong>New Cost:</strong> $ {props.s2.optimization_preview.new_cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          <li><strong>Savings:</strong> <span class="good-text">$ {props.s2.optimization_preview.savings.toLocaleString(undefined, { maximumFractionDigits: 2 })}/month</span></li>
        </ul>
      </div>
    {:else if props.scenario === 3 && props.s3}
      <div class="result-block">
        <div class="result-title">💰 1. Campaign Cost Summary</div>
        <ul class="result-list">
          <li><strong>Total Campaign Cost:</strong> $ {props.s3.total_campaign_cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          <li><strong>Cost per Content:</strong> $ {props.s3.cost_per_content.toLocaleString(undefined, { maximumFractionDigits: 4 })}</li>
        </ul>
      </div>

      <div class="result-block">
        <div class="result-title">📊 2. Model Comparison</div>
        <ul class="result-list">
          {#each Object.entries(props.s3.model_costs) as [m, c]}
            <li><strong>{m}:</strong> $ {c.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          {/each}
        </ul>
      </div>

      <div class="result-block highlight">
        <div class="result-title">💡 3. Optimization Suggestions</div>
        <ul class="result-list">
          {#each props.s3.suggestions as sug}
            <li>{sug}</li>
          {/each}
        </ul>
      </div>

      <div class="result-block">
        <div class="result-title">🔄 4. Scenario Planning</div>
        <ul class="result-list">
          <li><strong>New Cost:</strong> $ {props.s3.scenario_planning.new_cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          <li><strong>Savings:</strong> <span class="good-text">$ {props.s3.scenario_planning.savings.toLocaleString(undefined, { maximumFractionDigits: 2 })}</span></li>
        </ul>
      </div>

      <div class="result-block">
        <div class="result-title">📈 5. Cost Scaling Insight</div>
        <div class="result-text">{props.s3.scaling_insight}</div>
      </div>
    {:else if props.scenario === 4 && props.s4}
      <div class="result-block">
        <div class="result-title">💰 1. Profit Summary</div>
        <ul class="result-list">
          <li><strong>Revenue:</strong> $ {props.s4.revenue.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          <li><strong>Cost:</strong> $ {props.s4.cost.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          <li><strong>Profit:</strong> $ {props.s4.profit.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          <li>
            <strong>ROI:</strong>
            <span class:good-text={props.s4.roi_percent >= 0} class:bad-text={props.s4.roi_percent < 0}>
              {props.s4.roi_percent}%
            </span>
          </li>
        </ul>
      </div>

      <div class="result-block">
        <div class="result-title">📊 2. Business Insight</div>
        <div class="result-text">{props.s4.business_insight}</div>
      </div>

      {#if props.s4.risk_alert}
        <div class="result-block warning">
          <div class="result-title">⚠️ 3. Risk Alert</div>
          <div class="result-text">{props.s4.risk_alert}</div>
        </div>
      {/if}

      <div class="result-block highlight">
        <div class="result-title">💡 4. Smart Recommendation</div>
        <ul class="result-list">
          {#each props.s4.recommendation as rec}
            <li>{rec}</li>
          {/each}
        </ul>
      </div>

      <div class="result-block">
        <div class="result-title">🔄 5. Scenario Simulation</div>
        <ul class="result-list">
          {#each Object.entries(props.s4.simulation) as [k, v]}
            <li><strong>{k.replaceAll("_", " ")}:</strong> {v.toLocaleString(undefined, { maximumFractionDigits: 2 })}</li>
          {/each}
        </ul>
      </div>
    {:else}
      <p class="placeholder-text">Pick a scenario and click Calculate.</p>
    {/if}
  </div>
</section>

