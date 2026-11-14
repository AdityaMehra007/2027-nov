"""
Comprehensive Test Suite for 996.ICU Integration, Analytics, and Licensing Tooling
"""

import os
import sys
import json
import sqlite3
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.anti996_tool import (
    cmd_check,
    cmd_apply,
    cmd_badge,
    cmd_audit_company,
    ANTI_996_FULL_LICENSE,
    ANTI_996_RIDER,
)
from scripts.search_dev_universe import search, DB_PATH


class DummyArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def test_dataset_json_integrity():
    dataset_path = BASE_DIR / "data" / "996_icu_dataset.json"
    assert dataset_path.exists(), "996_icu_dataset.json should exist"

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = data.get("stats", {})
    assert stats.get("active_blacklisted_companies", 0) >= 200
    assert stats.get("whitelisted_wlb_companies", 0) >= 10
    assert stats.get("anti996_licensed_projects", 0) >= 150
    assert stats.get("community_proposals", 0) >= 5

    # Check known companies
    active_bl = data.get("active_blacklist", [])
    pdd = next((c for c in active_bl if "拼多多" in c["company_name"]), None)
    assert pdd is not None, "拼多多 should be in active blacklist"
    assert "11116" in pdd["schedule"] or "996" in pdd["schedule"]

    wl = data.get("whitelist", [])
    ibm = next((c for c in wl if "IBM" in c["company_name"]), None)
    assert ibm is not None, "IBM should be in whitelist"
    assert "9-6-5" in ibm["schedule"]


def test_markdown_report_generated():
    report_path = BASE_DIR / "docs" / "996_ICU_LABOR_RIGHTS_REPORT.md"
    assert report_path.exists(), "996_ICU_LABOR_RIGHTS_REPORT.md should exist"

    text = report_path.read_text(encoding="utf-8")
    assert "Executive Summary" in text
    assert "Labor Law of the PRC" in text
    assert "Active Blacklisted Companies" in text
    assert "Verified 965 / 955 Work-Life Balance Directory" in text
    assert "Anti-996 License Legal Analysis" in text


def test_anti996_tool_badge_generation(capsys):
    args = DummyArgs(style="flat-square")
    ret = cmd_badge(args)
    assert ret == 0
    captured = capsys.readouterr()
    assert "Anti%20996" in captured.out
    assert "996.icu" in captured.out


def test_anti996_tool_audit_company(capsys):
    # Blacklisted entity
    args_bl = DummyArgs(company="拼多多")
    ret_bl = cmd_audit_company(args_bl)
    assert ret_bl == 0
    out_bl = capsys.readouterr().out
    assert "ALERT - BLACKLISTED" in out_bl
    assert "拼多多" in out_bl

    # Whitelisted entity
    args_wl = DummyArgs(company="IBM")
    ret_wl = cmd_audit_company(args_wl)
    assert ret_wl == 0
    out_wl = capsys.readouterr().out
    assert "COMMENDATION - WHITELISTED" in out_wl
    assert "IBM" in out_wl

    # Unknown entity
    args_unk = DummyArgs(company="NonExistentFictionalCorp999")
    ret_unk = cmd_audit_company(args_unk)
    assert ret_unk == 0
    out_unk = capsys.readouterr().out
    assert "No records found" in out_unk


def test_anti996_tool_apply_and_check(tmp_path, capsys):
    project_dir = tmp_path / "my_project"
    project_dir.mkdir()

    license_file = project_dir / "LICENSE"
    readme_file = project_dir / "README.md"

    # Start with standard MIT license
    license_file.write_text("MIT License\n\nCopyright (c) 2026 Test\n", encoding="utf-8")
    readme_file.write_text("# My Project\n\nA great library.\n", encoding="utf-8")

    # Audit before applying
    args_check1 = DummyArgs(path=str(project_dir))
    ret1 = cmd_check(args_check1)
    assert ret1 == 0
    out1 = capsys.readouterr().out
    assert "MIT (Standard)" in out1
    assert "Standard license detected" in out1

    # Apply rider and badges
    args_apply = DummyArgs(
        dest=str(license_file),
        mode="rider",
        holder="Test Org",
        year="2026",
        add_badge=True,
        readme=str(readme_file),
    )
    ret_apply = cmd_apply(args_apply)
    assert ret_apply == 0

    # Verify license file contains rider
    license_content = license_file.read_text(encoding="utf-8")
    assert "ANTI-996 LABOR RIGHTS COMPLIANCE RIDER" in license_content

    # Verify README contains badge
    readme_content = readme_file.read_text(encoding="utf-8")
    assert "996.icu" in readme_content

    # Audit after applying
    args_check2 = DummyArgs(path=str(project_dir))
    ret2 = cmd_check(args_check2)
    assert ret2 == 0
    out2 = capsys.readouterr().out
    assert "Dual/Rider Anti-996" in out2
    assert "COMPLIANT with Anti-996 Ethical Labor Licensing" in out2


def test_dev_universe_database_fts():
    assert DB_PATH.exists(), "dev_universe.db should exist"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT count(*) FROM resources;")
    total = cursor.fetchone()[0]
    assert total >= 11000, f"Expected at least 11,000 resources, got {total}"

    cursor.execute("SELECT count(*) FROM resources WHERE source_repo = '996.ICU';")
    icu_count = cursor.fetchone()[0]
    assert icu_count >= 150, f"Expected at least 150 996.ICU resources, got {icu_count}"

    cursor.execute("SELECT count(*) FROM resources WHERE source_repo = 'project-based-learning';")
    pbl_count = cursor.fetchone()[0]
    assert pbl_count >= 300, f"Expected at least 300 PBL resources, got {pbl_count}"
    conn.close()

    # Test FTS queries via search function
    results_anti = search(query="Anti-996", limit=5)
    assert len(results_anti) > 0, "FTS search for Anti-996 should return matches"

    results_pbl = search(query="Memory Allocator", limit=5)
    assert len(results_pbl) > 0, "FTS search for Memory Allocator should return matches"
