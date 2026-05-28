"""Offline bioinformatics helpers for HelixMind Bio AI.

The functions in this module are intentionally local-first. They do not call
cloud APIs, do not upload sequences, and are suitable for small FASTA files,
classroom work, portfolio demos, and quick desktop analysis.
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

RESTRICTION_ENZYMES = {
    "EcoRI": "GAATTC",
    "BamHI": "GGATCC",
    "HindIII": "AAGCTT",
    "NotI": "GCGGCCGC",
    "XhoI": "CTCGAG",
    "NdeI": "CATATG",
    "KpnI": "GGTACC",
    "SacI": "GAGCTC",
    "PstI": "CTGCAG",
    "SmaI": "CCCGGG",
}


def clean_sequence(sequence: str, alphabet: str = "ACGTU") -> str:
    return "".join(base for base in sequence.upper() if base in alphabet)


def dna_sequence(sequence: str) -> str:
    return clean_sequence(sequence).replace("U", "T")


def gc_content(sequence: str) -> str:
    seq = dna_sequence(sequence)
    if not seq:
        return "No DNA/RNA sequence found."
    gc = seq.count("G") + seq.count("C")
    return f"GC content: {(gc / len(seq)) * 100:.2f}% across {len(seq)} bases."


def gc_percent(sequence: str) -> float:
    seq = dna_sequence(sequence)
    if not seq:
        return 0.0
    return ((seq.count("G") + seq.count("C")) / len(seq)) * 100


def reverse_complement(sequence: str) -> str:
    seq = dna_sequence(sequence)
    if not seq:
        return "No DNA sequence found."
    return seq.translate(DNA_COMPLEMENT)[::-1]


def transcribe(sequence: str) -> str:
    seq = dna_sequence(sequence)
    if not seq:
        return "No DNA sequence found."
    return seq.replace("T", "U")


def translate_dna(sequence: str) -> str:
    seq = dna_sequence(sequence)
    if len(seq) < 3:
        return "Need at least one full codon."
    ignored = len(seq) % 3
    protein = "".join(CODON_TABLE.get(seq[i:i + 3], "X") for i in range(0, len(seq) - ignored, 3))
    note = "" if ignored == 0 else f" Ignored {ignored} trailing base(s)."
    return f"{protein}{note}"


def find_motif(sequence: str, motif: str) -> str:
    seq = dna_sequence(sequence)
    query = dna_sequence(motif)
    if not seq or not query:
        return "Give both a sequence and a motif."
    positions = [str(i + 1) for i in range(len(seq) - len(query) + 1) if seq[i:i + len(query)] == query]
    if not positions:
        return f"Motif {query} not found."
    return f"Motif {query} found at 1-based positions: {', '.join(positions)}."


def kmer_counts(sequence: str, k: int = 3, top: int = 10) -> str:
    seq = dna_sequence(sequence)
    if k < 1 or k > 12:
        return "Choose a k-mer size from 1 to 12."
    if len(seq) < k:
        return f"Need at least {k} bases."
    counts = Counter(seq[i:i + k] for i in range(len(seq) - k + 1))
    rows = [f"{kmer}: {count}" for kmer, count in counts.most_common(top)]
    return "Top k-mers:\n" + "\n".join(rows)


def codon_usage(sequence: str, top: int = 12) -> str:
    seq = dna_sequence(sequence)
    if len(seq) < 3:
        return "Need at least one codon."
    codons = [seq[i:i + 3] for i in range(0, len(seq) - (len(seq) % 3), 3)]
    counts = Counter(codons)
    rows = [f"{codon} ({CODON_TABLE.get(codon, 'X')}): {count}" for codon, count in counts.most_common(top)]
    return "Top codons:\n" + "\n".join(rows)


def longest_orf(sequence: str) -> str:
    seq = dna_sequence(sequence)
    best = ""
    best_frame = 0
    best_start = 0
    for frame in range(3):
        active = ""
        active_start = 0
        for index in range(frame, len(seq) - 2, 3):
            codon = seq[index:index + 3]
            aa = CODON_TABLE.get(codon, "X")
            if codon == "ATG" and not active:
                active = "M"
                active_start = index + 1
            elif active and aa == "*":
                if len(active) > len(best):
                    best = active
                    best_frame = frame + 1
                    best_start = active_start
                active = ""
            elif active:
                active += aa
        if len(active) > len(best):
            best = active
            best_frame = frame + 1
            best_start = active_start
    if not best:
        return "Longest ORF protein: none found."
    return f"Longest ORF protein: {best}\nFrame: {best_frame}\nStart base: {best_start}\nLength: {len(best)} aa"


def protein_weight(protein: str) -> str:
    seq = clean_sequence(protein, alphabet="ARNDCEQGHILKMFPSTWYV")
    if not seq:
        return "No protein sequence found."
    weight = sum(PROTEIN_WEIGHTS[aa] for aa in seq)
    return f"Approximate protein molecular weight: {weight:.2f} Da for {len(seq)} residues."


def primer_stats(primer: str) -> str:
    seq = dna_sequence(primer)
    if not seq:
        return "No primer sequence found."
    if len(seq) < 14 or len(seq) > 35:
        length_note = "outside the common 14-35 bp range"
    else:
        length_note = "inside the common 14-35 bp range"
    gc = gc_percent(seq)
    if len(seq) < 14:
        tm = (seq.count("A") + seq.count("T")) * 2 + (seq.count("G") + seq.count("C")) * 4
    else:
        tm = 64.9 + 41 * (seq.count("G") + seq.count("C") - 16.4) / len(seq)
    tail = seq[-5:] if len(seq) >= 5 else seq
    gc_clamp = tail.count("G") + tail.count("C")
    return (
        f"Primer length: {len(seq)} bp ({length_note})\n"
        f"GC: {gc:.2f}%\n"
        f"Estimated Tm: {tm:.2f} C\n"
        f"3-prime GC clamp count in last 5 bases: {gc_clamp}"
    )


def restriction_scan(sequence: str) -> str:
    seq = dna_sequence(sequence)
    if not seq:
        return "No DNA sequence found."
    hits: list[str] = []
    for enzyme, motif in RESTRICTION_ENZYMES.items():
        positions = [str(i + 1) for i in range(len(seq) - len(motif) + 1) if seq[i:i + len(motif)] == motif]
        if positions:
            hits.append(f"{enzyme} ({motif}): {', '.join(positions)}")
    if not hits:
        return "No common restriction sites found in the built-in panel."
    return "Restriction sites found:\n" + "\n".join(hits)


def compare_sequences(seq_a: str, seq_b: str) -> str:
    a = dna_sequence(seq_a)
    b = dna_sequence(seq_b)
    if not a or not b:
        return "Give two DNA/RNA sequences."
    limit = min(len(a), len(b))
    changes = []
    for index in range(limit):
        if a[index] != b[index]:
            changes.append(f"{index + 1}:{a[index]}>{b[index]}")
    if len(a) != len(b):
        changes.append(f"Length differs: {len(a)} vs {len(b)} bases")
    if not changes:
        return "Sequences match exactly."
    preview = ", ".join(changes[:25])
    suffix = "" if len(changes) <= 25 else f" ... plus {len(changes) - 25} more"
    return f"Differences: {len(changes)}\n{preview}{suffix}"


def sequence_report(sequence: str) -> str:
    seq = dna_sequence(sequence)
    if not seq:
        return "No DNA/RNA sequence found."
    counts = Counter(seq)
    at = counts["A"] + counts["T"]
    gc = counts["G"] + counts["C"]
    n50 = len(seq) if seq else 0
    return (
        "Sequence report\n"
        f"Length: {len(seq)} bases\n"
        f"A: {counts['A']}  T: {counts['T']}  G: {counts['G']}  C: {counts['C']}\n"
        f"GC: {(gc / len(seq)) * 100:.2f}%  AT: {(at / len(seq)) * 100:.2f}%\n"
        f"Reverse complement preview: {reverse_complement(seq)[:80]}\n"
        f"Translation preview: {translate_dna(seq)[:80]}\n"
        f"N50: {n50} for this single sequence"
    )


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
    lengths = sorted((len(seq) for seq in records.values()), reverse=True)
    total = sum(lengths)
    running = 0
    n50 = 0
    for length in lengths:
        running += length
        if running >= total / 2:
            n50 = length
            break
    lines = [f"Records: {len(records)}", f"Total bases: {total}", f"N50: {n50}"]
    for name, seq in records.items():
        lines.append(f"{name}: {len(seq)} bases, GC {gc_percent(seq):.2f}%")
    return "\n".join(lines)


def write_fasta(path_text: str, name: str, sequence: str) -> str:
    path = Path(path_text.strip().strip('"'))
    seq = dna_sequence(sequence)
    if not seq:
        return "No DNA/RNA sequence found."
    lines = [f">{name or 'helixmind_sequence'}"]
    lines.extend(seq[i:i + 70] for i in range(0, len(seq), 70))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return f"Saved FASTA file: {path}"


def global_align(seq_a: str, seq_b: str) -> str:
    a = dna_sequence(seq_a)
    b = dna_sequence(seq_b)
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
    identity = sum(1 for left, right in zip(a, b) if left == right) / max(len(a), len(b)) * 100
    return f"Needleman-Wunsch score: {score[-1][-1]}\nQuick identity estimate: {identity:.2f}%"
