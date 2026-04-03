<script lang="ts">
  import { onMount } from "svelte";
  import "./ai-calc.css";
  import ScenarioSelector from "./components/ScenarioSelector.svelte";
  import Scenario1Form from "./components/Scenario1Form.svelte";
  import Scenario2Form from "./components/Scenario2Form.svelte";
  import Scenario3Form from "./components/Scenario3Form.svelte";
  import Scenario4Form from "./components/Scenario4Form.svelte";
  import ScenarioOutputs from "./components/ScenarioOutputs.svelte";

  import { tokensValue } from "./components/scenario-types";
  import type { TokenUnit, ModelId } from "./components/types";
  import type {
    Scenario1Response,
    Scenario2Response,
    Scenario3Response,
    Scenario4Response,
  } from "./components/scenario-types";

  let activeTopTab = $state<"cost" | "token">("cost");
  let activeScenario = $state<1 | 2 | 3 | 4>(1);
  let loading = $state(false);
  let error = $state<string | null>(null);

  // Scenario 1 state
  let s1_usersPerDay = $state(1000);
  let s1_messagesPerUser = $state(8);
  let s1_chatbotType = $state<
    "simple_faq" | "standard_assistant" | "advanced_assistant" | "custom" | "none"
  >("standard_assistant");
  let s1_avgInput = $state(100);
  let s1_avgInputUnit = $state<TokenUnit>("1");
  let s1_avgOutput = $state(300);
  let s1_avgOutputUnit = $state<TokenUnit>("1");
  let s1_models = $state<ModelId[]>(["gpt-4", "claude", "gpt-3.5"]);
  let s1_daysPerMonth = $state(30);
  let s1_qualityPref = $state<"low_cost" | "balanced" | "high_quality">("balanced");

  // Scenario 2 state
  let s2_usersPerDay = $state(1000);
  let s2_messagesPerUser = $state(8);
  let s2_avgInput = $state(100);
  let s2_avgInputUnit = $state<TokenUnit>("1");
  let s2_avgOutput = $state(300);
  let s2_avgOutputUnit = $state<TokenUnit>("1");
  let s2_daysPerMonth = $state(30);
  let s2_retryRate = $state(10);
  let s2_extraOutputGrowth = $state(20);
  let s2_memoryMultiplier = $state(1.5);
  let s2_systemPromptSize = $state(200);

  // Scenario 3 state
  let s3_contentType = $state<"blog" | "ads" | "email" | "product_description">("blog");
  let s3_numberOfOutputs = $state(10000);
  let s3_wordsPerOutput = $state(800);
  let s3_avgInput = $state(100);
  let s3_avgOutput = $state(300);
  let s3_models = $state<ModelId[]>(["claude", "gpt-4"]);
  let s3_daysPerMonth = $state(30);
  let s3_qualityPref = $state<"low_cost" | "balanced" | "high_quality">("balanced");

  // Scenario 4 state
  let s4_usersPerDay = $state(1000);
  let s4_messagesPerUser = $state(8);
  let s4_daysPerMonth = $state(30);
  let s4_avgInput = $state(100);
  let s4_avgInputUnit = $state<TokenUnit>("1");
  let s4_avgOutput = $state(300);
  let s4_avgOutputUnit = $state<TokenUnit>("1");
  let s4_models = $state<ModelId[]>(["claude", "gpt-4"]);
  let s4_qualityPref = $state<"low_cost" | "balanced" | "high_quality">("balanced");
  let s4_revenuePerConversion = $state(10);
  let s4_conversionRate = $state(5);
  let s4_subscriptionPrice = $state(20);
  let s4_costBudget = $state(3000);

  // Responses
  let resp1 = $state<Scenario1Response | null>(null);
  let resp2 = $state<Scenario2Response | null>(null);
  let resp3 = $state<Scenario3Response | null>(null);
  let resp4 = $state<Scenario4Response | null>(null);

  // Tokenization tool state
  let tk_text = $state("");
  let tk_model = $state("gpt-4o");
  /** API TokenizeRequest.mode: decoded text, numeric ids, or both */
  let tk_mode = $state<"text" | "ids" | "both">("both");
  let tk_loading = $state(false);
  let tk_error = $state<string | null>(null);
  let tk_result = $state<{
    token_count: number;
    char_count: number;
    tokens: { text?: string | null; token_id?: number | null; color?: string | null }[];
  } | null>(null);

  /** Invalidate in-flight tokenize calls when newer input arrives */
  let tokenizeSeq = 0;
  const TOKENIZE_DEBOUNCE_MS = 380;

  async function runTokenize() {
    const text = tk_text.trim();
    if (!text) {
      tk_result = null;
      tk_error = null;
      tk_loading = false;
      return;
    }

    const seq = ++tokenizeSeq;
    tk_loading = true;
    tk_error = null;

    try {
      const res = await fetch("/api/tokenize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: tk_text,
          model: tk_model,
          mode: tk_mode,
          include_colors: true,
        }),
      });
      if (!res.ok) throw new Error(`Tokenize failed (${res.status})`);
      const data = await res.json();
      if (seq !== tokenizeSeq) return;
      tk_result = data;
    } catch (e) {
      console.error(e);
      if (seq !== tokenizeSeq) return;
      tk_error = "Could not tokenize text. Please try again.";
    } finally {
      if (seq === tokenizeSeq) tk_loading = false;
    }
  }

  $effect(() => {
    if (activeTopTab !== "token") return;

    const text = tk_text;

    if (!text.trim()) {
      tokenizeSeq++;
      tk_result = null;
      tk_error = null;
      tk_loading = false;
      return;
    }

    void tk_model;
    void tk_mode;

    const t = setTimeout(() => {
      void runTokenize();
    }, TOKENIZE_DEBOUNCE_MS);

    return () => clearTimeout(t);
  });

  function resetTokenization() {
    tokenizeSeq++;
    tk_text = "";
    tk_model = "gpt-4o";
    tk_mode = "both";
    tk_result = null;
    tk_error = null;
    tk_loading = false;
  }

  async function postJSON<T>(url: string, payload: unknown): Promise<T> {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error(`Request failed (${res.status})`);
    return (await res.json()) as T;
  }

  async function calculate() {
    loading = true;
    error = null;

    try {
      if (activeScenario === 1) {
        resp1 = await postJSON<Scenario1Response>("/api/scenario1/estimate-chatbot-cost", {
          users_per_day: Number(s1_usersPerDay),
          messages_per_user: Number(s1_messagesPerUser),
          chatbot_type: s1_chatbotType,
          avg_input_tokens_per_message: tokensValue(s1_avgInput, s1_avgInputUnit),
          avg_output_tokens_per_response: tokensValue(s1_avgOutput, s1_avgOutputUnit),
          selected_models: s1_models,
          days_per_month: Number(s1_daysPerMonth),
          quality_preference: s1_qualityPref,
        });
      } else if (activeScenario === 2) {
        resp2 = await postJSON<Scenario2Response>("/api/scenario2/hidden-costs", {
          users_per_day: Number(s2_usersPerDay),
          messages_per_user: Number(s2_messagesPerUser),
          avg_input_tokens_per_message: tokensValue(s2_avgInput, s2_avgInputUnit),
          avg_output_tokens_per_response: tokensValue(s2_avgOutput, s2_avgOutputUnit),
          days_per_month: Number(s2_daysPerMonth),
          retry_rate: Number(s2_retryRate),
          extra_output_growth: Number(s2_extraOutputGrowth),
          memory_multiplier: Number(s2_memoryMultiplier),
          system_prompt_size: Number(s2_systemPromptSize),
        });
      } else if (activeScenario === 3) {
        resp3 = await postJSON<Scenario3Response>("/api/scenario3/bulk-usage", {
          content_type: s3_contentType,
          number_of_outputs: Number(s3_numberOfOutputs),
          words_per_output: Number(s3_wordsPerOutput),
          avg_input_tokens_per_message: Number(s3_avgInput),
          avg_output_tokens_per_response: Number(s3_avgOutput),
          selected_models: s3_models,
          days_per_month: Number(s3_daysPerMonth),
          quality_preference: s3_qualityPref,
        });
      } else if (activeScenario === 4) {
        resp4 = await postJSON<Scenario4Response>("/api/scenario4/roi", {
          users_per_day: Number(s4_usersPerDay),
          messages_per_user: Number(s4_messagesPerUser),
          days_per_month: Number(s4_daysPerMonth),
          avg_input_tokens_per_message: tokensValue(s4_avgInput, s4_avgInputUnit),
          avg_output_tokens_per_response: tokensValue(s4_avgOutput, s4_avgOutputUnit),
          selected_models: s4_models,
          quality_preference: s4_qualityPref,
          revenue_per_conversion: Number(s4_revenuePerConversion),
          conversion_rate: Number(s4_conversionRate),
          subscription_price: Number(s4_subscriptionPrice),
          cost_budget: Number(s4_costBudget),
        });
      }
    } catch (err) {
      console.error("Error while calling /api/calculate", err);
      error = "Could not calculate. Please check inputs and try again.";
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    calculate();
  });
</script>

<div class="page">
  <header class="header">
    <div class="logo">AI</div>
    <div class="header-text">
      <h1>AI Cost & ROI Optimizer</h1>
      <p>Pick a scenario to see cost, savings, risks, and ROI.</p>
    </div>
  </header>

  <div class="top-nav">
    <button
      type="button"
      class="top-nav-tab"
      class:active={activeTopTab === "cost"}
      on:click={() => (activeTopTab = "cost")}
    >
      1. Cost Calculator
    </button>
    <button
      type="button"
      class="top-nav-tab"
      class:active={activeTopTab === "token"}
      on:click={() => (activeTopTab = "token")}
    >
      2. Tokenization
    </button>
  </div>

  {#if activeTopTab === "cost"}
  <main class="main">
    <section class="card inputs">
      <h2>Choose a scenario</h2>
      <ScenarioSelector bind:active={activeScenario} />

      {#if activeScenario === 1}
        <Scenario1Form
          bind:usersPerDay={s1_usersPerDay}
          bind:messagesPerUser={s1_messagesPerUser}
          bind:chatbotType={s1_chatbotType}
          bind:avgInput={s1_avgInput}
          bind:avgInputUnit={s1_avgInputUnit}
          bind:avgOutput={s1_avgOutput}
          bind:avgOutputUnit={s1_avgOutputUnit}
          bind:selectedModels={s1_models}
          bind:daysPerMonth={s1_daysPerMonth}
          bind:qualityPreference={s1_qualityPref}
        />
      {:else if activeScenario === 2}
        <Scenario2Form
          bind:usersPerDay={s2_usersPerDay}
          bind:messagesPerUser={s2_messagesPerUser}
          bind:avgInput={s2_avgInput}
          bind:avgInputUnit={s2_avgInputUnit}
          bind:avgOutput={s2_avgOutput}
          bind:avgOutputUnit={s2_avgOutputUnit}
          bind:daysPerMonth={s2_daysPerMonth}
          bind:retryRate={s2_retryRate}
          bind:extraOutputGrowth={s2_extraOutputGrowth}
          bind:memoryMultiplier={s2_memoryMultiplier}
          bind:systemPromptSize={s2_systemPromptSize}
        />
      {:else if activeScenario === 3}
        <Scenario3Form
          bind:contentType={s3_contentType}
          bind:numberOfOutputs={s3_numberOfOutputs}
          bind:wordsPerOutput={s3_wordsPerOutput}
          bind:avgInputTokens={s3_avgInput}
          bind:avgOutputTokens={s3_avgOutput}
          bind:selectedModels={s3_models}
          bind:daysPerMonth={s3_daysPerMonth}
          bind:qualityPreference={s3_qualityPref}
        />
      {:else}
        <Scenario4Form
          bind:usersPerDay={s4_usersPerDay}
          bind:messagesPerUser={s4_messagesPerUser}
          bind:daysPerMonth={s4_daysPerMonth}
          bind:avgInput={s4_avgInput}
          bind:avgInputUnit={s4_avgInputUnit}
          bind:avgOutput={s4_avgOutput}
          bind:avgOutputUnit={s4_avgOutputUnit}
          bind:selectedModels={s4_models}
          bind:qualityPreference={s4_qualityPref}
          bind:revenuePerConversion={s4_revenuePerConversion}
          bind:conversionRate={s4_conversionRate}
          bind:subscriptionPrice={s4_subscriptionPrice}
          bind:costBudget={s4_costBudget}
        />
      {/if}

      <button class="primary-button" on:click|preventDefault={calculate} disabled={loading}>
        {#if loading}
          <span class="button-spinner" aria-hidden="true"></span>
          <span>Calculating...</span>
        {:else}
          <span>Calculate</span>
        {/if}
      </button>
    </section>

    <ScenarioOutputs
      scenario={activeScenario}
      {loading}
      {error}
      s1={resp1}
      s2={resp2}
      s3={resp3}
      s4={resp4}
    />
  </main>
  {:else}
  <main class="main token-main">
    <section class="card inputs token-input-panel">
      <h2>Tokenization</h2>
      <p class="token-live-hint">
        <span class="token-live-dot" aria-hidden="true"></span>
        Live — results update shortly after you pause typing
      </p>
      <div class="field">
        <label for="tokenModel">Tokenizer model</label>
        <select id="tokenModel" bind:value={tk_model}>
          <option value="gpt-4o">gpt-4o</option>
          <option value="gpt-4">gpt-4</option>
          <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
        </select>
      </div>

      <div class="field">
        <label id="tokenModeLabel" class="token-mode-field-label">Output mode</label>
        <div
          class="token-mode-toggle"
          role="group"
          aria-labelledby="tokenModeLabel"
        >
          <button
            type="button"
            class="token-mode-btn"
            class:active={tk_mode === "text"}
            aria-pressed={tk_mode === "text"}
            on:click={() => (tk_mode = "text")}
          >
            Text
          </button>
          <button
            type="button"
            class="token-mode-btn"
            class:active={tk_mode === "ids"}
            aria-pressed={tk_mode === "ids"}
            on:click={() => (tk_mode = "ids")}
          >
            Token IDs
          </button>
          <button
            type="button"
            class="token-mode-btn"
            class:active={tk_mode === "both"}
            aria-pressed={tk_mode === "both"}
            on:click={() => (tk_mode = "both")}
          >
            Both
          </button>
        </div>
        <p class="field-hint token-mode-hint">
          {#if tk_mode === "text"}
            Chips show decoded token pieces only (matches <code>mode: "text"</code>).
          {:else if tk_mode === "ids"}
            Chips show numeric token IDs only (<code>mode: "ids"</code>).
          {:else}
            Chips show text; hover for ID (<code>mode: "both"</code>).
          {/if}
        </p>
      </div>

      <div class="field">
        <label for="tokenText">Text</label>
        <textarea
          id="tokenText"
          class="token-textarea"
          rows="12"
          bind:value={tk_text}
          placeholder="Type or paste text — token count updates automatically…"
        />
      </div>

      <button
        type="button"
        class="secondary-button token-refresh-btn"
        on:click|preventDefault={() => runTokenize()}
      >
        Refresh now
      </button>
      <button
        type="button"
        class="secondary-button token-reset-btn"
        on:click|preventDefault={resetTokenization}
      >
        Reset
      </button>
    </section>

    <section class="outputs token-outputs">
      <div class="card token-result-card">
        <div class="token-result-header">
          <h2 class="token-result-title">Token count</h2>
          {#if tk_loading && tk_text.trim()}
            <span class="token-updating-pill" aria-live="polite">Updating…</span>
          {/if}
        </div>

        {#if tk_error}
          <p class="error-text token-error-large">{tk_error}</p>
        {:else if !tk_text.trim()}
          <p class="token-empty-hint">
            Start typing on the left — your <strong>token total</strong> and <strong>token breakdown</strong> show
            here.
          </p>
        {:else if tk_result}
          <div class="token-hero">
            <div class="token-hero-primary">
              <span class="token-hero-label">Tokens</span>
              <span class="token-hero-value">
                {tk_result.token_count.toLocaleString()}
              </span>
            </div>
            <div class="token-hero-secondary">
              <span class="token-hero-label">Characters</span>
              <span class="token-hero-value-sub">
                {tk_result.char_count.toLocaleString()}
              </span>
            </div>
          </div>

          <div class="token-model-tag">
            Model: <strong>{tk_model}</strong>
            · Mode:
            <strong>{tk_mode}</strong>
            {#if tk_loading}
              <span class="token-pulse" aria-hidden="true">●</span>
            {/if}
          </div>

          <div class="token-breakdown-wrap">
            <h3 class="token-breakdown-heading">Token breakdown</h3>
            <p class="token-breakdown-sub">
              {#if tk_mode === "text"}
                Decoded subword pieces from the API.
              {:else if tk_mode === "ids"}
                Numeric token IDs from the API (one chip per token).
              {:else}
                Decoded text and ID per token.
              {/if}
            </p>
            <div class="token-chip-row token-chip-row-prominent">
              {#each tk_result.tokens as t}
                <span
                  class="token-chip token-chip-lg"
                  class:token-chip-id={tk_mode === "ids"}
                  style={t.color ? `background-color: ${t.color}28; border-color: ${t.color}70;` : ""}
                  title={tk_mode === "both" && t.token_id != null
                    ? `ID: ${t.token_id}`
                    : tk_mode === "ids" && t.token_id != null
                      ? `Token ID ${t.token_id}`
                      : undefined}
                >
                  {#if tk_mode === "ids"}
                    {t.token_id ?? "—"}
                  {:else if tk_mode === "both"}
                    {t.text ?? ""}{" "}
                    <span class="token-id-inline">
                      ({t.token_id ?? "—"})
                    </span>
                  {:else}
                    {t.text ?? ""}
                  {/if}
                </span>
              {/each}
            </div>
          </div>
        {:else}
          <p class="placeholder-text">Preparing…</p>
        {/if}
      </div>
    </section>
  </main>
  {/if}
</div>