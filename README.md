# HelixMind Bio AI

**HelixMind Bio AI** is a local-first Windows assistant for bioinformatics and safe desktop work. She is designed to feel like a real-time worker living in your computer: always ready in the console, accepting text or voice commands, keeping session notes, queueing jobs, handling files in her workspace, and processing sequence tasks locally.

Wake word: `helix`

## Personality

HelixMind is not just a generic Jarvis clone. She is a focused local coworker for bioinformatics, research support, notes, folders, simple files, web searches, and lightweight productivity.

She can:

- stay open in text or voice mode
- report what she is doing with `helix status`
- remember session notes while running
- queue multiple jobs and process them together
- write a local session log to `helixmind_session_log.txt`
- create and read files inside `HelixMind_Workspace`
- open allowed apps and useful websites
- work offline for core DNA/RNA/protein analysis

## What She Can Do

Bioinformatics:

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

General safe work:

- create folders in her workspace
- write small text files in her workspace
- read text files
- list files
- make checklists
- summarize pasted text
- draft email text
- open Notepad, Calculator, Paint, Explorer, Chrome, or VS Code if installed
- search the web in your browser

## Quick Start

1. Install Python 3.10+ and tick **Add python.exe to PATH**.
2. Double-click `install_helixmind_bio_ai.bat`.
3. Double-click `HelixMindBioAI.bat`.
4. Choose `text` or `voice` mode.

If voice input is difficult on your laptop, choose text mode. All commands still work.

## Real-Time Worker Commands

```text
helix status
helix project CRISPR off-target study
helix note check GC before primer design
helix show notes
helix add job gc content of ATGCGCGTTA
helix add job write file plan.txt with analyze FASTA and design primers
helix show jobs
helix run jobs
helix presence on
helix quiet mode
```

## General Work Commands

```text
helix create folder crispr_project
helix write file notes.txt with today I checked primer GC
helix read file notes.txt
helix list files
helix make checklist collect FASTA, run GC, design primers
helix summarize text paste your paragraph here
helix draft email I finished the sequence report and primer check
helix open app notepad
helix open app calculator
helix open google
helix open github
helix search web for ncbi blast tutorial
```

## Bioinformatics Example Commands

```text
helix help
helix report ATGCGCGTTA
helix gc content of ATGCGCGTTA
helix reverse complement of ATGCCGTA
helix transcribe ATGCCGTA
helix translate dna ATGGCCATTGTA
helix longest orf of AAATGAAATTTTAA
helix codon usage ATGGCCATTGTA
helix restriction scan GAATTCGGATCC
helix primer stats ATGCGTACGTAGCTAGCTA
helix find motif ATG in CCCAATGTTTATG
helix kmer count 3 ATGCGCGTTA
helix protein weight of MTEYK
helix compare ATGCC with ATGCA
helix align ATGCC with ATGCA
helix summarize fasta C:\path\to\file.fasta
helix save fasta ATGCGT named sample1 to C:\path\sample.fasta
helix search pubmed for crispr diagnostics
helix open blast
```

## Local-First Privacy

The built-in bioinformatics tools run on the computer. HelixMind Bio AI does not upload your sequences to a cloud service. Browser-opening commands only open websites in your browser.

She does not watch private files automatically. You give her a folder, sequence, FASTA path, or command when you want work done.

## Safety Rules

- No API keys are hardcoded.
- No destructive system commands are included.
- The assistant does not run unknown shell commands from generated text.
- File writing is limited to explicit FASTA export commands, the local session log, and `HelixMind_Workspace`.
- Restart, shutdown, delete, and system-control commands are intentionally not implemented.
- App launching is allowlisted.

## Windows Installer

The included GitHub Actions workflow builds a Windows installer:

```text
.github/workflows/build-helixmind-bio-ai-installer.yml
```

When the workflow succeeds, it publishes `HelixMindBioAISetup.exe` in the latest release.

Latest release:

```text
https://github.com/meenavignesh-svg/HELIX_MINDBIO_AI/releases/latest
```

## Project Files

```text
helixmind_bio_ai.py                 Main assistant app
bioinformatics_tools.py             Offline bioinformatics engine
HelixMindBioAI.bat                  Windows launcher
install_helixmind_bio_ai.bat        Dependency installer
requirements_helixmind_bio_ai.txt   Python requirements
helixmind_bio_ai.spec               PyInstaller build config
installer/HelixMindBioAI.iss        Inno Setup installer script
docs/COMMANDS.md                    Command guide
docs/PERSONALITY.md                 Personality and safety spec
sample_data/example_gene.fasta      Example FASTA file
```

## Status

HelixMind Bio AI is now a clean local bioinformatics and safe-work desktop assistant.
