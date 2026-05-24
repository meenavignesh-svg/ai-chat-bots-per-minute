# Low-Token Chatbot Factory

This repo now uses a low-token setup for repetitive chatbot generation.

## What Runs Automatically

GitHub Actions runs `.github/workflows/generate-chatbot.yml` once per hour. It calls:

```bash
python tools/chatbot_factory/generate.py
```

The generator creates a new project under `ai-chatbots/` and commits it back to the repo.

## Token Strategy

- Python templates create the repeated file structure.
- Built-in theme data creates browser demo replies without external tokens.
- Optional Ollama support can generate small theme copy if you provide `OLLAMA_URL` and `OLLAMA_MODEL` secrets.
- Codex/ChatGPT should be saved for bugs, architecture, biotech logic, optimization, and review.

## Optional Ollama

GitHub-hosted runners cannot access your laptop's local Ollama server. To use Ollama in Actions, run a self-hosted GitHub runner on a machine where Ollama is available, or expose an Ollama endpoint carefully and store it as the `OLLAMA_URL` secret.

If Ollama is unavailable, the generator still works using templates.

## Manual Run

Go to Actions -> Generate chatbot project -> Run workflow. You can optionally provide a theme slug such as:

- `robot-gardener`
- `startup-coach`
- `biotech-notes`
- `game-master`

## Output

Each generated chatbot includes:

- browser demo mode that works without setup
- optional Vercel real AI mode
- visitor-provided OpenAI API key flow
- README deployment notes
