# Wazuh Integration Design for PromptShield

## 1. Overview

PromptShield is an LLM security gateway designed to detect and block common prompt-injection attempts before they reach the downstream ShopBot application.

The current implementation uses a heuristic security layer and stores request and security-event information in PostgreSQL.

Wazuh is considered a **proposed future SIEM integration** for centralized security monitoring and alerting. Wazuh was not deployed in the current PromptShield development environment.

---

## 2. Current Security Pipeline

The implemented architecture is:

```text
User
  |
  v
PromptShield Gateway
  |
  v
Heuristic Shield
  |
  +---- BLOCK ----> PostgreSQL request_logs
  |
  +---- ALLOW ----> ShopBot
                         |
                         v
                    PostgreSQL logs
```

The heuristic layer currently identifies categories including:

* `heuristic:jailbreak`
* `heuristic:extraction`
* `heuristic:social_engineering`
* `heuristic:base64`

Blocked requests are recorded in the PostgreSQL logging system.

---

## 3. Proposed Wazuh Architecture

A future Wazuh deployment could consume PromptShield security events and provide centralized monitoring.

```text
                    PromptShield
                         |
                         v
                  PostgreSQL Logs
                         |
                         v
                 Wazuh Agent / Log
                    Collection
                         |
                         v
                   Wazuh Manager
                         |
                  Custom Detection
                       Rules
                         |
                         v
                  Security Alerts
                         |
                         v
                  Wazuh Dashboard
```

The proposed integration would allow PromptShield events to be correlated with other security telemetry.

---

## 4. Events Suitable for Monitoring

The following PromptShield events could be monitored by Wazuh:

| Event                            | Meaning                                                    | Suggested Severity |
| -------------------------------- | ---------------------------------------------------------- | -----------------: |
| `heuristic:jailbreak`            | Possible attempt to bypass model restrictions              |               High |
| `heuristic:extraction`           | Attempt to obtain system instructions or hidden prompts    |               High |
| `heuristic:social_engineering`   | Attempt to impersonate an administrator or trusted role    |        Medium/High |
| `heuristic:base64`               | Encoded content potentially used to evade simple detection |             Medium |
| Repeated blocked requests        | Possible automated attack activity                         |               High |
| High block rate from one API key | Possible abuse of an authenticated client                  |               High |

Severity would ultimately depend on the organization's detection policy and surrounding evidence.

---

## 5. Example Detection Logic

A future Wazuh rule set could conceptually contain rules such as:

```xml
<group name="promptshield,">

  <rule id="100100" level="10">
    <match>heuristic:jailbreak</match>
    <description>PromptShield detected a possible jailbreak attempt</description>
  </rule>

  <rule id="100101" level="10">
    <match>heuristic:extraction</match>
    <description>PromptShield detected a possible prompt extraction attempt</description>
  </rule>

  <rule id="100102" level="8">
    <match>heuristic:social_engineering</match>
    <description>PromptShield detected possible social engineering</description>
  </rule>

  <rule id="100103" level="7">
    <match>heuristic:base64</match>
    <description>PromptShield detected possible encoded input</description>
  </rule>

</group>
```

These are **illustrative detection rules**, not rules currently deployed in Wazuh.

A production implementation would first define the exact PromptShield log format and then configure the appropriate Wazuh decoder and rule structure.

---

## 6. Possible Security Correlation

Wazuh could provide additional detection by correlating multiple PromptShield events.

For example:

```text
Client/API Key
      |
      +--> jailbreak
      |
      +--> extraction
      |
      +--> social_engineering
      |
      +--> repeated blocked requests
                    |
                    v
             Possible Abuse
                    |
                    v
              Wazuh Alert
```

This could help distinguish an isolated blocked request from sustained attack activity.

Possible future correlation signals include:

* repeated blocked prompts from the same API key
* repeated attacks within a short time period
* multiple attack categories from one client
* unusual increases in blocked-request rate
* correlation with network or host security events

---

## 7. Expected Wazuh Results

If deployed, the integration could provide alerts similar to:

```text
HIGH
PromptShield detected jailbreak attempt

Source/API Key: <authenticated client>
Detection: heuristic:jailbreak
Action: blocked
```

Another example:

```text
HIGH
Repeated PromptShield security violations

Detection categories:
- heuristic:jailbreak
- heuristic:extraction
- heuristic:social_engineering

Action:
Investigate source and review associated requests.
```

These examples describe **expected future monitoring results**, not results produced by a Wazuh deployment in this project.

---

## 8. Relationship with the Analytics Component

PromptShield already includes an analytics component:

```text
PostgreSQL
    |
    v
analytics/dashboard.py
    |
    v
Security Analytics
```

The proposed Wazuh integration would complement this rather than replace it.

The analytics dashboard is intended for application-level analysis of PromptShield events, while Wazuh could provide centralized SIEM monitoring, alerting, and correlation with other security telemetry.

---

## 9. Current Implementation Status

| Component                   | Status       |
| --------------------------- | ------------ |
| PromptShield Gateway        | Implemented  |
| Heuristic Shield            | Implemented  |
| PostgreSQL Security Logging | Implemented  |
| Security Analytics Code     | Implemented  |
| Burp Suite Testing          | Completed    |
| OWASP ZAP Testing           | Completed    |
| Wazuh Agent                 | Not deployed |
| Wazuh Manager               | Not deployed |
| Custom Wazuh Rules          | Proposed     |
| Wazuh Dashboard             | Not deployed |

Therefore, this document should be interpreted as an **integration design and future implementation plan**, not evidence of a deployed Wazuh environment.

---

## 10. Future Implementation Steps

If additional infrastructure becomes available, the proposed implementation would be:

1. Deploy Wazuh Manager and the required components.
2. Configure a Wazuh agent or suitable log-collection mechanism.
3. Define a stable PromptShield security-event format.
4. Configure a Wazuh decoder for PromptShield events.
5. Add custom Wazuh detection rules.
6. Test jailbreak, extraction, social-engineering, and encoded-input events.
7. Validate alert severity and event correlation.
8. Create Wazuh dashboard visualizations.
9. Document the resulting alerts and test evidence.

---

## 11. Conclusion

PromptShield currently provides the core LLM security gateway, heuristic prompt-injection detection, PostgreSQL security logging, and analytics functionality.

Wazuh is documented as a **proposed SIEM integration** that could extend the project with centralized security monitoring, alerting, and event correlation.

The current project does not claim a live Wazuh deployment.
