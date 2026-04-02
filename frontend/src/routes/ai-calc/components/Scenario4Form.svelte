<script lang="ts">
  import ModelMultiSelect from "./ModelMultiSelect.svelte";
  import TokenUnitInput from "./TokenUnitInput.svelte";
  import type { ModelId, TokenUnit } from "./types";

  let {
    usersPerDay = $bindable(1000),
    messagesPerUser = $bindable(8),
    daysPerMonth = $bindable(30),
    avgInput = $bindable(100),
    avgInputUnit = $bindable<TokenUnit>("1"),
    avgOutput = $bindable(300),
    avgOutputUnit = $bindable<TokenUnit>("1"),
    selectedModels = $bindable<ModelId[]>(["claude", "gpt-4"]),
    qualityPreference = $bindable<"low_cost" | "balanced" | "high_quality">("balanced"),
    revenuePerConversion = $bindable(10),
    conversionRate = $bindable(5),
    subscriptionPrice = $bindable(20),
    costBudget = $bindable(3000),
  } = $props<{
    usersPerDay?: number;
    messagesPerUser?: number;
    daysPerMonth?: number;
    avgInput?: number;
    avgInputUnit?: TokenUnit;
    avgOutput?: number;
    avgOutputUnit?: TokenUnit;
    selectedModels?: ModelId[];
    qualityPreference?: "low_cost" | "balanced" | "high_quality";
    revenuePerConversion?: number;
    conversionRate?: number;
    subscriptionPrice?: number;
    costBudget?: number;
  }>();
</script>

<div class="scenario-card">
  <header class="scenario-header">
    <div>
      <h4>Scenario 4: Profit & ROI Analysis</h4>
      <p>Connect cost to revenue, conversion, and budget.</p>
    </div>
  </header>

  <div class="scenario-body">
    <div class="field-group">
      <div class="field">
        <label for="usersPerDay4">Number of users per day</label>
        <input id="usersPerDay4" type="number" min="0" bind:value={usersPerDay} />
      </div>
      <div class="field">
        <label for="messagesPerUser4">Messages per user</label>
        <input id="messagesPerUser4" type="number" min="0" bind:value={messagesPerUser} />
      </div>
    </div>

    <div class="field-group">
      <div class="field">
        <label for="daysPerMonth4">Days per month</label>
        <input id="daysPerMonth4" type="number" min="0" max="31" bind:value={daysPerMonth} />
      </div>
      <div class="field">
        <label>Quality preference</label>
        <div class="pill-row">
          <button
            type="button"
            class="pill"
            class:active={qualityPreference === "low_cost"}
            on:click={() => (qualityPreference = "low_cost")}
          >
            Low Cost
          </button>
          <button
            type="button"
            class="pill"
            class:active={qualityPreference === "balanced"}
            on:click={() => (qualityPreference = "balanced")}
          >
            Balanced
          </button>
          <button
            type="button"
            class="pill"
            class:active={qualityPreference === "high_quality"}
            on:click={() => (qualityPreference = "high_quality")}
          >
            High Quality
          </button>
        </div>
      </div>
    </div>

    <div class="field-group">
      <TokenUnitInput
        id="avgInput4"
        label="Avg input tokens per message"
        bind:value={avgInput}
        bind:unit={avgInputUnit}
      />
      <TokenUnitInput
        id="avgOutput4"
        label="Avg output tokens per response"
        bind:value={avgOutput}
        bind:unit={avgOutputUnit}
      />
    </div>

    <ModelMultiSelect bind:selected={selectedModels} />

    <div class="field-group">
      <div class="field">
        <label for="revenuePerConversion">Revenue per conversion ($)</label>
        <input id="revenuePerConversion" type="number" min="0" step="0.01" bind:value={revenuePerConversion} />
      </div>
      <div class="field">
        <label for="conversionRate">Conversion rate (%)</label>
        <input id="conversionRate4" type="number" min="0" max="100" step="0.1" bind:value={conversionRate} />
      </div>
    </div>

    <div class="field-group">
      <div class="field">
        <label for="subscriptionPrice">Monthly subscription price ($)</label>
        <input id="subscriptionPrice" type="number" min="0" step="0.01" bind:value={subscriptionPrice} />
      </div>
      <div class="field">
        <label for="costBudget4">Cost budget ($)</label>
        <input id="costBudget4" type="number" min="0" step="0.01" bind:value={costBudget} />
      </div>
    </div>
  </div>
</div>

