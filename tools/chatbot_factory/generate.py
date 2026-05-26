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
DOCS = ROOT / "docs"
PAGES_BASE = "https://meenavignesh-svg.github.io/ai-chat-bots-per-minute"

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
PALETTES = [("#38bdf8", "#14b8a6"), ("#2dd4bf", "#f472b6"), ("#facc15", "#60a5fa"), ("#a78bfa", "#34d399"), ("#fb7185", "#fbbf24"), ("#93c5fd", "#22c55e"), ("#c084fc", "#67e8f9"), ("#f97316", "#84cc16"), ("#e879f9", "#38bdf8"), ("#10b981", "#f59e0b"), ("#ef4444", "#22d3ee"), ("#8b5cf6", "#f97316"), ("#06b6d4", "#eab308"), ("#84cc16", "#ec4899"), ("#0ea5e9", "#f43f5e"), ("#14b8a6", "#a855f7")]
LAYOUTS = [
    {"id": "split-command", "label": "Split Command Center", "body": "splitBody", "extra": "briefPanel"},
    {"id": "studio-board", "label": "Studio Board", "body": "studioBody", "extra": "promptRail"},
    {"id": "insight-deck", "label": "Insight Deck", "body": "deckBody", "extra": "qualityMeter"},
    {"id": "mission-console", "label": "Mission Console", "body": "consoleBody", "extra": "missionPanel"},
    {"id": "research-desk", "label": "Research Desk", "body": "researchBody", "extra": "sourcePanel"},
    {"id": "clinic-hub", "label": "Clinic Hub", "body": "clinicBody", "extra": "carePanel"},
    {"id": "voice-studio", "label": "Voice Studio", "body": "voiceBody", "extra": "callPanel"},
    {"id": "learning-lab", "label": "Learning Lab", "body": "learningBody", "extra": "quizPanel"},
    {"id": "ops-wall", "label": "Operations Wall", "body": "opsBody", "extra": "automationPanel"},
    {"id": "evidence-room", "label": "Evidence Room", "body": "evidenceBody", "extra": "citationPanel"},
    {"id": "focus-suite", "label": "Focus Suite", "body": "focusBody", "extra": "priorityPanel"},
    {"id": "model-bench", "label": "Model Bench", "body": "benchBody", "extra": "evalPanel"},
]
FEATURES = [
    {"id": "brief-builder", "label": "Brief Builder", "chips": ["Summarize", "Risks", "Next steps"]},
    {"id": "decision-lens", "label": "Decision Lens", "chips": ["Options", "Tradeoffs", "Recommendation"]},
    {"id": "practice-coach", "label": "Practice Coach", "chips": ["Quiz me", "Hint", "Review"]},
    {"id": "ops-check", "label": "Ops Check", "chips": ["Checklist", "Blockers", "Automate"]},
]


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


def choice_for(slug: str, items: list[dict], salt: str) -> dict:
    digest = hashlib.sha1(f"{slug}:{salt}".encode("utf-8")).hexdigest()
    return items[int(digest[:2], 16) % len(items)]


def used_variants() -> tuple[set[str], set[str], set[str]]:
    layouts, palettes, signatures = set(), set(), set()
    for meta in OUT.glob("*/project.json"):
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("layout"):
            layouts.add(str(data["layout"]))
        if data.get("palette"):
            palettes.add(str(data["palette"]))
        if data.get("code_signature"):
            signatures.add(str(data["code_signature"]))
    return layouts, palettes, signatures


def choose_unused_dict(slug: str, items: list[dict], used: set[str], key: str, salt: str) -> dict:
    pool = [item for item in items if item[key] not in used] or items
    return choice_for(slug, pool, salt)


def choose_unused_palette(slug: str, used: set[str]) -> tuple[str, str]:
    pool = [pair for pair in PALETTES if "-".join(pair) not in used] or PALETTES
    digest = hashlib.sha1(f"{slug}:palette".encode("utf-8")).hexdigest()
    return pool[int(digest[:2], 16) % len(pool)]


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
        "The chatbot must be useful, specific, portfolio-worthy, and different from a generic chat demo. "
        "Category must be one of: " + ", ".join(CATEGORIES) + ". "
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


def cover_svg(title: str, category: str, accent: str, accent2: str, layout: dict, feature: dict) -> str:
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    safe_category = category.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" role="img" aria-label="{safe_title} cover">
      <defs>
        <linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient>
      </defs>
      <rect width="1200" height="900" fill="#10151d"/>
      <path d="M110 680 C310 500 460 720 650 560 C800 430 920 500 1090 350" fill="none" stroke="url(#g)" stroke-width="42" stroke-linecap="round" opacity="0.8"/>
      <rect x="86" y="80" width="1028" height="710" rx="42" fill="none" stroke="rgba(255,255,255,.24)" stroke-width="3"/>
      <text x="112" y="155" fill="{accent}" font-size="30" font-family="Inter, Arial" font-weight="800">{safe_category} / {feature["label"]}</text>
      <text x="112" y="700" fill="white" font-size="76" font-family="Inter, Arial" font-weight="800">{safe_title}</text>
      <text x="116" y="758" fill="rgba(255,255,255,.76)" font-size="32" font-family="Inter, Arial">{layout["label"]}</text>
    </svg>
    """


def screenshot_svg(title: str, category: str, accent: str, accent2: str, layout: dict, feature: dict) -> str:
    safe_title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 1000" role="img" aria-label="{safe_title} screenshot">
      <rect width="1440" height="1000" fill="#0f131b"/>
      <rect x="70" y="64" width="1300" height="820" rx="28" fill="#151b25" stroke="rgba(255,255,255,.18)" stroke-width="3"/>
      <rect x="105" y="108" width="510" height="720" rx="18" fill="url(#g)"/>
      <rect x="660" y="108" width="675" height="120" rx="18" fill="#202938"/>
      <rect x="660" y="260" width="675" height="350" rx="18" fill="#111827"/>
      <rect x="660" y="645" width="675" height="92" rx="18" fill="#f8fafc"/>
      <defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient></defs>
      <text x="140" y="715" fill="#fff" font-size="56" font-family="Inter, Arial" font-weight="800">{safe_title}</text>
      <text x="690" y="178" fill="{accent}" font-size="24" font-family="Inter, Arial" font-weight="800">{category} / {layout["label"]}</text>
      <text x="690" y="330" fill="#f8fafc" font-size="34" font-family="Inter, Arial" font-weight="800">{feature["label"]}</text>
      <text x="690" y="385" fill="#cbd5e1" font-size="26" font-family="Inter, Arial">Premium browser demo with unique template and palette.</text>
    </svg>
    """


def render_index(title: str, category: str, photo: str, layout: dict, feature: dict) -> str:
    chips = "".join(f"<button type=\"button\" class=\"chip\">{chip}</button>" for chip in feature["chips"])
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{title}</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body data-variant="{layout["id"]}" data-feature="{feature["id"]}">
      <main class="app-shell {layout["body"]}">
        <section class="hero">
          <img src="{photo}" alt="{category} visual" onerror="this.onerror=null;this.src='cover.svg';">
          <div class="hero-copy"><p>{category}</p><h1>{title}</h1><span>{layout["label"]}</span></div>
        </section>
        <section class="chat">
          <header><div><p>{feature["label"]}</p><h2>{title}</h2></div><span id="status">demo ready</span></header>
          <aside class="tool-panel"><strong>Starter actions</strong><div class="chips">{chips}</div><small id="quality">Premium variant: {layout["id"]}</small></aside>
          <form id="keyForm" class="key-form"><input id="apiKey" type="password" placeholder="Optional OpenAI API key"><button>Use Key</button></form>
          <div id="messages"></div>
          <form id="chatForm" class="chat-form"><input id="text" placeholder="Ask for a sharp answer..."><button>Send</button></form>
        </section>
      </main>
      <script src="script.js"></script>
    </body>
    </html>
    """


def render_style(accent: str, accent2: str, layout: dict) -> str:
    if layout["id"] == "studio-board":
        grid = "grid-template-columns: minmax(360px, .72fr) minmax(420px, 1.28fr);"
        hero_min = "100vh"
        chat_bg = f"linear-gradient(135deg, #111318, #172033 55%, {accent}22)"
    elif layout["id"] == "insight-deck":
        grid = "grid-template-columns: minmax(420px, 1fr) minmax(420px, 1fr);"
        hero_min = "92vh"
        chat_bg = f"radial-gradient(circle at 85% 10%, {accent2}2d, transparent 24rem), #10151d"
    else:
        grid = "grid-template-columns: minmax(320px, .9fr) minmax(380px, 1.1fr);"
        hero_min = "100vh"
        chat_bg = f"radial-gradient(circle at 14% 12%, {accent}24, transparent 22rem), radial-gradient(circle at 90% 20%, {accent2}24, transparent 24rem), #10151d"
    return f"""
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background: #111318; color: #f8fafc; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: #111318; }}
    .app-shell {{ min-height: 100vh; display: grid; {grid} }}
    .hero {{ position: relative; min-height: {hero_min}; overflow: hidden; background: #121923; }}
    .hero img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: saturate(1.08) contrast(1.04); }}
    .hero::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(8,12,18,.12), rgba(8,12,18,.86)); }}
    .hero-copy {{ position: absolute; z-index: 1; left: 32px; right: 32px; bottom: 34px; }}
    .hero-copy p, header p {{ margin: 0 0 8px; color: {accent}; text-transform: uppercase; font-size: .75rem; letter-spacing: .08em; font-weight: 800; }}
    h1 {{ margin: 0 0 14px; font-size: clamp(2.2rem, 6vw, 4.8rem); line-height: .95; max-width: 760px; }}
    .hero-copy span, .chip {{ display: inline-flex; border: 1px solid rgba(255,255,255,.34); border-radius: 999px; padding: 8px 12px; background: rgba(0,0,0,.24); color: #fff; }}
    .chat {{ min-height: 100vh; display: grid; grid-template-rows: auto auto auto 1fr auto; background: {chat_bg}; }}
    header, form, .tool-panel {{ display: grid; gap: 10px; padding: 18px 22px; border-bottom: 1px solid #ffffff1a; }}
    header {{ grid-template-columns: 1fr auto; align-items: center; }}
    h2 {{ margin: 0; font-size: clamp(1.35rem, 3vw, 2rem); }}
    #status {{ border: 1px solid {accent}; color: {accent}; padding: 6px 10px; border-radius: 999px; font-size: .78rem; white-space: nowrap; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip {{ cursor: pointer; font: inherit; color: #f8fafc; }}
    #messages {{ padding: 22px; display: flex; flex-direction: column; gap: 14px; overflow: auto; }}
    .msg {{ max-width: min(84%, 620px); padding: 12px 14px; border-radius: 8px; line-height: 1.5; white-space: pre-wrap; background: #202936; border: 1px solid rgba(255,255,255,.08); box-shadow: 0 18px 42px rgba(0,0,0,.22); }}
    .user {{ align-self: flex-end; background: {accent}; color: #061014; border-color: transparent; }}
    form {{ grid-template-columns: 1fr auto; }}
    input, button {{ min-height: 46px; border: 0; border-radius: 8px; font: inherit; }}
    input {{ padding: 0 14px; background: #f8fafc; color: #111318; min-width: 0; }}
    button {{ padding: 0 18px; background: {accent2}; color: #07110c; font-weight: 800; cursor: pointer; }}
    button:disabled {{ opacity: .7; cursor: wait; }}
    @media (max-width: 860px) {{ .app-shell {{ grid-template-columns: 1fr; }} .hero {{ min-height: 42vh; }} .chat {{ min-height: 58vh; }} }}
    @media (max-width: 560px) {{ .hero-copy {{ left: 20px; right: 20px; bottom: 22px; }} header, form {{ grid-template-columns: 1fr; }} h1 {{ font-size: 2.25rem; }} }}
    """


def render_script(demo: str, feature: dict, layout: dict) -> str:
    chips = json.dumps(feature["chips"])
    opener = json.dumps(demo)
    return f"""
    const messages = document.querySelector('#messages');
    const text = document.querySelector('#text');
    const apiInput = document.querySelector('#apiKey');
    const statusEl = document.querySelector('#status');
    const qualityEl = document.querySelector('#quality');
    const sendButton = document.querySelector('#chatForm button');
    const quickActions = {chips};
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

    function demoReply(value) {{
      const chosen = quickActions.find((item) => value.toLowerCase().includes(item.toLowerCase())) || '{feature["label"]}';
      return `${{chosen}} mode: {demo} Requested focus: "${{value}}".`;
    }}

    document.querySelectorAll('.chip').forEach((button) => {{
      button.addEventListener('click', () => {{
        text.value = `${{button.textContent}}: `;
        text.focus();
        qualityEl.textContent = `Premium variant: {layout["id"]} / ${{button.textContent}}`;
      }});
    }});

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
        const reply = demoReply(value);
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
        add(demoReply(value));
      }} finally {{
        setBusy(false);
      }}
    }});

    add({opener});
    """


def build() -> str:
    theme = pick_theme()
    slug, title, category, focus = theme["slug"], theme["title"], theme["category"], theme["focus"]
    demo = theme["demo"]
    used_layouts, used_palettes, used_signatures = used_variants()
    layout = choose_unused_dict(slug, LAYOUTS, used_layouts, "id", "layout")
    feature = choice_for(slug, FEATURES, "feature")
    accent, accent2 = choose_unused_palette(slug, used_palettes)
    palette_id = "-".join((accent, accent2))
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%d-%H%M%Sz")
    made = now.strftime("%Y-%m-%d %H:%M UTC")
    folder = OUT / f"{slug}-chatbot-{stamp}"
    demo_folder = DOCS / folder.name
    project_path = folder.relative_to(ROOT).as_posix()
    live_demo = f"{PAGES_BASE}/{folder.name}/"
    code_signature = hashlib.sha1(f"{slug}:{layout['id']}:{feature['id']}:{palette_id}:{stamp}".encode("utf-8")).hexdigest()
    if code_signature in used_signatures:
        raise SystemExit("Generated code signature already exists; refusing duplicate chatbot code.")
    system = f"You are {title}, a premium practical chatbot for {focus}. Use the {feature['label']} interaction style and keep answers crisp, specific, and action-oriented."
    photo = image_url(theme)

    write(folder / "README.md", f"""
    # {title}

    A premium browser-demo chatbot generated by automation pipeline.

    ## Premium Build

    - Layout variant: {layout["label"]}
    - Interaction feature: {feature["label"]}
    - Unique palette: `{palette_id}`
    - Visual cover with image fallback
    - Screenshot asset: `screenshots/preview.svg`
    - Browser demo mode plus optional Vercel/OpenAI mode

    ## Live Demo

    Browser demo link when GitHub Pages is enabled:

    {live_demo}

    You can also open `public/index.html` in a browser. Demo mode works without setup.

    ## Optional Real AI Mode

    Deploy this folder to Vercel and set `OPENAI_API_KEY`, or let visitors enter their own OpenAI API key in the browser UI. Browser-entered keys stay in `sessionStorage`.

    ## Folder

    `{project_path}`
    """)
    write(folder / "public/cover.svg", cover_svg(title, category, accent, accent2, layout, feature))
    write(folder / "screenshots/preview.svg", screenshot_svg(title, category, accent, accent2, layout, feature))
    write(folder / "package.json", json.dumps({"name": f"{slug}-chatbot", "version": "1.0.0", "type": "module", "scripts": {"start": "vercel dev", "dev": "vercel dev"}, "dependencies": {"@vercel/node": "^3.2.27", "openai": "^5.0.0"}, "devDependencies": {"vercel": "^34.3.0"}, "engines": {"node": ">=18"}}, indent=2))
    write(folder / "vercel.json", '{\n  "version": 2,\n  "routes": [\n    { "src": "/api/chat", "dest": "/api/chat.js" },\n    { "src": "/(.*)", "dest": "/public/$1" }\n  ]\n}')
    write(folder / "api/chat.js", f"""
    import OpenAI from 'openai';

    export default async function handler(req, res) {{
      if (req.method !== 'POST') return res.status(405).json({{ error: 'Method not allowed.' }});
      const visitorKey = req.headers.authorization?.replace(/^Bearer\\s+/i, '') || req.body?.apiKey;
      const apiKey = process.env.OPENAI_API_KEY || visitorKey;
      if (!apiKey) return res.status(400).json({{ error: 'OpenAI API key required for real AI mode.' }});
      const messages = Array.isArray(req.body?.messages) ? req.body.messages.slice(-12) : [];
      const input = messages.map((m) => ({{ role: m.role === 'assistant' ? 'assistant' : 'user', content: String(m.content || '').slice(0, 2400) }}));
      const client = new OpenAI({{ apiKey }});
      const response = await client.responses.create({{ model: process.env.OPENAI_MODEL || 'gpt-4.1-mini', instructions: {json.dumps(system)}, input }});
      return res.status(200).json({{ reply: response.output_text || 'Please try again.' }});
    }}
    """)
    index_html = render_index(title, category, photo, layout, feature)
    style_css = render_style(accent, accent2, layout)
    script_js = render_script(demo, feature, layout)
    write(folder / "public/index.html", index_html)
    write(folder / "public/style.css", style_css)
    write(folder / "public/script.js", script_js)
    write(folder / "project.json", json.dumps({"title": title, "category": category, "layout": layout["id"], "feature": feature["id"], "palette": palette_id, "live_demo": live_demo, "generated_at": made, "code_signature": code_signature}, indent=2))
    write(demo_folder / "index.html", index_html)
    write(demo_folder / "style.css", style_css)
    write(demo_folder / "script.js", script_js)
    write(demo_folder / "cover.svg", cover_svg(title, category, accent, accent2, layout, feature))

    number = next_number(read("README.md"))
    append_row("README.md", f"| {number} | {title} | {made} | {category} | `{project_path}` | Premium {layout['label']} with {feature['label']} and unique palette | Browser demo + Vercel/OpenAI-ready | {live_demo} |")
    append_row("tracking/successful-projects.md", f"| {number} | {title} | {made} | `{project_path}` | Premium {layout['label']} chatbot with {feature['label']}, screenshot, and live demo path. |")
    append_row("tracking/model-usage.md", f"| {number} | {title} | Browser rules | gpt-4.1-mini via server/visitor key | generated by {theme['source']} with {layout['id']} / {feature['id']} / {palette_id} |")
    append_row("tracking/deployment-links.md", f"| {number} | {title} | `{project_path}` | {live_demo} | GitHub Pages browser demo; Vercel optional for real AI mode |")
    return project_path


if __name__ == "__main__":
    print(f"Created {build()}")
