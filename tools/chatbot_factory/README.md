# Chatbot Factory

Generates one unique chatbot project at a time.

## Behavior

- Reads existing catalog entries from `README.md`.
- Picks an unused theme from `tools/chatbot_factory/generate.py`.
- Creates a complete browser-demo chatbot in `ai-chatbots/`.
- Updates tracking files.
- Stops when all themes are used, so duplicates are avoided.

## Manual Run

```bash
python tools/chatbot_factory/generate.py
```
