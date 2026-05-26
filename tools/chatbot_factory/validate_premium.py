#!/usr/bin/env python3
"""Fail when a generated product does not meet the premium standard."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

REQUIRED_FILES = [
    "README.md",
    "PRODUCT_SPEC.md",
    "sample-data.json",
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

CHECKS = {
    "README.md": ["premium", "$1000", "deployment", "OpenAI"],
    "PRODUCT_SPEC.md": ["ICP", "Workflow", "Differentiation", "Pricing"],
    "api/chat.js": ["OpenAI", "responses.create", "OPENAI_API_KEY"],
    "public/index.html": ["data-product", "hero", "workspace", "insights"],
    "public/style.css": ["box-shadow", "@media", "grid"],
    "public/script.js": ["sampleData", "sessionStorage", "fetch", "score"],
}


def generated_path(log_file: Path) -> str:
    text = log_file.read_text(encoding="utf-8")
    for line in reversed(text.splitlines()):
        if line.startswith("Created "):
            value = line.removeprefix("Created ").strip()
            if value.startswith("ai-chatbots/"):
                return value
    raise SystemExit("No generated product path found.")


def contains(project: Path, rel: str, words: list[str]) -> None:
    text = (project / rel).read_text(encoding="utf-8").lower()
    missing = [word for word in words if word.lower() not in text]
    if missing:
        raise SystemExit(f"{rel} is missing: {', '.join(missing)}")


def main() -> None:
    log = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "generated-product.txt")
    rel = generated_path(log)
    project = ROOT / rel
    missing = [name for name in REQUIRED_FILES if not (project / name).is_file()]
    if missing:
        raise SystemExit("Missing premium files: " + ", ".join(missing))

    package = json.loads((project / "package.json").read_text(encoding="utf-8"))
    if "openai" not in package.get("dependencies", {}):
        raise SystemExit("Official OpenAI SDK dependency required.")

    meta = json.loads((project / "project.json").read_text(encoding="utf-8"))
    for key in ["title", "category", "price_anchor", "live_demo", "quality_score"]:
        if not meta.get(key):
            raise SystemExit(f"project.json missing {key}")
    if int(meta["quality_score"]) < 90:
        raise SystemExit("Quality score must be at least 90.")

    demo = DOCS / project.name
    for name in ["index.html", "style.css", "script.js", "cover.svg"]:
        if not (demo / name).is_file():
            raise SystemExit(f"Missing Pages demo file: {name}")

    for rel_file, words in CHECKS.items():
        contains(project, rel_file, words)

    print(f"Premium validation passed: {rel}")


if __name__ == "__main__":
    main()
