# HelixMind Bio AI

HelixMind Bio AI is a local assistant built for bioinformatics work.

Wake word: `helix`

## Quick Start

1. Install Python 3.10+ and tick **Add python.exe to PATH**.
2. Double-click `install_helixmind_bio_ai.bat`.
3. Double-click `HelixMindBioAI.bat`.
4. Choose `text` or `voice` mode.

## Bioinformatics Jobs

HelixMind Bio AI works locally for:

- GC content
- reverse complement
- DNA to RNA transcription
- DNA translation
- longest ORF search
- motif search
- k-mer counts
- FASTA summaries
- protein molecular weight
- simple global alignment score
- opening NCBI, BLAST, and UniProt

## Example Commands

```text
helix explain bioinformatics
helix gc content of ATGCGCGTTA
helix reverse complement of ATGCCGTA
helix transcribe ATGCCGTA
helix translate dna ATGGCCATTGTA
helix longest orf of AAATGAAATTTTAA
helix find motif ATG in CCCAATGTTTATG
helix kmer count 3 ATGCGCGTTA
helix protein weight of MTEYK
helix align ATGCC with ATGCA
helix summarize fasta C:\path\to\file.fasta
helix open ncbi
helix open blast
helix open uniprot
```

## Windows Installer

The included workflow builds `HelixMindBioAISetup.exe`:

```text
.github/workflows/build-helixmind-bio-ai-installer.yml
```

It packages the app with PyInstaller and Inno Setup.

## Local First

The core bioinformatics tools run locally. No OpenAI, Gemini, or cloud API key is required.

## Source Note

This package has been cleaned and refocused into a local bioinformatics AI assistant.
