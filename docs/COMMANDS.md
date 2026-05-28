# JANET Command Guide

Use `janet` before a command in voice mode. In text mode, either style works. The old `helix` wake word still works as a fallback.

## Speed And Theme

```text
janet fast mode
janet normal mode
janet light theme
janet voice output off
janet voice output on
janet status
```

## Desktop Control

```text
janet desktop status
janet open any app chrome
janet open any app notepad
janet open any app visual studio code
janet type text Hello, I am JANET.
janet paste text This goes into the active window.
janet press key enter
janet press key tab
janet hotkey ctrl+s
janet hotkey ctrl+a
janet hotkey ctrl+c
janet hotkey ctrl+v
janet wait 0.2
janet click
janet click 500 300
```

## Desktop Workflow Example

```text
janet add job open any app notepad
janet add job wait 0.5
janet add job type text JANET is working inside this computer.
janet add job hotkey ctrl+s
janet run jobs
```

## Real-Time Presence

```text
janet status
janet project CRISPR off-target study
janet presence on
janet quiet mode
janet what are you doing
janet are you there
```

## Session Notes

```text
janet note extracted sample from patient dataset
janet show notes
```

## Job Queue

```text
janet add job gc content of ATGCGCGTTA
janet add job primer stats ATGCGTACGTAGCTAGCTA
janet add job write file plan.txt with analyze FASTA and design primers
janet show jobs
janet run jobs
janet clear jobs
```

## General Safe Work

```text
janet create folder crispr_project
janet write file notes.txt with today I checked primer GC
janet read file notes.txt
janet list files
janet list files crispr_project
janet make checklist collect FASTA, run GC, design primers
janet summarize text paste your paragraph here
janet draft email I finished the sequence report and primer check
```

## Apps And Websites

```text
janet open app notepad
janet open app calculator
janet open app paint
janet open app explorer
janet open app chrome
janet open app vscode
janet open google
janet open youtube
janet open github
janet open chatgpt
janet search web for ncbi blast tutorial
```

## Core

```text
janet help
janet time
janet exit
```

## Sequence Analysis

```text
janet report ATGCGCGTTA
janet gc content of ATGCGCGTTA
janet reverse complement of ATGCCGTA
janet transcribe ATGCCGTA
janet translate dna ATGGCCATTGTA
janet longest orf of AAATGAAATTTTAA
```

## Bioinformatics Utilities

```text
janet codon usage ATGGCCATTGTA
janet restriction scan GAATTCGGATCC
janet primer stats ATGCGTACGTAGCTAGCTA
janet find motif ATG in CCCAATGTTTATG
janet kmer count 3 ATGCGCGTTA
janet protein weight of MTEYK
janet compare ATGCC with ATGCA
janet align ATGCC with ATGCA
```

## FASTA

```text
janet summarize fasta C:\path\to\file.fasta
janet save fasta ATGCGT named sample1 to C:\path\sample.fasta
```

## Science Websites

```text
janet open ncbi
janet open blast
janet open uniprot
janet open ensembl
janet open pdb
janet open pubmed
janet search pubmed for crispr diagnostics
```

## Safety Limits

JANET can open apps and type into the active window, but she will not type passwords, OTPs, API keys, secrets, credit card details, or run destructive system commands.
