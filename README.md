# HelixMind Bio AI

**HelixMind Bio AI** is a local-first Windows desktop assistant for bioinformatics work. It supports text and voice control, runs core analysis offline, and is designed for lightweight laptops.

Wake word: `helix`

## What She Can Do

HelixMind Bio AI can help with:

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

## Quick Start

1. Install Python 3.10+ and tick **Add python.exe to PATH**.
2. Double-click `install_helixmind_bio_ai.bat`.
3. Double-click `HelixMindBioAI.bat`.
4. Choose `text` or `voice` mode.

If voice input is difficult on your laptop, choose text mode. All bioinformatics commands still work.

## Example Commands

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

The built-in bioinformatics tools run on the computer. HelixMind Bio AI does not upload your sequences to a cloud service. Browser-opening commands only open public science websites in your browser.

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
```

## Safety Rules

- No API keys are hardcoded.
- No destructive system commands are included.
- The assistant does not run unknown shell commands from generated text.
- File writing is limited to explicit FASTA export commands.
- Restart, shutdown, delete, and system-control commands are intentionally not implemented.

## Status

HelixMind Bio AI is now focused as a clean bioinformatics desktop assistant instead of a generic Jarvis clone.
