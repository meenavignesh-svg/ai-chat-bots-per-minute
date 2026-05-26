# Chatbot Factory

Generates one unique chatbot project at a time.

## Behavior

- Reads existing catalog entries from `README.md`.
- Uses OpenAI or Gemini for fresh premium concepts when secrets are available.
- Falls back to the local idea engine if AI keys are not available.
- Creates a complete visual browser-demo chatbot in `ai-chatbots/`.
- Updates tracking files.
- Avoids repeated slugs.

## Manual Run

```bash
python tools/chatbot_factory/generate.py
```
