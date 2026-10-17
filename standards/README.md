# Diafyx engineering standard

The rules every Diafyx repository follows, written so that both the maintainer and coding agents (Codex, Claude Code) can apply them exactly.

**Current version: 1.0.0.** The version is in the heading of [`core.md`](core.md) and in each synced block.

## Files

| File | What it is |
|---|---|
| [`core.md`](core.md) | Part B: core rules for every repository (boundaries, issues, labels, sizes, branches, commits, PRs, CI, versioning, releases, security) |
| [`profiles/python-pypi.md`](profiles/python-pypi.md) | Part C for Python libraries published to PyPI |
| [`profiles/content-site.md`](profiles/content-site.md) | Part C for prose-first sites deployed to GitHub Pages |
| [`profiles/web-app.md`](profiles/web-app.md) | Part C for browser applications deployed as static sites |
| [`project-facts.md`](project-facts.md) | Part A template: the per-repository facts an agent needs |
| [`repository-baseline.md`](repository-baseline.md) | Settings, rulesets, security, labels and files every repository must have, with exact commands |
| [`labels.json`](labels.json) | The canonical label set |
| [`rulesets/`](rulesets) | The canonical rulesets, as JSON for the GitHub API |
| [`prompts.md`](prompts.md) | Short prompts to start and steer a Codex or Claude Code session |
| [`tools/sync-standard.py`](tools/sync-standard.py) | Builds a repository's `AGENTS.md` (Parts A, B and C) and `CLAUDE.md` |
| [`tools/sync-labels.py`](tools/sync-labels.py) | Plans and applies the label set for a repository |

## How a repository uses it

Each repository carries its own `AGENTS.md`:
- **Part A:** facts the repository owns.
- **Part B:** the core rules, copied from here.
- **Part C:** one profile, copied from here.

Its `CLAUDE.md` is the single line `@AGENTS.md`. Codex reads `AGENTS.md` directly, and Claude Code reads it through that import, so both agents follow identical text.

Copies are used instead of links because agents are confined to the project directory and may run offline. Agents are allowed to read [`repository-baseline.md`](repository-baseline.md) read-only through `gh` when setting up or retrofitting a repository.

```
python3 ~/org_setup/.github/standards/tools/sync-standard.py ~/org_setup/REPO --profile python-pypi
```

The tool:
- creates `AGENTS.md` from the Part A template, or replaces only the Part B and Part C blocks of an existing one;
- creates `CLAUDE.md` if it is missing;
- refuses to produce an `AGENTS.md` larger than 32 KiB. Codex silently truncates beyond its default `project_doc_max_bytes`, so keep Part A short.

`--check` reports drift without writing. Run it on a branch, then commit through a normal PR.

## Changing the standard

1. Open a `design:` issue in `Diafyx/.github` describing the change and why.
2. Change the files here in one PR, and bump the version:
   - **patch:** wording that does not change any rule;
   - **minor:** a new or changed rule;
   - **major:** a change that requires repositories to restructure.
3. After merge, open one `maintenance:` issue per repository to re-sync (`sync-standard.py`, `sync-labels.py`, rulesets).

## Decisions and their reasons

| Decision | Reason |
|---|---|
| Squash and merge only | GitHub signs the squash commit, so `main` is always Verified and linear. Rebase merging recreates commits **without** signature verification, because GitHub cannot sign with the contributor's key ([GitHub docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github)). |
| Signed commits required, plus DCO sign-off | The signature proves who made the commit. The sign-off certifies the right to contribute ([developercertificate.org](https://developercertificate.org/)). They are separate guarantees. Squash messages keep the sign-offs (`COMMIT_MESSAGES`). |
| No Git or GitHub writes by agents | The maintainer reviews and runs every state-changing command. Agents prepare commands and verifying helpers. |
| One aggregate `CI result` check | Required checks stay stable while jobs and matrices change. |
| Size labels on one scale for issues and PRs | One vocabulary for planning and review; XL must be justified, XXL must be split. |
| Changelog only in release PRs | Avoids per-PR noise and merge conflicts. PRs record user impact in the template, and labels drive release notes. |
| Explicit `0.x` and `1.0` rules | `0.x` minor releases carry features and breaking changes; `1.0` needs documented API, stability over two minors, real use and written support and deprecation policies. |
| Apache-2.0 for code, CC BY 4.0 for prose | Apache-2.0 adds an explicit patent grant. CC BY 4.0 is the standard license for reusable writing. Existing MIT repositories stay MIT. |
| 32 KiB limit on `AGENTS.md` | The Codex default `project_doc_max_bytes` ([OpenAI docs](https://developers.openai.com/codex/guides/agents-md)). |
