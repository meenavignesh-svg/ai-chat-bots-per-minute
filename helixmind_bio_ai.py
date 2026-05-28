"""HelixMind Bio AI - offline assistant for bioinformatics work."""

from __future__ import annotations

import datetime as dt
import webbrowser

import pyttsx3
import speech_recognition as sr

import bioinformatics_tools as bio


WAKE_WORD = "helix"


class HelixMindBioAI:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.recognizer = sr.Recognizer()

    def speak(self, text: str) -> None:
        print(f"HelixMind: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=10)
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower().strip()
        except Exception:
            return ""

    def answer(self, command: str) -> tuple[str, bool]:
        command = command.lower().strip()
        if command.startswith(WAKE_WORD):
            command = command.replace(WAKE_WORD, "", 1).strip(" ,")

        if command in {"exit", "quit", "stop", "sleep"}:
            return "Goodbye. I will stop now.", False
        if "time" in command:
            return f"The time is {dt.datetime.now().strftime('%I:%M %p')}.", True
        if "open ncbi" in command:
            webbrowser.open("https://www.ncbi.nlm.nih.gov/")
            return "Opening NCBI.", True
        if "open uniprot" in command:
            webbrowser.open("https://www.uniprot.org/")
            return "Opening UniProt.", True
        if "open blast" in command:
            webbrowser.open("https://blast.ncbi.nlm.nih.gov/")
            return "Opening BLAST.", True
        if "explain bioinformatics" in command:
            return "Bioinformatics uses computing to study DNA, RNA, proteins, variants, genomes, and biological datasets.", True

        if command.startswith("gc content of "):
            return bio.gc_content(command.replace("gc content of ", "", 1)), True
        if command.startswith("reverse complement of "):
            return bio.reverse_complement(command.replace("reverse complement of ", "", 1)), True
        if command.startswith("transcribe "):
            return bio.transcribe(command.replace("transcribe ", "", 1)), True
        if command.startswith("translate dna "):
            return bio.translate_dna(command.replace("translate dna ", "", 1)), True
        if command.startswith("longest orf of "):
            return bio.longest_orf(command.replace("longest orf of ", "", 1)), True
        if command.startswith("protein weight of "):
            return bio.protein_weight(command.replace("protein weight of ", "", 1)), True
        if command.startswith("kmer count "):
            payload = command.replace("kmer count ", "", 1)
            parts = payload.split(" ", 1)
            if parts and parts[0].isdigit() and len(parts) == 2:
                return bio.kmer_counts(parts[1], int(parts[0])), True
            return bio.kmer_counts(payload), True
        if command.startswith("find motif "):
            payload = command.replace("find motif ", "", 1)
            if " in " not in payload:
                return "Use: find motif ATG in ATGCGTATG", True
            motif, sequence = payload.split(" in ", 1)
            return bio.find_motif(sequence, motif), True
        if command.startswith("summarize fasta "):
            try:
                return bio.summarize_fasta(command.replace("summarize fasta ", "", 1)), True
            except Exception as exc:
                return f"Could not read FASTA file: {exc}", True
        if command.startswith("align "):
            payload = command.replace("align ", "", 1)
            if " with " not in payload:
                return "Use: align ATGCC with ATGCA", True
            seq_a, seq_b = payload.split(" with ", 1)
            return bio.global_align(seq_a, seq_b), True

        return "I can help with GC content, reverse complement, transcription, translation, ORFs, motifs, k-mers, FASTA summaries, protein weight, and simple alignment.", True

    def run_text_mode(self) -> None:
        self.speak("HelixMind Bio AI text mode is ready.")
        while True:
            command = input("You: ")
            response, keep_running = self.answer(command)
            self.speak(response)
            if not keep_running:
                break

    def run_voice_mode(self) -> None:
        self.speak("HelixMind Bio AI voice mode is ready. Say Helix, then your command.")
        while True:
            command = self.listen()
            if not command or WAKE_WORD not in command:
                continue
            response, keep_running = self.answer(command)
            self.speak(response)
            if not keep_running:
                break


if __name__ == "__main__":
    assistant = HelixMindBioAI()
    mode = input("Type mode or voice mode? [text/voice]: ").strip().lower()
    if mode.startswith("v"):
        assistant.run_voice_mode()
    else:
        assistant.run_text_mode()
