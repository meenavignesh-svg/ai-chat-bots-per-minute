#!/usr/bin/env python3
"""Keep the root catalog stable after generation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

if README.exists():
    text = README.read_text(encoding="utf-8").rstrip() + "\n"
    README.write_text(text, encoding="utf-8")
