"""
Tests for OmniDev Universe extended components:
- awesome-selfhosted parsing
- developer-roadmap parsing
- SQLite DB & FTS5 full-text search
- SaaS alternative search matching
- Self-hosted Docker Compose generator & launcher
"""

import sqlite3
import pytest
from pathlib import Path
from scripts.index_dev_universe import parse_awesome_selfhosted, parse_developer_roadmaps, DB_PATH
from scripts.search_dev_universe import search
from scripts.selfhosted_launcher import STACKS, generate_stack

BASE_DIR = Path(__file__).resolve().parent.parent

def test_selfhosted_readme_parsing():
    readme_path = BASE_DIR / "awesome-selfhosted" / "README.md"
    assert readme_path.exists(), "awesome-selfhosted/README.md must exist"

    records = parse_awesome_selfhosted(readme_path, is_non_free=False)
    assert len(records) > 1000, f"Expected >1000 self-hosted records, got {len(records)}"

    # Check known software entries exist
    titles = {r["title"].lower() for r in records}
    assert any("nextcloud" in t for t in titles), "Nextcloud should be present"
    assert any("vaultwarden" in t or "bitwarden" in t for t in titles), "Vaultwarden / Bitwarden should be present"
    assert any("plausible" in t or "umami" in t for t in titles), "Plausible or Umami should be present"

    sample = records[0]
    assert sample["type"] == "self-hosted"
    assert sample["source_repo"] == "awesome-selfhosted"
    assert sample["url"].startswith("http")

def test_selfhosted_nonfree_parsing():
    nonfree_path = BASE_DIR / "awesome-selfhosted" / "non-free.md"
    if nonfree_path.exists():
        records = parse_awesome_selfhosted(nonfree_path, is_non_free=True)
        assert len(records) > 10, f"Expected non-free records, got {len(records)}"
        assert all(r["type"] == "self-hosted-proprietary" for r in records)

def test_developer_roadmaps_parsing():
    roadmaps_dir = BASE_DIR / "developer-roadmap" / "roadmaps"
    assert roadmaps_dir.exists(), "developer-roadmap/roadmaps must exist"

    records = parse_developer_roadmaps(roadmaps_dir)
    assert len(records) >= 80, f"Expected >= 80 roadmaps, got {len(records)}"

    subcats = {r["subcategory"] for r in records}
    assert "backend" in subcats, "Backend roadmap should exist"
    assert "frontend" in subcats, "Frontend roadmap should exist"
    assert any("ai" in s for s in subcats), "AI roadmaps should exist"

def test_sqlite_db_and_fts_queries():
    assert DB_PATH.exists(), f"dev_universe.db must exist at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verify count
    cursor.execute("SELECT COUNT(*) FROM resources")
    total = cursor.fetchone()[0]
    assert total > 9000, f"Expected >9,000 resources in SQLite, got {total}"

    # Verify FTS on self-hosted
    cursor.execute("""
        SELECT r.title, r.type, r.category
        FROM resources r
        WHERE r.id IN (SELECT rowid FROM resources_fts WHERE resources_fts MATCH 'analytics*')
          AND r.type = 'self-hosted'
        LIMIT 5;
    """)
    rows = cursor.fetchall()
    assert len(rows) > 0, "FTS query for self-hosted analytics should return results"

    conn.close()

def test_search_saas_alternatives():
    # Test searching Notion alternative
    results = search(saas="notion", limit=10)
    assert len(results) > 0, "Searching for Notion alternatives should return results"
    for r in results:
        assert r["type"].startswith("self-hosted")

    # Test searching Slack alternative
    results_slack = search(saas="slack", limit=10)
    assert len(results_slack) > 0, "Searching for Slack alternatives should return results"

def test_selfhosted_launcher_stacks_integrity():
    required_keys = ["name", "category", "replaces", "port", "compose", "env_defaults"]
    assert len(STACKS) >= 10, "Should have at least 10 production-ready stacks"

    for key, spec in STACKS.items():
        for rk in required_keys:
            assert rk in spec, f"Stack '{key}' missing required key: {rk}"
        assert isinstance(spec["port"], int), f"Port for '{key}' must be integer"
        assert "services:" in spec["compose"], f"Compose for '{key}' must contain 'services:'"

def test_selfhosted_launcher_generate(tmp_path):
    out_dir = tmp_path / "test_umami"
    generate_stack("umami", out_dir, domain="analytics.example.com", with_caddy=True)

    compose_file = out_dir / "docker-compose.yml"
    env_file = out_dir / ".env"
    caddy_file = out_dir / "Caddyfile"

    assert compose_file.exists(), "docker-compose.yml must be created"
    assert env_file.exists(), ".env must be created"
    assert caddy_file.exists(), "Caddyfile must be created"

    compose_txt = compose_file.read_text(encoding="utf-8")
    assert "umami" in compose_txt
    assert "postgres" in compose_txt

    env_txt = env_file.read_text(encoding="utf-8")
    assert "APP_SECRET=" in env_txt
    assert "POSTGRES_PASSWORD=" in env_txt

    caddy_txt = caddy_file.read_text(encoding="utf-8")
    assert "analytics.example.com" in caddy_txt
    assert "reverse_proxy localhost:3000" in caddy_txt

def test_system_design_primer_ingestion():
    from scripts.index_dev_universe import parse_system_design_primer
    base_dir = Path(__file__).resolve().parent.parent
    sdp_dir = base_dir / "system-design-primer"
    if not sdp_dir.exists():
        pytest.skip("system-design-primer repo not cloned")

    records = parse_system_design_primer(sdp_dir)
    assert len(records) >= 200, f"Expected at least 200 records from SDP, got {len(records)}"

    types = {r["type"] for r in records}
    assert "system-design-solution" in types
    assert "system-design-concept" in types
    assert "ood-solution" in types
    assert "flashcards" in types

    titles = [r["title"] for r in records]
    assert any("Pastebin" in t for t in titles)
    assert any("Twitter" in t for t in titles)
    assert any("Call Center" in t for t in titles)
