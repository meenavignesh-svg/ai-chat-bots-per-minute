"""HelixMind Bio AI - local voice/text assistant for bioinformatics and desktop work."""

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

try:
    import pyautogui
    import pyperclip
except Exception:
    pyautogui = None
    pyperclip = None

import bioinformatics_tools as bio

WAKE_WORD = "helix"
APP_NAME = "HelixMind Bio AI"
LOG_FILE = Path("helixmind_session_log.txt")
WORKSPACE = Path("HelixMind_Workspace")
SENSITIVE_WORDS = ("password", "passcode", "otp", "api key", "secret", "token", "private key", "credit card", "card number", "cvv")
BLOCKED_KEYS = {"delete", "backspace"}
BLOCKED_HOTKEYS = {"alt+f4", "ctrl+w", "ctrl+q", "shift+delete"}


class HelixMindBioAI:
    def __init__(self) -> None:
        self.fast_mode = os.getenv("HELIXMIND_FAST", "1").strip().lower() not in {"0", "false", "off", "no"}
        self.voice_output_enabled = os.getenv("HELIXMIND_VOICE_OUTPUT", "0").strip().lower() in {"1", "true", "on", "yes"}
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 220 if self.fast_mode else 172)
        self.recognizer = sr.Recognizer()
        self.session_notes: list[str] = []
        self.job_queue: list[str] = []
        self.completed_jobs: list[str] = []
        self.active_project = "bioinformatics workspace"
        self.presence_enabled = True
        if pyautogui is not None:
            pyautogui.PAUSE = 0.02 if self.fast_mode else 0.10
        WORKSPACE.mkdir(exist_ok=True)

    def action_delay(self) -> float:
        return 0.08 if self.fast_mode else 0.40

    def speak(self, text: str) -> None:
        print(f"\n{APP_NAME}: {text}\n")
        self.write_log(f"HELIXMIND: {text}")
        if self.fast_mode and not self.voice_output_enabled:
            return
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
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2 if self.fast_mode else 0.5)
            audio = self.recognizer.listen(source, timeout=4 if self.fast_mode else 6, phrase_time_limit=8 if self.fast_mode else 12)
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
            return "Closing. Local log saved in helixmind_session_log.txt.", False
        if command in {"help", "commands", "what can you do"}:
            return self.help_text(), True
        if command in {"status", "what are you doing", "are you there"}:
            return self.status_report(), True
        if command in {"fast mode", "work fast", "speed up"}:
            self.fast_mode = True
            self.voice_output_enabled = False
            if pyautogui is not None:
                pyautogui.PAUSE = 0.02
            self.engine.setProperty("rate", 220)
            return "Fast mode on. Voice output is off and desktop delays are reduced.", True
        if command in {"normal mode", "slow mode"}:
            self.fast_mode = False
            if pyautogui is not None:
                pyautogui.PAUSE = 0.10
            self.engine.setProperty("rate", 172)
            return "Normal mode on.", True
        if command in {"voice output on", "talk out loud"}:
            self.voice_output_enabled = True
            return "Voice output on.", True
        if command in {"voice output off", "silent mode"}:
            self.voice_output_enabled = False
            return "Voice output off. I will respond in text only.", True
        if command in {"presence on", "stay awake"}:
            self.presence_enabled = True
            return "Presence mode on.", True
        if command in {"presence off", "quiet mode"}:
            self.presence_enabled = False
            return "Quiet mode on.", True
        if command.startswith("project "):
            self.active_project = command.replace("project ", "", 1).strip() or self.active_project
            return f"Active project set to {self.active_project}.", True
        if "time" in command:
            return f"The time is {dt.datetime.now().strftime('%I:%M %p')}.", True

        site_response = self.open_science_site(command) or self.open_general_site(command)
        if site_response:
            return site_response, True

        response = self.run_desktop_command(command) or self.run_work_command(command) or self.run_bio_command(command)
        if response:
            self.completed_jobs.append(command)
            return self.with_personality(response), True

        return self.help_text(), True

    def with_personality(self, response: str) -> str:
        if self.fast_mode:
            return response
        if not self.presence_enabled:
            return response
        prefix = "I finished that."
        if "No " in response or "Could not" in response or "Use:" in response or "blocked" in response.lower():
            prefix = "I checked it and need a cleaner or safer input."
        return f"{prefix}\n{response}"

    def desktop_ready(self) -> bool:
        return pyautogui is not None and pyperclip is not None

    def unsafe_text(self, text: str) -> bool:
        lowered = text.lower()
        return any(word in lowered for word in SENSITIVE_WORDS)

    def run_desktop_command(self, command: str) -> str | None:
        if command == "desktop status":
            return "Desktop ready." if self.desktop_ready() else "Desktop dependencies missing. Run install_helixmind_bio_ai.bat again."
        if command.startswith("open any app "):
            return self.open_any_app(command.replace("open any app ", "", 1))
        if command.startswith("type text "):
            return self.type_text(command.replace("type text ", "", 1))
        if command.startswith("paste text "):
            return self.paste_text(command.replace("paste text ", "", 1))
        if command.startswith("press key "):
            return self.press_key(command.replace("press key ", "", 1))
        if command.startswith("hotkey "):
            return self.hotkey(command.replace("hotkey ", "", 1))
        if command.startswith("wait "):
            return self.wait_seconds(command.replace("wait ", "", 1))
        if command.startswith("click"):
            return self.click_mouse(command)
        return None

    def open_any_app(self, app_name: str) -> str:
        if not self.desktop_ready():
            return "Desktop dependencies missing. Run install_helixmind_bio_ai.bat again."
        app_name = app_name.strip()
        if not app_name:
            return "Use: open any app chrome"
        pyautogui.hotkey("win")
        time.sleep(self.action_delay())
        pyperclip.copy(app_name)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(self.action_delay())
        pyautogui.press("enter")
        return f"Opening: {app_name}."

    def type_text(self, text: str) -> str:
        if not self.desktop_ready():
            return "Desktop dependencies missing. Run install_helixmind_bio_ai.bat again."
        if self.unsafe_text(text):
            return "Blocked: I will not type passwords, secrets, tokens, OTPs, API keys, or credit card data."
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        return "Typed."

    def paste_text(self, text: str) -> str:
        return self.type_text(text)

    def press_key(self, key: str) -> str:
        if not self.desktop_ready():
            return "Desktop dependencies missing. Run install_helixmind_bio_ai.bat again."
        key = key.strip().lower()
        if key in BLOCKED_KEYS:
            return f"Blocked: {key} is not allowed as a direct command."
        pyautogui.press(key)
        return f"Pressed {key}."

    def hotkey(self, keys_text: str) -> str:
        if not self.desktop_ready():
            return "Desktop dependencies missing. Run install_helixmind_bio_ai.bat again."
        cleaned = keys_text.strip().lower().replace(" ", "")
        if cleaned in BLOCKED_HOTKEYS:
            return f"Blocked: {cleaned} is not allowed."
        keys = [key for key in re.split(r"\+|,", cleaned) if key]
        if not keys or len(keys) > 4:
            return "Use: hotkey ctrl+s"
        pyautogui.hotkey(*keys)
        return f"Hotkey {'+'.join(keys)}."

    def wait_seconds(self, text: str) -> str:
        match = re.search(r"\d+(?:\.\d+)?", text)
        seconds = float(match.group()) if match else 0.2
        seconds = max(0.05, min(seconds, 30.0))
        time.sleep(seconds)
        return f"Waited {seconds:g}s."

    def click_mouse(self, command: str) -> str:
        if not self.desktop_ready():
            return "Desktop dependencies missing. Run install_helixmind_bio_ai.bat again."
        match = re.search(r"click\s+(\d+)\s+(\d+)", command)
        if match:
            x, y = int(match.group(1)), int(match.group(2))
            pyautogui.click(x, y)
            return f"Clicked {x},{y}."
        pyautogui.click()
        return "Clicked."

    def run_work_command(self, command: str) -> str | None:
        if command.startswith("note "):
            note = command.replace("note ", "", 1).strip()
            self.session_notes.append(note)
            return f"Note {len(self.session_notes)} added."
        if command in {"show notes", "list notes"}:
            if not self.session_notes:
                return "No notes."
            return "Notes:\n" + "\n".join(f"{i + 1}. {note}" for i, note in enumerate(self.session_notes))
        if command.startswith("add job "):
            job = command.replace("add job ", "", 1).strip()
            if not job:
                return "Give me a job after add job."
            self.job_queue.append(job)
            return f"Job added. Queue: {len(self.job_queue)}."
        if command in {"show jobs", "list jobs"}:
            return self.show_jobs()
        if command in {"run jobs", "process jobs", "start work"}:
            return self.run_jobs()
        if command in {"clear jobs", "empty jobs"}:
            self.job_queue.clear()
            return "Jobs cleared."
        if command.startswith("open folder "):
            return self.open_folder(command.replace("open folder ", "", 1))
        if command.startswith("create folder "):
            return self.create_folder(command.replace("create folder ", "", 1))
        if command.startswith("write file "):
            return self.write_text_file(command)
        if command.startswith("read file "):
            return self.read_text_file(command.replace("read file ", "", 1))
        if command.startswith("list files"):
            folder = command.replace("list files", "", 1).strip() or str(WORKSPACE)
            return self.list_files(folder)
        if command.startswith("make checklist "):
            return self.make_checklist(command.replace("make checklist ", "", 1))
        if command.startswith("summarize text "):
            return self.summarize_text(command.replace("summarize text ", "", 1))
        if command.startswith("draft email "):
            return self.draft_email(command.replace("draft email ", "", 1))
        if command.startswith("open app "):
            return self.open_app(command.replace("open app ", "", 1))
        if command.startswith("search web for "):
            query = command.replace("search web for ", "", 1).strip()
            webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))
            return f"Searching: {query}."
        return None

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
            return "No queued jobs."
        reports = []
        start = time.perf_counter()
        while self.job_queue:
            job = self.job_queue.pop(0)
            response = self.run_desktop_command(job) or self.run_work_command(job) or self.run_bio_command(job) or f"Could not run: {job}"
            self.completed_jobs.append(job)
            reports.append(f"{job}: {response}" if self.fast_mode else f"Job: {job}\nResult:\n{response}")
        elapsed = time.perf_counter() - start
        if self.fast_mode:
            return f"Processed {len(reports)} job(s) in {elapsed:.2f}s.\n" + "\n".join(reports)
        return "I processed the queued jobs.\n\n" + "\n\n".join(reports)

    def show_jobs(self) -> str:
        if not self.job_queue:
            return "No queued jobs."
        return "Queued jobs:\n" + "\n".join(f"{i + 1}. {job}" for i, job in enumerate(self.job_queue))

    def status_report(self) -> str:
        desktop = "ready" if self.desktop_ready() else "missing dependencies"
        return (
            f"Active project: {self.active_project}\n"
            f"Workspace: {WORKSPACE.resolve()}\n"
            f"Desktop control: {desktop}\n"
            f"Fast mode: {'on' if self.fast_mode else 'off'}\n"
            f"Voice output: {'on' if self.voice_output_enabled else 'off'}\n"
            f"Queued jobs: {len(self.job_queue)}\n"
            f"Completed jobs: {len(self.completed_jobs)}\n"
            f"Notes: {len(self.session_notes)}"
        )

    def safe_workspace_path(self, path_text: str) -> Path:
        cleaned = path_text.strip().strip('"')
        path = Path(cleaned)
        if not path.is_absolute():
            path = WORKSPACE / cleaned
        resolved_workspace = WORKSPACE.resolve()
        resolved_path = path.resolve()
        if resolved_workspace not in resolved_path.parents and resolved_path != resolved_workspace:
            raise ValueError("For safety, file writing is limited to the HelixMind_Workspace folder.")
        return resolved_path

    def create_folder(self, folder_text: str) -> str:
        try:
            path = self.safe_workspace_path(folder_text)
            path.mkdir(parents=True, exist_ok=True)
            return f"Created: {path}"
        except Exception as exc:
            return f"Could not create folder: {exc}"

    def write_text_file(self, command: str) -> str:
        match = re.match(r"write file (.+?) with (.+)", command, flags=re.DOTALL)
        if not match:
            return "Use: write file notes.txt with your text here"
        filename, content = match.groups()
        try:
            path = self.safe_workspace_path(filename)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content + "\n", encoding="utf-8")
            return f"Wrote: {path}"
        except Exception as exc:
            return f"Could not write file: {exc}"

    def read_text_file(self, path_text: str) -> str:
        try:
            path = Path(path_text.strip().strip('"')).expanduser()
            if not path.exists():
                path = self.safe_workspace_path(path_text)
            text = path.read_text(encoding="utf-8")[:3000]
            return f"{path}:\n{text}"
        except Exception as exc:
            return f"Could not read file: {exc}"

    def list_files(self, folder_text: str) -> str:
        try:
            path = Path(folder_text.strip().strip('"')).expanduser()
            if not path.exists():
                path = self.safe_workspace_path(folder_text)
            if not path.exists() or not path.is_dir():
                return f"Folder not found: {path}"
            entries = sorted(path.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))[:50]
            if not entries:
                return f"No files in {path}."
            return "Files:\n" + "\n".join(("[folder] " if item.is_dir() else "[file] ") + item.name for item in entries)
        except Exception as exc:
            return f"Could not list files: {exc}"

    def make_checklist(self, text: str) -> str:
        items = [item.strip(" .") for item in re.split(r",|;| and ", text) if item.strip(" .")]
        if not items:
            return "Give checklist items."
        return "Checklist:\n" + "\n".join(f"[ ] {item}" for item in items)

    def summarize_text(self, text: str) -> str:
        sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
        if not sentences:
            return "Give text to summarize."
        return "Short summary:\n" + " ".join(sentences[:3])

    def draft_email(self, text: str) -> str:
        return "Email draft:\nSubject: Quick update\n\nHi,\n\n" + text.strip() + "\n\nBest,\n"

    def open_app(self, app_name: str) -> str:
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "explorer": "explorer.exe",
            "chrome": "chrome.exe",
            "vscode": "code.cmd",
            "vs code": "code.cmd",
        }
        key = app_name.strip().lower()
        if key not in apps:
            return "For any installed app, use: open any app app-name"
        try:
            subprocess.Popen(apps[key], shell=False)
            return f"Opening {key}."
        except Exception as exc:
            return f"Could not open {key}: {exc}"

    def open_general_site(self, command: str) -> str | None:
        sites = {
            "open google": "https://www.google.com/",
            "open youtube": "https://www.youtube.com/",
            "open github": "https://github.com/",
            "open chatgpt": "https://chatgpt.com/",
        }
        for phrase, url in sites.items():
            if phrase in command:
                webbrowser.open(url)
                return f"Opening {phrase.replace('open ', '')}."
        return None

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
            return f"Searching PubMed: {query}."
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
            "Fast commands:\n"
            "helix fast mode\n"
            "helix voice output off\n"
            "helix desktop status\n"
            "helix open any app chrome\n"
            "helix type text Hello, I am HelixMind.\n"
            "helix hotkey ctrl+s\n"
            "helix wait 0.2\n"
            "helix add job open any app notepad\n"
            "helix add job wait 0.5\n"
            "helix add job type text Sequence report ready.\n"
            "helix run jobs\n"
            "helix gc content of ATGCGCGTTA"
        )

    def heartbeat(self) -> None:
        if self.presence_enabled and not self.fast_mode:
            print(f"{APP_NAME}: standing by for {self.active_project}. Type 'helix help' or add a job.")

    def run_text_mode(self) -> None:
        self.speak("Ready. Fast mode is on by default. Type helix help for commands.")
        last_heartbeat = time.time()
        while True:
            try:
                if self.presence_enabled and time.time() - last_heartbeat > 180:
                    self.heartbeat()
                    last_heartbeat = time.time()
                command = input("You: ")
            except KeyboardInterrupt:
                self.speak("Closing safely.")
                break
            response, keep_running = self.answer(command)
            self.speak(response)
            if not keep_running:
                break

    def run_voice_mode(self) -> None:
        self.voice_output_enabled = True
        self.speak("Voice mode ready. Say Helix, then your command.")
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
