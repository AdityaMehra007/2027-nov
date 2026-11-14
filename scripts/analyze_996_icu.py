#!/usr/bin/env python3
"""
996.ICU Comprehensive Data Extraction & Analytics Engine
Extracts, structures, and analyzes:
  - Blacklisted companies (forced overtime, 996, 11-11-6, unpaid overtime)
  - Whitelisted companies (965, 955, flexible hours, work-life balance)
  - Remote-friendly tech companies
  - Community proposals & labor law guidelines
  - Projects adopting the Anti-996 License

Outputs:
  - data/996_icu_dataset.json
  - docs/996_ICU_LABOR_RIGHTS_REPORT.md
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR / "996.ICU"
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = BASE_DIR / "docs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSON = DATA_DIR / "996_icu_dataset.json"
OUTPUT_REPORT = DOCS_DIR / "996_ICU_LABOR_RIGHTS_REPORT.md"


def clean_str(s: str) -> str:
    if not s:
        return ""
    return re.sub(r'\s+', ' ', s).strip()


def parse_link(cell: str):
    """Extract text and url from markdown link like [Name](url) or return plain text."""
    cell = clean_str(cell)
    match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', cell)
    if match:
        return clean_str(match.group(1)), match.group(2).strip()
    return cell, ""


def extract_all_links(cell: str):
    """Extract all markdown links from a cell."""
    links = []
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', cell):
        links.append({"text": clean_str(m.group(1)), "url": m.group(2).strip()})
    return links


def parse_blacklist(file_path: Path):
    if not file_path.exists():
        return {"active": [], "canceled": []}

    content = file_path.read_text(encoding="utf-8", errors="replace")
    
    # Split by section
    sections = content.split("##")
    
    canceled_list = []
    active_list = []
    
    lines = content.splitlines()
    in_canceled_table = False
    in_active_table = False

    for line in lines:
        line_clean = line.strip()
        if "已取消996名单列表" in line_clean:
            in_canceled_table = True
            in_active_table = False
            continue
        elif "名单列表" in line_clean and "已取消" not in line_clean:
            in_canceled_table = False
            in_active_table = True
            continue

        if not line_clean.startswith("|") or line_clean.startswith("|:---") or line_clean.startswith("| :-"):
            continue

        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 5:
            continue
        # cols[0] is empty if line starts with |
        cols = [c for c in cols if c != ""]
        if not cols:
            continue
        if "所在城市" in cols[0] or "城市" in cols[0]:
            continue

        city = cols[0]
        comp_cell = cols[1] if len(cols) > 1 else ""
        date_cell = cols[2] if len(cols) > 2 else ""
        schedule_cell = cols[3] if len(cols) > 3 else ""
        evidence_cell = cols[4] if len(cols) > 4 else ""

        comp_name, comp_url = parse_link(comp_cell)
        if not comp_name:
            continue

        evidence_links = extract_all_links(evidence_cell)

        item = {
            "city": city,
            "company_name": comp_name,
            "company_url": comp_url,
            "date": date_cell,
            "schedule": schedule_cell,
            "evidence": evidence_cell,
            "evidence_links": evidence_links
        }

        if in_canceled_table:
            if len(cols) > 5:
                item["canceled_evidence"] = cols[5]
            canceled_list.append(item)
        elif in_active_table:
            active_list.append(item)

    return {"active": active_list, "canceled": canceled_list}


def parse_whitelist(file_path: Path):
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    items = []
    in_table = False

    for line in lines:
        line_clean = line.strip()
        if "名单列表" in line_clean:
            in_table = True
            continue
        if not in_table or not line_clean.startswith("|"):
            continue
        if ":---" in line_clean or "城市" in line_clean:
            continue

        cols = [c.strip() for c in line.split("|") if c.strip() != ""]
        if len(cols) < 4:
            continue

        city = cols[0]
        comp_name, comp_url = parse_link(cols[1])
        date_val = cols[2]
        schedule = cols[3]
        evidence = cols[4] if len(cols) > 4 else ""
        evidence_links = extract_all_links(evidence)

        items.append({
            "city": city,
            "company_name": comp_name,
            "company_url": comp_url,
            "date": date_val,
            "schedule": schedule,
            "evidence": evidence,
            "evidence_links": evidence_links
        })

    return items


def parse_remotelist(remotelist_dir: Path):
    if not remotelist_dir.exists():
        return []

    items = []
    for md_file in remotelist_dir.glob("**/remotelist.md"):
        city_match = re.search(r'##\s*([^\s]+)市?支持远程', md_file.read_text(encoding="utf-8", errors="replace"))
        city_from_dir = md_file.parent.name.capitalize()
        city = city_match.group(1) if city_match else city_from_dir

        lines = md_file.read_text(encoding="utf-8", errors="replace").splitlines()
        for line in lines:
            line_clean = line.strip()
            if not line_clean.startswith("|") or "---" in line_clean or "公司名称" in line_clean:
                continue
            cols = [c.strip() for c in line.split("|") if c.strip() != ""]
            if len(cols) < 2:
                continue
            comp_name, _ = parse_link(cols[0])
            if not comp_name:
                continue
            site_name, site_url = parse_link(cols[1])
            positions = cols[2] if len(cols) > 2 else "All / Various"

            items.append({
                "city": city,
                "company_name": comp_name,
                "company_url": site_url,
                "positions": positions
            })

    return items


def parse_awesomelist(file_path: Path):
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8", errors="replace")
    items = []
    lines = content.splitlines()
    in_table = False

    for line in lines:
        line_clean = line.strip()
        if "| LOGO |" in line_clean:
            in_table = True
            continue
        if not in_table or not line_clean.startswith("|"):
            continue
        if ":---" in line_clean or "项目" in line_clean:
            continue

        cols = [c.strip() for c in line.split("|")]
        # Remove boundary empty entries
        if cols and cols[0] == "":
            cols = cols[1:]
        if cols and cols[-1] == "":
            cols = cols[:-1]

        if len(cols) < 5:
            continue

        proj_cell = cols[1]
        official_cell = cols[2]
        stars_cell = cols[3]
        desc_cell = cols[4]
        license_cell = cols[5] if len(cols) > 5 else "Anti-996"

        proj_name, proj_url = parse_link(proj_cell)
        official_name, official_url = parse_link(official_cell)
        target_url = proj_url or official_url

        if not proj_name:
            continue

        items.append({
            "project_name": proj_name,
            "project_url": target_url,
            "description": clean_str(desc_cell),
            "stars_badge": stars_cell,
            "license": clean_str(license_cell)
        })

    return items


def parse_proposals(proposal_dir: Path):
    if not proposal_dir.exists():
        return []

    proposals = []
    for f in proposal_dir.glob("*.md"):
        if f.name.lower() == "readme.md" or "template" in f.name.lower():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        title = f.stem.replace("_", " ").title()
        first_line = text.strip().splitlines()[0] if text.strip() else ""
        if first_line.startswith("#"):
            title = first_line.lstrip("#").strip()

        proposals.append({
            "title": title,
            "filename": f.name,
            "path": str(f.relative_to(BASE_DIR)),
            "summary": clean_str(text[:300]) + "..."
        })
    return proposals


def analyze_dataset():
    blacklist_data = parse_blacklist(REPO_DIR / "blacklist" / "README.md")
    whitelist_data = parse_whitelist(REPO_DIR / "whitelist" / "README.md")
    remotelist_data = parse_remotelist(REPO_DIR / "remotelist")
    awesomelist_data = parse_awesomelist(REPO_DIR / "awesomelist" / "README.md")
    proposals_data = parse_proposals(REPO_DIR / "proposal")

    active_blacklist = blacklist_data["active"]
    canceled_blacklist = blacklist_data["canceled"]

    # Statistics
    cities_blacklisted = Counter([item["city"] for item in active_blacklist if item["city"]])
    cities_whitelisted = Counter([item["city"] for item in whitelist_data if item["city"]])

    # Classify schedule violations
    schedules = []
    for item in active_blacklist:
        s = item["schedule"]
        if "11116" in s or "两班倒" in s:
            schedules.append("11-11-6 / Two-Shift Extreme")
        elif "997" in s:
            schedules.append("997 (7 Days/Week)")
        elif "996" in s:
            schedules.append("996 Standard (72h/wk)")
        elif "大小周" in s:
            schedules.append("Alternating 6-day (大小周)")
        elif "无偿" in s or "义务" in s:
            schedules.append("Unpaid Mandatory Overtime")
        elif "966" in s or "9106" in s or "10106" in s:
            schedules.append("Other 6-day Schedules (966/10106)")
        else:
            schedules.append("Custom Excessive Overtime")

    schedule_counts = Counter(schedules)

    dataset = {
        "metadata": {
            "source": "996.ICU",
            "repository": "https://github.com/996icu/996.ICU",
            "license": "Anti-996 License 1.0 (Draft)"
        },
        "stats": {
            "active_blacklisted_companies": len(active_blacklist),
            "canceled_blacklisted_companies": len(canceled_blacklist),
            "whitelisted_wlb_companies": len(whitelist_data),
            "remote_friendly_companies": len(remotelist_data),
            "anti996_licensed_projects": len(awesomelist_data),
            "community_proposals": len(proposals_data),
            "top_blacklist_cities": dict(cities_blacklisted.most_common(10)),
            "top_whitelist_cities": dict(cities_whitelisted.most_common(10)),
            "schedule_patterns": dict(schedule_counts)
        },
        "active_blacklist": active_blacklist,
        "canceled_blacklist": canceled_blacklist,
        "whitelist": whitelist_data,
        "remotelist": remotelist_data,
        "awesomelist": awesomelist_data,
        "proposals": proposals_data
    }

    # Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved structured dataset to: {OUTPUT_JSON}")

    # Generate Markdown Report
    generate_report(dataset)


def generate_report(data):
    stats = data["stats"]
    active_bl = data["active_blacklist"]
    wl = data["whitelist"]
    remote = data["remotelist"]
    awesome = data["awesomelist"]
    proposals = data["proposals"]

    md = []
    md.append("# 996.ICU Comprehensive Labor Rights & Ecosystem Intelligence Report")
    md.append("")
    md.append("> **Analysis Date:** 2026-11-14 | **Source:** `996.ICU` Official Repository Archive")
    md.append("")
    md.append("## Executive Summary")
    md.append("")
    md.append("The **996.ICU** movement began as a grassroots open source initiative addressing unlawful overtime practices in technology enterprises. ")
    md.append("Under Chinese labor law (Articles 36, 41, and 44 of the *Labor Law of the PRC*), the statutory standard work week is **40 hours** (8 hours/day, 5 days/week), with daily overtime capped at **3 hours** and monthly overtime strictly capped at **36 hours**, requiring overtime premiums of 150% (weekdays), 200% (rest days), or 300% (statutory holidays). ")
    md.append("A **996 schedule** entails at least **72 hours per week** (over 128 hours of overtime monthly), representing a direct breach of statutory thresholds when enforced without compensation or union negotiation.")
    md.append("")
    md.append("### Key Intelligence Metrics")
    md.append("")
    md.append(f"| Metric | Count | Context |")
    md.append(f"| :--- | :--- | :--- |")
    md.append(f"| **Active Blacklisted Companies** | **{stats['active_blacklisted_companies']}** | Documented companies enforcing unlawful overtime |")
    md.append(f"| **Canceled / Remediated Companies** | **{stats['canceled_blacklisted_companies']}** | Companies that formally revoked 996 policies with proof |")
    md.append(f"| **Whitelisted (955/965) Companies** | **{stats['whitelisted_wlb_companies']}** | Verified standard work-life balance employers |")
    md.append(f"| **Remote-Friendly Employers** | **{stats['remote_friendly_companies']}** | Distributed tech employers across Tier-1 metro areas |")
    md.append(f"| **Anti-996 Licensed Open Source Projects** | **{stats['anti996_licensed_projects']}** | OSS repositories incorporating the Anti-996 license clause |")
    md.append(f"| **Statutory & Community Reform Proposals** | **{stats['community_proposals']}** | Concrete legal, union, and blockchain proposals |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. Geographic & Overtime Pattern Distribution")
    md.append("")
    md.append("### Top Cities with Reported 996 Practices")
    md.append("| City | Reported Companies | Primary Sectors |")
    md.append("| :--- | :--- | :--- |")
    for city, count in stats["top_blacklist_cities"].items():
        md.append(f"| **{city}** | {count} | Internet, E-commerce, Gaming, Fintech |")
    md.append("")
    md.append("### Breakdown of Overtime Regimes")
    md.append("| Overtime Regime | Incident Count | Typical Weekly Hours | Statutory Overrun |")
    md.append("| :--- | :--- | :--- | :--- |")
    for pattern, count in stats["schedule_patterns"].items():
        if "11-11-6" in pattern or "997" in pattern:
            hours = "~84h+"
            over = "+44h+"
        elif "996" in pattern:
            hours = "~72h"
            over = "+32h"
        elif "大小周" in pattern:
            hours = "~50-60h"
            over = "+10-20h"
        else:
            hours = "~48-60h"
            over = "+8-20h"
        md.append(f"| **{pattern}** | {count} | {hours} | {over} over legal limit |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 2. Whitelist: Verified 965 / 955 Work-Life Balance Directory")
    md.append("")
    md.append("The following employers maintain verified records of standard working hours (9:00 AM – 5:00 PM or 9:00 AM – 6:00 PM with lunch break):")
    md.append("")
    md.append("| City | Company | Schedule | Verification Proof |")
    md.append("| :--- | :--- | :--- | :--- |")
    for item in wl:
        name = f"[{item['company_name']}]({item['company_url']})" if item['company_url'] else item['company_name']
        evidence_txt = item['evidence'].replace("|", "/")
        md.append(f"| {item['city']} | {name} | `{item['schedule']}` | {evidence_txt} |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 3. Remote-Friendly Employers")
    md.append("")
    md.append("| City Hub | Company | Website | Eligible Roles |")
    md.append("| :--- | :--- | :--- | :--- |")
    for r in remote:
        comp = f"[{r['company_name']}]({r['company_url']})" if r['company_url'] else r['company_name']
        site = r['company_url'] or "N/A"
        md.append(f"| {r['city']} | {comp} | {site} | {r['positions']} |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 4. Notable Anti-996 Open Source Projects")
    md.append("")
    md.append("A growing catalog of open source tools, frameworks, and developer utilities that protect worker sovereignty by conditioning code reuse on labor law compliance:")
    md.append("")
    md.append("| Project | Description | Stars / Status |")
    md.append("| :--- | :--- | :--- |")
    for p in awesome[:25]:
        pname = f"[{p['project_name']}]({p['project_url']})" if p['project_url'] else p['project_name']
        desc = p['description'] or "Open source software library under Anti-996 license"
        md.append(f"| **{pname}** | {desc} | Protected under Anti-996 |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 5. Anti-996 License Legal Analysis")
    md.append("")
    md.append("### Clause Mechanics")
    md.append("The Anti-996 License combines permissive software usage rights with mandatory labor compliance obligations:")
    md.append("1. **Condition 2 (Labor Law Compliance):**")
    md.append("   > *\"The individual or the legal entity must strictly comply with all applicable laws, regulations, rules and standards of the jurisdiction relating to labor and employment... In case that the jurisdiction has no such laws... required to comply with Core International Labor Standards.\"*")
    md.append("2. **Condition 3 (No Rights Waivers):**")
    md.append("   > *\"Shall not induce, suggest or force its employee(s)... to agree in oral or written form, to directly or indirectly restrict, weaken or relinquish his or her rights... nor limit the rights of reporting violations.\"*")
    md.append("")
    md.append("### Legal Enforcement Model")
    md.append("- **Condition vs. Covenant:** When structured as a condition precedent to the copyright grant, a licensee in breach of labor laws automatically loses license permission, rendering continued deployment of the software an act of copyright infringement under applicable copyright acts (such as 17 U.S.C. § 101 et seq. or PRC Copyright Law).")
    md.append("- **Dual-Licensing Strategy:** Projects can offer a dual-licensing structure (e.g., MIT + Anti-996 Rider, or Apache 2.0 with Labor Rights Rider) allowing seamless compliance validation across enterprise CI/CD.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 6. Community Proposals & Roadmaps")
    md.append("")
    for prop in proposals:
        md.append(f"### {prop['title']}")
        md.append(f"- **File:** [`{prop['path']}`](file:///{BASE_DIR.as_posix()}/{prop['path']})")
        md.append(f"- **Summary:** {prop['summary']}")
        md.append("")

    report_text = "\n".join(md)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"[+] Saved comprehensive report to: {OUTPUT_REPORT}")


if __name__ == "__main__":
    analyze_dataset()
