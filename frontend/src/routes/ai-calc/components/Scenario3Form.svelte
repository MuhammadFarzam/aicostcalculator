<script lang="ts">
  import ModelMultiSelect from "./ModelMultiSelect.svelte";
  import type { ModelId } from "./types";

  let {
    contentType = $bindable<"blog" | "ads" | "email" | "product_description">("blog"),
    numberOfOutputs = $bindable(10000),
    wordsPerOutput = $bindable(800),
    avgInputTokens = $bindable(100),
    avgOutputTokens = $bindable(300),
    selectedModels = $bindable<ModelId[]>(["claude", "gpt-4"]),
    daysPerMonth = $bindable(30),
    qualityPreference = $bindable<"low_cost" | "balanced" | "high_quality">("balanced"),
  } = $props<{
    contentType?: "blog" | "ads" | "email" | "product_description";
    numberOfOutputs?: number;
    wordsPerOutput?: number;
    avgInputTokens?: number;
    avgOutputTokens?: number;
    selectedModels?: ModelId[];
    daysPerMonth?: number;
    qualityPreference?: "low_cost" | "balanced" | "high_quality";
  }>();
</script>

<div class="scenario-card">
  <header class="scenario-header">
    <div>
      <h4>Scenario 3: Bulk Usage Calculator</h4>
      <p>Convert a bulk content plan into total AI cost.</p>
    </div>
  </header>

  <div class="scenario-body">
    <div class="field">
      <label>Content type</label>
      <div class="pill-row">
        <button type="button" class="pill" class:active={contentType === "blog"} on:click={() => (contentType = "blog")}>
          Blog
        </button>
        <button type="button" class="pill" class:active={contentType === "ads"} on:click={() => (contentType = "ads")}>
          Ads
        </button>
        <button type="button" class="pill" class:active={contentType === "email"} on:click={() => (contentType = "email")}>
          Email
        </button>
        <button
          type="button"
          class="pill"
          class:active={contentType === "product_description"}
          on:click={() => (contentType = "product_description")}
        >
          Product Description
        </button>
      </div>
    </div>

    <div class="field-group">
      <div class="field">
        <label for="numberOfOutputs">Number of outputs</label>
        <input id="numberOfOutputs" type="number" min="0" bind:value={numberOfOutputs} />
      </div>
      <div class="field">
        <label for="wordsPerOutput">Words per output</label>
        <input id="wordsPerOutput3" type="number" min="0" bind:value={wordsPerOutput} />
      </div>
    </div>

    <div class="field-group">
      <div class="field">
        <label for="avgInputTokens3">Avg input tokens (prefilled)</label>
        <input id="avgInputTokens3" type="number" min="0" bind:value={avgInputTokens} readonly />
      </div>
      <div class="field">
        <label for="avgOutputTokens3">Avg output tokens (prefilled)</label>
        <input id="avgOutputTokens3" type="number" min="0" bind:value={avgOutputTokens} readonly />
      </div>
    </div>

    <ModelMultiSelect bind:selected={selectedModels} />

    <div class="field-group">
      <div class="field">
        <label for="daysPerMonth3">Days per month</label>
        <input id="daysPerMonth3" type="number" min="0" max="31" bind:value={daysPerMonth} />
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

