# PromptShield — Tool-First Build Roadmap (4 Months)
### Build an AI security gateway while learning real cybersecurity tools — not tutorials

> **One-liner:** *Cloudflare for LLMs* — a layer between an app and its AI model that inspects every prompt and response in real time to block prompt injection, jailbreaks, and data exfiltration.

---

## Your starting point (so this roadmap fits *you*)

| Area | Your level | What this roadmap does about it |
|------|-----------|-------------------------------|
| Auth/authz, CIA, web-attack theory | Solid basics | Reinforces by *exploiting*, not re-defining |
| Hands-on pentest tools | Beginner (3 THM rooms) | **Core focus** — you'll run real tools weekly |
| SIEM / Wazuh | Some exposure | Made central — Wazuh becomes your monitoring brain |
| Python | Intermediate | Used heavily; comfortable enough |
| SQL / dashboards (Power BI, Tableau, pandas) | Intermediate | Your superpower — drives the analytics layer |
| ML (training models) | New | Taught carefully in Phase 2 with guardrails |
| Prompt injection / AI security | Basic awareness | The whole project turns this into deep expertise |
| Time | 14 hrs/week, 4th-yr B.Tech | Plan = **16 weeks**, paced for 14 hrs |

---

## The core principle of this roadmap

**You are NOT here to learn full-stack coding.** Claude Code builds the app; Claude Design builds the UI. Your time goes to the thing that gets you *hired in security*:

> **Claude Code writes the code. You attack it, measure it, and defend it — using the same tools professional security engineers use.**

Every phase has three parts:
- 🔧 **Tool Lab** — a real security tool you learn hands-on by pointing it at *your own* project.
- 🤖 **What Claude builds** — the code you direct (don't hand-write; *review and understand* it).
- 🧠 **What YOU must own** — the security concepts you must be able to explain in an interview.

You learn a tool by *using it against a system you built and understand* — that's the opposite of consuming a tutorial.

---

## The security tools you'll actually master (your resume's tools section)

| Tool | What it is | Where you use it |
|------|-----------|------------------|
| **Burp Suite** | Intercepting proxy (industry standard) | Phase 1 — inspect/replay traffic through your gateway |
| **garak** | NVIDIA's LLM vulnerability scanner | Phase 0 & 2 — scan your victim app for AI flaws |
| **OWASP ZAP** | Web app vulnerability scanner | Phase 1 — DAST scan your gateway |
| **Nmap / Wireshark** | Network mapping & packet analysis | Phase 0 — understand what a proxy really sees |
| **LLM Guard** (Protect AI) | Open-source input/output scanners | Phase 2 — study it, then build your own engine |
| **Rebuff** | Prompt-injection detector | Phase 2 — reference for layered detection |
| **promptfoo** | LLM red-teaming & evaluation | Phase 2 & 4 — measure your detection accuracy |
| **PyRIT** (Microsoft) | AI red-teaming framework | Phase 4 — automated attacks on your defended app |
| **Wazuh** | SIEM / SOC platform | Phase 3 — ingest PromptShield logs, write detection rules |
| **Kali Linux** | Pentest OS | Throughout — your attack workstation |

> Being able to say *"I've used Burp, garak, PyRIT, promptfoo and Wazuh on a real project"* puts you ahead of most fresher security applicants instantly.

---

## Phases at a glance

| Phase | Weeks | Theme | You walk away knowing |
|-------|-------|-------|----------------------|
| 0 | 1–2 | Attacker mindset + tooling setup | How to break an LLM app with real tools |
| 1 | 3–5 | Gateway + intercept/scan it | Proxies, Burp, ZAP, traffic analysis |
| 2 | 6–10 | Detection engine + AI-sec tools | LLM Guard, garak, promptfoo, basic ML |
| 3 | 11–13 | Wazuh SIEM + analytics dashboard | SOC monitoring, detection rules, data viz |
| 4 | 14–15 | Output guardrails + red-team it | PyRIT, output defense, hardening |
| 5 | 16 | Deploy + portfolio | Shipping, documenting, selling it |

---

# PHASE 0 — Attacker Mindset & Tool Setup
**Weeks 1–2 · You can't defend what you can't break.**

Before any building, learn to *attack* an LLM app with real tools. This makes everything after it click.

### 🔧 Tool Lab
- **Set up Kali Linux** (VM or WSL2). Your attack box for the whole project.
- **Install & run garak** against any public LLM or a local one — watch an automated AI vulnerability scanner work. Read its report; learn the vocabulary (jailbreak, encoding attacks, prompt leaking).
- **Nmap + Wireshark warm-up**: map a target, capture HTTP traffic. You're learning what a gateway sits in the middle of.

### 🤖 What Claude builds
- A deliberately **vulnerable victim app ("ShopBot")** — a naive LLM chatbot with a secret system prompt and a fake admin discount code. This is your permanent attack target and demo centerpiece.

### 🧠 What YOU must own
- Read the **OWASP Top 10 for LLMs** end to end — it's your project spec and interview script.
- Understand **direct vs. indirect prompt injection** and the **"lethal trifecta"** (untrusted input + private data access + exfiltration channel).
- Write a **one-page threat model** in the repo (rare and impressive — most students skip it).

### ✅ Milestone
You attack ShopBot by hand *and* with garak, make it leak its system prompt, and you've documented the threats you'll defend. You've *seen* the enemy.

---

# PHASE 1 — The Gateway, and Tools to Probe It
**Weeks 3–5 · Ship the proxy; learn the tools that inspect it.**

Claude Code builds a working gateway fast. Your job: understand the request flow deeply enough to attack and scan it — using the tools real AppSec engineers use daily.

### 🔧 Tool Lab
- **Burp Suite** (the big one): route your gateway's traffic through Burp. Intercept requests, modify prompts mid-flight, replay attacks with Repeater, fuzz with Intruder. *This is the #1 tool in web security job descriptions — spend real time here.*
- **OWASP ZAP**: run an automated DAST scan against your gateway; read the findings.

### 🤖 What Claude builds
- A **FastAPI gateway**: `/v1/chat` endpoint → forwards prompts to a real LLM → returns the answer (the passthrough).
- A **heuristic shield** (layer 1): regex/rules for known jailbreak strings, base64 blobs, instruction-override language → block + log to PostgreSQL.
- **API-key auth** so only authorized apps use the gateway.

### 🧠 What YOU must own
- How a **reverse proxy / gateway / WAF** works and why it's the right pattern here.
- Why heuristics are fast but brittle (you'll *see* Burp bypass them).
- How to read your own logs to spot an attack.

### ✅ Milestone
ShopBot's traffic runs through PromptShield. You block hand-attacks **and** demonstrate — via Burp — both what gets caught and what slips past layer 1 (motivating Phase 2). A complete, demoable product exists.

---

# PHASE 2 — The Detection Engine (the technical heart)
**Weeks 6–10 · Study the pro AI-security tools, then build your own engine — and learn just enough ML.**

This is your strongest interview material and where you grow the most. The lesson: **defense-in-depth** — cheap checks first, expensive checks only when needed. *Five weeks because the ML is new to you — that's intentional.*

### 🔧 Tool Lab
- **LLM Guard** (Protect AI): install it, run its input/output scanners on ShopBot. **Read how its prompt-injection scanner works** — you're studying a production guardrail, then building your own informed version (this is "learn the tool," not "import the tool and stop thinking").
- **Rebuff**: see a second detection approach for contrast.
- **promptfoo**: set up an eval that throws an attack dataset at your detection engine and **scores accuracy** — your numbers for the README and interviews.

### 🤖 What Claude builds (you direct + tune)
- **Layer 2 — ML classifier** (Weeks 6–8): embed prompts (`sentence-transformers`), train a classifier on a public **prompt-injection dataset** (HuggingFace). *You* own the evaluation: confusion matrix, precision vs. recall, the false-positive tradeoff.
- **Layer 3 — LLM-as-judge** (Weeks 9–10): for ambiguous cases only, escalate to a model that returns `{verdict, category, reason}`.
- **The orchestrator**: runs layers in cost order, short-circuits when confident — the "smart routing" that signals engineering maturity.

### 🧠 What YOU must own
- Embeddings, what a classifier is doing, and **why false positives matter** (blocking real users is a failure too).
- When to use a cheap check vs. an expensive LLM call (latency/cost tradeoff — gold in interviews).
- Your engine's **measured accuracy** vs. LLM Guard's, from promptfoo.

### ✅ Milestone
PromptShield catches *novel* attacks, categorizes and explains them, and you can quote real accuracy numbers comparing your engine to a production tool.

---

# PHASE 3 — Wazuh SIEM + Security Analytics
**Weeks 11–13 · Turn logs into a SOC. This is where your data skills + Wazuh exposure shine.**

Most projects stop at "it blocks stuff." You'll build the *monitoring and analytics* layer — the blue-team skillset that maps to SOC analyst and security data analyst roles (your two target jobs).

### 🔧 Tool Lab
- **Wazuh** (you've touched it — now go deep): forward PromptShield's security logs into Wazuh. **Write custom detection rules** (e.g., alert on repeated injection attempts from one API key). Build **Wazuh dashboards** for attack trends. This is genuine SOC work and a rare portfolio piece.

### 🤖 What Claude builds (you design the metrics)
- Analytics API: attacks over time, breakdown by category, top-targeted endpoints, per-app **risk score**, false-positive rate.
- A **React + Tailwind dashboard** (Claude Design) reading those endpoints — overview, attack explorer with the LLM explanations, headline security score, time-series charts.

### 🧠 What YOU must own (your strength — lead here)
- Which **SQL aggregations** answer which security question (`GROUP BY`, time bucketing).
- Which **chart** communicates which threat — you already know this from Power BI/Tableau.
- How a SIEM alerting pipeline works end to end.

### ✅ Milestone
Two views of the same data: a polished product dashboard *and* a Wazuh SOC view with custom rules firing on attacks. You can demo both — full-stack + data analysis + SOC monitoring in one screen.

---

# PHASE 4 — Output Guardrails & Red-Teaming Your Own App
**Weeks 14–15 · Defend the response side, then attack everything you built with pro red-team tools.**

### 🔧 Tool Lab
- **PyRIT** (Microsoft's AI red-teaming framework): run automated, multi-turn attacks against your *defended* app. Find what still gets through. This is cutting-edge AI-security tooling — naming it in interviews turns heads.
- **promptfoo red-team mode**: a second automated adversary for coverage.

### 🤖 What Claude builds
- **Output scanner**: inspect the model's reply before returning it — block/redact leaked system prompts, PII, API keys, fake credentials (the lethal-trifecta defense most projects miss).
- **Hardening**: rate limiting per key, input size limits, hashed API keys, sanitized errors.
- A **test suite + GitHub Actions CI** (green badges on your repo = visible professionalism).

### 🧠 What YOU must own
- Why output filtering matters as much as input filtering.
- How PII/secret detection works (regex + entropy for high-entropy strings).
- What PyRIT found that you *didn't* expect — and how you fixed it (a great story).

### ✅ Milestone
Both directions defended, app survives an automated red-team pass, repo has passing CI. You'd show this to a senior engineer without flinching.

---

# PHASE 5 — Deploy, Document & Convert to Job Offers
**Week 16 · A project nobody can see or understand doesn't get you hired. Non-negotiable.**

### 🔧 Tool Lab
- **Docker**: containerize the gateway + dashboard.
- Deploy to **Railway/Render/Fly.io** with a live public URL + managed Postgres.

### 🤖 What Claude builds
- A **README that sells**: one-liner, the *prompt-injection-is-the-new-SQLi* analogy, architecture diagram, your accuracy numbers, threat-model link, the tools you used.

### 🧠 What YOU must own (do these yourself — they're the hiring signal)
- **The demo GIF** (the money shot): attack ShopBot raw → it leaks → route through PromptShield → blocked → Wazuh + dashboard light up. Put it at the top of the README.
- **A blog post / LinkedIn writeup**: *"I built an AI firewall and red-teamed it with PyRIT and garak — here's what I learned."* In security, writing about your work is half the hiring signal.

### ✅ Milestone
Live URL, polished repo, demo GIF, blog post. Top of your resume; you can walk an interviewer through it end to end.

---

## Stretch goals (only if ahead)
- A "scan my app" **red-team-as-a-service** mode (PyRIT under the hood) producing a customer security report.
- Map detections to **MITRE ATLAS** (adversarial-ML framework) — serious credibility.
- Multi-LLM-provider support.

---

## Hireability checklist (revisit each milestone)
- [ ] Explain the project in 2 min to a recruiter (the SQLi analogy).
- [ ] Whiteboard the architecture + the layered detection engine.
- [ ] Quote real numbers: detection accuracy, p95 latency, requests handled.
- [ ] Name the tools you used hands-on: **Burp, garak, LLM Guard, promptfoo, PyRIT, Wazuh**.
- [ ] Threat-model doc in the repo.
- [ ] 30-second demo GIF.
- [ ] A public blog post.
- [ ] Tests + CI passing.

All eight checked = this project carries a fresher interview on its own.

---

## Risks & how to avoid them
1. **Treating Claude's code as a black box.** You don't write it, but you *must* be able to explain every security decision in it. Review every PR-sized chunk.
2. **Skipping Phase 5.** Deployment + docs + demo *is* the project's hiring value, not an afterthought.
3. **Drowning in the ML (Phase 2).** One decent classifier is enough. Use promptfoo to know when it's "good enough" and move on.
4. **The latency trap.** Cheap checks inline, LLM judge only when ambiguous, cache verdicts — then talk about this tradeoff in interviews.
5. **Collecting tools without depth.** Better to *truly* know Burp + garak + Wazuh than to name-drop ten tools shallowly.

---

## Weekly cadence (14 hrs/week)
- **~3 hrs** — Tool Lab: hands-on with the week's security tool against your own app.
- **~7 hrs** — Direct Claude Code to build the feature; review and understand the output.
- **~3 hrs** — Attack / measure / tune: break what you built, record metrics.
- **~1 hr** — Friday dev-log note (these become your blog post and interview stories for free).

> The roadmap is a guide, not a contract. If a phase runs long, cut a stretch goal — never cut Phase 5, and never skip the Tool Lab.
