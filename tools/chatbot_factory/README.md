# Chatbot Factory

Generates one premium chatbot project at a time.

## Premium-Only Rule

The workflow must not commit a generated chatbot unless it passes `validate_premium.py`.

A project must include:

- a polished browser UI
- a first-screen visual hero with image/fallback artwork
- browser demo mode
- optional real AI mode through the OpenAI SDK
- `OPENAI_API_KEY` kept on the server when deployed
- visitor API-key support through browser `sessionStorage`
- README, package, Vercel config, API route, and public UI files

## Behavior

- Reads existing catalog entries from `README.md`.
- Uses OpenAI or Gemini for fresh premium concepts when secrets are available.
- Falls back to the local idea engine if AI keys are not available.
- Creates a complete visual browser-demo chatbot in `ai-chatbots/`.
- Validates the generated project before the workflow can commit it.
- Updates tracking files.
- Avoids repeated slugs.

## Manual Run

```bash
python tools/chatbot_factory/generate.py
python tools/chatbot_factory/validate_premium.py generated-chatbot.txt
```
