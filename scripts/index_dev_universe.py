#!/usr/bin/env python3
"""
OmniDev Universe: Universal Developer Knowledge Indexer
Ingests and indexes:
  - free-programming-books (books, courses, podcasts, cheatsheets, interactive)
  - build-your-own-x (recreate technologies from scratch)
  - public-apis (categorized public web APIs)
  - awesome (curated lists)
  - awesome-python (curated Python libraries and resources)
  - awesome-selfhosted (free and open source self-hostable software and services)
  - developer-roadmap (step-by-step career, architecture, and language roadmaps)
Builds SQLite with FTS5, JSON export, and web data JS for visual explorer.
"""

import os
import re
import sys
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "dev_universe.db"
JSON_PATH = DATA_DIR / "dev_universe_index.json"
STATS_PATH = DATA_DIR / "dev_universe_stats.json"

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'[*_`]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_format_and_author(line: str):
    fmt = "Web/HTML"
    author = ""
    formats_found = []
    for f in ["PDF", "EPUB", "Mobi", "HTML"]:
        if re.search(r'\b' + f + r'\b', line, re.IGNORECASE):
            formats_found.append(f.upper())
    if formats_found:
        fmt = ", ".join(dict.fromkeys(formats_found))
    
    author_match = re.search(r'-\s+([^\(\[\n]+)', line)
    if author_match:
        author = author_match.group(1).strip()
    return fmt, author

def init_db(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS resources_fts;")
    cursor.execute("DROP TABLE IF EXISTS resources;")
    
    cursor.execute("""
    CREATE TABLE resources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT,
        language TEXT,
        format TEXT,
        description TEXT,
        source_repo TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("CREATE INDEX idx_resources_type ON resources(type);")
    cursor.execute("CREATE INDEX idx_resources_cat ON resources(category);")
    cursor.execute("CREATE INDEX idx_resources_source ON resources(source_repo);")

    cursor.execute("""
    CREATE VIRTUAL TABLE resources_fts USING fts5(
        title,
        category,
        subcategory,
        description,
        type,
        source_repo,
        content='resources',
        content_rowid='id'
    );
    """)
    conn.commit()

def parse_fpb_file(filepath: Path, item_type: str, default_cat: str = "General"):
    records = []
    if not filepath.exists():
        return records

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    current_cat = default_cat
    current_subcat = ""

    for line in lines:
        raw = line.strip()
        if not raw:
            continue

        h3_match = re.match(r'^###\s+(.+)$', raw)
        if h3_match:
            cat_name = clean_text(h3_match.group(1))
            if not cat_name.lower().startswith("index") and not cat_name.lower().startswith("contributing"):
                current_cat = cat_name
                current_subcat = ""
            continue

        h4_match = re.match(r'^####\s+(.+)$', raw)
        if h4_match:
            current_subcat = clean_text(h4_match.group(1))
            continue

        link_matches = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', raw)
        for title, url in link_matches:
            if any(skip in url for skip in ["badge", "shields.io", "travis-ci", "rawgit", "sponsors", "creativecommons"]):
                continue
            
            clean_title = clean_text(title)
            if not clean_title or len(clean_title) < 2:
                continue

            fmt, author = extract_format_and_author(raw)
            desc = f"Author: {author}" if author else ""
            if "courses" in filepath.name:
                fmt = "Video/Course"
            elif "casts" in filepath.name:
                fmt = "Podcast/Audio"
            elif "cheatsheet" in filepath.name:
                fmt = "Cheatsheet"
            elif "interactive" in filepath.name:
                fmt = "Interactive"

            records.append({
                "title": clean_title,
                "url": url.strip(),
                "type": item_type,
                "category": current_cat,
                "subcategory": current_subcat,
                "language": current_cat if "langs" in filepath.name else "English",
                "format": fmt,
                "description": desc,
                "source_repo": "free-programming-books"
            })
    return records

def parse_build_your_own_x(filepath: Path):
    records = []
    if not filepath.exists():
        return records

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    current_cat = "General"
    for line in lines:
        raw = line.strip()
        h_match = re.match(r'^#{2,4}\s+(.+)$', raw)
        if h_match:
            header = h_match.group(1).replace("Build your own", "").strip()
            header = clean_text(header)
            if header and not header.lower().startswith("tutorials"):
                current_cat = header
            continue

        matches = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', raw)
        for title, url in matches:
            if "github-banner" in url or ("codecrafters" in url and "banner" in url):
                continue
            
            lang_match = re.match(r'^\*?\*?([A-Za-z0-9#\+\.\s]+)\*?\*?:\s*(.+)$', title)
            lang = ""
            clean_title = clean_text(title)
            if lang_match:
                lang = clean_text(lang_match.group(1))
                clean_title = clean_text(lang_match.group(2))

            records.append({
                "title": f"Build your own {current_cat}: {clean_title}" if current_cat not in clean_title else clean_title,
                "url": url.strip(),
                "type": "build-project",
                "category": f"Build Your Own {current_cat}",
                "subcategory": current_cat,
                "language": lang or "Multi-language",
                "format": "Code Tutorial",
                "description": f"Step-by-step implementation guide in {lang or 'source code'}",
                "source_repo": "build-your-own-x"
            })
    return records

def parse_public_apis(filepath: Path):
    records = []
    if not filepath.exists():
        return records

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    current_cat = "General"
    for line in lines:
        raw = line.strip()
        h_match = re.match(r'^###\s+([^\n]+)', raw)
        if h_match:
            current_cat = clean_text(h_match.group(1))
            continue

        if raw.startswith("|") and not raw.startswith("|:--") and not raw.startswith("| API"):
            cols = [c.strip() for c in raw.split("|")[1:-1]]
            if len(cols) >= 2:
                api_col = cols[0]
                desc = clean_text(cols[1])
                auth = cols[2] if len(cols) > 2 else "No"
                https = cols[3] if len(cols) > 3 else "Yes"
                cors = cols[4] if len(cols) > 4 else "Unknown"

                url_match = re.search(r'\[([^\]]+)\]\((https?://[^\)]+)\)', api_col)
                if url_match:
                    name = clean_text(url_match.group(1))
                    url = url_match.group(2)
                    full_desc = f"{desc} (Auth: {auth}, HTTPS: {https}, CORS: {cors})"
                    records.append({
                        "title": f"{name} API",
                        "url": url.strip(),
                        "type": "api",
                        "category": current_cat,
                        "subcategory": "Public API",
                        "language": "HTTP/REST",
                        "format": "JSON/REST API",
                        "description": full_desc,
                        "source_repo": "public-apis"
                    })
    return records

def parse_awesome(filepath: Path):
    records = []
    if not filepath.exists():
        return records

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    current_cat = "Curated Awesome"
    for line in lines:
        raw = line.strip()
        h_match = re.match(r'^##\s+(.+)$', raw)
        if h_match:
            title = clean_text(h_match.group(1))
            if title.lower() not in ["contents", "license", "contributing"]:
                current_cat = title
            continue

        link_matches = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', raw)
        for title, url in link_matches:
            if any(skip in url for skip in ["sindresorhus", "badge", "shields.io", "creativecommons"]):
                continue
            clean_title = clean_text(title)
            if not clean_title or len(clean_title) < 2:
                continue

            desc_match = re.search(r'-\s+([^\n]+)', raw)
            desc = clean_text(desc_match.group(1)) if desc_match else "Curated awesome collection"

            records.append({
                "title": clean_title,
                "url": url.strip(),
                "type": "curated-list",
                "category": current_cat,
                "subcategory": "Awesome List",
                "language": current_cat if "Languages" in current_cat else "General",
                "format": "Markdown/GitHub",
                "description": desc,
                "source_repo": "awesome"
            })
    return records

def parse_awesome_python(filepath: Path):
    records = []
    if not filepath.exists():
        return records

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    in_projects = False
    in_resources = False
    current_cat = "General"
    current_subcat = ""

    for line in lines:
        raw = line.strip()
        if not raw:
            continue

        if raw.startswith("## Projects"):
            in_projects = True
            in_resources = False
            continue
        elif raw.startswith("## Resources"):
            in_projects = False
            in_resources = True
            continue
        elif raw.startswith("## Contributing") or raw.startswith("## License"):
            break

        if raw.startswith("### "):
            current_cat = clean_text(raw.replace("### ", ""))
            current_subcat = ""
            continue

        if in_projects or in_resources:
            if raw.startswith("- ") and not raw.startswith("- ["):
                current_subcat = clean_text(raw.replace("- ", ""))
                continue

            match = re.search(r"\[([^\]]+)\]\((https?://[^\)]+)\)(?:\s*-\s*(.+))?", raw)
            if match:
                title = clean_text(match.group(1))
                url = match.group(2).strip()
                desc = clean_text(match.group(3)) if match.group(3) else f"Curated {current_cat} resource for Python."

                if in_resources:
                    res_type = "podcast" if "podcast" in current_cat.lower() else ("newsletter" if "newsletter" in current_cat.lower() else "website")
                else:
                    res_type = "library"

                records.append({
                    "title": title,
                    "url": url,
                    "type": res_type,
                    "category": current_cat,
                    "subcategory": current_subcat or "Awesome Python",
                    "language": "Python",
                    "format": "Python Package / Library",
                    "description": desc,
                    "source_repo": "awesome-python"
                })
    return records

def parse_awesome_selfhosted(filepath: Path, is_non_free: bool = False):
    """
    Parses awesome-selfhosted README.md and non-free.md into structured self-hosted application resources.
    """
    records = []
    if not filepath.exists():
        return records

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    current_cat = "Self-Hosted"
    current_subcat = ""

    for line in lines:
        raw = line.strip()
        if not raw:
            continue

        h3_match = re.match(r"^###\s+([^\n]+)", raw)
        if h3_match:
            cat_title = clean_text(h3_match.group(1))
            if cat_title.lower() not in ["contents", "contributing", "license", "list of licenses", "anti-features", "external links"]:
                current_cat = cat_title
                current_subcat = ""
            continue

        h4_match = re.match(r"^####\s+([^\n]+)", raw)
        if h4_match:
            current_subcat = clean_text(h4_match.group(1))
            continue

        if raw.startswith("- ["):
            link_m = re.match(r"^-\s+\[([^\]]+)\]\((https?://[^\)]+)\)(.*)$", raw)
            if link_m:
                title = clean_text(link_m.group(1))
                url = link_m.group(2).strip()
                rest = link_m.group(3).strip()

                if title.lower() in ["back to top", "^ back to top ^"]:
                    continue

                demo_match = re.search(r"\[Demo\]\((https?://[^\)]+)\)", rest)
                demo_url = demo_match.group(1) if demo_match else ""

                source_match = re.search(r"\[Source Code\]\((https?://[^\)]+)\)", rest)
                source_url = source_match.group(1) if source_match else ""

                tags = re.findall(r"`([^`]+)`", rest)
                license_tag = tags[0] if len(tags) > 0 else ("Proprietary" if is_non_free else "Open Source")
                tech_tag = tags[1] if len(tags) > 1 else ""

                # Extract description
                desc_part = rest
                desc_part = re.sub(r"^[`\s\u2000-\u3300\U0001F000-\U0001FAFF]+-\s*", "", desc_part)
                desc_part = re.sub(r"^-\s*", "", desc_part)
                desc_part = re.sub(r"\(\[(?:Demo|Source Code)\]\([^\)]+\)[^)]*\)", "", desc_part)
                desc_part = re.sub(r"`[^`]+`", "", desc_part)
                desc_part = re.sub(r"\s+", " ", desc_part).strip(" -.,")

                extra = []
                if license_tag:
                    extra.append(f"License: {license_tag}")
                if tech_tag:
                    extra.append(f"Tech: {tech_tag}")
                if source_url:
                    extra.append(f"Source: {source_url}")
                if demo_url:
                    extra.append(f"Demo: {demo_url}")

                full_desc = desc_part
                if extra:
                    full_desc += f" ({'; '.join(extra)})"

                records.append({
                    "title": title,
                    "url": url,
                    "type": "self-hosted" if not is_non_free else "self-hosted-proprietary",
                    "category": current_cat,
                    "subcategory": current_subcat or current_cat,
                    "language": tech_tag or ("Docker/Web" if not is_non_free else "Proprietary"),
                    "format": "Self-Hosted Application",
                    "description": full_desc,
                    "source_repo": "awesome-selfhosted"
                })
    return records

def parse_developer_roadmaps(roadmaps_dir: Path):
    """
    Parses developer-roadmap/roadmaps to extract career paths, skill trees, and technical roadmaps.
    """
    records = []
    if not roadmaps_dir.exists():
        return records

    for item in sorted(roadmaps_dir.iterdir()):
        if not item.is_dir():
            continue

        slug = item.name
        title = " ".join(word.capitalize() for word in slug.split("-")) + " Roadmap"

        content_dir = item / "content"
        topics_preview = []
        if content_dir.exists():
            topic_files = sorted(content_dir.glob("*.md"))
            for tf in topic_files[:10]:
                topic_name = tf.stem.split("@")[0].replace("-", " ").title()
                topics_preview.append(topic_name)

        preview_str = f"Covers: {', '.join(topics_preview)}..." if topics_preview else "Step-by-step career & technical roadmap."
        url = f"https://roadmap.sh/{slug}"

        records.append({
            "title": title,
            "url": url,
            "type": "roadmap",
            "category": "Developer Roadmaps",
            "subcategory": slug,
            "language": slug.capitalize(),
            "format": "Interactive Roadmap",
            "description": f"{preview_str} (Community-driven guide with topics, skills, and learning resources)",
            "source_repo": "developer-roadmap"
        })
    return records

def main():
    print("=" * 60)
    print("  OMNIDEV UNIVERSE: UNIFIED KNOWLEDGE INGESTION ENGINE")
    print("=" * 60)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    all_records = []

    # 1. free-programming-books
    fpb_dir = BASE_DIR / "free-programming-books"
    print("\n[*] Parsing free-programming-books...")
    
    langs_books = parse_fpb_file(fpb_dir / "books" / "free-programming-books-langs.md", "book", "Programming Languages")
    print(f"  + Language Books: {len(langs_books):,}")
    all_records.extend(langs_books)

    subject_books = parse_fpb_file(fpb_dir / "books" / "free-programming-books-subjects.md", "book", "Subjects")
    print(f"  + Subject Books: {len(subject_books):,}")
    all_records.extend(subject_books)

    courses = parse_fpb_file(fpb_dir / "courses" / "free-courses-en.md", "course", "Courses")
    print(f"  + English Video Courses: {len(courses):,}")
    all_records.extend(courses)

    casts = parse_fpb_file(fpb_dir / "casts" / "free-podcasts-screencasts-en.md", "podcast", "Podcasts")
    print(f"  + Podcasts & Screencasts: {len(casts):,}")
    all_records.extend(casts)

    cheatsheets = parse_fpb_file(fpb_dir / "more" / "free-programming-cheatsheets.md", "cheatsheet", "Cheatsheets")
    print(f"  + Cheatsheets: {len(cheatsheets):,}")
    all_records.extend(cheatsheets)

    interactive = parse_fpb_file(fpb_dir / "more" / "free-programming-interactive-tutorials-en.md", "interactive", "Interactive")
    print(f"  + Interactive Tutorials: {len(interactive):,}")
    all_records.extend(interactive)

    problems = parse_fpb_file(fpb_dir / "more" / "problem-sets-competitive-programming.md", "problem-set", "Competitive Programming")
    print(f"  + Problem Sets: {len(problems):,}")
    all_records.extend(problems)

    # 2. build-your-own-x
    byox_file = BASE_DIR / "build-your-own-x" / "README.md"
    print("\n[*] Parsing build-your-own-x...")
    byox = parse_build_your_own_x(byox_file)
    print(f"  + Build Your Own X Projects: {len(byox):,}")
    all_records.extend(byox)

    # 3. public-apis
    apis_file = BASE_DIR / "public-apis" / "README.md"
    print("\n[*] Parsing public-apis...")
    apis = parse_public_apis(apis_file)
    print(f"  + Public Web APIs: {len(apis):,}")
    all_records.extend(apis)

    # 4. awesome
    awesome_file = BASE_DIR / "awesome" / "readme.md"
    print("\n[*] Parsing awesome...")
    awesome = parse_awesome(awesome_file)
    print(f"  + Curated Awesome Lists: {len(awesome):,}")
    all_records.extend(awesome)

    # 5. awesome-python
    awesome_py_file = BASE_DIR / "awesome-python" / "README.md"
    if awesome_py_file.exists():
        print("\n[*] Parsing awesome-python...")
        awesome_py = parse_awesome_python(awesome_py_file)
        print(f"  + Curated Python Libraries & Resources: {len(awesome_py):,}")
        all_records.extend(awesome_py)

    # 6. awesome-selfhosted
    selfhosted_dir = BASE_DIR / "awesome-selfhosted"
    if selfhosted_dir.exists():
        print("\n[*] Parsing awesome-selfhosted (FOSS & Non-Free)...")
        sh_foss = parse_awesome_selfhosted(selfhosted_dir / "README.md", is_non_free=False)
        print(f"  + Open Source Self-Hosted Applications: {len(sh_foss):,}")
        all_records.extend(sh_foss)

        sh_prop = parse_awesome_selfhosted(selfhosted_dir / "non-free.md", is_non_free=True)
        print(f"  + Proprietary Self-Hosted Solutions: {len(sh_prop):,}")
        all_records.extend(sh_prop)

    # 7. developer-roadmap
    roadmaps_dir = BASE_DIR / "developer-roadmap" / "roadmaps"
    if roadmaps_dir.exists():
        print("\n[*] Parsing developer-roadmap...")
        roadmaps = parse_developer_roadmaps(roadmaps_dir)
        print(f"  + Developer & Technology Roadmaps: {len(roadmaps):,}")
        all_records.extend(roadmaps)

    # Deduplicate by URL
    seen_urls = set()
    unique_records = []
    for r in all_records:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            unique_records.append(r)

    print(f"\n[+] Total unique resources gathered: {len(unique_records):,} (from {len(all_records):,} raw items)")

    # Store in SQLite DB
    print(f"\n[*] Initializing SQLite Database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    cursor = conn.cursor()
    cursor.executemany("""
    INSERT INTO resources (title, url, type, category, subcategory, language, format, description, source_repo)
    VALUES (:title, :url, :type, :category, :subcategory, :language, :format, :description, :source_repo)
    """, unique_records)

    # Populate FTS
    cursor.execute("""
    INSERT INTO resources_fts(rowid, title, category, subcategory, description, type, source_repo)
    SELECT id, title, category, subcategory, description, type, source_repo FROM resources;
    """)
    conn.commit()
    conn.close()
    print("  + SQLite Database and FTS5 indices successfully populated!")

    # JSON & Web Data Export
    print(f"\n[*] Exporting JSON Index to: {JSON_PATH}")
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(unique_records, f, indent=2, ensure_ascii=False)
    print(f"  + JSON index written ({os.path.getsize(JSON_PATH) / (1024*1024):.2f} MB)")

    JS_PATH = BASE_DIR / "docs" / "dev_universe_data.js"
    print(f"\n[*] Exporting Web Data to: {JS_PATH}")
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write("window.DEV_UNIVERSE_DATA = ")
        json.dump(unique_records, f, ensure_ascii=False)
        f.write(";\n")
    print(f"  + JS export written ({os.path.getsize(JS_PATH) / (1024*1024):.2f} MB)")

    # Generate Stats
    type_counts = {}
    source_counts = {}
    cat_counts = {}

    for r in unique_records:
        t = r["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
        s = r["source_repo"]
        source_counts[s] = source_counts.get(s, 0) + 1
        c = r["category"]
        cat_counts[c] = cat_counts.get(c, 0) + 1

    top_categories = sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)[:30]

    stats = {
        "total_resources": len(unique_records),
        "by_type": type_counts,
        "by_source": source_counts,
        "top_30_categories": dict(top_categories)
    }

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"[*] Stats summary saved to: {STATS_PATH}")

    print("\n" + "=" * 60)
    print("  INGESTION SUMMARY:")
    print("=" * 60)
    print(f"  Total Unique Items: {stats['total_resources']:,}")
    print("\n  By Type:")
    for t, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    - {t:22}: {count:,}")
    print("\n  By Repository:")
    for s, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"    - {s:22}: {count:,}")
    print("=" * 60)

if __name__ == "__main__":
    main()
