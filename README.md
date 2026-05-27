# Professor Voice Assistant

## Download

**Windows app installer:** [Download ProfessorSetup.exe from the latest release](https://github.com/meenavignesh-svg/ai-chat-bots-per-minute/releases/latest)

Download `ProfessorSetup.exe`, open it, and install Professor like a normal Windows app. It adds a Start Menu shortcut and optional Desktop shortcut.

**Source ZIP:** [Download source ZIP](https://github.com/meenavignesh-svg/ai-chat-bots-per-minute/archive/refs/heads/main.zip)

A lightweight offline-first voice assistant for Windows 11. Professor can open apps, search the web, create safe folders, tell the time, help with beginner bioinformatics tasks, and optionally answer using OpenAI or Gemini when an API key exists.

This project is original code, built in the style of common desktop voice assistants. No API keys are stored in the repository.

## Features

- Wake word: `professor`
- `open chrome`
- `open vscode`
- `open youtube`
- `search google for <query>`
- `create folder <name>`
- `open folder`
- `tell time`
- `explain bioinformatics`
- `gc content of <DNA sequence>`
- `reverse complement of <DNA sequence>`
- `transcribe <DNA sequence>`
- `translate dna <DNA sequence>`
- `exit`
- Offline voice output with `pyttsx3`
- Optional OpenAI or Gemini response mode

## Install Like A Windows App

1. Open [latest release](https://github.com/meenavignesh-svg/ai-chat-bots-per-minute/releases/latest).
2. Download `ProfessorSetup.exe`.
3. Double-click `ProfessorSetup.exe`.
4. Finish the installer.
5. Open Professor from the Start Menu or Desktop shortcut.

If the latest release is not visible yet, open [Build Windows Installer](https://github.com/meenavignesh-svg/ai-chat-bots-per-minute/actions/workflows/build-windows-installer.yml), wait for the run to finish, then check the latest release again.

## Safety

- API keys are read only from environment variables.
- Keys are never hardcoded.
- AI responses are never executed as system commands.
- Dangerous commands like deleting system files are not included.
- Shutdown and restart are blocked unless a separate confirmation feature is added later.

## Simple ZIP Setup

Use this only if you do not want the installer:

1. Download the source ZIP.
2. Extract it.
3. Double-click `install.bat`.
4. Double-click `Professor.bat`.

If Windows asks for microphone permission, allow it.

## Manual Setup

1. Install Python 3.10 or newer.
2. Open PowerShell in this folder.
3. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

If `PyAudio` fails to install, use:

```powershell
pip install pipwin
pipwin install pyaudio
pip install -r requirements.txt
```

## Optional AI Mode

OpenAI:

```powershell
$env:OPENAI_API_KEY="your_openai_key_here"
```

Gemini:

```powershell
$env:GEMINI_API_KEY="your_gemini_key_here"
```

Professor still works without these keys.

## Run

Say:

```text
professor open chrome
professor open youtube
professor search google for python projects
professor create folder school notes
professor tell time
professor explain bioinformatics
professor gc content of ATGCGCGTTA
professor reverse complement of ATGCCGTA
professor transcribe ATGCCGTA
professor translate dna ATGGCCATTGTA
professor exit
```

## Offline Bioinformatics Tools

Professor can run these without any internet connection:

- GC percentage calculation
- DNA reverse complement
- DNA to RNA transcription
- Basic DNA codon translation
- Short beginner explanation of bioinformatics

## Low-End Laptop Notes

- Uses offline `pyttsx3` for voice output.
- Keeps local command handling simple and fast.
- Cloud AI loads only when a key exists and a command is not recognized locally.
