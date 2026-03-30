## Summary of UI changes for `ai-calc` page

- **Header layout**: Replaced the simple `AI Cost Calculator` heading with a structured header that includes:
  - A circular `AI` logo element.
  - Title text `AI Cost Optimizer`.
  - Subtitle text: “See how much you spend on AI models and optimize it.”

- **Two-column main layout**:
  - **Left column – Inputs card**:
    - Added a card titled `Inputs`.
    - Added a `Select AI Model` dropdown with options `GPT-4`, `GPT-3.5`, and `Claude`.
    - Added numeric inputs for:
      - `Input Tokens per Request` (default 500).
      - `Output Tokens per Request` (default 1500).
      - `Requests per Day` (default 100).
      - `Days per Month` (default 30).
      - `Budget Limit ($)` with a `$` prefix styling (default 2000).
    - Implemented an **Advanced Options** toggle:
      - Checkbox label `Advanced Options` with a chevron indicator.
      - When expanded, shows:
        - `Enable multi-model usage` checkbox.
        - `Turn on summarization layer` checkbox.
        - `Quality vs. Cost` slider (0–100) with labels `Cheaper`, `Balanced`, `Higher quality`.
    - All new inputs are wired to local Svelte state variables only (no backend calls yet).

  - **Right column – Outputs**:
    - Created a `Cost Summary` card with static example values:
      - `Total Monthly Cost: $2250`.
      - `GPT-4: $2250 (Input: $500, Output: $1750)`.
      - `GPT-3.5: $0`.
    - Created a `Savings Opportunities` card with a static list:
      - `Switch 50% of GPT-4 tasks to GPT-3.5 → Save $900/month`.
      - `Reduce average output tokens from 1500 → 1000 → Save $300/month`.
    - These values are currently hard-coded to match your description and can later be connected to real calculations.

- **Styling and structure**:
  - Wrapped the whole page in a `.page` container with a dark, modern gradient background.
  - Implemented responsive **two-column layout** on desktop (`grid` with inputs on the left, outputs on the right) and a single-column stack on smaller screens.
  - Added `card` styles for both inputs and outputs to give a consistent visual structure.
  - Styled form fields, labels, dropdowns, number inputs, slider, and advanced panel for a clean, dashboard-like look.
  - Added a small responsive tweak for mobile to reduce padding and stack content vertically.

- **Removed previous logic**:
  - Removed the old `calculateCost` function and the `/api/calculate` call from `+page.svelte`.
  - Removed the plain `<h1>AI Cost Calculator>`, two bare number inputs, `Calculate` button, and `Total Cost` paragraph.
  - The page is now focused on a structured layout and stateful inputs; cost computation can be reconnected later if desired.

