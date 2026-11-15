import re
import time
from typing import Tuple, List


class SecurityViolationException(Exception):
    """Raised when a prompt or tool payload violates enterprise safety guardrails."""
    pass


class GuardrailFirewall:
    """Enterprise firewall preventing prompt injection, PII exfiltration, and quota abuse."""

    INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(?:all\s+)?previous\s+instructions", re.IGNORECASE),
        re.compile(r"disregard\s+(?:all\s+)?prior\s+guidelines", re.IGNORECASE),
        re.compile(r"output\s+your\s+system\s+prompt", re.IGNORECASE),
        re.compile(r"reveal\s+(?:the\s+)?confidential\s+instructions", re.IGNORECASE),
        re.compile(r"bypass\s+(?:the\s+)?safety\s+filter", re.IGNORECASE),
        re.compile(r"dan\s+mode\s+enabled", re.IGNORECASE),
    ]

    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    CREDIT_CARD_PATTERN = re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")
    SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

    def __init__(self, token_budget_per_minute: int = 100000):
        self.token_budget_per_minute = token_budget_per_minute
        self.tokens_used_this_minute = 0
        self.current_minute_window = int(time.time() // 60)

    def _check_budget(self, token_estimate: int) -> None:
        now_minute = int(time.time() // 60)
        if now_minute > self.current_minute_window:
            self.current_minute_window = now_minute
            self.tokens_used_this_minute = 0

        if self.tokens_used_this_minute + token_estimate > self.token_budget_per_minute:
            raise SecurityViolationException(
                f"Tenant token budget exceeded: {self.tokens_used_this_minute + token_estimate} > {self.token_budget_per_minute}"
            )
        self.tokens_used_this_minute += token_estimate

    def inspect_prompt(self, prompt: str) -> None:
        """Inspects prompt for adversarial injections, jailbreaks, and budget."""
        token_estimate = max(1, len(prompt.split()))
        self._check_budget(token_estimate)

        for pattern in self.INJECTION_PATTERNS:
            if pattern.search(prompt):
                raise SecurityViolationException(
                    f"Prompt injection detected by enterprise guardrail filter matching: '{pattern.pattern}'"
                )

    def sanitize_input(self, text: str) -> Tuple[str, bool]:
        """Redacts sensitive PII (credit cards, emails, SSNs) with canonical redaction tags."""
        modified = False
        
        if self.EMAIL_PATTERN.search(text):
            text = self.EMAIL_PATTERN.sub("[REDACTED_EMAIL]", text)
            modified = True

        if self.CREDIT_CARD_PATTERN.search(text):
            text = self.CREDIT_CARD_PATTERN.sub("[REDACTED_CARD]", text)
            modified = True

        if self.SSN_PATTERN.search(text):
            text = self.SSN_PATTERN.sub("[REDACTED_SSN]", text)
            modified = True

        return text, modified
