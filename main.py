"""Professor voice assistant entry point."""

from __future__ import annotations

import config
from commands import handle_command
from permissions import first_run_setup
from speech import Speech


def remove_wake_word(text: str) -> str:
    if text.startswith(config.WAKE_WORD):
        return text[len(config.WAKE_WORD) :].strip(" ,")
    return text


def main() -> None:
    permissions = first_run_setup()
    speech = Speech()
    speech.say("Professor is ready. Say Professor, then your command.")

    running = True
    while running:
        try:
            heard = speech.listen()
        except Exception as exc:
            print(f"Microphone error: {exc}")
            continue

        if not heard:
            continue
        if config.WAKE_WORD not in heard and heard not in {"exit", "quit"}:
            continue

        command = remove_wake_word(heard)
        response, running = handle_command(command, permissions)
        speech.say(response)


if __name__ == "__main__":
    main()
