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

def test_unified_database_total_coverage():
    assert DB_PATH.exists(), f"dev_universe.db must exist at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM resources")
    total = cursor.fetchone()[0]
    assert total >= 11000, f"Expected >= 11,000 indexed resources, got {total}"

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
        "project-based-learning"
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
