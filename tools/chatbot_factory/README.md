# Chatbot Factory Tool

`generate.py` creates one new chatbot project with browser demo mode and optional Vercel real AI mode.

## GitHub Actions

The scheduled workflow installs Ollama, pulls `llama3.2:1b`, verifies the model response, and runs this generator. Ollama is mandatory for scheduled generation; if Ollama fails, the workflow fails.

## Run Locally

From the repository root with Ollama:

```bash
ollama serve
ollama pull llama3.2:1b
OLLAMA_URL=http://localhost:11434 OLLAMA_MODEL=llama3.2:1b python tools/chatbot_factory/generate.py
```

Optional theme:

```bash
CHATBOT_THEME=biotech-notes OLLAMA_URL=http://localhost:11434 OLLAMA_MODEL=llama3.2:1b python tools/chatbot_factory/generate.py
```
