# Premium AI Chatbot Products

This repository is a clean automation archive for building **two serious premium AI chatbot products per day**.

The goal is quality, not volume. Old low-value generated demos were removed. New projects must look and feel like products that could become paid tools.

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
| `tracking/` | Success, deployment, model, and quality logs |
| `.github/workflows/` | Automation workflows |

## Premium Product Catalog

| S.No | Product | Made On (UTC) | Category | Folder | Value | Demo |
| ---: | --- | --- | --- | --- | --- | --- |

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

For browser demos, enable GitHub Pages with either:

- Source: **Deploy from a branch**, branch `main`, folder `/docs`, or
- Source: **GitHub Actions** using the deploy workflow.

Demo home:

https://meenavignesh-svg.github.io/ai-chat-bots-per-minute/

## Quality Rule

If a generated product does not meet the premium standard, the workflow must fail and commit nothing.
