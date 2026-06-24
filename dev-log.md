# Day 2 Development Log

## What Surprised Me

The most surprising observation was that a simple DAN-style jailbreak prompt was accepted by the model without immediate rejection. This showed how easily an attacker can attempt to influence model behavior.

I was also surprised that the model processed Base64 encoded content instead of ignoring it. This demonstrated that encoded attacks can bypass basic keyword-based filtering.

---

## Most Concerning OWASP Risk

The most concerning risk is LLM01: Prompt Injection.

A successful prompt injection attack can completely change how a model behaves and may lead to disclosure of confidential information or bypassing of security controls.

---

## Assumptions That Changed

Before testing, I assumed that large language models would automatically reject most malicious prompts.

After performing manual security tests, I learned that attackers can use roleplay, encoding techniques, and instruction overrides to influence model behavior.

This highlighted the importance of building an additional protection layer such as PromptShield.
