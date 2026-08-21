# PromptShield — Project Roadmap & Final Status

> **PromptShield** is an LLM security gateway that sits between an application and its AI backend to inspect user prompts, detect common prompt-injection attempts, block suspicious requests, and record security events for analysis.

---

## Project Scope

The original roadmap explored a larger multi-layer AI-security platform involving ML classification, LLM-based judging, Wazuh deployment, automated red teaming, output guardrails, and a frontend dashboard.

The current project intentionally focuses on the **core security gateway and heuristic detection layer**. Additional components are documented as future enhancements rather than being represented as implemented features.

This keeps the repository aligned with the functionality that has actually been built and tested.

---

# Phase 0 — Environment & Security Research

### Status: ✅ Completed

### Completed work

* Kali Linux security testing environment
* Python development environment
* Local Ollama LLM setup
* Deliberately vulnerable ShopBot application
* OWASP LLM security research
* Threat modeling
* Prompt-injection attack research
* garak exploration/testing

### Documentation

* `THREAT_MODEL.md`
* `owasp-notes.md`
* `attack_notes.md`
* `dev-log.md`

---

# Phase 1 — Vulnerable ShopBot

### Status: ✅ Completed

ShopBot acts as the intentionally vulnerable target application.

### Implemented

* FastAPI-based chatbot service
* Local Ollama model integration
* Prompt processing endpoint
* Vulnerable system-prompt scenario
* Fake administrator discount-code scenario
* Direct prompt-injection testing

ShopBot provides the target against which PromptShield can be tested.

---

# Phase 2 — PromptShield Gateway

### Status: ✅ Completed

The PromptShield gateway provides the security boundary between the client and ShopBot.

### Implemented

* FastAPI gateway
* `/v1/chat` endpoint
* `/healthz` endpoint
* API-key authentication
* SHA-256 API-key hashing
* Gateway-to-ShopBot forwarding
* Request timeout handling
* Error handling
* PostgreSQL request logging

### Architecture

```text
Client
  |
  v
PromptShield Gateway
  |
  v
Heuristic Shield
  |
  +---- BLOCK ----> PostgreSQL
  |
  +---- ALLOW ----> ShopBot
                         |
                         v
                       Ollama
```

---

# Phase 3 — Layer 1 Heuristic Security Shield

### Status: ✅ Completed

The first PromptShield detection layer uses lightweight heuristic analysis.

### Implemented detection categories

* `heuristic:jailbreak`
* `heuristic:extraction`
* `heuristic:social_engineering`
* `heuristic:base64`

### Detection flow

```text
Incoming Prompt
      |
      v
Heuristic Inspection
      |
      +---- Suspicious ----> BLOCK
      |                         |
      |                         v
      |                    PostgreSQL
      |
      +---- Safe ----------> ShopBot
```

The heuristic layer returns a structured `ShieldResult` and the gateway records security events.

### Important security property

The heuristic layer is intentionally lightweight and fast, but it is not designed to detect every possible prompt-injection technique.

This limitation motivates future multi-layer detection.

---

# Phase 4 — Security Testing

### Status: ✅ Completed

PromptShield and ShopBot were tested using security-focused tools and manual attack techniques.

### Burp Suite

Completed activities include:

* Request interception
* Prompt modification
* Attack replay
* Security testing of gateway behavior
* Documentation of findings

Documentation:

`docs/burp-findings.md`

### OWASP ZAP

Completed activities include:

* Gateway scanning
* Web-security assessment
* Findings documentation

Documentation:

`docs/zap_findings.md`

### Additional research

Prompt-injection and LLM-security attacks were documented in:

* `attack_notes.md`
* `owasp-notes.md`

---

# Phase 5 — Security Analytics

### Status: ✅ Implemented

PromptShield includes an analytics component for analyzing security events stored in PostgreSQL.

### Analytics component

```text
PostgreSQL
    |
    v
analytics/dashboard.py
    |
    v
PromptShield Security Analytics
```

The dashboard provides application-level security visibility including:

* Total requests
* Allowed requests
* Blocked requests
* Block rate
* Attack categories
* Recent security events
* Recent requests

The analytics component is designed to consume the existing PromptShield PostgreSQL logs.

---

# Phase 6 — Proposed Wazuh Integration

### Status: 🟡 Designed / Documented — Not Deployed

Wazuh was considered as a SIEM layer for centralized monitoring of PromptShield security events.

Due to the resource constraints of the development environment, a full Wazuh deployment was intentionally not performed.

Instead, the proposed architecture and detection strategy are documented in:

`docs/wazuh-integration.md`

### Proposed architecture

```text
PromptShield
     |
     v
PostgreSQL Security Logs
     |
     v
Wazuh Log Collection
     |
     v
Wazuh Manager
     |
     v
Custom Detection Rules
     |
     v
Security Alerts
     |
     v
Wazuh Dashboard
```

### Possible future detections

* Repeated jailbreak attempts
* Repeated prompt-extraction attempts
* Repeated social-engineering attempts
* Encoded-input attacks
* High attack frequency from an API key
* Multiple attack categories from one client

**Important:** Wazuh is not currently deployed in this project. The integration documentation describes a possible future implementation.

---

# Current Core Architecture

The completed core system can be represented as:

```text
                    User / Client
                         |
                         v
                ┌─────────────────┐
                │  PromptShield   │
                │    Gateway      │
                │    :9000        │
                └────────┬────────┘
                         |
                         v
                ┌─────────────────┐
                │ Heuristic Shield│
                └────────┬────────┘
                         |
                ┌────────┴────────┐
                |                 |
              BLOCK             ALLOW
                |                 |
                v                 v
          PostgreSQL           ShopBot
           request_logs          |
                |                v
                |              Ollama
                |
                v
          Analytics
                |
                v
       Security Monitoring
```

---

# Current Repository Status

| Component                    | Status                |
| ---------------------------- | --------------------- |
| Vulnerable ShopBot           | ✅ Implemented         |
| Ollama integration           | ✅ Implemented         |
| FastAPI Gateway              | ✅ Implemented         |
| API-key authentication       | ✅ Implemented         |
| API-key hashing              | ✅ Implemented         |
| PostgreSQL logging           | ✅ Implemented         |
| Heuristic shield             | ✅ Implemented         |
| Jailbreak detection          | ✅ Implemented         |
| Prompt extraction detection  | ✅ Implemented         |
| Social-engineering detection | ✅ Implemented         |
| Base64 detection             | ✅ Implemented         |
| Burp Suite testing           | ✅ Completed           |
| OWASP ZAP testing            | ✅ Completed           |
| Threat model                 | ✅ Completed           |
| Security analytics code      | ✅ Implemented         |
| Wazuh integration design     | 🟡 Proposed           |
| Wazuh deployment             | ⏸️ Not implemented    |
| ML classifier                | ⏸️ Future enhancement |
| LLM-as-judge                 | ⏸️ Future enhancement |
| Output guardrails            | ⏸️ Future enhancement |
| React frontend               | ⏸️ Future enhancement |
| Automated PyRIT red teaming  | ⏸️ Future enhancement |
| Docker deployment            | ⏸️ Future enhancement |
| CI/CD                        | ⏸️ Future enhancement |

---

# Future Enhancements

The following features are intentionally outside the current core implementation:

## Multi-layer Detection

Possible future layers:

1. Heuristic detection
2. ML-based prompt-injection classifier
3. LLM-based judge for ambiguous cases

The layers could be orchestrated based on confidence, latency, and cost.

## Output Guardrails

A future output-security layer could inspect model responses for:

* System-prompt leakage
* API keys
* Credentials
* PII
* Other sensitive information

## Automated Red Teaming

Future testing could include:

* promptfoo
* PyRIT
* expanded garak testing

## SIEM Expansion

The proposed Wazuh integration could be deployed when sufficient infrastructure is available.

## Frontend

A dedicated React-based security dashboard could eventually replace or complement the current analytics component.

## Deployment

The system could eventually be containerized and deployed using Docker and a managed PostgreSQL service.

---

# Final Project Definition

The completed PromptShield core can be described as:

> **An LLM security gateway that uses heuristic prompt-injection detection to inspect and block malicious requests, authenticate clients, log security events in PostgreSQL, and provide security analytics, with a documented design for future SIEM integration through Wazuh.**

The project intentionally distinguishes between **implemented functionality** and **future enhancements**.

This distinction ensures that the repository accurately represents the current implementation and testing evidence.
