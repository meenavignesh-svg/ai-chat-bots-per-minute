# AI Chatbots Per Minute

An automated AI chatbot lab that generates small, polished, web-ready chatbot projects on a schedule.

This repository is built as an experimentation archive: each run creates a new chatbot concept, adds a premium browser demo, prepares optional real AI mode, updates tracking files, and records the result in the catalog.

## Highlights

- Automated chatbot generation with GitHub Actions
- AI-assisted concept creation using OpenAI or Gemini when keys are available
- Local fallback idea engine when external AI keys are not available
- Premium visual UI template with category-matched cover imagery
- Browser demo that works immediately without setup
- Optional Vercel/OpenAI mode for real AI responses
- Email notification after successful generation
- Catalog and tracking files updated on every run

## How It Works

1. GitHub Actions runs the chatbot factory.
2. The factory creates a fresh chatbot concept.
3. A complete project is written into `ai-chatbots/`.
4. The root catalog and tracking files are updated.
5. The workflow commits the new project back to the repository.
6. If email secrets are configured, a notification email is sent.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `ai-chatbots/` | Generated chatbot projects |
| `tools/chatbot_factory/` | Automation scripts that create projects |
| `.github/workflows/generate-chatbot.yml` | Scheduled GitHub Actions workflow |
| `tracking/` | Success, model, deployment, and experiment logs |
| `README.md` | Main project catalog and setup guide |

## Chatbot Catalog

| S.No | Chatbot | Made On (UTC) | Category | Folder | Status | Model | Deployment |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | Education Builder Daily Brief | 2026-05-26 15:41 UTC | Education | `ai-chatbots/learn-builder-brief-chatbot-2026-05-26-154115z` | Successful demo with visual cover | Browser demo + Vercel/OpenAI-ready | Not deployed |
| 2 | Biotech Evidence Navigator | 2026-05-26 15:43 UTC | Biotech | `ai-chatbots/biotech-evidence-navigator-chatbot-2026-05-26-154302z` | Successful demo with visual cover | Browser demo + Vercel/OpenAI-ready | Not deployed |
| 3 | Voice Agents Builder Idea Sprint | 2026-05-26 15:46 UTC | Voice Agents | `ai-chatbots/voice-builder-sprint-chatbot-2026-05-26-154639z` | Successful demo with visual cover | Browser demo + Vercel/OpenAI-ready | Not deployed |
| 4 | RAG Analyst Decision Helper | 2026-05-26 15:47 UTC | RAG | `ai-chatbots/rag-analyst-decision-chatbot-2026-05-26-154709z` | Successful demo with visual cover | Browser demo + Vercel/OpenAI-ready | Not deployed |
| 5 | Education Navigator Explainer | 2026-05-26 15:50 UTC | Education | `ai-chatbots/learn-nav-explain-chatbot-2026-05-26-155050z` | Successful demo with visual cover | Browser demo + Vercel/OpenAI-ready | Not deployed |
| 6 | Healthcare Planner Daily Brief | 2026-05-26 16:06 UTC | Healthcare | `ai-chatbots/care-planner-brief-chatbot-2026-05-26-160631z` | Premium Split Command Center with Ops Check and unique palette | Browser demo + Vercel/OpenAI-ready | https://meenavignesh-svg.github.io/ai-chat-bots-per-minute/care-planner-brief-chatbot-2026-05-26-160631z/ |
| 7 | Local LLM Coach Idea Sprint | 2026-05-26 16:07 UTC | Local LLM | `ai-chatbots/local-coach-sprint-chatbot-2026-05-26-160708z` | Premium Insight Deck with Practice Coach and unique palette | Browser demo + Vercel/OpenAI-ready | https://meenavignesh-svg.github.io/ai-chat-bots-per-minute/local-coach-sprint-chatbot-2026-05-26-160708z/ |

## Project Standard

Each generated chatbot includes:

- Premium first-screen visual cover
- External category-matched photo with local fallback artwork
- Browser demo mode that works without setup
- Optional Vercel/OpenAI real AI mode
- Visitor API-key support through browser `sessionStorage`
- `README.md`, `package.json`, `vercel.json`, `api/chat.js`, and public UI files
- Responsive HTML/CSS/JS interface
- Catalog and tracking updates

## GitHub Secrets

Add secrets at: Settings -> Secrets and variables -> Actions -> New repository secret.

### AI Concept Generation

Required for OpenAI-generated concepts:

- `OPENAI_API_KEY`

Optional:

- `OPENAI_MODEL` such as `gpt-4.1-mini`
- `GEMINI_API_KEY`
- `GEMINI_MODEL` such as `gemini-1.5-flash`

### Email Notifications

Required for email notifications:

- `MAIL_USERNAME`
- `MAIL_PASSWORD`

Optional:

- `MAIL_SERVER` defaults to `smtp.gmail.com`
- `MAIL_PORT` defaults to `465`
- `MAIL_FROM` defaults to `MAIL_USERNAME`

For Gmail, use a Gmail App Password instead of the normal account password.

## Running Manually

Use GitHub Actions:

1. Open the Actions tab.
2. Select `Generate chatbot project`.
3. Click `Run workflow`.

The workflow also runs automatically on its schedule.

## Deployment

Each chatbot is Vercel-ready.

For a generated chatbot:

1. Import this repository into Vercel.
2. Set the Vercel root directory to the chatbot folder.
3. Add `OPENAI_API_KEY` as a Vercel environment variable, or let visitors enter their own key in the UI.
4. Deploy and add the public URL to `tracking/deployment-links.md`.

## Tracking

- Successful projects: `tracking/successful-projects.md`
- Failed experiments: `tracking/failed-experiments.md`
- Model usage: `tracking/model-usage.md`
- Deployment links: `tracking/deployment-links.md`

## Goal

The goal is not to create random repo noise. The goal is to build a clean long-running archive of generated agent experiments with visible progress, consistent structure, strong UI quality, and repeatable automation.
