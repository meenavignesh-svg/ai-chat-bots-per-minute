# JANET Bio AI

**JANET** is a light-themed, local-first Windows desktop agent for bioinformatics and computer work. She is designed to work like a local OpenClaw-style assistant: chat, plan, remember task context, open apps, type, click, run visible steps, and use local tools.

Wake word: `janet`

Legacy wake word: `helix` still works.

## Local OpenClaw-Style Agent

JANET can:

- chat in a light desktop window
- make visible plans before work
- open desktop apps
- type or paste into the active window
- press keys and hotkeys
- click the mouse
- queue multi-step jobs
- keep local session notes
- run local bioinformatics tools
- use optional AI providers only when you configure them

Core execution stays local. JANET does not need cloud AI to open apps, type, click, manage notes, or run bioinformatics tools.

## Optional AI Providers

The chat window includes an **AI settings** row:

```text
Provider | Model | Endpoint | API key | Use AI
```

Supported modes:

- `local` fallback planning with no API key
- `ollama` for local LLMs
- `openai`
- `gemini`
- `anthropic`
- `openrouter`
- `compatible` for custom OpenAI-compatible APIs

API keys are not hardcoded in the repo. When pasted into the app, the key is kept in the running app session. You can also use environment variables yourself:

```text
JANET_AI_PROVIDER
JANET_AI_MODEL
JANET_AI_KEY
JANET_AI_ENDPOINT
```

## AI Commands

```text
ask ai explain this bioinformatics workflow
plan analyze this FASTA file, summarize GC, then open PubMed
agent plan open Chrome, search PubMed, and draft notes
```

If provider is `local`, JANET creates a simple local plan. If you choose a provider and paste a key, JANET uses that provider for reasoning while still using local desktop tools for actions.

## Desktop Control Commands

```text
janet desktop status
janet open any app chrome
janet open any app notepad
janet type text Hello, I am JANET.
janet paste text This goes into the active window.
janet press key enter
janet hotkey ctrl+s
janet wait 0.2
janet click
janet click 500 300
```

## Bioinformatics

JANET can help with:

- DNA/RNA cleanup and sequence reports
- GC and AT content
- reverse complement
- DNA to RNA transcription
- DNA translation
- longest ORF detection
- codon usage summaries
- motif search
- k-mer counting
- primer statistics and estimated Tm
- common restriction enzyme site scanning
- FASTA summaries with total bases and N50
- protein molecular weight estimation
- quick sequence comparison
- simple global alignment scoring
- PubMed, NCBI, BLAST, UniProt, Ensembl, and PDB opening/searching

## Desktop App

After installing, open **JANET** from the Start Menu or desktop shortcut.

The app opens a light chat window where you can type commands like:

```text
janet status
janet open any app chrome
janet type text Hello, I am JANET.
janet gc content of ATGCGCGTTA
janet search pubmed for crispr diagnostics
```

## Safety Rules

- No API keys are hardcoded.
- Session API keys are hidden in the UI field.
- She will not type passwords, OTPs, API keys, tokens, secrets, or credit card data into other apps.
- No destructive system commands are included.
- JANET does not run unknown shell commands from AI text.
- File writing is limited to explicit FASTA export commands, the local session log, and `JANET_Workspace`.
- Restart, shutdown, delete, and destructive system control are intentionally not implemented.

## Windows Installer

GitHub Actions builds:

```text
JANETSetup.exe
```

Latest release:

```text
https://github.com/meenavignesh-svg/HELIX_MINDBIO_AI/releases/latest
```
