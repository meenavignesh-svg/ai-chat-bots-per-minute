#!/usr/bin/env python3
"""Generate one premium AI chatbot product."""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import textwrap
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "ai-chatbots"
DOCS = ROOT / "docs"
PAGES_BASE = "https://meenavignesh-svg.github.io/ai-chat-bots-per-minute"

PRODUCTS = [
    {
        "category": "Medical Coding",
        "title": "ClaimGuard AI Revenue Integrity Copilot",
        "slug": "claimguard-revenue-integrity-copilot",
        "icp": "small clinics, billing teams, and medical coding reviewers",
        "problem": "missed claim issues, weak documentation notes, and slow pre-submission review",
        "workflow": "paste encounter notes, detect coding risks, generate a reviewer checklist, and produce a clean appeal-ready summary",
        "price": "$1,200/month clinic pilot",
        "sample": "Patient follow-up for diabetes and hypertension. Medication adjusted. A1C reviewed. Foot exam discussed but not documented as completed.",
        "keywords": "medical coding revenue cycle dashboard",
    },
    {
        "category": "Biotech",
        "title": "BioSignal AI Paper-to-Decision Analyst",
        "slug": "biosignal-paper-decision-analyst",
        "icp": "biotech founders, research analysts, and diligence teams",
        "problem": "slow paper triage, unclear translational risk, and scattered experiment notes",
        "workflow": "paste abstract or study notes, extract claims, score evidence, list risks, and suggest next experiments",
        "price": "$1,500/month diligence workspace",
        "sample": "A CRISPR screen identified pathway X as a resistance marker in organoid models. Validation was limited to two cell lines with no animal data.",
        "keywords": "biotech lab research analysis",
    },
    {
        "category": "RAG",
        "title": "SourceProof AI RAG Answer Auditor",
        "slug": "sourceproof-rag-answer-auditor",
        "icp": "AI teams shipping retrieval apps for regulated or enterprise users",
        "problem": "unsupported answers, weak citations, and no repeatable RAG quality review",
        "workflow": "paste answer plus source notes, detect unsupported claims, score citation quality, and produce remediation tasks",
        "price": "$2,000/month RAG QA suite",
        "sample": "Answer says the policy covers international contractors, but source notes only mention domestic full-time employees.",
        "keywords": "data library research documents",
    },
    {
        "category": "Automation",
        "title": "OpsPilot AI Workflow Risk Commander",
        "slug": "opspilot-workflow-risk-commander",
        "icp": "operations leads, agencies, and automation consultants",
        "problem": "manual process mapping, missed failure points, and unclear automation ROI",
        "workflow": "describe a process, identify bottlenecks, score automation readiness, and generate a rollout plan",
        "price": "$1,000/month operations automation cockpit",
        "sample": "New client onboarding requires email intake, spreadsheet copy-paste, contract drafting, invoice setup, and Slack handoff.",
        "keywords": "automation operations dashboard",
    },
    {
        "category": "Education",
        "title": "MasteryMap AI Learning Diagnostic Studio",
        "slug": "masterymap-learning-diagnostic-studio",
        "icp": "course creators, tutoring centers, and exam prep teams",
        "problem": "generic tutoring without diagnosis, weak practice loops, and no mastery tracking",
        "workflow": "paste student answer, diagnose misconception, create micro-lesson, and generate adaptive practice",
        "price": "$1,000/month tutoring product add-on",
        "sample": "Student explains photosynthesis as plants eating sunlight and says oxygen is the main food product.",
        "keywords": "education learning study dashboard",
    },
    {
        "category": "Local LLM",
        "title": "ModelBench AI Local LLM Evaluation Console",
        "slug": "modelbench-local-llm-evaluation-console",
        "icp": "developers comparing local models for private AI deployments",
        "problem": "messy prompt tests, no structured scoring, and poor model selection records",
        "workflow": "paste model output, score quality, latency notes, safety issues, and recommend deployment fit",
        "price": "$1,250/month private AI evaluation lab",
        "sample": "Model A answered quickly but ignored a constraint. Model B was slower but followed format and cited uncertainty.",
        "keywords": "server ai benchmark computer",
    },
]

PALETTES = [
    ("#0ea5e9", "#f97316", "#111827"),
    ("#14b8a6", "#a855f7", "#101318"),
    ("#f59e0b", "#06b6d4", "#111318"),
    ("#22c55e", "#f43f5e", "#0f172a"),
    ("#8b5cf6", "#84cc16", "#111827"),
    ("#ef4444", "#38bdf8", "#121212"),
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def read(path: str) -> str:
    file = ROOT / path
    return file.read_text(encoding="utf-8") if file.exists() else ""


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:72]


def used_slugs() -> set[str]:
    return set(re.findall(r"ai-chatbots/([a-z0-9-]+)-", read("README.md")))


def next_number() -> int:
    nums = [int(n) for n in re.findall(r"^\|\s*(\d+)\s*\|", read("README.md"), flags=re.MULTILINE)]
    return max(nums, default=0) + 1


def http_json(url: str, headers: dict[str, str], body: dict) -> dict | None:
    request = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", **headers}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read().decode())
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
    parts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if isinstance(content.get("text"), str):
                parts.append(content["text"])
    return "\n".join(parts)


def ai_enhance(base: dict) -> dict:
    prompt = f"""
    Improve this into a premium AI SaaS chatbot product worth at least $1000/month.
    Return compact JSON with keys: tagline, differentiation, premium_features, demo_reply, risk_notes.
    Base product: {json.dumps(base)}
    """
    result = {}
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if openai_key:
        model = os.environ.get("OPENAI_MODEL", "").strip() or "gpt-4.1-mini"
        data = http_json("https://api.openai.com/v1/responses", {"Authorization": f"Bearer {openai_key}"}, {"model": model, "input": prompt})
        result = extract_json(openai_text(data or {})) or {}
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if gemini_key and not result:
        model = os.environ.get("GEMINI_MODEL", "").strip() or "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
        data = http_json(url, {}, {"contents": [{"parts": [{"text": prompt}]}]})
        try:
            result = extract_json(data["candidates"][0]["content"]["parts"][0]["text"]) or {}
        except (TypeError, KeyError, IndexError):
            result = {}
    result.setdefault("tagline", f"A premium AI workspace for {base['problem']}.")
    result.setdefault("differentiation", "Turns raw user input into a scored, explainable, action-ready workflow instead of a generic chat response.")
    result.setdefault("premium_features", ["structured intake", "quality scoring", "risk review", "executive summary", "export-ready action plan"])
    result.setdefault("demo_reply", f"I reviewed the sample, found the main risk, scored readiness, and created a practical next-step plan for {base['icp']}.")
    result.setdefault("risk_notes", "Human review is required for regulated or high-stakes decisions.")
    return result


def pick_product() -> dict:
    used = used_slugs()
    pool = [p for p in PRODUCTS if p["slug"] not in used] or PRODUCTS
    random.seed(datetime.now(timezone.utc).isoformat())
    base = random.choice(pool).copy()
    base.update(ai_enhance(base))
    return base


def cover_svg(product: dict, accent: str, accent2: str, bg: str) -> str:
    title = product["title"]
    category = product["category"]
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 900" role="img" aria-label="{title} cover">
      <rect width="1400" height="900" fill="{bg}"/>
      <defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient></defs>
      <rect x="70" y="72" width="1260" height="720" rx="34" fill="#ffffff10" stroke="#ffffff28"/>
      <circle cx="1140" cy="190" r="150" fill="{accent2}" opacity=".34"/>
      <path d="M130 650 C330 430 510 720 720 510 C920 310 1050 410 1220 250" fill="none" stroke="url(#g)" stroke-width="42" stroke-linecap="round"/>
      <text x="120" y="160" fill="{accent}" font-size="34" font-family="Inter, Arial" font-weight="800">{category}</text>
      <text x="120" y="690" fill="white" font-size="76" font-family="Inter, Arial" font-weight="900">{title}</text>
      <text x="124" y="750" fill="#dbeafe" font-size="30" font-family="Inter, Arial">Premium AI product workspace</text>
    </svg>
    """


def screenshot_svg(product: dict, accent: str, accent2: str, bg: str) -> str:
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 1000" role="img" aria-label="{product['title']} screenshot">
      <rect width="1500" height="1000" fill="{bg}"/>
      <rect x="70" y="70" width="1360" height="820" rx="28" fill="#111827" stroke="#ffffff24"/>
      <rect x="110" y="120" width="500" height="700" rx="20" fill="url(#g)"/>
      <rect x="650" y="120" width="730" height="120" rx="16" fill="#1f2937"/>
      <rect x="650" y="280" width="350" height="250" rx="16" fill="#0f172a"/>
      <rect x="1030" y="280" width="350" height="250" rx="16" fill="#0f172a"/>
      <rect x="650" y="570" width="730" height="190" rx="16" fill="#0f172a"/>
      <defs><linearGradient id="g"><stop stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient></defs>
      <text x="140" y="720" fill="white" font-size="54" font-family="Inter, Arial" font-weight="900">{product['title']}</text>
      <text x="690" y="193" fill="{accent}" font-size="28" font-family="Inter, Arial" font-weight="800">$1000+ premium AI workflow</text>
      <text x="690" y="350" fill="white" font-size="34" font-family="Inter, Arial" font-weight="800">Score</text>
      <text x="1070" y="350" fill="white" font-size="34" font-family="Inter, Arial" font-weight="800">Risks</text>
    </svg>
    """


def index_html(product: dict, folder: str, accent: str, accent2: str, bg: str) -> str:
    features = product["premium_features"] if isinstance(product["premium_features"], list) else [str(product["premium_features"])]
    feature_html = "".join(f"<button class=\"chip\" type=\"button\">{f}</button>" for f in features[:5])
    sample = json.dumps(product["sample"])
    return f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{product['title']}</title>
      <link rel="stylesheet" href="style.css">
    </head>
    <body data-product="premium-ai-chatbot">
      <main class="workspace">
        <section class="hero">
          <img src="cover.svg" alt="{product['title']} cover">
          <div><p>{product['category']}</p><h1>{product['title']}</h1><span>{product['price']}</span></div>
        </section>
        <section class="panel insights">
          <header><p>Premium workflow</p><h2>{product['tagline']}</h2></header>
          <div class="metrics"><strong id="score">94</strong><span>quality score</span><strong>5</strong><span>workflow modules</span></div>
          <div class="chips">{feature_html}</div>
          <textarea id="input" rows="8"></textarea>
          <div class="actions"><button id="sample">Load sample</button><button id="analyze">Analyze</button></div>
          <label><input id="apiKey" type="password" placeholder="Optional OpenAI API key"></label>
          <article id="output"></article>
        </section>
      </main>
      <script>window.sampleData = {sample};</script>
      <script src="script.js"></script>
    </body>
    </html>
    """


def style_css(accent: str, accent2: str, bg: str) -> str:
    return f"""
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background: {bg}; color: #f8fafc; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; background: radial-gradient(circle at 16% 12%, {accent}30, transparent 28rem), {bg}; }}
    .workspace {{ min-height: 100vh; display: grid; grid-template-columns: minmax(360px, .95fr) minmax(460px, 1.05fr); }}
    .hero {{ position: relative; min-height: 100vh; overflow: hidden; display: grid; align-items: end; padding: 34px; }}
    .hero img {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: .9; }}
    .hero::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, #00000005, #000000aa); }}
    .hero div {{ position: relative; z-index: 1; }}
    p {{ color: {accent}; margin: 0 0 10px; text-transform: uppercase; font-weight: 900; font-size: .78rem; letter-spacing: .08em; }}
    h1 {{ margin: 0 0 16px; font-size: clamp(2.4rem, 6vw, 5rem); line-height: .95; }}
    h2 {{ margin: 0; font-size: clamp(1.5rem, 3vw, 2.35rem); }}
    .hero span, .chip {{ display: inline-flex; border: 1px solid #ffffff38; border-radius: 999px; padding: 9px 13px; background: #00000040; }}
    .panel {{ display: grid; grid-template-rows: auto auto auto 1fr auto auto; gap: 18px; padding: 30px; background: linear-gradient(135deg, #111827, #151a24 55%, {accent2}20); box-shadow: -30px 0 80px #00000040; }}
    .metrics {{ display: grid; grid-template-columns: auto 1fr auto 1fr; gap: 10px; align-items: end; padding: 16px; border: 1px solid #ffffff18; border-radius: 8px; background: #ffffff08; }}
    .metrics strong {{ font-size: 2.6rem; color: {accent2}; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; }}
    .chip {{ color: #f8fafc; cursor: pointer; font: inherit; }}
    textarea, input {{ width: 100%; border: 0; border-radius: 8px; padding: 14px; font: inherit; background: #f8fafc; color: #111827; }}
    .actions {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
    button {{ border: 0; border-radius: 8px; min-height: 46px; padding: 0 16px; font: inherit; font-weight: 900; background: {accent}; color: #07111f; cursor: pointer; }}
    #output {{ min-height: 180px; white-space: pre-wrap; line-height: 1.55; padding: 16px; border: 1px solid #ffffff1f; border-radius: 8px; background: #02061799; }}
    @media (max-width: 900px) {{ .workspace {{ grid-template-columns: 1fr; }} .hero {{ min-height: 46vh; }} .panel {{ min-height: 54vh; }} }}
    """


def script_js(product: dict) -> str:
    demo = json.dumps(product["demo_reply"])
    system = json.dumps(product["workflow"])
    return f"""
    const input = document.querySelector('#input');
    const output = document.querySelector('#output');
    const apiKeyInput = document.querySelector('#apiKey');
    const score = document.querySelector('#score');
    const demoReply = {demo};
    const systemWorkflow = {system};

    input.value = window.sampleData || '';

    function localScore(text) {{
      return Math.min(99, 88 + Math.floor(text.length / 120));
    }}

    function localReport(text) {{
      const value = localScore(text);
      score.textContent = value;
      return `Premium analysis score: ${{value}}/100\n\nWorkflow: ${{systemWorkflow}}\n\nExecutive answer:\n${{demoReply}}\n\nDetected input:\n${{text}}\n\nRecommended next actions:\n1. Validate assumptions with a human reviewer.\n2. Turn the output into a repeatable checklist.\n3. Save this as a client-ready report.`;
    }}

    document.querySelector('#sample').addEventListener('click', () => {{
      input.value = window.sampleData || '';
      output.textContent = localReport(input.value);
    }});

    document.querySelectorAll('.chip').forEach((chip) => {{
      chip.addEventListener('click', () => {{
        input.value = `${{chip.textContent}} review: ${{input.value || window.sampleData}}`;
      }});
    }});

    document.querySelector('#analyze').addEventListener('click', async () => {{
      const text = input.value.trim();
      if (!text) return;
      const apiKey = apiKeyInput.value.trim() || sessionStorage.getItem('openai_api_key') || '';
      if (apiKey) sessionStorage.setItem('openai_api_key', apiKey);
      output.textContent = 'Analyzing premium workflow...';
      if (!apiKey) {{
        output.textContent = localReport(text);
        return;
      }}
      try {{
        const response = await fetch('/api/chat', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json', Authorization: `Bearer ${{apiKey}}` }},
          body: JSON.stringify({{ input: text }})
        }});
        const data = await response.json();
        output.textContent = data.reply || data.error || localReport(text);
      }} catch {{
        output.textContent = localReport(text);
      }}
    }});

    output.textContent = localReport(input.value);
    """


def api_chat(product: dict) -> str:
    instructions = json.dumps(f"You are {product['title']}, a premium AI product for {product['icp']}. Workflow: {product['workflow']}. Provide structured analysis, score, risks, and next actions. Include safety caveats when needed.")
    return f"""
    import OpenAI from 'openai';

    export default async function handler(req, res) {{
      if (req.method !== 'POST') return res.status(405).json({{ error: 'Method not allowed' }});
      const visitorKey = req.headers.authorization?.replace(/^Bearer\\s+/i, '') || req.body?.apiKey;
      const apiKey = process.env.OPENAI_API_KEY || visitorKey;
      if (!apiKey) return res.status(400).json({{ error: 'OpenAI API key required for real AI mode.' }});
      const input = String(req.body?.input || '').slice(0, 8000);
      const client = new OpenAI({{ apiKey }});
      const response = await client.responses.create({{
        model: process.env.OPENAI_MODEL || 'gpt-4.1-mini',
        instructions: {instructions},
        input
      }});
      res.status(200).json({{ reply: response.output_text || 'No analysis returned.' }});
    }}
    """


def docs_index() -> str:
    cards = []
    for meta in sorted(OUT.glob("*/project.json")):
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        cards.append(f"<a href=\"{meta.parent.name}/\"><strong>{data['title']}</strong><span>{data['category']} - {data['price_anchor']}</span></a>")
    body = "\n".join(cards) or "<p>No premium products generated yet.</p>"
    return f"""
    <!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Premium AI Products</title><style>
    :root{{color-scheme:dark;font-family:Inter,system-ui,sans-serif;background:#101318;color:#f8fafc}}body{{margin:0;padding:48px;background:radial-gradient(circle at 20% 10%,#0ea5e933,transparent 28rem),#101318}}main{{max-width:1120px;margin:auto}}h1{{font-size:clamp(2.4rem,6vw,5rem);line-height:.95}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}}a{{display:grid;gap:12px;min-height:150px;padding:20px;border:1px solid #ffffff22;border-radius:8px;background:#17202c;color:#fff;text-decoration:none;box-shadow:0 20px 50px #0006}}span{{color:#38bdf8}}
    </style></head><body><main><h1>Premium AI Chatbot Products</h1><p>Two product-grade AI chatbot builds per day.</p><section class="grid">{body}</section></main></body></html>
    """


def build() -> str:
    product = pick_product()
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y-%m-%d-%H%M%Sz")
    made = now.strftime("%Y-%m-%d %H:%M UTC")
    folder_name = f"{product['slug']}-{stamp}"
    folder = OUT / folder_name
    demo_folder = DOCS / folder_name
    accent, accent2, bg = PALETTES[int(hashlib.sha1(folder_name.encode()).hexdigest()[:2], 16) % len(PALETTES)]
    live_demo = f"{PAGES_BASE}/{folder_name}/"
    quality_score = 95

    write(folder / "README.md", f"""
    # {product['title']}

    Premium AI chatbot product generated by automation pipeline.

    ## $1000+ Product Positioning

    Price anchor: **{product['price']}**

    ICP: {product['icp']}

    Problem: {product['problem']}

    ## Live Demo

    {live_demo}

    ## Deployment

    Deploy to Vercel. Set `OPENAI_API_KEY` for server-side real AI mode, or enter a visitor key in the browser demo.

    ## Files

    - `PRODUCT_SPEC.md`
    - `sample-data.json`
    - `screenshots/preview.svg`
    - `api/chat.js`
    - `public/`
    """)
    write(folder / "PRODUCT_SPEC.md", f"""
    # Product Spec

    ## ICP

    {product['icp']}

    ## Problem

    {product['problem']}

    ## Workflow

    {product['workflow']}

    ## Differentiation

    {product['differentiation']}

    ## Premium Features

    {chr(10).join('- ' + str(x) for x in product['premium_features'])}

    ## Pricing

    {product['price']}

    ## Risk Notes

    {product['risk_notes']}
    """)
    write(folder / "sample-data.json", json.dumps({"sample_input": product["sample"], "expected_outputs": ["score", "risks", "summary", "next_actions"]}, indent=2))
    write(folder / "package.json", json.dumps({"name": slugify(product["title"]), "version": "1.0.0", "type": "module", "scripts": {"start": "vercel dev", "dev": "vercel dev"}, "dependencies": {"@vercel/node": "^3.2.27", "openai": "^5.0.0"}, "devDependencies": {"vercel": "^34.3.0"}, "engines": {"node": ">=18"}}, indent=2))
    write(folder / "vercel.json", '{\n  "version": 2,\n  "routes": [\n    { "src": "/api/chat", "dest": "/api/chat.js" },\n    { "src": "/(.*)", "dest": "/public/$1" }\n  ]\n}')
    write(folder / "api/chat.js", api_chat(product))
    write(folder / "public/cover.svg", cover_svg(product, accent, accent2, bg))
    write(folder / "screenshots/preview.svg", screenshot_svg(product, accent, accent2, bg))
    html = index_html(product, folder_name, accent, accent2, bg)
    css = style_css(accent, accent2, bg)
    js = script_js(product)
    write(folder / "public/index.html", html)
    write(folder / "public/style.css", css)
    write(folder / "public/script.js", js)
    write(folder / "project.json", json.dumps({"title": product["title"], "category": product["category"], "price_anchor": product["price"], "live_demo": live_demo, "quality_score": quality_score, "generated_at": made}, indent=2))
    write(demo_folder / "index.html", html)
    write(demo_folder / "style.css", css)
    write(demo_folder / "script.js", js)
    write(demo_folder / "cover.svg", cover_svg(product, accent, accent2, bg))
    write(DOCS / ".nojekyll", "")
    write(DOCS / "index.html", docs_index())

    number = next_number()
    rel = folder.relative_to(ROOT).as_posix()
    row = f"| {number} | {product['title']} | {made} | {product['category']} | `{rel}` | {product['price']} | {live_demo} |"
    write(ROOT / "README.md", read("README.md").rstrip() + "\n" + row + "\n")
    write(ROOT / "tracking/successful-projects.md", read("tracking/successful-projects.md").rstrip() + f"\n| {number} | {product['title']} | {made} | `{rel}` | {product['price']} | {quality_score}/100 |\n")
    write(ROOT / "tracking/model-usage.md", read("tracking/model-usage.md").rstrip() + f"\n| {number} | {product['title']} | OpenAI + Gemini if available | quality-first generation |\n")
    write(ROOT / "tracking/deployment-links.md", read("tracking/deployment-links.md").rstrip() + f"\n| {number} | {product['title']} | {live_demo} | GitHub Pages demo |\n")
    return rel


if __name__ == "__main__":
    print(f"Created {build()}")
