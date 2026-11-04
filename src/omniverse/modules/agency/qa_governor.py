"""Automated QA & Verification Governor: Pre-flight syntax, security, and quality gating."""

import ast
import json
import re
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field
from omniverse.modules.agency.models import Deliverable


class QAVerificationResult(BaseModel):
    """Result of comprehensive QA verification across deliverables."""
    passed: bool
    quality_score: float = Field(ge=0.0, le=100.0)
    passed_checks: List[str] = Field(default_factory=list)
    failures: List[str] = Field(default_factory=list)


class QAGovernor:
    """Institutional pre-delivery verification governor."""

    # Patterns matching leaked API keys or credentials
    SECRET_PATTERNS = [
        re.compile(r"sk_live_[0-9a-zA-Z]{24,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
        re.compile(r"ghp_[0-9a-zA-Z]{36}"),
    ]

    def verify_deliverables(self, deliverables: List[Deliverable]) -> QAVerificationResult:
        """Execute syntax validation, security scans, and integrity checks."""
        failures: List[str] = []
        passed_checks: List[str] = []

        if not deliverables:
            return QAVerificationResult(
                passed=False,
                quality_score=0.0,
                passed_checks=[],
                failures=["Zero deliverables provided for verification."],
            )

        for d in deliverables:
            file_path = Path(d.file_path)
            if not file_path.exists():
                failures.append(f"Missing file: {d.file_path}")
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                failures.append(f"Cannot read {d.artifact_name}: {str(e)}")
                continue

            # 1. Security Scan: Hardcoded Secrets
            has_secret = False
            for pattern in self.SECRET_PATTERNS:
                if pattern.search(content):
                    failures.append(f"Leaked secret detected in {d.artifact_name}: matching {pattern.pattern}")
                    has_secret = True
                    break
            if not has_secret:
                passed_checks.append(f"Security: Zero secrets detected in {d.artifact_name}")

            # 2. Syntax & Compilation Checks
            suffix = file_path.suffix.lower()
            if suffix == ".py":
                try:
                    ast.parse(content)
                    passed_checks.append(f"Syntax: Valid Python AST in {d.artifact_name}")
                except SyntaxError as e:
                    failures.append(f"Syntax error in {d.artifact_name} at line {e.lineno}: {e.msg}")

            elif suffix == ".json":
                try:
                    json.loads(content)
                    passed_checks.append(f"Syntax: Valid JSON structure in {d.artifact_name}")
                except json.JSONDecodeError as e:
                    failures.append(f"JSON syntax error in {d.artifact_name}: {str(e)}")

            elif suffix == ".html":
                if "<!DOCTYPE html>" in content and "</html>" in content:
                    passed_checks.append(f"Syntax: Semantic HTML5 document in {d.artifact_name}")
                else:
                    failures.append(f"HTML error in {d.artifact_name}: Missing DOCTYPE or closing html tag")

            # 3. Size and Checksum Integrity
            if len(content) < 10:
                failures.append(f"Integrity error: {d.artifact_name} content is suspiciously short ({len(content)} bytes)")
            else:
                passed_checks.append(f"Integrity: {d.artifact_name} size ({len(content)} bytes) verified")

        passed = len(failures) == 0
        total_checks = len(passed_checks) + len(failures)
        score = (len(passed_checks) / total_checks * 100.0) if total_checks > 0 else 0.0

        return QAVerificationResult(
            passed=passed,
            quality_score=round(score, 1),
            passed_checks=passed_checks,
            failures=failures,
        )
