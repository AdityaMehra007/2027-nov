#!/usr/bin/env python3
"""
OmniDev Universe: Lightning CLI Search Engine
Fast full-text search across 10,000+ developer books, self-hosted software, roadmaps, courses, APIs, and code guides.
"""

import sys
import argparse
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "dev_universe.db"
STATS_PATH = DATA_DIR / "dev_universe_stats.json"

COLOR_CYAN = "\033[96m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_GRAY = "\033[90m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

TYPE_BADGES = {
    "book": f"{COLOR_CYAN}[BOOK]{COLOR_RESET}",
    "course": f"{COLOR_GREEN}[COURSE]{COLOR_RESET}",
    "build-project": f"{COLOR_MAGENTA}[BUILD-YOUR-OWN]{COLOR_RESET}",
    "api": f"{COLOR_YELLOW}[API]{COLOR_RESET}",
    "self-hosted": f"{COLOR_CYAN}[SELF-HOSTED]{COLOR_RESET}",
    "self-hosted-proprietary": f"{COLOR_YELLOW}[PROPRIETARY-HOST]{COLOR_RESET}",
    "roadmap": f"{COLOR_MAGENTA}[ROADMAP]{COLOR_RESET}",
    "cheatsheet": f"{COLOR_BLUE}[CHEATSHEET]{COLOR_RESET}",
    "interactive": f"{COLOR_CYAN}[INTERACTIVE]{COLOR_RESET}",
    "podcast": f"{COLOR_GREEN}[PODCAST]{COLOR_RESET}",
    "curated-list": f"{COLOR_GRAY}[CURATED]{COLOR_RESET}",
    "problem-set": f"{COLOR_MAGENTA}[PRACTICE]{COLOR_RESET}",
    "library": f"{COLOR_CYAN}[LIBRARY]{COLOR_RESET}",
    "newsletter": f"{COLOR_YELLOW}[NEWSLETTER]{COLOR_RESET}",
    "website": f"{COLOR_BLUE}[WEBSITE]{COLOR_RESET}"
}

def get_db():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}. Run 'python scripts/index_dev_universe.py' first.")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def search(query=None, item_type=None, category=None, source=None, saas=None, limit=20):
    conn = get_db()
    cursor = conn.cursor()

    conditions = []
    params = []

    if saas:
        # Search specifically for self-hosted alternatives to a SaaS product
        clean_saas = "".join(c if c.isalnum() or c.isspace() else " " for c in saas).strip()
        conditions.append("(r.type LIKE 'self-hosted%' AND (r.description LIKE ? OR r.title LIKE ?))")
        params.extend([f"%{clean_saas}%", f"%{clean_saas}%"])

    if query:
        clean_q = "".join(c if c.isalnum() or c.isspace() else " " for c in query).strip()
        if clean_q:
            fts_terms = " ".join(f'"{term}"*' for term in clean_q.split())
            conditions.append("r.id IN (SELECT rowid FROM resources_fts WHERE resources_fts MATCH ?)")
            params.append(fts_terms)

    if item_type:
        conditions.append("r.type = ?")
        params.append(item_type)

    if category:
        conditions.append("(r.category LIKE ? OR r.subcategory LIKE ?)")
        params.extend([f"%{category}%", f"%{category}%"])

    if source:
        conditions.append("r.source_repo LIKE ?")
        params.append(f"%{source}%")

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"""
    SELECT r.id, r.title, r.url, r.type, r.category, r.subcategory, r.language, r.format, r.description, r.source_repo
    FROM resources r
    {where_clause}
    ORDER BY r.id ASC
    LIMIT ?
    """
    params.append(limit)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

def format_row(row):
    badge = TYPE_BADGES.get(row["type"], f"[{row['type'].upper()}]")
    title = f"{COLOR_BOLD}{row['title']}{COLOR_RESET}"
    cat = f"{COLOR_GRAY}({row['category']}{' / ' + row['subcategory'] if row['subcategory'] and row['subcategory'] != row['category'] else ''}){COLOR_RESET}"
    url = f"{COLOR_BLUE}{row['url']}{COLOR_RESET}"
    fmt = f"{COLOR_YELLOW}[{row['format']}]{COLOR_RESET}" if row["format"] else ""
    tech = f"{COLOR_CYAN}[{row['language']}]{COLOR_RESET}" if row["language"] and row["type"].startswith("self-hosted") else ""

    out = f"  {badge} {title} {cat} {tech} {fmt}\n    {url}\n"
    if row["description"]:
        desc = row['description']
        out += f"    {COLOR_GRAY}{desc[:130]}{'...' if len(desc) > 130 else ''}{COLOR_RESET}\n"
    return out

def show_stats():
    if not STATS_PATH.exists():
        print("Stats file not found. Re-run indexer.")
        return
    with open(STATS_PATH, "r", encoding="utf-8") as f:
        stats = json.load(f)

    print(f"\n{COLOR_BOLD}{COLOR_CYAN}=== OMNIDEV UNIVERSE KNOWLEDGE METRICS ==={COLOR_RESET}")
    print(f"Total Curated Resources : {COLOR_BOLD}{stats['total_resources']:,}{COLOR_RESET}")
    print(f"\n{COLOR_BOLD}By Resource Type:{COLOR_RESET}")
    for t, cnt in sorted(stats["by_type"].items(), key=lambda x: x[1], reverse=True):
        badge = TYPE_BADGES.get(t, f"[{t}]")
        print(f"  {badge:<32} : {cnt:>5,}")

    print(f"\n{COLOR_BOLD}By Source Repository:{COLOR_RESET}")
    for s, cnt in sorted(stats["by_source"].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {s:<24} : {cnt:>5,}")

    print(f"\n{COLOR_BOLD}Top 20 Categories:{COLOR_RESET}")
    for idx, (c, cnt) in enumerate(list(stats["top_30_categories"].items())[:20], 1):
        print(f"  {idx:2d}. {c:<32} : {cnt:>4,}")
    print()

def interactive_mode():
    print(f"{COLOR_BOLD}{COLOR_CYAN}=== OMNIDEV UNIVERSE INTERACTIVE SEARCH ==={COLOR_RESET}")
    print("Commands: ':q' to quit, ':stats' for stats, ':help' for help")
    print("Filters: 'type:self-hosted', 'type:roadmap', 'type:book', 'saas:notion', 'cat:analytics'\n")

    while True:
        try:
            line = input(f"{COLOR_GREEN}omnidev>{COLOR_RESET} ").strip()
            if not line:
                continue
            if line in [":q", ":quit", "exit"]:
                break
            if line in [":stats", "stats"]:
                show_stats()
                continue
            if line in [":help", "help"]:
                print("Examples:")
                print("  rust                     -> search all for 'rust'")
                print("  type:self-hosted git     -> self-hosted git solutions (Gitea, GitLab)")
                print("  type:roadmap ai          -> roadmaps for AI and ML")
                print("  saas:notion              -> open-source alternatives to Notion")
                print("  saas:slack               -> open-source alternatives to Slack")
                print("  type:build-project redis -> guides to build Redis from scratch")
                continue

            query = line
            item_type = None
            category = None
            saas = None

            parts = line.split()
            remaining = []
            for p in parts:
                if p.startswith("type:"):
                    item_type = p.split(":", 1)[1]
                elif p.startswith("cat:") or p.startswith("category:"):
                    category = p.split(":", 1)[1]
                elif p.startswith("saas:") or p.startswith("alt:"):
                    saas = p.split(":", 1)[1]
                else:
                    remaining.append(p)
            query = " ".join(remaining)

            results = search(query=query or None, item_type=item_type, category=category, saas=saas, limit=15)
            print(f"\nFound {len(results)} matching entries:\n")
            for r in results:
                print(format_row(r))

        except (KeyboardInterrupt, EOFError):
            break
    print(f"\n{COLOR_GRAY}Goodbye!{COLOR_RESET}")

def main():
    parser = argparse.ArgumentParser(description="OmniDev Universe CLI Search Engine")
    parser.add_argument("-q", "--query", help="Keyword search query")
    parser.add_argument("-t", "--type", choices=[
        "book", "course", "build-project", "api", "self-hosted", "self-hosted-proprietary",
        "roadmap", "cheatsheet", "interactive", "podcast", "curated-list", "problem-set",
        "library", "newsletter", "website"
    ], help="Filter by type")
    parser.add_argument("-c", "--category", help="Filter by category/subject")
    parser.add_argument("-s", "--source", help="Filter by source repo")
    parser.add_argument("-S", "--saas", help="Find self-hosted alternatives to a proprietary SaaS (e.g. Notion, Slack, Trello, Zapier)")
    parser.add_argument("-l", "--limit", type=int, default=15, help="Max results (default: 15)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Launch interactive search shell")
    parser.add_argument("--stats", action="store_true", help="Display knowledge base metrics")

    args = parser.parse_args()

    if args.stats:
        show_stats()
        return

    if args.interactive or (not args.query and not args.type and not args.category and not args.source and not args.saas):
        interactive_mode()
        return

    results = search(
        query=args.query,
        item_type=args.type,
        category=args.category,
        source=args.source,
        saas=args.saas,
        limit=args.limit
    )
    print(f"\n{COLOR_BOLD}Matches found: {len(results)}{COLOR_RESET}\n")
    for r in results:
        print(format_row(r))

if __name__ == "__main__":
    main()
