# HelixMind Bio AI Command Guide

Use `helix` before a command in voice mode. In text mode, either style works.

## Core

```text
helix help
helix time
helix note extracted sample from patient dataset
helix show notes
helix exit
```

## Sequence Analysis

```text
helix report ATGCGCGTTA
helix gc content of ATGCGCGTTA
helix reverse complement of ATGCCGTA
helix transcribe ATGCCGTA
helix translate dna ATGGCCATTGTA
helix longest orf of AAATGAAATTTTAA
```

## Bioinformatics Utilities

```text
helix codon usage ATGGCCATTGTA
helix restriction scan GAATTCGGATCC
helix primer stats ATGCGTACGTAGCTAGCTA
helix find motif ATG in CCCAATGTTTATG
helix kmer count 3 ATGCGCGTTA
helix protein weight of MTEYK
helix compare ATGCC with ATGCA
helix align ATGCC with ATGCA
```

## FASTA

```text
helix summarize fasta C:\path\to\file.fasta
helix save fasta ATGCGT named sample1 to C:\path\sample.fasta
```

## Science Websites

```text
helix open ncbi
helix open blast
helix open uniprot
helix open ensembl
helix open pdb
helix open pubmed
helix search pubmed for crispr diagnostics
```
