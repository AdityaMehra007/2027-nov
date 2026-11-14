#!/usr/bin/env python3
"""
Anti-996 Licensing & Compliance CLI Utility
Provides tooling to:
  1. `check`: Audit local repositories for license files and Anti-996 labor compliance clauses.
  2. `apply`: Apply standalone Anti-996 License or dual-license rider to an existing license file.
  3. `badge`: Generate Markdown / HTML badges for README.md.
  4. `audit-company`: Check if a target company is listed in the 996 Blacklist or 955 WLB Whitelist.
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "996_icu_dataset.json"

ANTI_996_FULL_LICENSE = """Copyright (c) {year} {holder}

"Anti 996" License Version 1.0 (Draft)

Permission is hereby granted to any individual or legal entity
obtaining a copy of this licensed work (including the source code,
documentation and/or related items, hereinafter collectively referred
to as the "licensed work"), free of charge, to deal with the licensed
work for any purpose, including without limitation, the rights to use,
reproduce, modify, prepare derivative works of, distribute, publish
and sublicense the licensed work, subject to the following conditions:

1. The individual or the legal entity must conspicuously display,
without modification, this License and the notice on each redistributed
or derivative copy of the Licensed Work.

2. The individual or the legal entity must strictly comply with all
applicable laws, regulations, rules and standards of the jurisdiction
relating to labor and employment where the individual is physically
located or where the individual was born or naturalized; or where the
legal entity is registered or is operating (whichever is stricter). In
case that the jurisdiction has no such laws, regulations, rules and
standards or its laws, regulations, rules and standards are
unenforceable, the individual or the legal entity are required to
comply with Core International Labor Standards.

3. The individual or the legal entity shall not induce, suggest or force
its employee(s), whether full-time or part-time, or its independent
contractor(s), in any methods, to agree in oral or written form, to
directly or indirectly restrict, weaken or relinquish his or her
rights or remedies under such laws, regulations, rules and standards
relating to labor and employment as mentioned above, no matter whether
such written or oral agreements are enforceable under the laws of the
said jurisdiction, nor shall such individual or the legal entity
limit, in any methods, the rights of its employee(s) or independent
contractor(s) from reporting or complaining to the copyright holder or
relevant authorities monitoring the compliance of the license about
its violation(s) of the said license.

THE LICENSED WORK IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN ANY WAY CONNECTION WITH THE
LICENSED WORK OR THE USE OR OTHER DEALINGS IN THE LICENSED WORK.
"""

ANTI_996_RIDER = """
==============================================================================
ANTI-996 LABOR RIGHTS COMPLIANCE RIDER (Version 1.0)
==============================================================================
In addition to the permissions and conditions granted in the base license above,
use and redistribution of this licensed work are subject to the following mandatory conditions:

1. The individual or legal entity must strictly comply with all applicable laws,
   regulations, rules, and standards of the jurisdiction relating to labor and
   employment where the individual is physically located, born, or naturalized,
   or where the legal entity is registered or operating (whichever is stricter).
   Where local laws are absent or unenforced, the licensee must strictly comply
   with the Core International Labor Standards (ILO).

2. The licensee shall not induce, suggest, or compel any employee or contractor
   to waive, restrict, or relinquish statutory labor rights, overtime caps, or
   fair wage compensations, nor restrict any worker from reporting violations.
==============================================================================
"""

BADGES = {
    "license": "[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg?style={style})](https://github.com/996icu/996.ICU/blob/master/LICENSE)",
    "link": "[![996.icu](https://img.shields.io/badge/link-996.icu-%23FF4D5B.svg?style={style})](https://996.icu/#/en_US)",
    "wlb": "[![955.WLB](https://img.shields.io/badge/WLB-955-brightgreen.svg?style={style})](https://github.com/formulahendry/955.WLB)"
}


def cmd_check(args):
    target_dir = Path(args.path).resolve()
    print(f"\n[*] Scanning directory: {target_dir}")
    if not target_dir.exists():
        print(f"[!] Path does not exist: {target_dir}")
        return 1

    license_files = list(target_dir.glob("LICENSE*")) + list(target_dir.glob("license*"))
    readme_files = list(target_dir.glob("README*")) + list(target_dir.glob("readme*"))

    has_anti996_license = False
    has_rider = False
    has_badge = False
    license_type = "None"

    if license_files:
        license_path = license_files[0]
        content = license_path.read_text(encoding="utf-8", errors="replace")
        if "Anti 996" in content or "Anti-996" in content:
            has_anti996_license = True
            license_type = "Anti-996 License"
        elif "ANTI-996 LABOR RIGHTS COMPLIANCE RIDER" in content:
            has_rider = True
            license_type = "Dual/Rider Anti-996"
        elif "MIT" in content:
            license_type = "MIT (Standard)"
        elif "Apache" in content:
            license_type = "Apache 2.0 (Standard)"
        else:
            license_type = "Custom / Other"

    if readme_files:
        readme_path = readme_files[0]
        rcontent = readme_path.read_text(encoding="utf-8", errors="replace")
        if "996.icu" in rcontent.lower() or "anti%20996" in rcontent.lower():
            has_badge = True

    print("\n--- Audit Summary ---")
    print(f"Target Directory:    {target_dir.name}")
    print(f"License Detected:    {license_files[0].name if license_files else 'None'}")
    print(f"License Category:    {license_type}")
    print(f"Anti-996 Full Terms: {'YES [PASSED]' if has_anti996_license else 'NO'}")
    print(f"Labor Rights Rider:  {'YES [PASSED]' if has_rider else 'NO'}")
    print(f"996.ICU Badge:       {'YES [PRESENT]' if has_badge else 'NO'}")
    print("---------------------\n")

    if has_anti996_license or has_rider:
        print("[+] Status: COMPLIANT with Anti-996 Ethical Labor Licensing.")
    else:
        print("[!] Status: Standard license detected. Use 'apply' to add Anti-996 labor protections.")
    return 0


def cmd_apply(args):
    dest = Path(args.dest).resolve()
    year = args.year or "2026"
    holder = args.holder or "Omniverse & Contributors"
    mode = args.mode

    if mode == "standalone":
        content = ANTI_996_FULL_LICENSE.format(year=year, holder=holder)
        dest.write_text(content, encoding="utf-8")
        print(f"[+] Successfully wrote standalone Anti-996 License to: {dest}")
    elif mode == "rider":
        if not dest.exists():
            print(f"[!] Target license file does not exist to append rider: {dest}")
            print("    Creating base MIT license with rider...")
            base = f"MIT License\n\nCopyright (c) {year} {holder}\n\nPermission is hereby granted, free of charge..."
            dest.write_text(base + ANTI_996_RIDER, encoding="utf-8")
        else:
            existing = dest.read_text(encoding="utf-8", errors="replace")
            if "ANTI-996 LABOR RIGHTS COMPLIANCE RIDER" in existing:
                print(f"[!] File already contains Anti-996 Rider: {dest}")
                return 0
            dest.write_text(existing.rstrip() + "\n" + ANTI_996_RIDER, encoding="utf-8")
        print(f"[+] Successfully appended Anti-996 Labor Rights Rider to: {dest}")

    if args.add_badge and args.readme:
        readme_path = Path(args.readme).resolve()
        if readme_path.exists():
            rtext = readme_path.read_text(encoding="utf-8", errors="replace")
            badge_line = f"{BADGES['license'].format(style='flat-square')} {BADGES['link'].format(style='flat-square')}\n\n"
            if "996.icu" not in rtext:
                # Add after title
                lines = rtext.splitlines(keepends=True)
                if lines and lines[0].startswith("#"):
                    new_text = lines[0] + "\n" + badge_line + "".join(lines[1:])
                else:
                    new_text = badge_line + rtext
                readme_path.write_text(new_text, encoding="utf-8")
                print(f"[+] Added Anti-996 badges to: {readme_path}")
    return 0


def cmd_badge(args):
    style = args.style or "flat-square"
    print("\n--- Anti-996 Badges (Markdown) ---")
    print(f"License Badge:\n{BADGES['license'].format(style=style)}\n")
    print(f"Website Badge:\n{BADGES['link'].format(style=style)}\n")
    print(f"WLB 955 Badge:\n{BADGES['wlb'].format(style=style)}\n")
    print("--- HTML Format ---")
    print(f'<a href="https://github.com/996icu/996.ICU"><img src="https://img.shields.io/badge/license-Anti%20996-blue.svg?style={style}" alt="Anti 996 License"></a>')
    print("-----------------------------------\n")
    return 0


def cmd_audit_company(args):
    query = args.company.strip()
    print(f"\n[*] Auditing entity/company against 996.ICU database: '{query}'")

    if not DATASET_PATH.exists():
        print(f"[!] Dataset not found at: {DATASET_PATH}. Run 'python scripts/analyze_996_icu.py' first.")
        return 1

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    active_bl = data.get("active_blacklist", [])
    canceled_bl = data.get("canceled_blacklist", [])
    whitelist = data.get("whitelist", [])
    remotelist = data.get("remotelist", [])

    matched_bl = [c for c in active_bl if query.lower() in c["company_name"].lower()]
    matched_can = [c for c in canceled_bl if query.lower() in c["company_name"].lower()]
    matched_wl = [c for c in whitelist if query.lower() in c["company_name"].lower()]
    matched_rm = [c for c in remotelist if query.lower() in c["company_name"].lower()]

    found = False
    if matched_bl:
        found = True
        print(f"\n[ALERT - BLACKLISTED] Found {len(matched_bl)} matching record(s) on 996 Blacklist:")
        for m in matched_bl:
            print(f"  - Company:  {m['company_name']} ({m.get('city', 'Unknown')})")
            print(f"    Schedule: {m.get('schedule', '996')}")
            print(f"    Date:     {m.get('date', 'N/A')}")
            print(f"    Evidence: {m.get('evidence', 'Documented')[:150]}")
            print()

    if matched_can:
        found = True
        print(f"\n[NOTICE - REMEDIATED] Found {len(matched_can)} record(s) with Canceled 996 policies:")
        for m in matched_can:
            print(f"  - Company: {m['company_name']} ({m.get('city', 'Unknown')})")
            print(f"    Evidence: {m.get('evidence', 'Proof of cancellation submitted')}")
            print()

    if matched_wl:
        found = True
        print(f"\n[COMMENDATION - WHITELISTED] Found {len(matched_wl)} record(s) on 955/965 WLB Whitelist:")
        for m in matched_wl:
            print(f"  - Company:  {m['company_name']} ({m.get('city', 'Unknown')})")
            print(f"    Schedule: {m.get('schedule', '965')}")
            print(f"    Proof:    {m.get('evidence', 'Verified WLB')}")
            print()

    if matched_rm:
        found = True
        print(f"\n[REMOTE-FRIENDLY] Found {len(matched_rm)} remote employer record(s):")
        for m in matched_rm:
            print(f"  - Company:   {m['company_name']} ({m.get('city', 'Unknown')})")
            print(f"    Positions: {m.get('positions', 'All')}")
            print()

    if not found:
        print(f"[i] No records found for '{query}' in the 996.ICU registry.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Anti-996 Licensing & Compliance Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check
    p_check = subparsers.add_parser("check", help="Check directory for Anti-996 license compliance")
    p_check.add_argument("path", nargs="?", default=".", help="Path to project directory")

    # apply
    p_apply = subparsers.add_parser("apply", help="Apply Anti-996 license or rider")
    p_apply.add_argument("dest", help="Destination path (e.g. LICENSE or LICENSE.md)")
    p_apply.add_argument("--mode", choices=["standalone", "rider"], default="rider", help="standalone or rider")
    p_apply.add_argument("--holder", default="Omniverse & Contributors", help="Copyright holder name")
    p_apply.add_argument("--year", default="2026", help="Copyright year")
    p_apply.add_argument("--add-badge", action="store_true", help="Also add badge to README.md")
    p_apply.add_argument("--readme", default="README.md", help="Path to README.md")

    # badge
    p_badge = subparsers.add_parser("badge", help="Generate Anti-996 badge snippets")
    p_badge.add_argument("--style", default="flat-square", choices=["flat", "flat-square", "for-the-badge"])

    # audit-company
    p_audit = subparsers.add_parser("audit-company", help="Audit entity/company against 996.ICU database")
    p_audit.add_argument("company", help="Company name (e.g. 拼多多, 阿里巴巴, IBM, 长城宽带)")

    args = parser.parse_args()

    if args.command == "check":
        sys.exit(cmd_check(args))
    elif args.command == "apply":
        sys.exit(cmd_apply(args))
    elif args.command == "badge":
        sys.exit(cmd_badge(args))
    elif args.command == "audit-company":
        sys.exit(cmd_audit_company(args))


if __name__ == "__main__":
    main()
