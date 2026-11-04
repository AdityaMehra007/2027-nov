import os
import pytest
from omniverse.modules.agency.models import Deliverable
from omniverse.modules.agency.qa_governor import QAGovernor, QAVerificationResult


def test_qa_governor_passes_valid_deliverables(tmp_path):
    governor = QAGovernor()

    # Valid Python file
    py_file = tmp_path / "valid_script.py"
    py_file.write_text("def hello():\n    return 'world'\n", encoding="utf-8")

    # Valid JSON file
    json_file = tmp_path / "valid.json"
    json_file.write_text('{"name": "OMNIVERSE", "version": 1}', encoding="utf-8")

    # Valid HTML file
    html_file = tmp_path / "valid.html"
    html_file.write_text("<!DOCTYPE html><html><head><title>Test</title></head><body><h1>Hello</h1></body></html>", encoding="utf-8")

    deliverables = [
        Deliverable(artifact_name="valid_script.py", artifact_type="CODE", file_path=str(py_file), checksum="abc", size_bytes=30),
        Deliverable(artifact_name="valid.json", artifact_type="CONFIG", file_path=str(json_file), checksum="def", size_bytes=35),
        Deliverable(artifact_name="valid.html", artifact_type="CODE", file_path=str(html_file), checksum="ghi", size_bytes=80),
    ]

    result = governor.verify_deliverables(deliverables)
    assert isinstance(result, QAVerificationResult)
    assert result.passed is True
    assert result.quality_score >= 90.0
    assert len(result.failures) == 0


def test_qa_governor_detects_syntax_errors(tmp_path):
    governor = QAGovernor()

    # Broken Python file
    broken_py = tmp_path / "broken.py"
    broken_py.write_text("def broken(:\n    pass\n", encoding="utf-8")

    deliverables = [
        Deliverable(artifact_name="broken.py", artifact_type="CODE", file_path=str(broken_py), checksum="123", size_bytes=20)
    ]

    result = governor.verify_deliverables(deliverables)
    assert result.passed is False
    assert any("Syntax error" in f for f in result.failures)


def test_qa_governor_detects_hardcoded_secrets(tmp_path):
    governor = QAGovernor()

    # File with leaked live API key
    leaked_file = tmp_path / "leaked_keys.py"
    dummy_key = "sk_" + "live_" + "0" * 24
    leaked_file.write_text(f"STRIPE_API_KEY = '{dummy_key}'\n", encoding="utf-8")

    deliverables = [
        Deliverable(artifact_name="leaked_keys.py", artifact_type="CODE", file_path=str(leaked_file), checksum="999", size_bytes=60)
    ]

    result = governor.verify_deliverables(deliverables)
    assert result.passed is False
    assert any("Leaked secret detected" in f for f in result.failures)
