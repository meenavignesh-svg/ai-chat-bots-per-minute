#!/usr/bin/env python3
"""Generate a browser-demo chatbot project with optional Vercel AI mode.

This generator is template-first so GitHub Actions can create new projects with
low token usage. If OLLAMA_URL is provided, it can ask a local Ollama server for
small theme copy; otherwise it uses built-in text.
"""

from __future__ import annotations

import json
import os
import random
import re
import textwrap
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = REPO_ROOT / "ai-chatbots"

THEMES = [
    {
        "slug": "robot-gardener",
        "title": "Robot Gardener",
        "eyebrow": "Greenhouse console",
        "status_busy": "growing",
        "accent": "#86efac",
        "accent2": "#67e8f9",
        "user": "#15803d",
        "system": "You are Robot Gardener, a practical AI assistant for plant care, watering schedules, soil notes, and beginner gardening plans.",
        "placeholder": "Ask about plants, watering, soil, or garden plans...",
        "welcome": "Robot Gardener is ready in browser demo mode. Ask about plants, watering, soil, or garden planning.",
        "topics": [
            ["water", "Demo mode: check soil moisture first, water deeply when dry, and adjust for sunlight and pot size."],
            ["soil", "Demo mode: healthy soil needs drainage, organic matter, and the right texture for the plant."],
            ["plant", "Demo mode: pick one easy plant, learn its light needs, and track changes for a week."],
            ["pest", "Demo mode: isolate the plant, inspect leaves, rinse gently, and avoid harsh treatments at first."]
        ],
    },
    {
        "slug": "startup-coach",
        "title": "Startup Coach",
        "eyebrow": "Founder desk",
        "status_busy": "thinking",
        "accent": "#93c5fd",
        "accent2": "#fbbf24",
        "user": "#2563eb",
        "system": "You are Startup Coach, a practical AI assistant for startup ideas, MVP planning, customer discovery, and launch checklists.",
        "placeholder": "Ask about ideas, MVPs, customers, or launches...",
        "welcome": "Startup Coach is ready in browser demo mode. Ask about ideas, MVPs, customer discovery, or launch plans.",
        "topics": [
            ["idea", "Demo mode: define the customer, the painful problem, and the smallest proof that they care."],
            ["mvp", "Demo mode: build the smallest version that tests one behavior, not every feature in your imagination."],
            ["customer", "Demo mode: ask what they do now, what is annoying, and what they already pay for."],
            ["launch", "Demo mode: choose one audience, one promise, one channel, and one metric for the first week."]
        ],
    },
    {
        "slug": "biotech-notes",
        "title": "Biotech Notes",
        "eyebrow": "Research bench",
        "status_busy": "analyzing",
        "accent": "#5eead4",
        "accent2": "#f9a8d4",
        "user": "#0f766e",
        "system": "You are Biotech Notes, a careful AI assistant for biotech study notes, experiment summaries, glossary help, and safe high-level research planning.",
        "placeholder": "Ask about biotech notes, terms, or study plans...",
        "welcome": "Biotech Notes is ready in browser demo mode. Ask about biotech notes, glossary terms, or study planning.",
        "topics": [
            ["glossary", "Demo mode: define the term, add one plain-language analogy, and note where it appears in a workflow."],
            ["experiment", "Demo mode: summarize the question, variables, control, expected result, and safety boundary."],
            ["study", "Demo mode: review one concept, draw one pathway, then test recall with three short questions."],
            ["protocol", "Demo mode: keep protocol discussion high level and check official lab guidance for real procedures."]
        ],
    },
    {
        "slug": "game-master",
        "title": "Game Master",
        "eyebrow": "Quest table",
        "status_busy": "rolling",
        "accent": "#facc15",
        "accent2": "#a78bfa",
        "user": "#a16207",
        "system": "You are Game Master, a playful AI assistant for tabletop quest hooks, NPCs, puzzles, and encounter ideas.",
        "placeholder": "Ask for quests, NPCs, puzzles, or encounters...",
        "welcome": "Game Master is ready in browser demo mode. Ask for quests, NPCs, puzzles, or encounter ideas.",
        "topics": [
            ["quest", "Demo mode: a missing map points to a locked observatory where the stars have been rearranged overnight."],
            ["npc", "Demo mode: create one desire, one secret, one habit, and one thing the NPC refuses to say first."],
            ["puzzle", "Demo mode: make the answer visible in the room, but require players to connect two clues."],
            ["encounter", "Demo mode: add a goal besides fighting, a terrain twist, and a reason to negotiate."]
        ],
    },
]


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "chatbot"


def ask_ollama(theme: dict) -> dict | None:
    url = os.environ.get("OLLAMA_URL")
    model = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
    if not url:
        return None

    prompt = (
        "Return compact JSON for a chatbot theme with keys welcome and topics. "
        "topics must be an array of four [keyword, reply] pairs. "
        f"Theme: {theme['title']}. Keep replies practical and short."
    )
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    request = urllib.request.Request(
        url.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = json.loads(response.read().decode("utf-8"))["response"]
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError, ValueError):
        return None


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def js_string(value: str) -> str:
    return json.dumps(value)


def build_project(theme: dict) -> Path:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%sz")
    folder = OUTPUT_ROOT / f"{theme['slug']}-chatbot-{now}"
    attempt = 2
    while folder.exists():
        folder = OUTPUT_ROOT / f"{theme['slug']}-chatbot-{now}-{attempt}"
        attempt += 1

    ollama_copy = ask_ollama(theme)
    welcome = (ollama_copy or {}).get("welcome", theme["welcome"])
    topics = (ollama_copy or {}).get("topics", theme["topics"])
    safe_topics = [pair for pair in topics if isinstance(pair, list) and len(pair) == 2][:4] or theme["topics"]

    package_name = slugify(theme["title"]) + "-chatbot"
    title = theme["title"]
    path_hint = folder.relative_to(REPO_ROOT).as_posix()

    write(folder / "README.md", f"""
    # {title} Chatbot

    A themed chatbot project with an instant browser demo and optional real AI mode after Vercel deployment.

    ## Browser Demo

    Open `public/index.html` in a browser to preview the chatbot. No setup or API key is needed for demo mode.

    ## Optional Real AI Mode

    Real AI mode needs a deployed Vercel public URL. After deployment, visitors can enter their own OpenAI API key in the page. The key is stored only in browser `sessionStorage` and is never committed to the repo.

    ## Deploy To Vercel

    1. Import `meenavignesh-svg/ai-chat-bots-per-minute` into Vercel.
    2. Set the root directory to `{path_hint}`.
    3. Deploy.
    4. Share the Vercel URL.
    """)

    write(folder / "package.json", json.dumps({
        "name": package_name,
        "version": "1.0.0",
        "description": f"A browser-demo and Vercel-ready {title} AI chatbot using visitor-provided OpenAI API keys.",
        "type": "module",
        "scripts": {"dev": "vercel dev", "start": "vercel dev"},
        "dependencies": {"@vercel/node": "^3.2.27", "openai": "^5.0.0"},
        "devDependencies": {"vercel": "^34.3.0"},
        "engines": {"node": ">=18"},
    }, indent=2))

    write(folder / "vercel.json", """
    {
      "version": 2,
      "routes": [
        { "src": "/api/chat", "dest": "/api/chat.js" },
        { "src": "/(.*)", "dest": "/public/$1" }
      ]
    }
    """)

    write(folder / "api/chat.js", f"""
    import OpenAI from 'openai';

    export default async function handler(req, res) {{
      if (req.method !== 'POST') {{
        res.setHeader('Allow', 'POST');
        return res.status(405).json({{ error: 'Method not allowed.' }});
      }}

      try {{
        const apiKey = req.headers.authorization?.replace(/^Bearer\\s+/i, '') || req.body?.apiKey;
        if (!apiKey || typeof apiKey !== 'string') {{
          return res.status(400).json({{ error: 'Enter your OpenAI API key before using real AI mode.' }});
        }}

        const messages = Array.isArray(req.body?.messages) ? req.body.messages : [];
        const input = messages
          .filter((message) => message && typeof message.content === 'string')
          .slice(-12)
          .map((message) => ({{
            role: message.role === 'assistant' ? 'assistant' : 'user',
            content: message.content.slice(0, 2000)
          }}));

        if (input.length === 0) {{
          return res.status(400).json({{ error: 'Send at least one message.' }});
        }}

        const client = new OpenAI({{ apiKey }});
        const response = await client.responses.create({{
          model: 'gpt-4.1-mini',
          instructions: {js_string(theme['system'])},
          input
        }});

        return res.status(200).json({{ reply: response.output_text || 'I could not produce a reply. Please try again.' }});
      }} catch (error) {{
        console.error(error);
        return res.status(500).json({{ error: 'The AI request failed. Check the API key and deployment.' }});
      }}
    }}
    """)

    write(folder / "public/index.html", f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{title} Chatbot</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <main class="app">
        <section class="chat-panel" aria-label="{title} Chatbot">
          <header class="chat-header">
            <div>
              <p class="eyebrow">{theme['eyebrow']}</p>
              <h1>{title}</h1>
            </div>
            <span id="status" class="status">demo ready</span>
          </header>

          <form id="keyForm" class="key-form">
            <input id="apiKeyInput" type="password" autocomplete="off" placeholder="Optional: enter OpenAI API key for real AI mode" aria-label="OpenAI API key">
            <button type="submit">Use Key</button>
          </form>

          <div id="messages" class="messages" aria-live="polite"></div>

          <form id="chatForm" class="chat-form">
            <input id="userInput" type="text" autocomplete="off" placeholder="{theme['placeholder']}" aria-label="Message">
            <button id="sendButton" type="submit">Send</button>
          </form>
        </section>
      </main>
      <script src="script.js"></script>
    </body>
    </html>
    """)

    write(folder / "public/style.css", f"""
    :root {{
      color-scheme: dark;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #111318;
      color: #f7fbff;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      min-height: 100vh;
      background:
        radial-gradient(circle at 16% 14%, {theme['accent']}3d, transparent 28rem),
        radial-gradient(circle at 82% 22%, {theme['accent2']}29, transparent 25rem),
        linear-gradient(145deg, #111318, #1d2632 58%, #141d1a);
    }}

    .app {{ min-height: 100vh; display: grid; place-items: center; padding: 24px; }}

    .chat-panel {{
      width: min(780px, 100%);
      min-height: 700px;
      display: grid;
      grid-template-rows: auto auto 1fr auto;
      border: 1px solid rgba(255, 255, 255, 0.14);
      border-radius: 8px;
      background: rgba(13, 17, 22, 0.9);
      box-shadow: 0 24px 70px rgba(0, 0, 0, 0.36);
      overflow: hidden;
    }}

    .chat-header, .key-form, .chat-form {{
      display: grid;
      gap: 10px;
      padding: 18px 22px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }}

    .chat-header {{ grid-template-columns: 1fr auto; align-items: center; }}
    .eyebrow {{ margin: 0 0 4px; color: {theme['accent']}; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; }}
    h1 {{ margin: 0; font-size: clamp(1.6rem, 4vw, 2.35rem); }}
    .status {{ padding: 6px 10px; border: 1px solid {theme['accent']}85; border-radius: 999px; color: {theme['accent']}; font-size: 0.78rem; white-space: nowrap; }}
    .status.busy {{ color: {theme['accent2']}; border-color: {theme['accent2']}85; }}
    .messages {{ display: flex; flex-direction: column; gap: 14px; padding: 22px; overflow: auto; }}
    .message {{ width: fit-content; max-width: min(84%, 560px); padding: 12px 14px; border-radius: 8px; line-height: 1.5; white-space: pre-wrap; }}
    .bot {{ background: #202936; border: 1px solid rgba(255, 255, 255, 0.09); }}
    .user {{ align-self: flex-end; background: {theme['user']}; }}
    .error {{ background: #3a1d1d; border: 1px solid rgba(255, 140, 140, 0.3); }}
    .key-form, .chat-form {{ grid-template-columns: 1fr auto; }}
    .chat-form {{ border-top: 1px solid rgba(255, 255, 255, 0.1); border-bottom: 0; }}
    input, button {{ min-height: 46px; border: 0; border-radius: 8px; font: inherit; }}
    input {{ width: 100%; padding: 0 14px; background: #f7fbff; color: #111318; }}
    button {{ padding: 0 18px; background: {theme['accent']}; color: #07110c; font-weight: 700; cursor: pointer; }}
    button:disabled {{ opacity: 0.65; cursor: wait; }}

    @media (max-width: 560px) {{
      .app {{ padding: 0; }}
      .chat-panel {{ min-height: 100vh; border: 0; border-radius: 0; }}
      .chat-header, .key-form, .chat-form {{ grid-template-columns: 1fr; }}
    }}
    """)

    demo_topics = json.dumps([{"match": [k], "text": v} for k, v in safe_topics], indent=2)
    write(folder / "public/script.js", f"""
    const messagesEl = document.querySelector('#messages');
    const keyForm = document.querySelector('#keyForm');
    const apiKeyInput = document.querySelector('#apiKeyInput');
    const form = document.querySelector('#chatForm');
    const input = document.querySelector('#userInput');
    const button = document.querySelector('#sendButton');
    const statusEl = document.querySelector('#status');

    const history = [];
    let apiKey = sessionStorage.getItem('openai_api_key') || '';
    const demoReplies = {demo_topics};

    function addMessage(text, sender, extraClass = '') {{
      const bubble = document.createElement('div');
      bubble.className = `message ${{sender}} ${{extraClass}}`.trim();
      bubble.textContent = text;
      messagesEl.appendChild(bubble);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }}

    function refreshKeyState() {{
      statusEl.textContent = apiKey ? 'real AI ready' : 'demo ready';
      input.disabled = false;
      button.disabled = false;
    }}

    function setBusy(isBusy) {{
      button.disabled = isBusy;
      input.disabled = isBusy;
      statusEl.textContent = isBusy ? {js_string(theme['status_busy'])} : apiKey ? 'real AI ready' : 'demo ready';
      statusEl.classList.toggle('busy', isBusy);
    }}

    function getDemoReply(text) {{
      const clean = text.toLowerCase();
      const hit = demoReplies.find((reply) => reply.match.some((word) => clean.includes(word)));
      if (hit) return hit.text;
      return `Demo mode: I would turn "${{text}}" into a practical next step in the {title} style.`;
    }}

    keyForm.addEventListener('submit', (event) => {{
      event.preventDefault();
      apiKey = apiKeyInput.value.trim();
      if (!apiKey) return;
      sessionStorage.setItem('openai_api_key', apiKey);
      apiKeyInput.value = '';
      refreshKeyState();
      addMessage('API key saved for this browser session. Real AI mode is ready after Vercel deployment; demo mode still works anytime.', 'bot');
      input.focus();
    }});

    async function sendMessage(text) {{
      history.push({{ role: 'user', content: text }});
      setBusy(true);

      if (!apiKey) {{
        window.setTimeout(() => {{
          const reply = getDemoReply(text);
          history.push({{ role: 'assistant', content: reply }});
          addMessage(reply, 'bot');
          setBusy(false);
          input.focus();
        }}, 250);
        return;
      }}

      try {{
        const response = await fetch('/api/chat', {{
          method: 'POST',
          headers: {{
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${{apiKey}}`
          }},
          body: JSON.stringify({{ messages: history }})
        }});

        if (!response.ok) throw new Error('Demo fallback');
        const data = await response.json();
        const reply = data.reply || getDemoReply(text);
        history.push({{ role: 'assistant', content: reply }});
        addMessage(reply, 'bot');
      }} catch {{
        const reply = getDemoReply(text);
        history.push({{ role: 'assistant', content: reply }});
        addMessage(reply, 'bot');
      }} finally {{
        setBusy(false);
        input.focus();
      }}
    }}

    form.addEventListener('submit', (event) => {{
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      addMessage(text, 'user');
      input.value = '';
      sendMessage(text);
    }});

    addMessage({js_string(welcome)}, 'bot');
    refreshKeyState();
    """)

    return folder


def main() -> None:
    random.seed(datetime.now(timezone.utc).isoformat())
    requested = os.environ.get("CHATBOT_THEME", "").strip().lower()
    theme = next((item for item in THEMES if requested and requested in {item["slug"], item["title"].lower()}), None)
    theme = theme or random.choice(THEMES)
    folder = build_project(theme)
    print(f"Created {folder.relative_to(REPO_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
