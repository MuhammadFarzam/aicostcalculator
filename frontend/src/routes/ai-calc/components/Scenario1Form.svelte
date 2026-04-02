<script lang="ts">
  import TokenUnitInput from "./TokenUnitInput.svelte";
  import ModelMultiSelect from "./ModelMultiSelect.svelte";
  import { tokensValue } from "./scenario-types";
  import type { TokenUnit, ModelId } from "./types";

  let {
    usersPerDay = $bindable(1000),
    messagesPerUser = $bindable(8),
    chatbotType = $bindable<
      "simple_faq" | "standard_assistant" | "advanced_assistant" | "custom" | "none"
    >("standard_assistant"),
    avgInput = $bindable(100),
    avgInputUnit = $bindable<TokenUnit>("1"),
    avgOutput = $bindable(300),
    avgOutputUnit = $bindable<TokenUnit>("1"),
    selectedModels = $bindable<ModelId[]>(["gpt-4", "claude", "gpt-3.5"]),
    daysPerMonth = $bindable(30),
    qualityPreference = $bindable<"low_cost" | "balanced" | "high_quality">("balanced"),
  } = $props<{
    usersPerDay?: number;
    messagesPerUser?: number;
    chatbotType?: "simple_faq" | "standard_assistant" | "advanced_assistant" | "custom" | "none";
    avgInput?: number;
    avgInputUnit?: TokenUnit;
    avgOutput?: number;
    avgOutputUnit?: TokenUnit;
    selectedModels?: ModelId[];
    daysPerMonth?: number;
    qualityPreference?: "low_cost" | "balanced" | "high_quality";
  }>();

  const presets: Record<string, { in: number; out: number }> = {
    simple_faq: { in: 50, out: 150 },
    standard_assistant: { in: 100, out: 300 },
    advanced_assistant: { in: 200, out: 800 },
  };

  $effect(() => {
    if (chatbotType in presets) {
      const p = presets[chatbotType];
      avgInput = p.in;
      avgInputUnit = "1";
      avgOutput = p.out;
      avgOutputUnit = "1";
    }
  });

  const chatbotOptions = [
    { id: "simple_faq", label: "Simple FAQ Bot (50 in / 150 out)" },
    { id: "standard_assistant", label: "Standard Assistant (100 in / 300 out)" },
    { id: "advanced_assistant", label: "Advanced AI Assistant (200 in / 800 out)" },
    { id: "custom", label: "Custom (editable presets)" },
    { id: "none", label: "Without chatbot" },
  ] as const;
</script>

<div class="scenario-card">
  <header class="scenario-header">
    <div>
      <h4>Scenario 1: Estimate Chatbot Cost</h4>
      <p>Estimate requests, tokens, and your monthly AI bill.</p>
    </div>
  </header>

  <div class="scenario-body">
    <div class="field-group">
      <div class="field">
        <label for="usersPerDay">Number of users per day</label>
        <input id="usersPerDay" type="number" min="0" bind:value={usersPerDay} />
      </div>
      <div class="field">
        <label for="messagesPerUser">Messages per user</label>
        <input id="messagesPerUser" type="number" min="0" bind:value={messagesPerUser} />
      </div>
    </div>

    <div class="field">
      <label for="chatbotType">Chatbot type</label>
      <select id="chatbotType" bind:value={chatbotType}>
        {#each chatbotOptions as opt}
          <option value={opt.id}>{opt.label}</option>
        {/each}
      </select>
      <div class="field-hint">
        {#if chatbotType === "none"}
          Token fields won’t be auto-filled. Enter your own averages.
        {:else if chatbotType === "custom"}
          Presets won’t auto-overwrite. Adjust token fields freely.
        {:else}
          Presets are applied but you can still edit them.
        {/if}
      </div>
    </div>

    <div class="field-group">
      <TokenUnitInput
        id="avgInput"
        label="Avg input tokens per message"
        bind:value={avgInput}
        bind:unit={avgInputUnit}
      />
      <TokenUnitInput
        id="avgOutput"
        label="Avg output tokens per response"
        bind:value={avgOutput}
        bind:unit={avgOutputUnit}
      />
    </div>

    <div class="field-hint">
      Tokens per conversation: <strong>{tokensValue(avgInput, avgInputUnit) + tokensValue(avgOutput, avgOutputUnit)}</strong>
    </div>

    <ModelMultiSelect bind:selected={selectedModels} />

    <div class="field-group">
      <div class="field">
        <label for="daysPerMonth">Days per month</label>
        <input id="daysPerMonth" type="number" min="0" max="31" bind:value={daysPerMonth} />
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
  </div>
</div>

