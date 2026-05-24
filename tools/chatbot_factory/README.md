# Chatbot Factory Tool

`generate.py` creates one new chatbot project with browser demo mode and optional Vercel real AI mode.

## GitHub Actions

The scheduled workflow installs Ollama, pulls `llama3.2:1b`, and runs this generator. If Ollama is unavailable, the generator falls back to built-in templates.

## Run Locally

From the repository root:

```bash
python tools/chatbot_factory/generate.py
```

Optional theme:

```bash
CHATBOT_THEME=biotech-notes python tools/chatbot_factory/generate.py
```

Optional Ollama support:

```bash
ollama serve
ollama pull llama3.2:1b
OLLAMA_URL=http://localhost:11434 OLLAMA_MODEL=llama3.2:1b python tools/chatbot_factory/generate.py
```

Without Ollama, the script uses built-in templates.
