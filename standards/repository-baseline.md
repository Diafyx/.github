# Repository baseline (standard v1.0.0)

Every Diafyx repository meets this baseline. It is referenced from core rule B13.
- **Agents** read this file to prepare a setup or retrofit helper.
- **The maintainer** applies the helper and verifies the result by read-back.

Commands are bash. `REPO` means the repository name, for example `cachelint`.

## 1. Identity

| Item | Rule |
|---|---|
| Name | lowercase kebab-case, short, unique on PyPI/npm if it will be published |
| Description | one sentence: what it does, for whom; no trailing period needed |
| Topics | 3 to 8 lowercase topics |
| Homepage | only a real site, docs or package page |
| Visibility | public, unless there is a reason to stay private. On the Free plan, rulesets only work on public repositories. |
| Social preview | 1280×640 PNG uploaded in Settings → General |

## 2. Settings

| Setting | Value |
|---|---|
| Issues | on |
| Wiki, Projects, Discussions | off (Discussions only if someone will answer them) |
| Merge commits, rebase merging | off |
| Squash merging | on; title `PR_TITLE`, message `COMMIT_MESSAGES` (keeps DCO sign-offs) |
| Delete head branches on merge | on |
| Always suggest updating PR branches | on |
| Auto-merge | off |
| Require sign-off on web-based commits | on |

Apply and read back:

```
gh api --method PATCH repos/Diafyx/REPO -F has_issues=true -F has_wiki=false -F has_projects=false -F has_discussions=false -F allow_merge_commit=false -F allow_rebase_merge=false -F allow_squash_merge=true -f squash_merge_commit_title=PR_TITLE -f squash_merge_commit_message=COMMIT_MESSAGES -F delete_branch_on_merge=true -F allow_update_branch=true -F allow_auto_merge=false -F web_commit_signoff_required=true --jq '{has_issues,has_wiki,has_projects,has_discussions,allow_merge_commit,allow_rebase_merge,allow_squash_merge,squash_merge_commit_title,squash_merge_commit_message,delete_branch_on_merge,allow_update_branch,allow_auto_merge,web_commit_signoff_required}'
```

## 3. Rulesets

The JSON files are in [`rulesets/`](rulesets). Apply each with `gh api --method POST repos/Diafyx/REPO/rulesets --input <file>`. To replace an existing ruleset, `PUT` to `repos/Diafyx/REPO/rulesets/<id>`.

| Ruleset | File | When |
|---|---|---|
| Protect main | `protect-main.json` | always, right after creation |
| Required checks | `required-checks.json` | once `CI result` and `Org checks / DCO` have each reported at least once |
| Release tags: immutable | `release-tags-immutable.json` | profiles that release (`python-pypi`) |
| Release tags: maintainer only | `release-tags-creation.json` | profiles that release (`python-pypi`) |

"Protect main" requires signed commits. Every commit on a PR branch must be signed, or GitHub refuses the squash merge. GitHub signs the squash commit itself.

Read back: `gh api repos/Diafyx/REPO/rulesets --jq '.[] | {id, name, enforcement, target}'`

## 4. Security

| Item | How |
|---|---|
| Code security configuration | the org's "Public repos" configuration, which is the default for new public repos and enforced |
| Private vulnerability reporting | `gh api --method PUT repos/Diafyx/REPO/private-vulnerability-reporting` |
| Content reports | Settings → Moderation options → Reported content → "Prior contributors and collaborators" (UI only) |
| Pre-public scan | before a private repo goes public, the maintainer runs `gitleaks git --redact -v` over the full history and resolves every finding |

Read back: `gh api repos/Diafyx/REPO/code-security-configuration --jq '.status + " " + .configuration.name'`, `gh api repos/Diafyx/REPO/private-vulnerability-reporting`, `gh api repos/Diafyx/REPO/community/profile --jq .health_percentage` (expect 100).

## 5. Labels

The canonical set is in [`labels.json`](labels.json). Sync it, plus the project's extra `area:` labels:

```
python3 ~/org_setup/.github/standards/tools/sync-labels.py Diafyx/REPO --profile python-pypi --area "area: example=What it covers"
```

The command prints a plan. Re-run it with `--apply` to create or update labels. Labels outside the set are reported, never deleted automatically.

## 6. Files

| File | Source |
|---|---|
| `AGENTS.md`, `CLAUDE.md` | `python3 ~/org_setup/.github/standards/tools/sync-standard.py <repo-dir> --profile <profile>`, then fill Part A |
| `LICENSE` | Apache-2.0 (code) or CC BY 4.0 plus `LICENSE-CODE` Apache-2.0 (`content-site`); existing MIT repos keep MIT |
| `README.md` | problem, status, install, minimal example, limitations, contributing, license; badges for CI, license and version |
| `.editorconfig`, `.gitattributes`, `.gitignore` | from `repo-template`; `.gitignore` must contain `.tmp/` |
| `.github/CODEOWNERS` | `* @SEPURI-SAI-KRISHNA` |
| `.github/dependabot.yml` | the section 7 entries, one per ecosystem in use |
| `.github/release.yml` | from `repo-template` (release-note categories by label) |
| `.github/workflows/ci.yml` | the profile's gates, ending in the `CI result` job |
| `.github/workflows/org-checks.yml`, `pr-size.yml` | callers from `repo-template` |
| `CHANGELOG.md` | created by the first release-preparation PR (profiles that release) |
| `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `CODE_OF_CONDUCT.md`, issue forms, PR template | inherited from `Diafyx/.github`. Add a repo copy only for project-specific wording; a repo copy of `.github/ISSUE_TEMPLATE/` replaces all org forms, so copy the whole set. |

## 7. Dependabot entry shape

```yaml
  - package-ecosystem: github-actions   # or pip, npm, ...
    directory: /
    schedule:
      interval: weekly
      day: monday
    cooldown:
      default-days: 7
    open-pull-requests-limit: 5
    labels: ["dependencies", "area: ci"]   # "area: packaging" for package ecosystems
    commit-message:
      prefix: ci                           # "deps" for package ecosystems
    groups:
      all:
        patterns: ["*"]
```

## 8. Presence

Once a repository is public and usable:
- add it to the Projects table in `Diafyx/.github` `profile/README.md`;
- add it to the Work section of `diafyx.github.io`;
- pin it on the org profile if it is a flagship project.

## 9. Archiving a repository

When a project stops:
1. Close or transfer its open issues and PRs, each with a short comment.
2. Put a notice at the top of the README: the status, the date, what to use instead, and whether published packages stay installable.
3. For a package, publish no further versions. Yank only broken or dangerous releases.
4. Remove it from the org profile README, the website and the org pins.
5. Archive the repository in Settings → General (read-only, still public). Never delete a public repository that others may depend on.

Record these steps on a `maintenance:` issue opened before archiving.

## 10. Order for a new repository

1. Create the repository from the template: `gh repo create Diafyx/REPO --public --template Diafyx/repo-template --description "..."`
2. Apply section 2 and section 4, then "Protect main" (section 3), then labels (section 5).
3. Open the foundation issue. Its PR adds the profile files, CI and `AGENTS.md` Part A.
4. After that PR merges, apply "Required checks", plus the tag rulesets if the profile releases.
5. Read back everything, and record the results on the foundation issue.

## 11. Retrofit of an existing repository

Open one `maintenance:` issue listing every gap against sections 1–8. Fix settings, rulesets and labels by helper. Fix files in one PR. Record the read-backs on the issue.
