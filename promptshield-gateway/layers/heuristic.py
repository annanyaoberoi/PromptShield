import re
from dataclasses import dataclass


@dataclass
class ShieldResult:
    blocked: bool
    reason: str | None = None


JAILBREAK_PATTERNS = [
    r"\bDAN\b",
    r"ignore previous instructions",
    r"you are now",
    r"no restrictions",
    r"act as if",
]

EXTRACTION_PATTERNS = [
    r"repeat your instructions",
    r"what is your system prompt",
    r"print your prompt",
    r"reveal your instructions",
    r"word for word",
]

SOCIAL_PATTERNS = [
    r"system administrator",
    r"for debugging purposes",
    r"I am your creator",
    r"verify your configuration",
    r"store admin",
    r"store administrator",
    r"as the admin",
    r"as an admin",
]


def inspect_prompt(prompt: str) -> ShieldResult:

    # Layer 1a — Jailbreak
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return ShieldResult(
                blocked=True,
                reason="heuristic:jailbreak"
            )

    # Layer 1b — Prompt extraction
    for pattern in EXTRACTION_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return ShieldResult(
                blocked=True,
                reason="heuristic:extraction"
            )

    # Layer 1c — Social engineering
    for pattern in SOCIAL_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return ShieldResult(
                blocked=True,
                reason="heuristic:social_engineering"
            )

    # Layer 1d — Base64 detection
    b64_pattern = r"[A-Za-z0-9+/]{20,}={0,2}"

    if re.search(b64_pattern, prompt):
        return ShieldResult(
            blocked=True,
            reason="heuristic:base64"
        )

    return ShieldResult(
        blocked=False,
        reason=None
    )
