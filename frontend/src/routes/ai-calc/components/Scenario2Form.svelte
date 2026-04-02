<script lang="ts">
  import TokenUnitInput from "./TokenUnitInput.svelte";
  import type { TokenUnit } from "./types";

  let {
    usersPerDay = $bindable(1000),
    messagesPerUser = $bindable(8),
    avgInput = $bindable(100),
    avgInputUnit = $bindable<TokenUnit>("1"),
    avgOutput = $bindable(300),
    avgOutputUnit = $bindable<TokenUnit>("1"),
    daysPerMonth = $bindable(30),
    retryRate = $bindable(10),
    extraOutputGrowth = $bindable(20),
    memoryMultiplier = $bindable(1.5),
    systemPromptSize = $bindable(200),
  } = $props<{
    usersPerDay?: number;
    messagesPerUser?: number;
    avgInput?: number;
    avgInputUnit?: TokenUnit;
    avgOutput?: number;
    avgOutputUnit?: TokenUnit;
    daysPerMonth?: number;
    retryRate?: number;
    extraOutputGrowth?: number;
    memoryMultiplier?: number;
    systemPromptSize?: number;
  }>();
</script>

<div class="scenario-card">
  <header class="scenario-header">
    <div>
      <h4>Scenario 2: Find Hidden Costs</h4>
      <p>Reveal invisible cost leaks and get actionable fixes.</p>
    </div>
  </header>

  <div class="scenario-body">
    <div class="field-group">
      <div class="field">
        <label for="usersPerDay2">Number of users per day</label>
        <input id="usersPerDay2" type="number" min="0" bind:value={usersPerDay} />
      </div>
      <div class="field">
        <label for="messagesPerUser2">Messages per user</label>
        <input id="messagesPerUser2" type="number" min="0" bind:value={messagesPerUser} />
      </div>
    </div>

    <div class="field-group">
      <TokenUnitInput
        id="avgInput2"
        label="Avg input tokens per message"
        bind:value={avgInput}
        bind:unit={avgInputUnit}
      />
      <TokenUnitInput
        id="avgOutput2"
        label="Avg output tokens per response"
        bind:value={avgOutput}
        bind:unit={avgOutputUnit}
      />
    </div>

    <div class="field-group">
      <div class="field">
        <label for="daysPerMonth2">Days per month</label>
        <input id="daysPerMonth2" type="number" min="0" max="31" bind:value={daysPerMonth} />
      </div>
      <div class="field">
        <label for="retryRate">Retry rate (%)</label>
        <input id="retryRate" type="number" min="0" max="100" bind:value={retryRate} />
      </div>
    </div>

    <div class="field-group">
      <div class="field">
        <label for="extraOutputGrowth">Extra output growth (%)</label>
        <input id="extraOutputGrowth" type="number" min="0" max="100" bind:value={extraOutputGrowth} />
      </div>
      <div class="field">
        <label for="memoryMultiplier">Memory multiplier (x)</label>
        <input id="memoryMultiplier" type="number" min="1" step="0.1" bind:value={memoryMultiplier} />
      </div>
    </div>

    <div class="field">
      <label for="systemPromptSize">System prompt size (tokens)</label>
      <input id="systemPromptSize" type="number" min="0" bind:value={systemPromptSize} />
    </div>
  </div>
</div>

