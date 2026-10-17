# AGENTS.md: PROJECT_NAME

Instructions for coding agents (Codex reads this file; Claude Code reads it through `CLAUDE.md`). It has three parts:
- **Part A:** project facts, owned by this repository.
- **Part B:** the Diafyx core rules.
- **Part C:** the project-type profile.

Parts B and C are synced from `Diafyx/.github/standards/` by `sync-standard.py`. Never edit them here.

## Part A: Project facts

Edit this part in this repository. `TBD` means not decided yet: ask the maintainer before relying on it.

| Key | Value |
|---|---|
| `PROJECT_NAME` | TBD |
| `PURPOSE` | TBD: one sentence on the user problem and who it is for |
| `REPOSITORY` | `Diafyx/TBD` |
| `PROJECT_ROOT` | the directory containing this file |
| `DEFAULT_BRANCH` | `main` |
| `MAINTAINER` | `SEPURI-SAI-KRISHNA` |
| `COMMIT_NAME` | `Sepuri Sai Krishna` |
| `PROFILE` | TBD: `python-pypi`, `content-site` or `web-app` |
| `LICENSE` | TBD: `Apache-2.0` for code, `CC-BY-4.0` for prose-first |
| `STATUS` | TBD: e.g. pre-alpha, no release yet |
| `AREA_LABELS` | `area: core`, `area: ci`, `area: docs` (add project-specific areas here) |
| `REQUIRED_CHECKS` | `CI result`, `Org checks / DCO` |

### Profile values

<!-- Keep only the rows for this project's profile, and delete the other rows and this comment. -->

| Key | Value |
|---|---|
| `DISTRIBUTION_NAME` | TBD (python-pypi: the PyPI name) |
| `IMPORT_NAME` | TBD (python-pypi: the import package) |
| `PYTHON_FLOOR` | TBD (python-pypi: oldest supported CPython) |
| `OPTIONAL_INTEGRATIONS` | none (python-pypi: extras that must stay optional) |
| `SITE_URL` | TBD (content-site: the published URL) |
| `CONTENT_GUIDE` | `CONTENT_GUIDE.md` (content-site) |
| `PRODUCTION_URL` | TBD (web-app: the live URL) |
| `DEPLOY` | TBD (web-app: e.g. Cloudflare Pages Git integration) |
| `COVERAGE_FLOOR` | TBD (web-app: line coverage for logic and data modules) |

### Local commands

Run these from `PROJECT_ROOT`. CI runs the same checks.

| Purpose | Command |
|---|---|
| Set up | TBD |
| Format check | TBD |
| Lint | TBD |
| Type check | TBD |
| Test | TBD |
| Build | TBD |

### Project-specific rules

None yet. Add rules that apply only to this project here, each with its reason.
