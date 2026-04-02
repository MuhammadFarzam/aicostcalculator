<script lang="ts">
  import type { ModelId } from "./types";

  let { selected = $bindable<ModelId[]>(["gpt-4"]) } = $props<{
    selected?: ModelId[];
  }>();

  const models: { id: ModelId; label: string }[] = [
    { id: "gpt-4", label: "GPT-4" },
    { id: "claude", label: "Claude" },
    { id: "gemini", label: "Gemini" },
    { id: "gpt-3.5", label: "GPT-3.5" },
  ];

  function toggle(id: ModelId) {
    if (selected.includes(id)) selected = selected.filter((m) => m !== id);
    else selected = [...selected, id];
  }
</script>

<div class="field">
  <label>Select models</label>
  <div class="pill-row">
    {#each models as m}
      <button
        type="button"
        class="pill"
        class:active={selected.includes(m.id)}
        on:click={() => toggle(m.id)}
      >
        {m.label}
      </button>
    {/each}
  </div>
  <div class="field-hint">
    Selected: <strong>{selected.length}</strong>
  </div>
</div>

