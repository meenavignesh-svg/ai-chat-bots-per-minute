# Token And Compute Usage

| Date | Source | Usage Type | Estimate | Notes |
| --- | --- | --- | --- | --- |
| 2026-05-24 | Manual repository edits | assistant tokens | Not measured | Used for setup, debugging, and repo restructuring. |
| 2026-05-24 | GitHub Actions | compute minutes | Not measured | Scheduled chatbot generation attempts. |
| 2026-05-24 | Ollama | local inference | No API token cost | Uses runner CPU/RAM instead of hosted LLM tokens. |

## Tracking Plan

- Record chatbot count per day.
- Record failed workflow runs.
- Record model used for each generated project.
- Record whether generation used Ollama or template fallback.
