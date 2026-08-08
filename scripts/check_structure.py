#!/usr/bin/env python3
"""
BugLibrary structure verifier.
Safe, local-only. No network. No exploits.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "templates/bug-report-template.md",
    "templates/recon-template.md",
]

REQUIRED_DIRS = [
    "docs/00-Introduction",
    "docs/01-Mindset-and-Methodology",
    "docs/02-Reconnaissance",
    "docs/03-Web-Application-Hunting",
    "docs/04-API-GraphQL-Hunting",
    "docs/05-Mobile-Hunting",
    "docs/06-Cloud-and-Infrastructure",
    "docs/07-Binary-and-Reverse-Engineering",
    "docs/08-Advanced-Techniques",
    "docs/09-Automation-and-Tooling",
    "docs/10-Reporting-and-Communication",
    "docs/11-Legal-Ethics-and-OPSEC",
    "docs/12-Checklists-and-CheatSheets",
    "docs/13-Case-Studies",
    "docs/14-Resources-and-Continuous-Learning",
    "tools",
    "scripts",
    "templates",
    "assets",
]

REQUIRED_DOC_MARKERS = [
    ("docs/08-Advanced-Techniques/ai-agents-bug-hunting.md", "AI Agents"),
    ("docs/14-Resources-and-Continuous-Learning/living-document.md", "Living Document"),
]


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing file: {rel}")

    for rel in REQUIRED_DIRS:
        if not (ROOT / rel).is_dir():
            errors.append(f"missing dir: {rel}")

    # Each docs section should have a README and at least one other md
    for rel in REQUIRED_DIRS:
        if not rel.startswith("docs/"):
            continue
        d = ROOT / rel
        if not d.is_dir():
            continue
        mds = list(d.glob("*.md"))
        if not any(p.name == "README.md" for p in mds):
            errors.append(f"missing section README: {rel}")
        if len(mds) < 2:
            errors.append(f"section too thin (<2 md files): {rel}")

    for rel, marker in REQUIRED_DOC_MARKERS:
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing marker file: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if marker.lower() not in text.lower():
            errors.append(f"marker '{marker}' not found in {rel}")

    # README bilingual rough check
    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    if "## English" not in readme and "# English" not in readme:
        # accept FR/EN headers used in our README
        if "English" not in readme or "Français" not in readme:
            errors.append("README.md does not look bilingual (EN/FR)")

    # LICENSE MIT hint
    lic = (ROOT / "LICENSE").read_text(encoding="utf-8", errors="replace")
    if "MIT License" not in lic:
        errors.append("LICENSE does not look like MIT")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("OK")
    print(f"root={ROOT}")
    print(f"checked_files={len(REQUIRED_FILES)}")
    print(f"checked_dirs={len(REQUIRED_DIRS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
