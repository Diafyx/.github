#!/usr/bin/env python3
"""Sync a repository's labels with the Diafyx canonical set (labels.json).

Without --apply it only prints the plan. With --apply it creates missing labels and
updates color/description/name-case of existing ones, then reads the labels back.
Labels outside the set are reported, never deleted.

Usage:
  python3 sync-labels.py Diafyx/REPO --profile python-pypi
  python3 sync-labels.py Diafyx/REPO --profile python-pypi --area "area: cli=CLI commands and output" --apply

Requires the GitHub CLI (gh), authenticated. Never runs Git.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

STANDARDS = Path(__file__).resolve().parent.parent
AREA_COLOR = "bfdadc"
PROFILES = sorted(p.stem for p in (STANDARDS / "profiles").glob("*.md"))


def gh(*args: str) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(f"error: gh {' '.join(args)}\n{result.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return result.stdout


def wanted_labels(profile: str, extra_areas: list[str]) -> list[dict[str, str]]:
    data = json.loads((STANDARDS / "labels.json").read_text(encoding="utf-8"))
    labels = [label for group in data["groups"].values() for label in group]
    labels += data["profile_areas"][profile]
    for spec in extra_areas:
        name, _, description = spec.partition("=")
        name = name.strip()
        if not name.startswith("area: "):
            print(f"error: extra area '{name}' must start with 'area: '", file=sys.stderr)
            sys.exit(2)
        labels.append(
            {
                "name": name,
                "color": AREA_COLOR,
                "description": f"Area: {description.strip() or name[6:]}",
            }
        )
    names = [label["name"].lower() for label in labels]
    if len(names) != len(set(names)):
        print("error: duplicate label names in the wanted set", file=sys.stderr)
        sys.exit(2)
    return labels


def existing_labels(repo: str) -> dict[str, dict[str, str]]:
    raw = gh("label", "list", "--repo", repo, "--limit", "500", "--json", "name,color,description")
    return {label["name"].lower(): label for label in json.loads(raw or "[]")}


def plan(repo: str, wanted: list[dict[str, str]]) -> tuple[list[tuple[str, dict[str, str]]], list[str]]:
    have = existing_labels(repo)
    actions: list[tuple[str, dict[str, str]]] = []
    for label in wanted:
        current = have.get(label["name"].lower())
        if current is None:
            actions.append(("create", label))
        elif (
            current["name"] != label["name"]
            or current["color"].lower() != label["color"].lower()
            or (current.get("description") or "") != label["description"]
        ):
            actions.append(("update", {**label, "old_name": current["name"]}))
    wanted_names = {label["name"].lower() for label in wanted}
    extras = sorted(label["name"] for key, label in have.items() if key not in wanted_names)
    return actions, extras


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("repo", help="owner/name, e.g. Diafyx/cachelint")
    parser.add_argument("--profile", required=True, choices=PROFILES)
    parser.add_argument("--area", action="append", default=[], help='"area: x=Description"')
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    wanted = wanted_labels(args.profile, args.area)
    actions, extras = plan(args.repo, wanted)

    for action, label in actions:
        print(f"{action:7} {label['name']!r}  #{label['color']}  {label['description']}")
    for name in extras:
        print(f"extra   {name!r}  (not in the standard set; review by hand)")
    if not actions:
        print("labels in sync")

    if not args.apply or not actions:
        if actions:
            print("\nplan only; re-run with --apply to make these changes")
        return

    for action, label in actions:
        if action == "create":
            gh("label", "create", label["name"], "--repo", args.repo,
               "--color", label["color"], "--description", label["description"])
        else:
            gh("label", "edit", label["old_name"], "--repo", args.repo, "--name", label["name"],
               "--color", label["color"], "--description", label["description"])
        print(f"done    {label['name']!r}")
        time.sleep(1)

    remaining, _ = plan(args.repo, wanted)
    if remaining:
        print(f"error: {len(remaining)} label(s) still differ after apply", file=sys.stderr)
        sys.exit(1)
    print("verified: all standard labels match")


if __name__ == "__main__":
    main()
