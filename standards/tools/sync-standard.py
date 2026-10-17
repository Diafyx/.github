#!/usr/bin/env python3
"""Assemble a repository's AGENTS.md and CLAUDE.md from the Diafyx standard.

AGENTS.md = Part A (project facts, owned by the repository)
          + Part B (core rules, copied from standards/core.md)
          + Part C (profile rules, copied from standards/profiles/<profile>.md)

Parts B and C sit between BEGIN/END markers and are replaced on every sync.
Part A, and anything else outside the markers, is never changed.
CLAUDE.md imports AGENTS.md so Claude Code and Codex follow the same rules.

Usage:
  python3 sync-standard.py <repo-dir> --profile python-pypi
  python3 sync-standard.py <repo-dir> --profile content-site --check

Exit codes: 0 in sync or written, 1 out of date (--check), 2 error.
This tool never runs Git and never touches the network.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

STANDARDS = Path(__file__).resolve().parent.parent
PROFILES = sorted(p.stem for p in (STANDARDS / "profiles").glob("*.md"))
CODEX_LIMIT = 32 * 1024  # Codex project_doc_max_bytes default
WARN_AT = 30 * 1024
CLAUDE_IMPORT = "@AGENTS.md"
BLOCK = re.compile(
    r"<!-- BEGIN DIAFYX STANDARD: (?P<kind>core|profile)[^>]*-->\n"
    r".*?"
    r"<!-- END DIAFYX STANDARD: (?P=kind) -->\n",
    re.DOTALL,
)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(2)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def standard_version() -> str:
    match = re.search(r"standard v(\d+\.\d+\.\d+)", read(STANDARDS / "core.md"))
    if not match:
        fail("core.md does not state 'standard vX.Y.Z' in its heading")
    return match.group(1)


def block(kind: str, label: str, body: str, version: str) -> str:
    begin = (
        f"<!-- BEGIN DIAFYX STANDARD: {kind} {label} v{version} "
        "(synced from Diafyx/.github/standards; do not edit here) -->\n"
    )
    return f"{begin}{body.rstrip()}\n<!-- END DIAFYX STANDARD: {kind} -->\n"


def desired_agents(current: str | None, repo: Path, profile: str) -> str:
    version = standard_version()
    core = block("core", "rules", read(STANDARDS / "core.md"), version)
    prof = block("profile", profile, read(STANDARDS / "profiles" / f"{profile}.md"), version)

    if current is None:
        facts = read(STANDARDS / "project-facts.md")
        facts = facts.replace("# AGENTS.md: PROJECT_NAME", f"# AGENTS.md: {repo.name}", 1)
        facts = facts.replace(
            "| `PROFILE` | TBD: `python-pypi`, `content-site` or `web-app` |",
            f"| `PROFILE` | `{profile}` |",
            1,
        )
        return f"{facts.rstrip()}\n\n{core}\n{prof}"

    kinds = [m.group("kind") for m in BLOCK.finditer(current)]
    if kinds != ["core", "profile"]:
        fail(
            "AGENTS.md exists but does not contain exactly one core block followed by "
            "one profile block. Move its content into Part A of a fresh file, then re-run."
        )
    replacements = iter([core, prof])
    return BLOCK.sub(lambda _m: next(replacements), current)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("repo_dir", type=Path)
    parser.add_argument("--profile", required=True, choices=PROFILES)
    parser.add_argument("--check", action="store_true", help="report drift, write nothing")
    args = parser.parse_args()

    repo = args.repo_dir.resolve()
    if not repo.is_dir():
        fail(f"{repo} is not a directory")

    agents_path = repo / "AGENTS.md"
    claude_path = repo / "CLAUDE.md"
    current = read(agents_path) if agents_path.exists() else None
    agents = desired_agents(current, repo, args.profile)

    size = len(agents.encode("utf-8"))
    if size > CODEX_LIMIT:
        fail(f"AGENTS.md would be {size} bytes; Codex reads only {CODEX_LIMIT}. Shorten Part A.")

    problems: list[str] = []
    if current != agents:
        problems.append("AGENTS.md is out of date" if current else "AGENTS.md is missing")

    claude_current = read(claude_path) if claude_path.exists() else None
    claude_ok = claude_current is not None and CLAUDE_IMPORT in claude_current.split()
    if claude_current is not None and not claude_ok:
        fail(f"CLAUDE.md exists without an '{CLAUDE_IMPORT}' import line; add it by hand.")
    if claude_current is None:
        problems.append("CLAUDE.md is missing")

    gitignore = repo / ".gitignore"
    if not gitignore.exists() or ".tmp/" not in read(gitignore).split():
        print("warning: .gitignore does not ignore .tmp/ (agent scratch files)")
    if size > WARN_AT:
        print(f"warning: AGENTS.md is {size} bytes, close to the {CODEX_LIMIT}-byte Codex limit")

    if args.check:
        for problem in problems:
            print(problem)
        print("in sync" if not problems else "out of date")
        sys.exit(1 if problems else 0)

    if current != agents:
        agents_path.write_bytes(agents.encode("utf-8"))
        print(f"wrote {agents_path} ({size} bytes)")
    if claude_current is None:
        claude_path.write_bytes(f"{CLAUDE_IMPORT}\n".encode("utf-8"))
        print(f"wrote {claude_path}")
    if not problems:
        print("already in sync")


if __name__ == "__main__":
    main()
