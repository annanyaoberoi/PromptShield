# OWASP ZAP DAST Findings

## Project

PromptShield – Phase 1 Security Assessment

Date: July 2026

---

# Scan Targets

## Target 1

ShopBot (Victim Application)

URL

http://localhost:8000

---

## Target 2

PromptShield Gateway

URL

http://localhost:9000/docs

---

# Scan Methodology

Tool Used

- OWASP ZAP 2.17.0

Scan Type

- Traditional Spider
- Passive Scan
- Automated Scan

---

# Target 1 Findings (ShopBot)

## Medium Severity

- Content Security Policy (CSP) Header Not Set
- Missing Anti-Clickjacking Header
- HTTP Only Site

## Low Severity

- X-Content-Type-Options Header Missing
- Timestamp Disclosure

## Informational

- Modern Web Application detected
- Cache Control observations

---

# Target 2 Findings (PromptShield Gateway)

The PromptShield Gateway exposed significantly fewer findings.

Primary observations included security headers that are not yet configured.

## Medium Severity

- Content Security Policy Header Not Set
- Missing Anti-Clickjacking Header

## Low Severity

- X-Content-Type-Options Header Missing

## Informational

- Modern Web Application detected
- Cache related observations

---

# Comparison

| Feature | ShopBot | PromptShield Gateway |
|----------|----------|---------------------|
| Purpose | Vulnerable LLM application | Security Gateway |
| Authentication | None | API Key Authentication |
| Logging | No | PostgreSQL Logging |
| Prompt Inspection | No | Planned (Phase 1 Layer 1) |
| Request Forwarding | Direct | Gateway Controlled |
| Security Headers | Missing | Partially Missing |

---

# Security Analysis

The ShopBot application intentionally exposes a vulnerable surface for testing prompt injection attacks.

The PromptShield Gateway successfully acts as an intermediary between clients and the ShopBot service while enforcing authentication and request logging.

The ZAP scan primarily reported missing HTTP security headers. No critical vulnerabilities were identified during automated scanning.

Future phases will introduce heuristic prompt filtering, machine-learning based detection, and additional HTTP security hardening.

---

# Planned Improvements

- Add Content Security Policy
- Add X-Frame-Options
- Add X-Content-Type-Options
- Add Strict-Transport-Security
- Add Referrer-Policy
- Add Layer 1 Heuristic Prompt Shield
- Integrate LLM Guard
- Integrate Promptfoo
- Add Wazuh monitoring
- Add Output Guardrails

---

# Conclusion

OWASP ZAP was used to perform Dynamic Application Security Testing against both the vulnerable ShopBot application and the PromptShield Gateway.

The assessment confirmed that the gateway is functioning correctly as a reverse proxy with authentication and logging. Remaining findings are primarily HTTP security header improvements, which are scheduled for later development phases.
