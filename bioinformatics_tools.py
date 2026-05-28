"""Offline bioinformatics helpers for HelixMind Bio AI.

These functions avoid cloud calls and external services. They are meant for
small-to-medium classroom, portfolio, and notebook-style sequence tasks.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path


DNA_COMPLEMENT = str.maketrans("ACGTUacgtu", "TGCAAtgcaa")

CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

PROTEIN_WEIGHTS = {
    "A": 89.09, "R": 174.20, "N": 132.12, "D": 133.10, "C": 121.16,
    "E": 147.13, "Q": 146.15, "G": 75.07, "H": 155.16, "I": 131.17,
    "L": 131.17, "K": 146.19, "M": 149.21, "F": 165.19, "P": 115.13,
    "S": 105.09, "T": 119.12, "W": 204.23, "Y": 181.19, "V": 117.15,
}


def clean_sequence(sequence: str, alphabet: str = "ACGTU") -> str:
    return "".join(base for base in sequence.upper() if base in alphabet)


def gc_content(sequence: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    if not seq:
        return "No DNA/RNA sequence found."
    gc = seq.count("G") + seq.count("C")
    return f"GC content: {(gc / len(seq)) * 100:.2f}% across {len(seq)} bases."


def reverse_complement(sequence: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    if not seq:
        return "No DNA sequence found."
    return seq.translate(DNA_COMPLEMENT)[::-1]


def transcribe(sequence: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    if not seq:
        return "No DNA sequence found."
    return seq.replace("T", "U")


def translate_dna(sequence: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    if len(seq) < 3:
        return "Need at least one full codon."
    ignored = len(seq) % 3
    protein = "".join(CODON_TABLE.get(seq[i:i + 3], "X") for i in range(0, len(seq) - ignored, 3))
    note = "" if ignored == 0 else f" Ignored {ignored} trailing base(s)."
    return f"{protein}{note}"


def find_motif(sequence: str, motif: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    query = clean_sequence(motif).replace("U", "T")
    if not seq or not query:
        return "Give both a sequence and a motif."
    positions = [str(i + 1) for i in range(len(seq) - len(query) + 1) if seq[i:i + len(query)] == query]
    if not positions:
        return f"Motif {query} not found."
    return f"Motif {query} found at 1-based positions: {', '.join(positions)}."


def kmer_counts(sequence: str, k: int = 3, top: int = 10) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    if len(seq) < k:
        return f"Need at least {k} bases."
    counts = Counter(seq[i:i + k] for i in range(len(seq) - k + 1))
    rows = [f"{kmer}: {count}" for kmer, count in counts.most_common(top)]
    return "Top k-mers:\n" + "\n".join(rows)


def longest_orf(sequence: str) -> str:
    seq = clean_sequence(sequence).replace("U", "T")
    best = ""
    for frame in range(3):
        active = ""
        for index in range(frame, len(seq) - 2, 3):
            codon = seq[index:index + 3]
            aa = CODON_TABLE.get(codon, "X")
            if codon == "ATG" and not active:
                active = "M"
            elif active and aa == "*":
                if len(active) > len(best):
                    best = active
                active = ""
            elif active:
                active += aa
        if len(active) > len(best):
            best = active
    return f"Longest ORF protein: {best or 'none found'}"


def protein_weight(protein: str) -> str:
    seq = clean_sequence(protein, alphabet="ARNDCEQGHILKMFPSTWYV")
    if not seq:
        return "No protein sequence found."
    weight = sum(PROTEIN_WEIGHTS[aa] for aa in seq)
    return f"Approximate protein molecular weight: {weight:.2f} Da for {len(seq)} residues."


def read_fasta(path_text: str) -> dict[str, str]:
    path = Path(path_text.strip().strip('"'))
    records: dict[str, list[str]] = {}
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            current = line[1:].strip() or f"record_{len(records) + 1}"
            records[current] = []
        elif current:
            records[current].append(line)
    return {name: "".join(parts) for name, parts in records.items()}


def summarize_fasta(path_text: str) -> str:
    records = read_fasta(path_text)
    if not records:
        return "No FASTA records found."
    lines = [f"Records: {len(records)}"]
    for name, seq in records.items():
        lines.append(f"{name}: {len(seq)} bases, {gc_content(seq)}")
    return "\n".join(lines)


def global_align(seq_a: str, seq_b: str) -> str:
    a = clean_sequence(seq_a).replace("U", "T")
    b = clean_sequence(seq_b).replace("U", "T")
    if not a or not b:
        return "Give two DNA/RNA sequences."
    match, mismatch, gap = 1, -1, -2
    rows, cols = len(a) + 1, len(b) + 1
    score = [[0] * cols for _ in range(rows)]
    for i in range(1, rows):
        score[i][0] = i * gap
    for j in range(1, cols):
        score[0][j] = j * gap
    for i in range(1, rows):
        for j in range(1, cols):
            diag = score[i - 1][j - 1] + (match if a[i - 1] == b[j - 1] else mismatch)
            score[i][j] = max(diag, score[i - 1][j] + gap, score[i][j - 1] + gap)
    return f"Needleman-Wunsch global alignment score: {score[-1][-1]}"
