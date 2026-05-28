"""HelixMind Bio AI - local voice/text assistant for bioinformatics work."""

from __future__ import annotations

import datetime as dt
import os
import re
import subprocess
import time
import webbrowser
from pathlib import Path

import pyttsx3
import speech_recognition as sr

import bioinformatics_tools as bio

WAKE_WORD = "helix"
APP_NAME = "HelixMind Bio AI"
LOG_FILE = Path("helixmind_session_log.txt")


class HelixMindBioAI:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 172)
        self.recognizer = sr.Recognizer()
        self.session_notes: list[str] = []
        self.job_queue: list[str] = []
        self.completed_jobs: list[str] = []
        self.active_project = "bioinformatics workspace"
        self.presence_enabled = True

    def speak(self, text: str) -> None:
        print(f"\n{APP_NAME}: {text}\n")
        self.write_log(f"HELIXMIND: {text}")
        try:
            self.engine.say(text.replace("\n", ". "))
            self.engine.runAndWait()
        except Exception:
            print("Voice output is unavailable, but text mode is still working.")

    def write_log(self, text: str) -> None:
        timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with LOG_FILE.open("a", encoding="utf-8") as file:
                file.write(f"[{timestamp}] {text}\n")
        except OSError:
            pass

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=12)
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            self.write_log(f"USER: {text}")
            return text.lower().strip()
        except Exception:
            return ""

    def normalize(self, command: str) -> str:
        command = command.lower().strip()
        self.write_log(f"USER: {command}")
        if command.startswith(WAKE_WORD):
            command = command.replace(WAKE_WORD, "", 1).strip(" ,")
        return command

    def answer(self, command: str) -> tuple[str, bool]:
        command = self.normalize(command)

        if command in {"exit", "quit", "stop", "sleep"}:
            return "I am closing the session. Your local log is saved in helixmind_session_log.txt.", False
        if command in {"help", "commands", "what can you do"}:
            return self.help_text(), True
        if command in {"status", "what are you doing", "are you there"}:
            return self.status_report(), True
        if command in {"presence on", "stay awake"}:
            self.presence_enabled = True
            return "Presence mode is on. I will stay in the console and wait for your bioinformatics jobs.", True
        if command in {"presence off", "quiet mode"}:
            self.presence_enabled = False
            return "Quiet mode is on. I will only respond when you type or speak.", True
        if command.startswith("project "):
            self.active_project = command.replace("project ", "", 1).strip() or self.active_project
            return f"Active project set to {self.active_project}.", True
        if "time" in command:
            return f"The time is {dt.datetime.now().strftime('%I:%M %p')}.", True

        site_response = self.open_science_site(command)
        if site_response:
            return site_response, True

        if command.startswith("note "):
            note = command.replace("note ", "", 1).strip()
            self.session_notes.append(note)
            return f"Added session note {len(self.session_notes)}. I will keep it in this session and log it locally.", True
        if command in {"show notes", "list notes"}:
            if not self.session_notes:
                return "No session notes yet. Tell me: helix note your observation."
            return "Session notes:\n" + "\n".join(f"{i + 1}. {note}" for i, note in enumerate(self.session_notes)), True
        if command.startswith("add job "):
            job = command.replace("add job ", "", 1).strip()
            if not job:
                return "Give me a job after add job. Example: add job gc content of ATGCGT."
            self.job_queue.append(job)
            return f"Job added. Queue length is now {len(self.job_queue)}. Say run jobs when you want me to process them.", True
        if command in {"show jobs", "list jobs"}:
            return self.show_jobs(), True
        if command in {"run jobs", "process jobs", "start work"}:
            return self.run_jobs(), True
        if command in {"clear jobs", "empty jobs"}:
            self.job_queue.clear()
            return "Job queue cleared.", True
        if command.startswith("open folder "):
            return self.open_folder(command.replace("open folder ", "", 1)), True

        response = self.run_bio_command(command)
        if response:
            self.completed_jobs.append(command)
            return self.with_personality(response), True

        return self.help_text(), True

    def with_personality(self, response: str) -> str:
        if not self.presence_enabled:
            return response
        prefix = "I finished that analysis."
        if "No " in response or "Could not" in response or "Use:" in response:
            prefix = "I checked it and need a cleaner input."
        return f"{prefix}\n{response}"

    def run_bio_command(self, command: str) -> str | None:
        if "explain bioinformatics" in command:
            return "Bioinformatics uses computing to study DNA, RNA, proteins, variants, genomes, and biological datasets."
        if command.startswith("report "):
            return bio.sequence_report(command.replace("report ", "", 1))
        if command.startswith("gc content of "):
            return bio.gc_content(command.replace("gc content of ", "", 1))
        if command.startswith("reverse complement of "):
            return bio.reverse_complement(command.replace("reverse complement of ", "", 1))
        if command.startswith("transcribe "):
            return bio.transcribe(command.replace("transcribe ", "", 1))
        if command.startswith("translate dna "):
            return bio.translate_dna(command.replace("translate dna ", "", 1))
        if command.startswith("longest orf of "):
            return bio.longest_orf(command.replace("longest orf of ", "", 1))
        if command.startswith("protein weight of "):
            return bio.protein_weight(command.replace("protein weight of ", "", 1))
        if command.startswith("primer stats "):
            return bio.primer_stats(command.replace("primer stats ", "", 1))
        if command.startswith("restriction scan "):
            return bio.restriction_scan(command.replace("restriction scan ", "", 1))
        if command.startswith("codon usage "):
            return bio.codon_usage(command.replace("codon usage ", "", 1))
        if command.startswith("kmer count "):
            return self.handle_kmers(command)
        if command.startswith("find motif "):
            return self.handle_motif(command)
        if command.startswith("compare "):
            return self.handle_compare(command)
        if command.startswith("summarize fasta "):
            try:
                return bio.summarize_fasta(command.replace("summarize fasta ", "", 1))
            except Exception as exc:
                return f"Could not read FASTA file: {exc}"
        if command.startswith("save fasta "):
            return self.handle_save_fasta(command)
        if command.startswith("align "):
            return self.handle_alignment(command)
        return None

    def run_jobs(self) -> str:
        if not self.job_queue:
            return "No queued jobs. Add one with: helix add job gc content of ATGCGT."
        reports = []
        while self.job_queue:
            job = self.job_queue.pop(0)
            response = self.run_bio_command(job) or f"I could not run this job: {job}"
            self.completed_jobs.append(job)
            reports.append(f"Job: {job}\nResult:\n{response}")
        return "I processed the queued bioinformatics jobs.\n\n" + "\n\n".join(reports)

    def show_jobs(self) -> str:
        if not self.job_queue:
            return "No queued jobs. I am ready for a sequence, FASTA summary, primer check, or PubMed search."
        return "Queued jobs:\n" + "\n".join(f"{i + 1}. {job}" for i, job in enumerate(self.job_queue))

    def status_report(self) -> str:
        return (
            f"I am active inside your local console for {self.active_project}.\n"
            f"Queued jobs: {len(self.job_queue)}\n"
            f"Completed jobs this session: {len(self.completed_jobs)}\n"
            f"Session notes: {len(self.session_notes)}\n"
            f"Presence mode: {'on' if self.presence_enabled else 'off'}\n"
            "I am not watching private files automatically. Give me a folder, FASTA path, or sequence when you want work done."
        )

    def open_science_site(self, command: str) -> str | None:
        sites = {
            "open ncbi": "https://www.ncbi.nlm.nih.gov/",
            "open uniprot": "https://www.uniprot.org/",
            "open blast": "https://blast.ncbi.nlm.nih.gov/",
            "open ensembl": "https://www.ensembl.org/",
            "open pdb": "https://www.rcsb.org/",
            "open pubmed": "https://pubmed.ncbi.nlm.nih.gov/",
        }
        for phrase, url in sites.items():
            if phrase in command:
                webbrowser.open(url)
                return f"Opening {phrase.replace('open ', '').upper()}."
        if command.startswith("search pubmed for "):
            query = command.replace("search pubmed for ", "", 1).strip()
            webbrowser.open("https://pubmed.ncbi.nlm.nih.gov/?term=" + query.replace(" ", "+"))
            return f"Searching PubMed for {query}."
        return None

    def open_folder(self, folder_text: str) -> str:
        path = Path(folder_text.strip().strip('"')).expanduser()
        if not path.exists():
            return f"Folder not found: {path}"
        subprocess.Popen(f'explorer "{path}"')
        return f"Opening folder: {path}"

    def handle_kmers(self, command: str) -> str:
        payload = command.replace("kmer count ", "", 1)
        parts = payload.split(" ", 1)
        if parts and parts[0].isdigit() and len(parts) == 2:
            return bio.kmer_counts(parts[1], int(parts[0]))
        return bio.kmer_counts(payload)

    def handle_motif(self, command: str) -> str:
        payload = command.replace("find motif ", "", 1)
        if " in " not in payload:
            return "Use: find motif ATG in ATGCGTATG"
        motif, sequence = payload.split(" in ", 1)
        return bio.find_motif(sequence, motif)

    def handle_compare(self, command: str) -> str:
        payload = command.replace("compare ", "", 1)
        if " with " not in payload:
            return "Use: compare ATGCC with ATGCA"
        seq_a, seq_b = payload.split(" with ", 1)
        return bio.compare_sequences(seq_a, seq_b)

    def handle_alignment(self, command: str) -> str:
        payload = command.replace("align ", "", 1)
        if " with " not in payload:
            return "Use: align ATGCC with ATGCA"
        seq_a, seq_b = payload.split(" with ", 1)
        return bio.global_align(seq_a, seq_b)

    def handle_save_fasta(self, command: str) -> str:
        match = re.match(r"save fasta (.+?) named (.+?) to (.+)", command)
        if not match:
            return "Use: save fasta ATGCGT named sample1 to C:\\path\\sample.fasta"
        sequence, name, path = match.groups()
        try:
            return bio.write_fasta(path, name, sequence)
        except Exception as exc:
            return f"Could not save FASTA file: {exc}"

    def help_text(self) -> str:
        return (
            "I am your local bioinformatics workspace assistant. Try:\n"
            "helix status\n"
            "helix project CRISPR off-target study\n"
            "helix add job gc content of ATGCGCGTTA\n"
            "helix add job primer stats ATGCGTACGTAGCTAGCTA\n"
            "helix run jobs\n"
            "helix report ATGCGCGTTA\n"
            "helix restriction scan GAATTCGGATCC\n"
            "helix summarize fasta C:\\path\\to\\file.fasta\n"
            "helix search pubmed for crispr diagnostics"
        )

    def heartbeat(self) -> None:
        if self.presence_enabled:
            print(f"{APP_NAME}: standing by for {self.active_project}. Type 'helix help' or add a job.")

    def run_text_mode(self) -> None:
        self.speak(
            "I am awake inside this computer as your local bioinformatics assistant. "
            "Give me sequences, FASTA files, primers, motifs, or research searches. Type helix help for commands."
        )
        last_heartbeat = time.time()
        while True:
            try:
                if self.presence_enabled and time.time() - last_heartbeat > 180:
                    self.heartbeat()
                    last_heartbeat = time.time()
                command = input("You: ")
            except KeyboardInterrupt:
                self.speak("Session interrupted. I am closing safely.")
                break
            response, keep_running = self.answer(command)
            self.speak(response)
            if not keep_running:
                break

    def run_voice_mode(self) -> None:
        self.speak(
            "Voice presence mode is ready. Say Helix, then your command. "
            "I will stay local and wait for bioinformatics work."
        )
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
    preferred_mode = os.getenv("HELIXMIND_MODE", "").strip().lower()
    mode = preferred_mode or input("Type mode or voice mode? [text/voice]: ").strip().lower()
    if mode.startswith("v"):
        assistant.run_voice_mode()
    else:
        assistant.run_text_mode()
