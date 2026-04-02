<script lang="ts">
  import type { ScenarioId } from "./types";

  let { active = $bindable<ScenarioId>(1) } = $props<{
    active?: ScenarioId;
  }>();

  const scenarios: {
    id: ScenarioId;
    title: string;
    subtitle: string;
    icon: string;
  }[] = [
    {
      id: 1,
      icon: "💰",
      title: "Estimate AI Cost",
      subtitle: "Calculate your monthly AI usage cost",
    },
    {
      id: 2,
      icon: "🔍",
      title: "Find Hidden Costs",
      subtitle: "Detect where your money is leaking",
    },
    {
      id: 3,
      icon: "📦",
      title: "Bulk Usage Calculator",
      subtitle: "Estimate cost for large generation",
    },
    {
      id: 4,
      icon: "📈",
      title: "Profit & ROI Analysis",
      subtitle: "See if your AI usage is profitable",
    },
  ];
</script>

<div class="scenario-grid" role="tablist" aria-label="Scenarios">
  {#each scenarios as s}
    <button
      type="button"
      class="scenario-select-card"
      class:active={active === s.id}
      on:click={() => (active = s.id)}
      role="tab"
      aria-selected={active === s.id}
    >
      <div class="scenario-icon">{s.icon}</div>
      <div class="scenario-meta">
        <div class="scenario-title">{s.title}</div>
        <div class="scenario-subtitle">{s.subtitle}</div>
      </div>
    </button>
  {/each}
</div>

