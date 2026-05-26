#!/usr/bin/env python3
"""Fail the workflow when a generated chatbot misses the premium standard."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

REQUIRED_FILES = [
    "README.md",
    "package.json",
    "vercel.json",
    "api/chat.js",
    "public/index.html",
    "public/style.css",
    "public/script.js",
    "public/cover.svg",
    "screenshots/preview.svg",
    "project.json",
]

CONTENT_CHECKS = {
    "README.md": ["premium", "Vercel", "OpenAI", "Live Demo", "screenshot"],
    "package.json": ["openai", "start"],
    "api/chat.js": ["process.env.OPENAI_API_KEY", "responses.create", "visitorKey"],
    "public/index.html": ["<section class=\"hero\"", "<img", "data-variant", "tool-panel"],
    "public/style.css": [".hero", "@media", "box-shadow"],
    "public/script.js": ["sessionStorage", "demoReply", "fetch", "quickActions"],
}


def generated_path_from_log(log_file: Path) -> str:
    if not log_file.exists():
        raise SystemExit(f"Missing generation log: {log_file}")

    created = ""
    for line in log_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("Created "):
            created = line.removeprefix("Created ").strip()

    if not created:
        raise SystemExit("Could not find a generated chatbot path in the workflow log.")
    if not created.startswith("ai-chatbots/"):
        raise SystemExit(f"Generated path is outside ai-chatbots/: {created}")
    return created


def require_contains(project: Path, relative_path: str, needles: list[str]) -> None:
    text = (project / relative_path).read_text(encoding="utf-8")
    lower_text = text.lower()
    missing = [needle for needle in needles if needle.lower() not in lower_text]
    if missing:
        raise SystemExit(f"{relative_path} is missing premium markers: {', '.join(missing)}")


def require_package_quality(project: Path) -> None:
    package = json.loads((project / "package.json").read_text(encoding="utf-8"))
    dependencies = package.get("dependencies", {})
    scripts = package.get("scripts", {})
    if "openai" not in dependencies:
        raise SystemExit("package.json must depend on the official OpenAI SDK.")
    if "start" not in scripts:
        raise SystemExit("package.json must include a start script.")


def require_unique_metadata(project: Path) -> dict:
    metadata = json.loads((project / "project.json").read_text(encoding="utf-8"))
    required = ["layout", "feature", "palette", "live_demo", "code_signature"]
    missing = [key for key in required if not metadata.get(key)]
    if missing:
        raise SystemExit("project.json is missing unique metadata: " + ", ".join(missing))
    if "github.io" not in str(metadata["live_demo"]):
        raise SystemExit("project.json must include a GitHub Pages live demo URL.")
    return metadata


def require_static_demo(project_folder_name: str) -> None:
    demo = DOCS / project_folder_name
    required = ["index.html", "style.css", "script.js", "cover.svg"]
    missing = [path for path in required if not (demo / path).is_file()]
    if missing:
        raise SystemExit("Static live demo copy is missing files: " + ", ".join(missing))


def main() -> None:
    log_file = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "generated-chatbot.txt")
    relative_project = generated_path_from_log(log_file)
    project = ROOT / relative_project

    if not project.is_dir():
        raise SystemExit(f"Generated project folder does not exist: {relative_project}")

    missing_files = [path for path in REQUIRED_FILES if not (project / path).is_file()]
    if missing_files:
        raise SystemExit("Generated chatbot is missing required files: " + ", ".join(missing_files))

    require_package_quality(project)
    metadata = require_unique_metadata(project)
    require_static_demo(project.name)
    for relative_path, needles in CONTENT_CHECKS.items():
        require_contains(project, relative_path, needles)

    print(f"Premium validation passed: {relative_project} ({metadata['layout']} / {metadata['palette']})")


if __name__ == "__main__":
    main()
