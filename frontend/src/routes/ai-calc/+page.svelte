<script lang="ts">
  import { onMount } from "svelte";
  import "./ai-calc.css";
  let selectedModel = $state("gpt-4");
  let inputTokens = $state(500);
  let inputTokenUnit = $state<"1" | "K" | "M" | "B">("1");
  let outputTokens = $state(1500);
  let outputTokenUnit = $state<"1" | "K" | "M" | "B">("1");
  let requestsPerDay = $state(100);
  let daysPerMonth = $state(30);
  let budgetLimit = $state(2000);
  let showAdvanced = $state(false);

  let multiModelUsage = $state(false);
  let summarizationEnabled = $state(false);
  let quality = $state(80);

  let totalMonthlyCost = $state<number | null>(null);
  let models = $state<
    { name: string; input_cost: number; output_cost: number; total_cost: number }[]
  >([]);
  let savings = $state<{ description: string; monthly_saving: number }[]>([]);
  let withinBudget = $state<boolean | null>(null);
  let loading = $state(false);
  let error = $state<string | null>(null);

  function unitMultiplier(unit: "1" | "K" | "M" | "B") {
    if (unit === "K") return 1_000;
    if (unit === "M") return 1_000_000;
    if (unit === "B") return 1_000_000_000;
    return 1;
  }

  function tokensValue(base: number, unit: "1" | "K" | "M" | "B") {
    return Math.max(0, Math.floor(Number(base) * unitMultiplier(unit)));
  }

  async function recalculate() {
    loading = true;
    error = null;

    try {
      const res = await fetch("/api/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: selectedModel,
          input_tokens_per_request: tokensValue(inputTokens, inputTokenUnit),
          output_tokens_per_request: tokensValue(outputTokens, outputTokenUnit),
          requests_per_day: Number(requestsPerDay),
          days_per_month: Number(daysPerMonth),
          budget_limit: Number(budgetLimit),
          multi_model_usage: multiModelUsage,
          summarization_enabled: summarizationEnabled,
          quality: Number(quality),
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to calculate cost");
      }

      const data = await res.json();
      console.debug("Cost API response", data);
      totalMonthlyCost = data.total_monthly_cost;
      models = data.models;
      savings = data.savings_opportunities;
      withinBudget = data.within_budget;
    } catch (err) {
      console.error("Error while calling /api/calculate", err);
      error = "Something went wrong while calculating. Please try again.";
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    // Run an initial calculation so the right side is populated immediately
    recalculate();
  });
</script>

<div class="page">
  <header class="header">
    <div class="logo">AI</div>
    <div class="header-text">
      <h1>AI Cost Optimizer</h1>
      <p>See how much you spend on AI models and optimize it.</p>
    </div>
  </header>

  <main class="main">
    <section class="card inputs">
      <h2>Inputs</h2>

      <div class="field">
        <label for="model">Select AI Model</label>
        <select id="model" bind:value={selectedModel}>
          <option value="gpt-4">GPT-4</option>
          <option value="gpt-3.5">GPT-3.5</option>
          <option value="claude">Claude</option>
        </select>
      </div>

      <div class="field-group">
        <div class="field">
          <label for="inputTokens">Input Tokens per Request</label>
          <div class="token-input">
            <input
              id="inputTokens"
              type="number"
              min="0"
              step="1"
              bind:value={inputTokens}
            />
            <div class="unit-pills" role="group" aria-label="Input token unit">
              <button
                type="button"
                class="unit-pill"
                class:active={inputTokenUnit === "1"}
                on:click={() => (inputTokenUnit = "1")}
              >
                #
              </button>
              <button
                type="button"
                class="unit-pill"
                class:active={inputTokenUnit === "K"}
                on:click={() => (inputTokenUnit = "K")}
              >
                K
              </button>
              <button
                type="button"
                class="unit-pill"
                class:active={inputTokenUnit === "M"}
                on:click={() => (inputTokenUnit = "M")}
              >
                M
              </button>
              <button
                type="button"
                class="unit-pill"
                class:active={inputTokenUnit === "B"}
                on:click={() => (inputTokenUnit = "B")}
              >
                B
              </button>
            </div>
          </div>
          <div class="field-hint">
            Sending <strong>{tokensValue(inputTokens, inputTokenUnit).toLocaleString()}</strong> input
            tokens/request
          </div>
        </div>

        <div class="field">
          <label for="outputTokens">Output Tokens per Request</label>
          <div class="token-input">
            <input
              id="outputTokens"
              type="number"
              min="0"
              step="1"
              bind:value={outputTokens}
            />
            <div class="unit-pills" role="group" aria-label="Output token unit">
              <button
                type="button"
                class="unit-pill"
                class:active={outputTokenUnit === "1"}
                on:click={() => (outputTokenUnit = "1")}
              >
                #
              </button>
              <button
                type="button"
                class="unit-pill"
                class:active={outputTokenUnit === "K"}
                on:click={() => (outputTokenUnit = "K")}
              >
                K
              </button>
              <button
                type="button"
                class="unit-pill"
                class:active={outputTokenUnit === "M"}
                on:click={() => (outputTokenUnit = "M")}
              >
                M
              </button>
              <button
                type="button"
                class="unit-pill"
                class:active={outputTokenUnit === "B"}
                on:click={() => (outputTokenUnit = "B")}
              >
                B
              </button>
            </div>
          </div>
          <div class="field-hint">
            Sending <strong>{tokensValue(outputTokens, outputTokenUnit).toLocaleString()}</strong> output
            tokens/request
          </div>
        </div>
      </div>

      <div class="field-group">
        <div class="field">
          <label for="requestsPerDay">Requests per Day</label>
          <input
            id="requestsPerDay"
            type="number"
            min="0"
            bind:value={requestsPerDay}
          />
        </div>

        <div class="field">
          <label for="daysPerMonth">Days per Month</label>
          <input
            id="daysPerMonth"
            type="number"
            min="0"
            bind:value={daysPerMonth}
          />
        </div>
      </div>

      <div class="field">
        <label for="budgetLimit">Budget Limit ($)</label>
        <div class="input-prefix">
          <span>$</span>
          <input
            id="budgetLimit"
            type="number"
            min="0"
            bind:value={budgetLimit}
          />
        </div>
      </div>

      <button
        type="button"
        class="advanced-toggle"
        aria-expanded={showAdvanced}
        on:click={() => (showAdvanced = !showAdvanced)}
      >
        <div class="advanced-toggle-text">
          <div class="advanced-title">Advanced Options</div>
          <div class="advanced-subtitle">
            Multi-model, summarization, quality tuning
          </div>
        </div>
        <div class="advanced-toggle-right">
          {#if multiModelUsage}
            <span class="chip">Multi-model</span>
          {/if}
          {#if summarizationEnabled}
            <span class="chip">Summarization</span>
          {/if}
          <span class="chevron">{showAdvanced ? "▲" : "▼"}</span>
        </div>
      </button>

      {#if showAdvanced}
        <div class="advanced-panel">
          <div class="toggle-grid">
            <button
              type="button"
              class="toggle-card"
              class:active={multiModelUsage}
              on:click={() => (multiModelUsage = !multiModelUsage)}
              aria-pressed={multiModelUsage}
            >
              <div class="toggle-title">Multi-model usage</div>
              <div class="toggle-subtitle">Route some tasks to cheaper models</div>
            </button>

            <button
              type="button"
              class="toggle-card"
              class:active={summarizationEnabled}
              on:click={() => (summarizationEnabled = !summarizationEnabled)}
              aria-pressed={summarizationEnabled}
            >
              <div class="toggle-title">Summarization layer</div>
              <div class="toggle-subtitle">Shorten context before main call</div>
            </button>
          </div>

          <div class="field">
            <label for="quality">Quality vs. Cost</label>
            <input
              id="quality"
              type="range"
              min="0"
              max="100"
              step="1"
              bind:value={quality}
            />
            <div class="range-labels">
              <span>Cheaper</span>
              <span>Balanced</span>
              <span>Higher quality</span>
            </div>
          </div>
        </div>
      {/if}

      <button class="primary-button" on:click|preventDefault={recalculate} disabled={loading}>
        {#if loading}
          <span class="button-spinner" aria-hidden="true"></span>
          <span>Calculating...</span>
        {:else}
          <span>Recalculate</span>
        {/if}
      </button>
    </section>

    <section class="outputs">
      <div class="card">
        <h2>Cost Summary</h2>
        {#if error}
          <p class="error-text">{error}</p>
        {:else if totalMonthlyCost !== null}
          <p class="total-cost">
            Total Monthly Cost:
            <span class="highlight-amount">
              $ {totalMonthlyCost.toLocaleString(undefined, {
                maximumFractionDigits: 2,
              })}
            </span>
            {#if withinBudget !== null}
              <span class:badge-success={withinBudget} class:badge-warning={!withinBudget}>
                {withinBudget ? "Within budget" : "Over budget"}
              </span>
            {/if}
          </p>

          {#each models as model}
            <div class="model-row" class:muted={model.total_cost === 0}>
              <div class="model-name">{model.name}</div>
              <div class="model-details">
                <div class="model-total">
                  $ {model.total_cost.toLocaleString(undefined, {
                    maximumFractionDigits: 2,
                  })}
                </div>
                <div class="model-breakdown">
                  Input:
                  $ {model.input_cost.toLocaleString(undefined, {
                    maximumFractionDigits: 2,
                  })},
                  Output:
                  $ {model.output_cost.toLocaleString(undefined, {
                    maximumFractionDigits: 2,
                  })}
                </div>
              </div>
            </div>
          {/each}
        {:else}
          <p class="placeholder-text">
            Adjust inputs on the left and hit <strong>Recalculate</strong> to see your costs.
          </p>
        {/if}
      </div>

      <div class="card">
        <h2>Savings Opportunities</h2>
        {#if savings.length > 0}
          <ul class="savings-list">
            {#each savings as s}
              <li>
                {s.description} →
                <span class="highlight-amount">
                  Save
                  $ {s.monthly_saving.toLocaleString(undefined, {
                    maximumFractionDigits: 2,
                  })}
                  /month
                </span>
              </li>
            {/each}
          </ul>
        {:else}
          <p class="placeholder-text">
            Savings opportunities will appear here once you calculate costs.
          </p>
        {/if}
      </div>
    </section>
  </main>
</div>