#!/usr/bin/env python3
"""
Google Dork Generator — generates Google search ("dork") queries for a target
domain, grouped into the categories this repo's README already describes:
exposed files, login pages, public documents, directory listings, config
disclosure, and technology discovery.

This tool only builds query strings. It does not query Google itself, scrape
search results, or send any network request — you paste the generated
queries into Google (or a search API you're authorized to use) yourself.

Only use generated queries against domains/organizations you are authorized
to assess.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))+$"
)

CATEGORIES: dict[str, dict] = {
    "exposed_files": {
        "label": "Exposed files",
        "templates": [
            'site:{domain} filetype:pdf',
            'site:{domain} filetype:docx',
            'site:{domain} filetype:xlsx',
            'site:{domain} filetype:sql',
            'site:{domain} filetype:log',
            'site:{domain} filetype:env',
            'site:{domain} filetype:bak',
        ],
    },
    "login_pages": {
        "label": "Login pages",
        "templates": [
            'site:{domain} inurl:login',
            'site:{domain} inurl:signin',
            'site:{domain} inurl:admin',
            'site:{domain} intitle:"login"',
        ],
    },
    "public_documents": {
        "label": "Public documents",
        "templates": [
            'site:{domain} filetype:pdf',
            'site:{domain} filetype:doc OR filetype:docx',
            'site:{domain} filetype:ppt OR filetype:pptx',
        ],
    },
    "directory_listings": {
        "label": "Directory listings",
        "templates": [
            'site:{domain} intitle:"index of"',
            'site:{domain} intitle:"index of" "parent directory"',
        ],
    },
    "config_disclosure": {
        "label": "Publicly indexed configuration information",
        "templates": [
            'site:{domain} inurl:.env',
            'site:{domain} inurl:config filetype:yml',
            'site:{domain} inurl:wp-config.php',
            'site:{domain} filetype:env "DB_PASSWORD"',
        ],
    },
    "tech_discovery": {
        "label": "Technology discovery",
        "templates": [
            'site:{domain} inurl:wp-content',
            'site:{domain} inurl:wp-includes',
            'site:{domain} "powered by"',
            'site:{domain} inurl:api',
        ],
    },
}


def normalize_domain(raw: str) -> str:
    d = raw.strip().lower()
    d = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", d)
    d = d.split("/", 1)[0].rstrip(".")
    if not DOMAIN_RE.match(d):
        raise ValueError(f"Not a valid domain: {raw!r}")
    return d


def generate_dorks(domain: str, category: str) -> list[str]:
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category!r} (see --list-categories)")
    return [t.format(domain=domain) for t in CATEGORIES[category]["templates"]]


def generate_all(domain: str) -> dict[str, list[str]]:
    return {cat: generate_dorks(domain, cat) for cat in CATEGORIES}


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="dorkgen",
        description="Generate Google dork queries for an authorized target domain.",
    )
    p.add_argument("--domain", help="Target domain, e.g. example.com")
    p.add_argument("--category", choices=sorted(CATEGORIES), help="Generate only this category.")
    p.add_argument("--all", action="store_true", help="Generate every category.")
    p.add_argument("--list-categories", action="store_true", help="List available categories and exit.")
    p.add_argument("--out", type=Path, help="Write generated dorks to this file instead of stdout.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.list_categories:
        for cat, meta in CATEGORIES.items():
            print(f"{cat:20s} {meta['label']}")
        return 0

    if not args.domain:
        print("[!] --domain is required (unless using --list-categories)", file=sys.stderr)
        return 1

    try:
        domain = normalize_domain(args.domain)
    except ValueError as e:
        print(f"[!] {e}", file=sys.stderr)
        return 1

    lines: list[str] = []
    if args.all or not args.category:
        for cat, dorks in generate_all(domain).items():
            lines.append(f"# {CATEGORIES[cat]['label']}")
            lines.extend(dorks)
            lines.append("")
    else:
        try:
            dorks = generate_dorks(domain, args.category)
        except ValueError as e:
            print(f"[!] {e}", file=sys.stderr)
            return 1
        lines.append(f"# {CATEGORIES[args.category]['label']}")
        lines.extend(dorks)

    output = "\n".join(lines)
    if args.out:
        args.out.write_text(output + "\n")
        print(f"[+] Wrote dorks to {args.out}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
