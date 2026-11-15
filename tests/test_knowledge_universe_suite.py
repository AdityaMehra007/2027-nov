"""
Comprehensive Test Suite for OmniDev Universe Knowledge Core
Tests parsing, indexing, full-text search, and dataset integrity across:
- coding-interview-university
- system-design-primer
- 996.ICU
- project-based-learning
- developer-roadmap
- awesome-selfhosted
- free-programming-books
- build-your-own-x
- public-apis
- awesome & awesome-python
"""

import json
import sqlite3
import pytest
from pathlib import Path
from scripts.index_dev_universe import (
    parse_coding_interview_university,
    parse_system_design_primer,
    parse_project_based_learning,
    parse_openclaw,
    parse_opendots,
    parse_developer_roadmaps,
    DB_PATH,
    DATA_DIR
)
from scripts.search_dev_universe import search

BASE_DIR = Path(__file__).resolve().parent.parent

def test_coding_interview_university_parsing():
    ciu_dir = BASE_DIR / "coding-interview-university"
    assert ciu_dir.exists(), "coding-interview-university directory must exist"

    records = parse_coding_interview_university(ciu_dir)
    assert len(records) > 500, f"Expected >500 records from CIU, got {len(records)}"

    types = {r["type"] for r in records}
    assert "interview-prep" in types or "video-lecture" in types, "Should extract interview prep or video lectures"

    titles = " ".join(r["title"].lower() for r in records)
    assert "binary search" in titles or "array" in titles or "tree" in titles, "Should cover core data structures"

def test_system_design_primer_parsing():
    sdp_dir = BASE_DIR / "system-design-primer"
    assert sdp_dir.exists(), "system-design-primer directory must exist"

    records = parse_system_design_primer(sdp_dir)
    assert len(records) > 150, f"Expected >150 records from SDP, got {len(records)}"

    types = {r["type"] for r in records}
    assert any("system-design" in t for t in types), "Should extract system design types"

    # Check key architectures
    titles = " ".join(r["title"].lower() for r in records)
    assert "system design" in titles, "Should extract system design topics"

def test_996_icu_dataset_integrity():
    dataset_file = DATA_DIR / "996_icu_dataset.json"
    assert dataset_file.exists(), f"996.ICU dataset must exist at {dataset_file}"

    with open(dataset_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "blacklisted_companies" in data or "blacklist" in data or "companies" in data or "metadata" in data
    report_file = BASE_DIR / "docs" / "996_ICU_LABOR_RIGHTS_REPORT.md"
    assert report_file.exists(), "996_ICU_LABOR_RIGHTS_REPORT.md must exist in docs/"

def test_project_based_learning_parsing():
    pbl_dir = BASE_DIR / "project-based-learning"
    assert pbl_dir.exists(), "project-based-learning directory must exist"

    records = parse_project_based_learning(pbl_dir)
    assert len(records) > 300, f"Expected >300 records from PBL, got {len(records)}"
    assert all(r["source_repo"] == "project-based-learning" for r in records)

def test_openclaw_parsing():
    openclaw_dir = BASE_DIR / "openclaw"
    assert openclaw_dir.exists(), "openclaw directory must exist"

    records = parse_openclaw(openclaw_dir)
    assert len(records) >= 50, f"Expected >=50 records from OpenClaw, got {len(records)}"
    types = {r["type"] for r in records}
    assert "agent-skill" in types, "Should parse agent skills"

def test_opendots_parsing():
    opendots_dir = BASE_DIR / "OpenDots"
    assert opendots_dir.exists(), "OpenDots directory must exist"

    records = parse_opendots(opendots_dir)
    assert len(records) >= 5, f"Expected >=5 records from OpenDots, got {len(records)}"
    types = {r["type"] for r in records}
    assert any("coworker" in t or "stack" in t for t in types), "Should parse coworker agent concepts or stacks"

def test_developer_roadmap_parsing():
    rd_dir = BASE_DIR / "developer-roadmap" / "roadmaps"
    assert rd_dir.exists(), "developer-roadmap/roadmaps directory must exist"

    records = parse_developer_roadmaps(rd_dir)
    assert len(records) > 30000, f"Expected >30,000 records from developer-roadmap, got {len(records)}"

    types = {r["type"] for r in records}
    assert "roadmap" in types, "Should extract roadmap overviews"
    assert "roadmap-topic" in types, "Should extract roadmap topics"
    assert "article" in types or "official-doc" in types, "Should extract curated learning resources"

    titles = " ".join(r["title"].lower() for r in records)
    assert "claude code" in titles or "ai agent" in titles, "Should cover modern 2026/2027 AI engineering tracks"

def test_unified_database_total_coverage():
    assert DB_PATH.exists(), f"dev_universe.db must exist at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM resources")
    total = cursor.fetchone()[0]
    assert total >= 40000, f"Expected >= 40,000 indexed resources, got {total}"

    cursor.execute("SELECT DISTINCT source_repo FROM resources")
    sources = {row[0] for row in cursor.fetchall()}
    expected_sources = {
        "free-programming-books",
        "build-your-own-x",
        "public-apis",
        "awesome",
        "awesome-python",
        "awesome-selfhosted",
        "developer-roadmap",
        "coding-interview-university",
        "system-design-primer",
        "996.ICU",
        "project-based-learning",
        "openclaw",
        "OpenDots"
    }
    for es in expected_sources:
        assert es in sources, f"Source '{es}' must be present in database"

    conn.close()

def test_cross_repository_search_engine():
    # 1. Search for interview prep
    res_interview = search(query="binary search", limit=5)
    assert len(res_interview) > 0, "Should find binary search resources"

    # 2. Search for system design
    res_sys = search(query="distributed system", limit=5)
    assert len(res_sys) > 0, "Should find distributed system resources"

    # 3. Search for Python
    res_py = search(query="fastapi", limit=5)
    assert len(res_py) > 0, "Should find fastapi resources"

    # 4. Search for OpenClaw skills
    res_claw = search(query="openclaw", limit=5)
    assert len(res_claw) > 0, "Should find openclaw resources"

    # 5. Search for Developer Roadmaps (Claude Code & Vibe Coding)
    res_claude = search(query="claude code", limit=5)
    assert len(res_claude) > 0, "Should find claude code roadmap items"

    res_vibe = search(query="vibe coding", limit=5)
    assert len(res_vibe) > 0, "Should find vibe coding roadmap items"
