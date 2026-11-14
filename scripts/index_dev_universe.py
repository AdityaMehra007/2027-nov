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

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True, errors="replace")
    except Exception:
        pass

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
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA synchronous = NORMAL;")
    try:
        cursor.execute("DROP TABLE IF EXISTS resources_fts;")
        conn.commit()
    except Exception:
        pass
    try:
        cursor.execute("DROP TABLE IF EXISTS resources;")
        conn.commit()
    except Exception:
        pass
    
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

    try:
        entries = sorted([d for d in roadmaps_dir.iterdir() if d.is_dir()])
    except Exception:
        return records

    for item in entries:
        slug = item.name
        title = " ".join(word.capitalize() for word in slug.split("-")) + " Roadmap"

        content_dir = item / "content"
        topics_preview = []
        if content_dir.exists():
            try:
                with os.scandir(content_dir) as it:
                    for entry in it:
                        if entry.name.endswith(".md"):
                            topic_name = entry.name.split("@")[0].replace("-", " ").title()
                            topics_preview.append(topic_name)
                            if len(topics_preview) >= 8:
                                break
            except Exception:
                pass

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

def parse_system_design_primer(sdp_dir: Path):
    """
    Parses system-design-primer to extract:
    - Comprehensive system design interview solutions & blueprints
    - Object-oriented design questions & notebook solutions
    - Distributed systems architecture concepts & guides
    - Real-world distributed architectures & company engineering case studies
    - Spaced-repetition flashcard decks (.apkg)
    """
    records = []
    if not sdp_dir.exists():
        return records

    readme_path = sdp_dir / "README.md"
    base_gh_url = "https://github.com/donnemartin/system-design-primer/blob/master"

    # 1. Parse Solutions in solutions/system_design/
    sys_solutions_dir = sdp_dir / "solutions" / "system_design"
    if sys_solutions_dir.exists():
        for item in sorted(sys_solutions_dir.iterdir()):
            if item.is_dir() and item.name != "template":
                sol_readme = item / "README.md"
                if sol_readme.exists():
                    with open(sol_readme, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()

                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = clean_text(title_match.group(1)) if title_match else f"Design {item.name.replace('_', ' ').title()}"

                    use_cases = []
                    use_case_match = re.search(r'###\s+Use cases.*?(?=###|\Z)', content, re.DOTALL | re.IGNORECASE)
                    if use_case_match:
                        uc_text = use_case_match.group(0)
                        bullet_points = re.findall(r'^\*\s+(.+)$', uc_text, re.MULTILINE)
                        use_cases = [clean_text(b) for b in bullet_points[:4]]

                    desc = "System design interview solution with architecture diagrams and trade-off analysis."
                    if use_cases:
                        desc += " Key use cases: " + "; ".join(use_cases)

                    records.append({
                        "title": title,
                        "url": f"{base_gh_url}/solutions/system_design/{item.name}/README.md",
                        "type": "system-design-solution",
                        "category": "System Design Interview Solutions",
                        "subcategory": item.name.replace("_", " ").title(),
                        "language": "Python / Architecture",
                        "format": "Case Study & Architecture Blueprint",
                        "description": desc,
                        "source_repo": "system-design-primer"
                    })

    # 2. Parse Solutions in solutions/object_oriented_design/
    ood_dir = sdp_dir / "solutions" / "object_oriented_design"
    if ood_dir.exists():
        for item in sorted(ood_dir.iterdir()):
            if item.is_dir():
                py_file = item / f"{item.name}.py"
                ipynb_file = item / f"{item.name}.ipynb"
                if not py_file.exists():
                    py_files = list(item.glob("*.py"))
                    py_file = py_files[0] if py_files else None
                if not ipynb_file.exists():
                    ipynb_files = list(item.glob("*.ipynb"))
                    ipynb_file = ipynb_files[0] if ipynb_files else None

                title = f"Design {item.name.replace('_', ' ').title()}"
                url = f"{base_gh_url}/solutions/object_oriented_design/{item.name}/"
                if ipynb_file:
                    url = f"{base_gh_url}/solutions/object_oriented_design/{item.name}/{ipynb_file.name}"
                elif py_file:
                    url = f"{base_gh_url}/solutions/object_oriented_design/{item.name}/{py_file.name}"

                records.append({
                    "title": f"OOD: {title}",
                    "url": url,
                    "type": "ood-solution",
                    "category": "Object-Oriented Design Solutions",
                    "subcategory": item.name.replace("_", " ").title(),
                    "language": "Python",
                    "format": "Interactive Notebook / Code Solution",
                    "description": f"Object-oriented design problem and Python implementation for {item.name.replace('_', ' ')}.",
                    "source_repo": "system-design-primer"
                })

    # 3. Parse Core Concepts, Tables & Blogs from README.md
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        in_topics = False
        current_section = ""
        current_main_topic = "System Design"

        def slugify(text: str) -> str:
            slug = text.lower()
            slug = re.sub(r'[^\w\s-]', '', slug)
            slug = re.sub(r'[\s_]+', '-', slug)
            return slug.strip('-')

        i = 0
        while i < len(lines):
            line = lines[i]
            raw = line.strip()

            if raw.startswith("## Index of system design topics"):
                in_topics = True
                i += 1
                continue

            if in_topics:
                if raw.startswith("## Under development") or raw.startswith("## Credits") or raw.startswith("## License"):
                    break

                # Track sections
                if raw.startswith("### Real world architectures"):
                    current_section = "real_world_arch"
                elif raw.startswith("### Company architectures"):
                    current_section = "company_arch"
                elif raw.startswith("### Company engineering blogs"):
                    current_section = "eng_blogs"
                elif raw.startswith("### Additional system design interview questions"):
                    current_section = "more_questions"
                elif raw.startswith("## ") or raw.startswith("### "):
                    if not raw.startswith("### Source"):
                        current_section = "general"

                # Main Section H2
                h2_match = re.match(r'^##\s+([^#\n]+)', raw)
                if h2_match:
                    h2_title = clean_text(h2_match.group(1))
                    current_main_topic = h2_title
                    anchor = slugify(h2_title)

                    desc_lines = []
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith("#"):
                        t = clean_text(lines[j])
                        if t and not t.startswith("<") and not t.startswith("[![") and not t.startswith("!["):
                            desc_lines.append(t)
                            if len(desc_lines) >= 2:
                                break
                        j += 1
                    desc = " ".join(desc_lines) if desc_lines else f"System design core principles covering {h2_title}."

                    if h2_title.lower() not in ["study guide", "anki flashcards", "contributing", "how to approach a system design interview question", "system design interview questions with solutions", "object-oriented design interview questions with solutions", "appendix"]:
                        records.append({
                            "title": f"System Design: {h2_title}",
                            "url": f"https://github.com/donnemartin/system-design-primer#{anchor}",
                            "type": "system-design-concept",
                            "category": "System Design Concepts",
                            "subcategory": current_main_topic,
                            "language": "Architecture",
                            "format": "Guide / Deep Dive",
                            "description": desc,
                            "source_repo": "system-design-primer"
                        })
                    i += 1
                    continue

                # Subtopic H3
                h3_match = re.match(r'^###\s+([^#\n]+)', raw)
                if h3_match and current_section == "general":
                    h3_title = clean_text(h3_match.group(1))
                    anchor = slugify(h3_title)

                    desc_lines = []
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith("#"):
                        t = clean_text(lines[j])
                        if t and not t.startswith("<") and not t.startswith("[![") and not t.startswith("!["):
                            desc_lines.append(t)
                            if len(desc_lines) >= 2:
                                break
                        j += 1
                    desc = " ".join(desc_lines) if desc_lines else f"Comprehensive guide to {h3_title} in distributed systems."

                    if not h3_title.lower().startswith("source") and not h3_title.lower().startswith("view exercise") and not h3_title.lower().startswith("step"):
                        records.append({
                            "title": f"{h3_title} ({current_main_topic})",
                            "url": f"https://github.com/donnemartin/system-design-primer#{anchor}",
                            "type": "system-design-concept",
                            "category": current_main_topic,
                            "subcategory": h3_title,
                            "language": "Architecture",
                            "format": "Technical Guide",
                            "description": desc,
                            "source_repo": "system-design-primer"
                        })
                    i += 1
                    continue

                # Real world architecture table parsing
                if current_section == "real_world_arch":
                    if ("| Data processing |" in raw or "| Data store |" in raw or "| File system |" in raw or "| Misc |" in raw):
                        cols = [c.strip() for c in raw.split("|")[1:-1]]
                        if len(cols) >= 3:
                            subcat = cols[0]
                            sys_desc = clean_text(cols[1])
                            ref_col = cols[2]
                            name_match = re.search(r'\*\*([^\*]+)\*\*', cols[1])
                            sys_name = name_match.group(1) if name_match else sys_desc.split("-")[0].strip()
                            url_match = re.search(r'\((https?://[^\)]+)\)', ref_col)
                            ref_url = url_match.group(1) if url_match else f"{base_gh_url}/#real-world-architectures"
                            records.append({
                                "title": f"Real-World Architecture: {sys_name}",
                                "url": ref_url,
                                "type": "architecture-case-study",
                                "category": "Real-World Distributed Architectures",
                                "subcategory": subcat,
                                "language": "Architecture",
                                "format": "Whitepaper / Technical Talk",
                                "description": sys_desc,
                                "source_repo": "system-design-primer"
                            })

                # Additional system design interview questions table parsing
                elif current_section == "more_questions":
                    if raw.startswith("|") and not raw.startswith("| Question") and not raw.startswith("|:--"):
                        cols = [c.strip() for c in raw.split("|")[1:-1]]
                        if len(cols) >= 2:
                            q_name = clean_text(cols[0])
                            links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', cols[1])
                            for link_title, link_url in links:
                                records.append({
                                    "title": f"Interview Question: {q_name}",
                                    "url": link_url,
                                    "type": "interview-question",
                                    "category": "System Design Interview Scenarios",
                                    "subcategory": "Interview Problem",
                                    "language": "Architecture",
                                    "format": f"Reference: {link_title}",
                                    "description": f"System design scenario: {q_name}. Referenced from {link_title}.",
                                    "source_repo": "system-design-primer"
                                })

                # Company Architectures table parsing
                elif current_section == "company_arch":
                    if raw.startswith("|") and not raw.startswith("| Company") and not raw.startswith("|:--"):
                        cols = [c.strip() for c in raw.split("|")[1:-1]]
                        if len(cols) >= 2:
                            company = clean_text(cols[0])
                            links = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', cols[1])
                            for link_title, link_url in links:
                                records.append({
                                    "title": f"{company} Architecture: {clean_text(link_title)}",
                                    "url": link_url,
                                    "type": "company-architecture",
                                    "category": "Company System Architectures",
                                    "subcategory": company,
                                    "language": "Architecture",
                                    "format": "Engineering Case Study / Talk",
                                    "description": f"Real-world production engineering deep dive at {company}: {clean_text(link_title)}.",
                                    "source_repo": "system-design-primer"
                                })

                # Company Engineering blogs parsing
                elif current_section == "eng_blogs":
                    blog_match = re.search(r'^\*\s+\[([^\]]+)\]\((https?://[^\)]+)\)', raw)
                    if blog_match:
                        blog_title = clean_text(blog_match.group(1))
                        blog_url = blog_match.group(2)
                        records.append({
                            "title": f"{blog_title}",
                            "url": blog_url,
                            "type": "engineering-blog",
                            "category": "Engineering Blogs",
                            "subcategory": "Tech Blogs",
                            "language": "Various",
                            "format": "Technical Blog",
                            "description": f"Official technology and engineering publication: {blog_title}.",
                            "source_repo": "system-design-primer"
                        })

            i += 1

    # 4. Flashcards in resources/flash_cards/
    flashcards_dir = sdp_dir / "resources" / "flash_cards"
    if flashcards_dir.exists():
        for card_file in flashcards_dir.glob("*.apkg"):
            deck_name = card_file.stem
            records.append({
                "title": f"Anki Flashcards: {deck_name}",
                "url": f"{base_gh_url}/resources/flash_cards/{card_file.name.replace(' ', '%20')}",
                "type": "flashcards",
                "category": "Study Resources & Flashcards",
                "subcategory": "Anki Spaced Repetition",
                "language": "Study Guide",
                "format": "Anki Deck (.apkg)",
                "description": f"Spaced-repetition flashcard deck for {deck_name} retention and interview practice.",
                "source_repo": "system-design-primer"
            })

    return records

def parse_coding_interview_university(ciu_dir: Path):
    """
    Parses Coding Interview University README.md and programming-language-resources.md.
    Extracts computer science fundamentals, data structures, algorithms, system design,
    interview prep questions, video lectures, books, and language tutorials.
    """
    records = []
    if not ciu_dir.exists():
        return records

    readme_file = ciu_dir / "README.md"
    lang_file = ciu_dir / "programming-language-resources.md"
    IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.gif', '.svg')

    # 1. Parse README.md
    if readme_file.exists():
        with open(readme_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        current_h2 = "General CS"
        current_h3 = ""
        current_subcat = ""

        for line in lines:
            raw = line.strip()
            if not raw:
                continue

            if raw.startswith("## "):
                current_h2 = clean_text(raw[3:])
                current_h3 = ""
                current_subcat = ""
                continue
            elif raw.startswith("### "):
                current_h3 = clean_text(raw[4:])
                current_subcat = current_h3
                continue
            elif raw.startswith("- ### "):
                current_subcat = clean_text(raw[6:])
                continue

            # Skip table of contents and translations sections
            if current_h2.lower() in ["table of contents", "translations", "translations in progress:", "what is it?"]:
                continue

            link_matches = re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)(.*)', raw)
            for m in link_matches:
                title = clean_text(m.group(1))
                url = m.group(2).strip()
                extra_text = clean_text(m.group(3)).strip(" -:()")

                if any(skip in url for skip in ["travis-ci", "badge", "shields.io", "github.com/jwasham/coding-interview-university/issues"]):
                    continue
                if any(url.lower().endswith(ext) for ext in IMAGE_EXTS):
                    continue
                if title.lower() in ["back to top", "⬆ back to top", "here", "article"]:
                    continue

                url_lower = url.lower()
                title_lower = title.lower()
                cat_lower = (current_h2 + " " + (current_subcat or current_h3)).lower()

                # Infer type and format
                if any(v in url_lower for v in ["youtube.com", "youtu.be", "archive.org/details", "coursera.org/lecture"]) or "(video)" in raw.lower():
                    item_type = "video-lecture"
                    fmt = "Video Lecture"
                elif any(b in url_lower for b in ["amazon.com", "geni.us", "books.google"]) or "book" in title_lower or "edition" in title_lower:
                    item_type = "book"
                    fmt = "Book"
                elif "cheat" in title_lower or "cheat" in url_lower:
                    item_type = "cheatsheet"
                    fmt = "Cheat Sheet"
                elif any(p in url_lower for p in ["leetcode.com", "hackerrank.com", "topcoder.com", "codeforces.com", "algoexpert.io", "interviewbit.com", "codility.com", "codewars.com", "exercism.org"]):
                    item_type = "practice-problem"
                    fmt = "Practice Problem / Platform"
                elif "system design" in cat_lower:
                    item_type = "system-design"
                    fmt = "System Design Guide"
                else:
                    item_type = "interview-prep"
                    fmt = "Study Guide / Article"

                desc_core = f"{current_h2}"
                sub_detail = current_subcat or current_h3
                if sub_detail and sub_detail != current_h2:
                    desc_core += f" - {sub_detail}"
                if extra_text:
                    desc_core += f": {extra_text}"

                # Infer language
                detected_lang = "CS Theory / Multi-language"
                for lang_candidate in ["Python", "C++", "Java", "C", "Go", "Rust", "JavaScript"]:
                    if f" {lang_candidate.lower()} " in f" {cat_lower} ":
                        detected_lang = lang_candidate
                        break

                records.append({
                    "title": title,
                    "url": url,
                    "type": item_type,
                    "category": current_h2,
                    "subcategory": current_subcat or current_h3 or current_h2,
                    "language": detected_lang,
                    "format": fmt,
                    "description": desc_core,
                    "source_repo": "coding-interview-university"
                })

    # 2. Parse programming-language-resources.md
    if lang_file.exists():
        with open(lang_file, "r", encoding="utf-8", errors="replace") as f:
            lang_lines = f.readlines()

        current_lang = "General"
        for line in lang_lines:
            raw = line.strip()
            if not raw:
                continue

            m_lang = re.match(r"^-\s+([A-Za-z0-9\+#\.]+)\s*$", raw)
            if m_lang:
                current_lang = m_lang.group(1).strip()
                continue

            m_link = re.search(r"\[([^\]]+)\]\((https?://[^\)]+|<https?://[^>]+>)\)(.*)", raw)
            if m_link:
                title = clean_text(m_link.group(1))
                url = m_link.group(2).strip("<> ")
                extra_text = clean_text(m_link.group(3)).strip(" -:()")

                if title.lower() in ["back to top"]:
                    continue

                url_lower = url.lower()
                title_lower = title.lower()

                if "(video)" in raw.lower() or any(v in url_lower for v in ["youtube.com", "youtu.be"]):
                    item_type = "video-lecture"
                    fmt = "Video Lecture"
                elif any(b in url_lower for b in ["amazon.com", "books.google"]) or "book" in title_lower:
                    item_type = "book"
                    fmt = "Book"
                elif "cheat sheet" in title_lower or "cheat" in url_lower:
                    item_type = "cheatsheet"
                    fmt = "Cheat Sheet"
                elif "interview questions" in title_lower:
                    item_type = "interview-prep"
                    fmt = "Interview Questions"
                else:
                    item_type = "tutorial"
                    fmt = "Programming Tutorial"

                desc = f"Language reference for {current_lang}: {title}"
                if extra_text:
                    desc += f" ({extra_text})"

                records.append({
                    "title": f"{title} ({current_lang})",
                    "url": url,
                    "type": item_type,
                    "category": "Programming Language Resources",
                    "subcategory": current_lang,
                    "language": current_lang,
                    "format": fmt,
                    "description": desc,
                    "source_repo": "coding-interview-university"
                })

    return records

def parse_996_icu(icu_dir: Path):
    records = []
    if not icu_dir.exists():
        return records

    # 1. Whitelist (955 / 965 companies)
    wl_file = icu_dir / "whitelist" / "README.md"
    if wl_file.exists():
        with open(wl_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        in_table = False
        for line in lines:
            raw = line.strip()
            if "名单列表" in raw:
                in_table = True
                continue
            if not in_table or not raw.startswith("|") or ":---" in raw:
                continue
            cols = [c.strip() for c in raw.split("|") if c.strip() != ""]
            if len(cols) < 4:
                continue
            city = cols[0]
            comp_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', cols[1])
            if comp_match:
                cname, curl = comp_match.group(1).strip(), comp_match.group(2).strip()
            else:
                cname, curl = cols[1].strip(), ""
            sched = cols[3]
            evidence = cols[4] if len(cols) > 4 else ""
            target_url = curl if curl.startswith("http") else f"https://github.com/996icu/996.ICU/tree/master/whitelist#{city}"
            
            records.append({
                "title": f"WLB Employer: {cname} ({city})",
                "url": target_url,
                "type": "wlb-employer",
                "category": "Work-Life Balance & Labor Rights",
                "subcategory": f"{city} WLB Employers",
                "language": "Management / Culture",
                "format": "Verified Company Profile",
                "description": f"Verified standard work schedule: {sched}. Evidence: {clean_text(evidence)}",
                "source_repo": "996.ICU"
            })

    # 2. Remote List
    remotelist_dir = icu_dir / "remotelist"
    if remotelist_dir.exists():
        for md_file in remotelist_dir.glob("**/remotelist.md"):
            city = md_file.parent.name.capitalize()
            with open(md_file, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
            for line in lines:
                raw = line.strip()
                if not raw.startswith("|") or "---" in raw or "公司名称" in raw:
                    continue
                cols = [c.strip() for c in raw.split("|") if c.strip() != ""]
                if len(cols) < 2:
                    continue
                cname = cols[0]
                site_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', cols[1])
                curl = site_match.group(2).strip() if site_match else (cols[1].strip() if cols[1].startswith("http") else "")
                pos = cols[2] if len(cols) > 2 else "All Roles"
                if not cname:
                    continue
                target_url = curl if curl.startswith("http") else f"https://github.com/996icu/996.ICU/tree/master/remotelist/{md_file.parent.name}"
                records.append({
                    "title": f"Remote Employer: {cname} ({city})",
                    "url": target_url,
                    "type": "remote-employer",
                    "category": "Remote Work & Careers",
                    "subcategory": f"{city} Remote Tech",
                    "language": "Careers / Remote",
                    "format": "Remote Company Profile",
                    "description": f"Distributed/remote-friendly employer in {city}. Eligible roles: {pos}.",
                    "source_repo": "996.ICU"
                })

    # 3. Anti-996 Awesomelist Projects
    awesome_file = icu_dir / "awesomelist" / "README.md"
    if awesome_file.exists():
        with open(awesome_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        in_table = False
        for line in lines:
            raw = line.strip()
            if "| LOGO |" in raw:
                in_table = True
                continue
            if not in_table or not raw.startswith("|") or ":---" in raw:
                continue
            cols = [c.strip() for c in raw.split("|")]
            if cols and cols[0] == "":
                cols = cols[1:]
            if cols and cols[-1] == "":
                cols = cols[:-1]
            if len(cols) < 5:
                continue
            pmatch = re.search(r'\[([^\]]+)\]\(([^)]+)\)', cols[1])
            omatch = re.search(r'\[([^\]]+)\]\(([^)]+)\)', cols[2])
            pname = pmatch.group(1).strip() if pmatch else cols[1].strip()
            purl = pmatch.group(2).strip() if pmatch else (omatch.group(2).strip() if omatch else "")
            desc = clean_text(cols[4])
            if not pname or not purl.startswith("http"):
                continue
            records.append({
                "title": f"Anti-996 OSS: {pname}",
                "url": purl,
                "type": "anti996-project",
                "category": "Anti-996 Open Source Projects",
                "subcategory": "Ethical Open Source Software",
                "language": "Software",
                "format": "Open Source Code / Library",
                "description": f"{desc} (Protected under Anti-996 Ethical Labor License)",
                "source_repo": "996.ICU"
            })

    # 4. Proposals & Labor Guides
    prop_dir = icu_dir / "proposal"
    if prop_dir.exists():
        for f in prop_dir.glob("*.md"):
            if f.name.lower() in ["readme.md", "proposal_template.md"]:
                continue
            text = f.read_text(encoding="utf-8", errors="replace")
            lines = text.strip().splitlines()
            title = lines[0].lstrip("#").strip() if lines and lines[0].startswith("#") else f.stem.replace("_", " ").title()
            summary = clean_text(text[:300])
            records.append({
                "title": f"Labor Rights: {title}",
                "url": f"https://github.com/996icu/996.ICU/blob/master/proposal/{f.name}",
                "type": "labor-rights-guide",
                "category": "Labor Law & Worker Rights",
                "subcategory": "Proposals & Legal Frameworks",
                "language": "Legal / Policy",
                "format": "Statutory Proposal & Framework",
                "description": f"{summary}... Labor protection guidelines and worker rights reform.",
                "source_repo": "996.ICU"
            })

    return records


def parse_project_based_learning(pbl_dir: Path):
    records = []
    readme = pbl_dir / "README.md"
    if not readme.exists():
        return records

    with open(readme, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    current_lang = "General"
    in_content = False

    for line in lines:
        raw = line.strip()
        if not raw:
            continue

        h2_match = re.match(r'^##\s+([^#:\n]+):?', raw)
        if h2_match:
            h2_title = clean_text(h2_match.group(1))
            if h2_title.lower() not in ["table of contents", "contributing", "additional resources"]:
                current_lang = h2_title
                in_content = True
            continue

        if in_content:
            link_matches = re.findall(r'\[([^\]]+)\]\((https?://[^\)]+)\)', raw)
            for title, url in link_matches:
                if any(skip in url for skip in ["badge", "shields.io", "gitter.im", "travis-ci", "github.com/practical-tutorials"]):
                    continue
                clean_t = clean_text(title)
                if not clean_t or len(clean_t) < 3:
                    continue

                note_match = re.search(r'\)\s*([^\n\r]+)', raw)
                note = clean_text(note_match.group(1)) if note_match else ""
                desc = f"Build a real-world application from scratch in {current_lang}: {clean_t}."
                if note:
                    desc += f" {note}"

                records.append({
                    "title": f"Build in {current_lang}: {clean_t}",
                    "url": url.strip(),
                    "type": "project-tutorial",
                    "category": "Project-Based Learning",
                    "subcategory": f"{current_lang} Projects",
                    "language": current_lang,
                    "format": "Hands-on Project Tutorial",
                    "description": desc,
                    "source_repo": "project-based-learning"
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

    # 8. coding-interview-university
    ciu_dir = BASE_DIR / "coding-interview-university"
    if ciu_dir.exists():
        print("\n[*] Parsing coding-interview-university...")
        ciu_records = parse_coding_interview_university(ciu_dir)
        print(f"  + Coding Interview University Resources: {len(ciu_records):,}")
        all_records.extend(ciu_records)

    # 9. system-design-primer
    sdp_dir = BASE_DIR / "system-design-primer"
    if sdp_dir.exists():
        print("\n[*] Parsing system-design-primer...")
        sdp_records = parse_system_design_primer(sdp_dir)
        print(f"  + System Design Resources: {len(sdp_records):,}")
        all_records.extend(sdp_records)

    # 10. 996.ICU
    icu_dir = BASE_DIR / "996.ICU"
    if icu_dir.exists():
        print("\n[*] Parsing 996.ICU...")
        icu_records = parse_996_icu(icu_dir)
        print(f"  + 996.ICU WLB, Remote & Open Source Resources: {len(icu_records):,}")
        all_records.extend(icu_records)

    # 11. project-based-learning
    pbl_dir = BASE_DIR / "project-based-learning"
    if pbl_dir.exists():
        print("\n[*] Parsing project-based-learning...")
        pbl_records = parse_project_based_learning(pbl_dir)
        print(f"  + Project-Based Learning Tutorials: {len(pbl_records):,}")
        all_records.extend(pbl_records)

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
    for p in [DB_PATH, DATA_DIR / f"{DB_PATH.name}-journal", DATA_DIR / f"{DB_PATH.name}-wal", DATA_DIR / f"{DB_PATH.name}-shm"]:
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass

    conn = sqlite3.connect(DB_PATH, timeout=60.0)
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
    tmp_json = JSON_PATH.with_suffix(".tmp")
    with open(tmp_json, "w", encoding="utf-8") as f:
        json.dump(unique_records, f, indent=2, ensure_ascii=False)
    if JSON_PATH.exists():
        try:
            JSON_PATH.unlink()
        except Exception:
            pass
    tmp_json.replace(JSON_PATH)
    print(f"  + JSON index written ({os.path.getsize(JSON_PATH) / (1024*1024):.2f} MB)")

    JS_PATH = BASE_DIR / "docs" / "dev_universe_data.js"
    print(f"\n[*] Exporting Web Data to: {JS_PATH}")
    tmp_js = JS_PATH.with_suffix(".tmp")
    with open(tmp_js, "w", encoding="utf-8") as f:
        f.write("window.DEV_UNIVERSE_DATA = ")
        json.dump(unique_records, f, ensure_ascii=False)
        f.write(";\n")
    if JS_PATH.exists():
        try:
            JS_PATH.unlink()
        except Exception:
            pass
    tmp_js.replace(JS_PATH)
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
