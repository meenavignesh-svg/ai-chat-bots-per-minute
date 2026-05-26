#!/usr/bin/env python3
"""Generate one fresh premium browser-demo chatbot and update repo indexes."""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "ai-chatbots"

CATEGORIES = ["Healthcare", "Biotech", "Education", "Automation", "Productivity", "Medical Coding", "Local LLM", "RAG", "Voice Agents"]
CATEGORY_QUERY = {
    "Healthcare": "healthcare,clinic,technology",
    "Biotech": "biotechnology,laboratory,research",
    "Education": "learning,library,students",
    "Automation": "automation,workflow,technology",
    "Productivity": "workspace,planning,desk",
    "Medical Coding": "medical,documents,healthcare",
    "Local LLM": "computer,server,ai",
    "RAG": "library,data,research",
    "Voice Agents": "microphone,studio,voice",
}
DOMAINS = [
    ("Healthcare", "care", "safe wellness, appointment preparation, and care notes"),
    ("Biotech", "bio", "biotech terms, study notes, and research summaries"),
    ("Education", "learn", "tutoring, quiz practice, and clear explanations"),
    ("Automation", "flow", "workflow planning, task breakdowns, and process checks"),
    ("Productivity", "focus", "prioritization, planning, and personal systems"),
    ("Medical Coding", "code", "coding terminology and claim-review concepts"),
    ("Local LLM", "local", "local model testing and prompt-result notes"),
    ("RAG", "rag", "retrieval planning and source-grounded answers"),
    ("Voice Agents", "voice", "call flows and spoken interaction design"),
]
ROLES = [("Navigator", "nav"), ("Coach", "coach"), ("Analyst", "analyst"), ("Tutor", "tutor"), ("Planner", "planner"), ("Reviewer", "reviewer"), ("Builder", "builder"), ("Scribe", "scribe")]
JOBS = [("Daily Brief", "brief"), ("Decision Helper", "decision"), ("Practice Lab", "practice"), ("Checklist Maker", "checklist"), ("Explainer", "explain"), ("Quality Check", "quality"), ("Idea Sprint", "sprint"), ("Troubleshooter", "fix")]
PALETTES = [("#38bdf8", "#14b8a6"), ("#2dd4bf", "#f472b6"), ("#facc15", "#60a5fa"), ("#a78bfa", "#34d399"), ("#fb7185", "#fbbf24"), ("#93c5fd", "#22c55e"), ("#c084fc", "#67e8f9"), ("#f97316", "#84cc16"), ("#e879f9", "#38bdf8")]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def read(path: str) -> str:
    file = ROOT / path
    return file.read_text(encoding="utf-8") if file.exists() else ""


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:54] or "chatbot"


def used_slugs() -> set[str]:
    return set(re.findall(r"ai-chatbots/([a-z0-9-]+)-chatbot-", read("README.md")))


def next_number(text: str) -> int:
    nums = [int(n) for n in re.findall(r"^\|\s*(\d+)\s*\|", text, flags=re.MULTILINE)]
    return max(nums, default=0) + 1


def append_row(path: str, row: str) -> None:
    write(ROOT / path, read(path).rstrip() + "\n" + row)


def palette_for(slug: str) -> tuple[str, str]:
    digest = hashlib.sha1(slug.encode("utf-8")).hexdigest()
    return PALETTES[int(digest[:2], 16) % len(PALETTES)]


def http_json(url: str, headers: dict[str, str], body: dict) -> dict | None:
    request = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json", **headers}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def extract_json(text: str) -> dict | None:
    start, end = text.find("{"), text.rfind("}") + 1
    if start < 0 or end <= start:
        return None
    try:
        return json.loads(text[start:end])
    except json.JSONDecodeError:
        return None


def openai_text(data: dict) -> str:
    if isinstance(data.get("output_text"), str):
        return data["output_text"]
    chunks = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if isinstance(content.get("text"), str):
                chunks.append(content["text"])
    return "\n".join(chunks)


def ai_prompt(used: set[str]) -> str:
    return (
        "Invent one premium web chatbot concept for an AI experimentation archive. "
        "Return only compact JSON with keys: title, category, focus, demo_reply, image_keywords. "
        "The chatbot must feel useful, specific, portfolio-worthy, and visually designable. "
        "Category must be one of: " + ", ".join(CATEGORIES) + ". "
        "image_keywords should be 2-4 comma-separated visual search words. "
        "Avoid these used slugs: " + ", ".join(sorted(used)[-80:])
    )


def ask_openai(used: set[str]) -> dict | None:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    model = os.environ.get("OPENAI_MODEL", "").strip() or "gpt-4.1-mini"
    data = http_json("https://api.openai.com/v1/responses", {"Authorization": f"Bearer {api_key}"}, {"model": model, "input": ai_prompt(used)})
    return extract_json(openai_text(data or {})) if data else None


def ask_gemini(used: set[str]) -> dict | None:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    model = os.environ.get("GEMINI_MODEL", "").strip() or "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    data = http_json(url, {}, {"contents": [{"parts": [{"text": ai_prompt(used)}]}]})
    try:
        return extract_json(data["candidates"][0]["content"]["parts"][0]["text"])
    except (TypeError, KeyError, IndexError):
        return None


def normalize_ai_theme(raw: dict | None, used: set[str]) -> dict[str, str] | None:
    if not raw:
        return None
    title = str(raw.get("title", "")).strip()[:70]
    category = str(raw.get("category", "Productivity")).strip()[:40]
    focus = str(raw.get("focus", "helpful planning and practical answers")).strip()[:240]
    demo = str(raw.get("demo_reply", "Ask a specific question and I will suggest a useful next step.")).strip()[:300]
    image_keywords = str(raw.get("image_keywords", CATEGORY_QUERY.get(category, "technology,workspace"))).strip()[:90]
    if not title:
        return None
    slug = slugify(title)
    if slug in used:
        slug = slugify(f"{title}-{datetime.now(timezone.utc).strftime('%H%M%S')}")
    accent, accent2 = palette_for(slug)
    return {"slug": slug, "title": title, "category": category, "focus": focus, "demo": demo, "accent": accent, "accent2": accent2, "image_keywords": image_keywords, "source": "AI idea engine"}


def local_ideas() -> list[dict[str, str]]:
    ideas = []
    for domain, domain_slug, domain_focus in DOMAINS:
        for role, role_slug in ROLES:
            for job, job_slug in JOBS:
                slug = f"{domain_slug}-{role_slug}-{job_slug}"
                accent, accent2 = palette_for(slug)
                title = f"{domain} {role} {job}"
                focus = f"{domain_focus}; practical {job.lower()} support; clear next-step guidance"
                ideas.append({"slug": slug, "title": title, "category": domain, "focus": focus, "demo": f"I can help with {focus}. Ask one specific question and I will turn it into a useful action.", "accent": accent, "accent2": accent2, "image_keywords": CATEGORY_QUERY.get(domain, "technology,workspace"), "source": "local idea engine"})
    return ideas


def pick_theme() -> dict[str, str]:
    used = used_slugs()
    ai_theme = normalize_ai_theme(ask_openai(used), used) or normalize_ai_theme(ask_gemini(used), used)
    if ai_theme:
        return ai_theme
    available = [idea for idea in local_ideas() if idea["slug"] not in used]
    if not available:
        raise SystemExit("No unused idea combinations left. Add more idea parts before running again.")
    random.seed(datetime.now(timezone.utc).isoformat())
    return random.choice(available)


def image_url(theme: dict[str, str]) -> str:
    query = urllib.parse.quote(theme.get("image_keywords") or CATEGORY_QUERY.get(theme["category"], "technology,workspace"))
    return f"https://source.unsplash.com/1400x1000/?{query}"


def cover_svg(title: str, category: str, accent: str, accent2: str) -> str:
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_category = category.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" role="img" aria-label="{safe_title} cover">
      <defs>
        <linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient>
        <filter id="blur"><feGaussianBlur stdDeviation="35"/></filter>
      </defs>
      <rect width="1200" height="900" fill="#10151d"/>
      <circle cx="210" cy="190" r="170" fill="{accent}" opacity="0.55" filter="url(#blur)"/>
      <circle cx="970" cy="250" r="210" fill="{accent2}" opacity="0.42" filter="url(#blur)"/>
      <path d="M150 650 C330 520 460 720 620 590 C760 475 890 520 1050 430" fill="none" stroke="url(#g)" stroke-width="34" stroke-linecap="round" opacity="0.78"/>
      <rect x="90" y="90" width="1020" height="700" rx="46" fill="none" stroke="rgba(255,255,255,.24)" stroke-width="3"/>
      <text x="110" y="710" fill="white" font-size="76" font-family="Inter, Arial, sans-serif" font-weight="800">{safe_title}</text>
      <text x="116" y="768" fill="rgba(255,255,255,.76)" font-size="34" font-family="Inter, Arial, sans-serif">{safe_category} chatbot</text>
    </svg>
    """


def build() -> str:
    theme = pick_theme()
    slug, title, category, focus = theme["slug"], theme["title"], theme["category"], theme["focus"]
    demo, accent, accent2 = theme["demo"], theme["accent"], theme["accent2"]
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%d-%H%M%Sz")
    made = now.strftime("%Y-%m-%d %H:%M UTC")
    folder = OUT / f"{slug}-chatbot-{stamp}"
    project_path = folder.relative_to(ROOT).as_posix()
    system = f"You are {title}, a premium practical chatbot for {focus}. Ask sharp clarifying questions when useful. Give crisp, safe, specific, high-quality answers with next actions."
    photo = image_url(theme)

    write(folder / "README.md", f"""
    # {title}

    A premium browser-demo chatbot generated by automation pipeline.

    ## Browser Demo

    Open `public/index.html` in a browser. Demo mode works without setup and includes a visual cover.

    ## Optional Real AI Mode

    Deploy this folder to Vercel and set `OPENAI_API_KEY`, or let visitors enter their own OpenAI API key in the browser UI. Browser-entered keys stay in `sessionStorage`.

    ## Folder

    `{project_path}`
    """)
    write(folder / "public/cover.svg", cover_svg(title, category, accent, accent2))
    write(folder / "package.json", json.dumps({"name": f"{slug}-chatbot", "version": "1.0.0", "type": "module", "scripts": {"dev": "vercel dev"}, "dependencies": {"@vercel/node": "^3.2.27", "openai": "^5.0.0"}, "devDependencies": {"vercel": "^34.3.0"}, "engines": {"node": ">=18"}}, indent=2))
    write(folder / "vercel.json", '{\n  "version": 2,\n  "routes": [\n    { "src": "/api/chat", "dest": "/api/chat.js" },\n    { "src": "/(.*)", "dest": "/public/$1" }\n  ]\n}')
    write(folder / "api/chat.js", f"""
    import OpenAI from 'openai';

    export default async function handler(req, res) {{
      if (req.method !== 'POST') return res.status(405).json({{ error: 'Method not allowed.' }});
      const visitorKey = req.headers.authorization?.replace(/^Bearer\s+/i, '') || req.body?.apiKey;
      const apiKey = process.env.OPENAI_API_KEY || visitorKey;
      if (!apiKey) return res.status(400).json({{ error: 'OpenAI API key required for real AI mode.' }});
      const messages = Array.isArray(req.body?.messages) ? req.body.messages.slice(-12) : [];
      const input = messages.map((m) => ({{ role: m.role === 'assistant' ? 'assistant' : 'user', content: String(m.content || '').slice(0, 2400) }}));
      const client = new OpenAI({{ apiKey }});
      const response = await client.responses.create({{ model: process.env.OPENAI_MODEL || 'gpt-4.1-mini', instructions: {json.dumps(system)}, input }});
      return res.status(200).json({{ reply: response.output_text || 'Please try again.' }});
    }}
    """)
    write(folder / "public/index.html", f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{title}</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body>
      <main class="app-shell">
        <section class="hero">
          <img src="{photo}" alt="{category} visual" onerror="this.onerror=null;this.src='cover.svg';">
          <div class="hero-copy"><p>{category}</p><h1>{title}</h1><span>Premium browser demo</span></div>
        </section>
        <section class="chat">
          <header><div><p>{category}</p><h2>{title}</h2></div><span id="status">demo ready</span></header>
          <form id="keyForm" class="key-form"><input id="apiKey" type="password" placeholder="Optional OpenAI API key"><button>Use Key</button></form>
          <div id="messages"></div>
          <form id="chatForm" class="chat-form"><input id="text" placeholder="Ask this chatbot for a sharp answer..."><button>Send</button></form>
        </section>
      </main>
      <script src="script.js"></script>
    </body>
    </html>
    """)
    write(folder / "public/style.css", f"""
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background: #111318; color: #f8fafc; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: #111318; }}
    .app-shell {{ min-height: 100vh; display: grid; grid-template-columns: minmax(320px, 0.9fr) minmax(380px, 1.1fr); }}
    .hero {{ position: relative; min-height: 100vh; overflow: hidden; background: #121923; }}
    .hero img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(1.08) contrast(1.04); }}
    .hero::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(8,12,18,.18), rgba(8,12,18,.84)); }}
    .hero-copy {{ position: absolute; z-index: 1; left: 32px; right: 32px; bottom: 34px; }}
    .hero-copy p, header p {{ margin: 0 0 8px; color: {accent}; text-transform: uppercase; font-size: .75rem; letter-spacing: .08em; font-weight: 800; }}
    h1 {{ margin: 0 0 14px; font-size: clamp(2.25rem, 6vw, 4.7rem); line-height: .95; max-width: 760px; }}
    .hero-copy span {{ display: inline-flex; border: 1px solid rgba(255,255,255,.34); border-radius: 999px; padding: 8px 12px; background: rgba(0,0,0,.24); }}
    .chat {{ min-height: 100vh; display: grid; grid-template-rows: auto auto 1fr auto; background: radial-gradient(circle at 14% 12%, {accent}24, transparent 22rem), radial-gradient(circle at 90% 20%, {accent2}24, transparent 24rem), #10151d; }}
    header, form {{ display: grid; gap: 10px; padding: 18px 22px; border-bottom: 1px solid #ffffff1a; }}
    header {{ grid-template-columns: 1fr auto; align-items: center; }}
    h2 {{ margin: 0; font-size: clamp(1.35rem, 3vw, 2rem); }}
    #status {{ border: 1px solid {accent}; color: {accent}; padding: 6px 10px; border-radius: 999px; font-size: .78rem; white-space: nowrap; }}
    #messages {{ padding: 22px; display: flex; flex-direction: column; gap: 14px; overflow: auto; }}
    .msg {{ max-width: min(84%, 620px); padding: 12px 14px; border-radius: 8px; line-height: 1.5; white-space: pre-wrap; background: #202936; border: 1px solid rgba(255,255,255,.08); }}
    .user {{ align-self: flex-end; background: {accent}; color: #061014; border-color: transparent; }}
    form {{ grid-template-columns: 1fr auto; }}
    input, button {{ min-height: 46px; border: 0; border-radius: 8px; font: inherit; }}
    input {{ padding: 0 14px; background: #f8fafc; color: #111318; min-width: 0; }}
    button {{ padding: 0 18px; background: {accent2}; color: #07110c; font-weight: 800; cursor: pointer; }}
    button:disabled {{ opacity: .7; cursor: wait; }}
    @media (max-width: 820px) {{ .app-shell {{ grid-template-columns: 1fr; }} .hero {{ min-height: 42vh; }} .chat {{ min-height: 58vh; }} }}
    @media (max-width: 560px) {{ .hero-copy {{ left: 20px; right: 20px; bottom: 22px; }} header, form {{ grid-template-columns: 1fr; }} h1 {{ font-size: 2.3rem; }} }}
    """)
    write(folder / "public/script.js", f"""
    const messages = document.querySelector('#messages');
    const text = document.querySelector('#text');
    const apiInput = document.querySelector('#apiKey');
    const statusEl = document.querySelector('#status');
    const sendButton = document.querySelector('#chatForm button');
    let apiKey = sessionStorage.getItem('openai_api_key') || '';
    const history = [];

    function add(content, role = 'bot') {{
      const node = document.createElement('div');
      node.className = `msg ${{role}}`;
      node.textContent = content;
      messages.appendChild(node);
      messages.scrollTop = messages.scrollHeight;
    }}

    function setBusy(isBusy) {{
      sendButton.disabled = isBusy;
      statusEl.textContent = isBusy ? 'thinking' : apiKey ? 'real AI ready' : 'demo ready';
    }}

    document.querySelector('#keyForm').addEventListener('submit', (event) => {{
      event.preventDefault();
      apiKey = apiInput.value.trim();
      if (!apiKey) return;
      sessionStorage.setItem('openai_api_key', apiKey);
      apiInput.value = '';
      statusEl.textContent = 'real AI ready';
      add('API key saved for this browser session. Real AI mode is ready after deployment.');
    }});

    document.querySelector('#chatForm').addEventListener('submit', async (event) => {{
      event.preventDefault();
      const value = text.value.trim();
      if (!value) return;
      text.value = '';
      add(value, 'user');
      history.push({{ role: 'user', content: value }});
      setBusy(true);
      if (!apiKey) {{
        const reply = {json.dumps(demo)};
        history.push({{ role: 'assistant', content: reply }});
        setTimeout(() => {{ add(reply); setBusy(false); }}, 220);
        return;
      }}
      try {{
        const response = await fetch('/api/chat', {{ method: 'POST', headers: {{ 'Content-Type': 'application/json', Authorization: `Bearer ${{apiKey}}` }}, body: JSON.stringify({{ messages: history }}) }});
        const data = await response.json();
        const reply = data.reply || data.error || 'No reply received.';
        history.push({{ role: 'assistant', content: reply }});
        add(reply);
      }} catch {{
        add({json.dumps(demo)});
      }} finally {{
        setBusy(false);
      }}
    }});

    add({json.dumps(demo)});
    """)
    number = next_number(read("README.md"))
    append_row("README.md", f"| {number} | {title} | {made} | {category} | `{project_path}` | Successful demo with visual cover | Browser demo + Vercel/OpenAI-ready | Not deployed |")
    append_row("tracking/successful-projects.md", f"| {number} | {title} | {made} | `{project_path}` | Premium visual browser demo created. |")
    append_row("tracking/model-usage.md", f"| {number} | {title} | Browser rules | gpt-4.1-mini via server/visitor key | generated by {theme['source']} with visual template |")
    append_row("tracking/deployment-links.md", f"| {number} | {title} | `{project_path}` | Pending | Not deployed |")
    return project_path


if __name__ == "__main__":
    print(f"Created {build()}")
