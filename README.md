# Premium AI Chatbot Products

This repository is a clean automation archive for building **two serious premium AI chatbot products per day**.

The goal is quality, not volume. New projects must look and feel like products that could become paid tools.

## Automation Standard

Each generated product must include:

- a focused high-value use case
- premium product positioning
- a complete browser demo
- a serverless OpenAI API route
- visitor API-key support for demos
- product specification
- sample input data
- screenshot asset
- GitHub Pages demo copy
- README with setup, deployment, and value proposition
- validation before commit

## Schedule

The workflow runs twice per day:

| Run | UTC Time | Purpose |
| --- | --- | --- |
| 1 | 00:30 | Build one premium AI chatbot product |
| 2 | 12:30 | Build one premium AI chatbot product |

Manual runs are also available from GitHub Actions.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `ai-chatbots/` | Generated premium AI chatbot products |
| `docs/` | GitHub Pages browser demos |
| `tools/chatbot_factory/` | Product generator and validator |
| `tracking/` | Success, deployment, model, quality, and metrics logs |
| `.github/workflows/` | Automation workflows |

## Flagship Direction

The archive is focused on five flagship product families:

| Product Family | Commercial Angle |
| --- | --- |
| Medical coding AI | Revenue integrity and claim review |
| Biotech research AI | Paper triage and diligence workflows |
| RAG QA AI | Source-grounded answer auditing |
| Automation AI | Operations workflow risk analysis |
| Local LLM AI | Private model evaluation and benchmarking |

## Premium Product Catalog

| S.No | Product | Made On (UTC) | Category | Folder | Value | Demo |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | SourceProof AI RAG Answer Auditor | 2026-05-26 16:31 UTC | RAG | `ai-chatbots/sourceproof-rag-answer-auditor-2026-05-26-163112z` | $2,000/month RAG QA suite | https://meenavignesh-svg.github.io/ai-chat-bots-per-minute/sourceproof-rag-answer-auditor-2026-05-26-163112z/ |
| 2 | ClaimGuard AI Revenue Integrity Copilot | 2026-05-26 16:33 UTC | Medical Coding | `ai-chatbots/claimguard-revenue-integrity-copilot-2026-05-26-163320z` | $1,200/month clinic pilot | https://meenavignesh-svg.github.io/ai-chat-bots-per-minute/claimguard-revenue-integrity-copilot-2026-05-26-163320z/ |
| 3 | BioSignal AI Paper-to-Decision Analyst | 2026-05-26 16:37 UTC | Biotech | `ai-chatbots/biosignal-paper-decision-analyst-2026-05-26-163716z` | $1,500/month diligence workspace | https://meenavignesh-svg.github.io/ai-chat-bots-per-minute/biosignal-paper-decision-analyst-2026-05-26-163716z/ |
| 4 | BioSignal AI Paper-to-Decision Analyst | 2026-05-26 16:45 UTC | Biotech | `ai-chatbots/biosignal-paper-decision-analyst-2026-05-26-164535z` | $1,500/month diligence workspace | https://meenavignesh-svg.github.io/ai-chat-bots-per-minute/biosignal-paper-decision-analyst-2026-05-26-164535z/ |

## Required Secrets

Set these in GitHub repository secrets:

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`

Optional:

- `OPENAI_MODEL`
- `GEMINI_MODEL`
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_FROM`

## Pages

Use one simple deployment path:

- Source: **Deploy from a branch**
- Branch: `main`
- Folder: `/docs`

Do not use the GitHub Actions Pages source for this repo. The generated chatbot demos are static files under `docs/`, so branch-based Pages is the most reliable option.

Demo home:

https://meenavignesh-svg.github.io/ai-chat-bots-per-minute/

## Quality Rule

If a generated product does not meet the premium standard, the workflow must fail and commit nothing.
