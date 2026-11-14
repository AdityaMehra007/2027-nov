import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from tests.test_dev_universe_extended import (
    test_selfhosted_readme_parsing,
    test_selfhosted_nonfree_parsing,
    test_developer_roadmaps_parsing,
    test_sqlite_db_and_fts_queries,
    test_search_saas_alternatives,
    test_selfhosted_launcher_stacks_integrity,
    test_selfhosted_launcher_generate
)

def run():
    print("==================================================")
    print("  RUNNING EXTENDED DEV UNIVERSE TEST SUITE")
    print("==================================================")

    print("[1/7] Testing awesome-selfhosted README parser...")
    test_selfhosted_readme_parsing()
    print("      ✓ PASSED")

    print("[2/7] Testing awesome-selfhosted non-free parser...")
    test_selfhosted_nonfree_parsing()
    print("      ✓ PASSED")

    print("[3/7] Testing developer-roadmap parser...")
    test_developer_roadmaps_parsing()
    print("      ✓ PASSED")

    print("[4/7] Testing SQLite database & FTS5 queries...")
    test_sqlite_db_and_fts_queries()
    print("      ✓ PASSED")

    print("[5/7] Testing SaaS alternative search...")
    test_search_saas_alternatives()
    print("      ✓ PASSED")

    print("[6/7] Testing selfhosted_launcher stacks integrity...")
    test_selfhosted_launcher_stacks_integrity()
    print("      ✓ PASSED")

    print("[7/7] Testing selfhosted_launcher stack generation...")
    with tempfile.TemporaryDirectory() as td:
        test_selfhosted_launcher_generate(Path(td))
    print("      ✓ PASSED")

    print("==================================================")
    print("  ✅ ALL 7 EXTENDED TESTS PASSED PERFECTLY!")
    print("==================================================")

if __name__ == "__main__":
    run()
