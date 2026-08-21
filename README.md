<div align="center">

# 🛡️ PromptShield
### An LLM Security Gateway — Detect, Block, and Log Prompt Injection in Real Time

*Cloudflare-style security layer for AI applications, built to defend against the OWASP Top 10 for LLMs.*

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Gateway-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Logging-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?style=flat-square)](https://ollama.com/)
![Status](https://img.shields.io/badge/Status-Active%20Development-yellow?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

**[Threat Model](THREAT_MODEL.md)** · **[Burp Findings](docs/burp-findings.md)** · **[ZAP Findings](docs/zap_findings.md)** · **[Wazuh Design](docs/wazuh-integration.md)**

</div>

---

## 🎯 The Problem

Prompt injection is the new SQL injection — except most LLM-powered apps ship with **zero protection** against it. A single crafted message can leak system prompts, bypass safety rules, or extract data the app was never meant to expose.

**PromptShield** sits between a client and its LLM backend, inspecting every request before it reaches the model — blocking known attack patterns, authenticating clients, and logging every security event for analysis.

---

## 🧪 Built By Attacking First

Before writing a single line of defense, this project attacked a deliberately vulnerable chatbot (**ShopBot**) using the same tools professional AppSec engineers use:

| Tool | Purpose | Evidence |
|---|---|---|
| 🔴 **Burp Suite** | Intercept, modify, and replay attack traffic | [`docs/burp-findings.md`](docs/burp-findings.md) |
| 🟠 **OWASP ZAP** | Automated DAST scan of the gateway | [`docs/zap_findings.md`](docs/zap_findings.md) |
| 🟡 **garak** | NVIDIA's LLM vulnerability scanner | [`attack_notes.md`](attack_notes.md) |
| 🔵 **Manual testing** | Hand-crafted jailbreaks, extraction, social engineering | [`attack_notes.md`](attack_notes.md) |

That research directly shaped the detection engine below — every rule blocks something that was proven to work first.

---

## 🏗️ Architecture

```text
                          User / Client
                                │
                                ▼
                    ┌───────────────────────┐
                    │  PromptShield Gateway │
                    │   FastAPI  ·  :9000   │
                    │  API-key auth (SHA256)│
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Heuristic Shield    │
                    │────────────────────────│
                    │ ⚡ Jailbreak            │
                    │ ⚡ Prompt Extraction    │
                    │ ⚡ Social Engineering   │
                    │ ⚡ Base64-encoded       │
                    └─────────┬─────────────┘
                              │
                     ┌────────┴────────┐
                     ▼                 ▼
                 🚫 BLOCK           ✅ ALLOW
                     │                 │
                     ▼                 ▼
              ┌─────────────┐   ┌─────────────┐
              │ PostgreSQL  │   │   ShopBot   │
              │request_logs │   │  (Ollama)   │
              └──────┬──────┘   └─────────────┘
                     │
                     ▼
          ┌───────────────────────┐
          │  Security Analytics   │
          │  analytics/dashboard  │
          └───────────────────────┘
```

---

## ✨ What It Actually Does

<table>
<tr>
<td width="50%" valign="top">

### 🛡️ Detection Engine
Regex-based heuristic layer catching:
- Direct instruction override
- System prompt extraction
- DAN-style jailbreaks
- Base64-encoded payloads
- Social-engineering / fake-authority prompts

Every block is categorized and logged — not just allow/deny.

</td>
<td width="50%" valign="top">

### 🔐 Gateway Security
- API-key authentication on every request
- Keys stored as SHA-256 hashes, never plaintext
- Full request/response audit trail in PostgreSQL
- Clean separation between the gateway and the vulnerable target app

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📊 Security Analytics
`analytics/dashboard.py` surfaces:
- Total / allowed / blocked requests
- Block rate
- Attack category breakdown
- Recent security events

</td>
<td width="50%" valign="top">

### 🔎 Tested Like a Real Target
- Burp Suite: intercept, tamper, replay
- OWASP ZAP: automated web-security scan
- Formal threat model mapped to OWASP LLM Top 10
- Documented SIEM design for Wazuh (proposed, not yet deployed — see below)

</td>
</tr>
</table>

---

## 📂 Project Structure

```text
PromptShield/
├── analytics/
│   └── dashboard.py               # Security analytics
│
├── docs/
│   ├── burp-findings.md           # Burp Suite attack log
│   ├── zap_findings.md            # OWASP ZAP scan results
│   ├── wazuh-integration.md       # Proposed SIEM design
│   └── roadmap.md
│
├── promptshield-gateway/
│   ├── layers/
│   │   └── heuristic.py           # Detection engine
│   ├── main.py                    # FastAPI gateway
│   └── requirements.txt
│
├── shopbot/
│   └── main.py                    # Vulnerable target app (Ollama)
│
├── THREAT_MODEL.md
├── attack_notes.md
└── owasp-notes.md
```

---

## 🚦 Implementation Status

Built to be honest about what's real vs. what's designed — a distinction that matters in security engineering.

| Layer | Status |
|---|:---:|
| Vulnerable ShopBot + Ollama | ✅ |
| FastAPI Gateway + API-key auth | ✅ |
| SHA-256 key hashing | ✅ |
| PostgreSQL security logging | ✅ |
| Heuristic Shield (jailbreak / extraction / social eng / base64) | ✅ |
| Threat model (OWASP LLM Top 10) | ✅ |
| Burp Suite testing | ✅ |
| OWASP ZAP testing | ✅ |
| Security analytics dashboard | ✅ |
| Wazuh SIEM — design documented | 🟡 Proposed |
| Wazuh SIEM — deployed | ⏸️ Planned |
| ML classifier | ⏸️ v2 |
| LLM-as-judge | ⏸️ v2 |
| Output guardrails | ⏸️ v2 |
| React dashboard | ⏸️ v2 |
| PyRIT automated red-teaming | ⏸️ v2 |
| Docker + CI/CD | ⏸️ v2 |

---

## 🔮 Roadmap — What's Next

```text
v1 (current)          v2 (planned)
─────────────         ─────────────────────────
Heuristics       →    + ML classifier
                       + LLM-as-judge (ambiguous cases)
                       + Output guardrails (leak/PII detection)
                       + Live Wazuh deployment
                       + React security dashboard
                       + PyRIT automated red-teaming
                       + Docker + CI/CD
```

---

## ⚠️ Known Limitations

Documented deliberately, not hidden:

1. Detection is heuristic-based — novel/obfuscated attacks can bypass it (this is what Layer 2 ML would catch, planned for v2).
2. Wazuh integration is **designed**, not deployed — see [`docs/wazuh-integration.md`](docs/wazuh-integration.md).
3. No output-side filtering yet — only inbound prompts are inspected.
4. Built and tested as a local research environment, not production-hardened.

---

## 🧠 Why This Project

Most student security projects stop at "I built a chatbot." PromptShield instead asks: **how would a real attacker break this, and how do you build defense-in-depth against it?**

Every component here was built by attacking first, documenting the threat model second, and only then writing the defense — the same workflow used by AppSec and detection-engineering teams in industry.

---
## ⚠️ Security Disclaimer

ShopBot is intentionally vulnerable and is included only as a controlled attack target for this project.

Do not expose the ShopBot application or its intentionally vulnerable configuration to the public internet.

---
<div align="center">

## 👤 Author

**Annanya Oberoi**
B.Tech Computer Science & Engineering — AI & ML

[GitHub](https://github.com/annanyaoberoi) · Open to Security / SOC Analyst roles

</div>
