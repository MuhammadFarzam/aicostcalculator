<script lang="ts">
  import type { TokenUnit } from "./types";

  let {
    id,
    label,
    value = $bindable(0),
    unit = $bindable<TokenUnit>("1"),
    disabled = false,
    readonly = false,
  } = $props<{
    id: string;
    label: string;
    value?: number;
    unit?: TokenUnit;
    disabled?: boolean;
    readonly?: boolean;
  }>();

  const units: { id: TokenUnit; label: string }[] = [
    { id: "1", label: "#" },
    { id: "K", label: "K" },
    { id: "M", label: "M" },
    { id: "B", label: "B" },
  ];
</script>

<div class="field">
  <label for={id}>{label}</label>
  <div class="token-input">
    <input
      {id}
      type="number"
      min="0"
      step="1"
      bind:value
      {disabled}
      {readonly}
    />
    <div class="unit-pills" role="group" aria-label={`${label} unit`}>
      {#each units as u}
        <button
          type="button"
          class="unit-pill"
          class:active={unit === u.id}
          on:click={() => (unit = u.id)}
          disabled={disabled}
        >
          {u.label}
        </button>
      {/each}
    </div>
  </div>
</div>

