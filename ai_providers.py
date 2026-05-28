"""Optional AI provider connector for JANET.

Keys are held in memory by the running app unless the user explicitly adds
environment variables outside the program. JANET stays local-first: if no
provider is configured, it falls back to local planning and command tools.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass
class AIConfig:
    provider: str = "local"
    model: str = ""
    api_key: str = ""
    endpoint: str = ""


class AIProviderManager:
    def __init__(self) -> None:
        self.config = AIConfig(
            provider=os.getenv("JANET_AI_PROVIDER", "local"),
            model=os.getenv("JANET_AI_MODEL", ""),
            api_key=os.getenv("JANET_AI_KEY", ""),
            endpoint=os.getenv("JANET_AI_ENDPOINT", ""),
        )

    def configure(self, provider: str, model: str = "", api_key: str = "", endpoint: str = "") -> None:
        self.config = AIConfig(provider=provider.strip().lower() or "local", model=model.strip(), api_key=api_key.strip(), endpoint=endpoint.strip())

    def status(self) -> str:
        key_state = "session key set" if self.config.api_key else "no key"
        return f"AI provider: {self.config.provider or 'local'} | model: {self.config.model or 'default'} | {key_state}"

    def ask(self, prompt: str, system: str = "You are JANET, a concise local desktop work assistant.") -> str:
        provider = self.config.provider.lower()
        if provider in {"", "local", "none"}:
            return self.local_fallback(prompt)
        if provider == "ollama":
            return self.ask_ollama(prompt, system)
        if provider == "gemini":
            return self.ask_gemini(prompt, system)
        if provider == "anthropic":
            return self.ask_anthropic(prompt, system)
        if provider in {"openai", "openrouter", "compatible", "custom"}:
            return self.ask_openai_compatible(prompt, system)
        return "Unknown provider. Use local, ollama, openai, gemini, anthropic, openrouter, or compatible."

    def local_fallback(self, prompt: str) -> str:
        goal = prompt.strip()
        if not goal:
            return "Give me a goal to plan."
        return (
            "Local plan:\n"
            f"1. Understand the goal: {goal}\n"
            "2. Identify the app, file, browser page, sequence, or dataset needed.\n"
            "3. Use JANET commands for app control, typing, files, or bioinformatics.\n"
            "4. Run one visible step at a time.\n"
            "5. Stop before secrets, deletion, payment data, or destructive actions."
        )

    def post_json(self, url: str, payload: dict, headers: dict | None = None, timeout: int = 60) -> dict:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json", **(headers or {})}, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")[:800]
            return {"error": f"HTTP {exc.code}: {details}"}
        except Exception as exc:
            return {"error": str(exc)}

    def ask_ollama(self, prompt: str, system: str) -> str:
        endpoint = self.config.endpoint or "http://localhost:11434/api/chat"
        model = self.config.model or "llama3.1"
        data = self.post_json(endpoint, {"model": model, "stream": False, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]})
        if "error" in data:
            return "Ollama error: " + data["error"]
        return data.get("message", {}).get("content", "No Ollama response.")

    def ask_openai_compatible(self, prompt: str, system: str) -> str:
        if not self.config.api_key:
            return "No API key set for this provider. Paste it in JANET's AI settings for this session."
        endpoint = self.config.endpoint
        if not endpoint:
            endpoint = "https://openrouter.ai/api/v1/chat/completions" if self.config.provider == "openrouter" else "https://api.openai.com/v1/chat/completions"
        model = self.config.model or ("openai/gpt-4o-mini" if self.config.provider == "openrouter" else "gpt-4o-mini")
        data = self.post_json(
            endpoint,
            {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}], "temperature": 0.3},
            {"Authorization": f"Bearer {self.config.api_key}"},
        )
        if "error" in data:
            return "AI provider error: " + data["error"]
        return data.get("choices", [{}])[0].get("message", {}).get("content", "No AI response.")

    def ask_gemini(self, prompt: str, system: str) -> str:
        if not self.config.api_key:
            return "No Gemini API key set. Paste it in JANET's AI settings for this session."
        model = self.config.model or "gemini-1.5-flash"
        endpoint = self.config.endpoint or f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.config.api_key}"
        data = self.post_json(endpoint, {"contents": [{"parts": [{"text": system + "\n\n" + prompt}]}]})
        if "error" in data:
            return "Gemini error: " + data["error"]
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "No Gemini response."

    def ask_anthropic(self, prompt: str, system: str) -> str:
        if not self.config.api_key:
            return "No Anthropic API key set. Paste it in JANET's AI settings for this session."
        endpoint = self.config.endpoint or "https://api.anthropic.com/v1/messages"
        model = self.config.model or "claude-3-5-haiku-latest"
        data = self.post_json(
            endpoint,
            {"model": model, "max_tokens": 900, "system": system, "messages": [{"role": "user", "content": prompt}]},
            {"x-api-key": self.config.api_key, "anthropic-version": "2023-06-01"},
        )
        if "error" in data:
            return "Anthropic error: " + data["error"]
        try:
            return data["content"][0]["text"]
        except Exception:
            return "No Anthropic response."
