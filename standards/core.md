## Part B: Diafyx core rules (standard v1.0.0)

These rules apply to every Diafyx repository. "You" means the coding agent. "The maintainer" is `MAINTAINER` in Part A. MUST and NEVER are mandatory. SHOULD is the default: deviate only with a stated reason.

Precedence: an explicit instruction from the maintainer in this session, then Part A, then Part C, then Part B. The B1 boundaries are relaxed only by an explicit instruction naming the specific action ("you may run X now"), never by inference.

### B1. Hard boundaries

1. Work only inside `PROJECT_ROOT`, the directory containing this file. Read, write or execute nothing outside it: no home directory, global config, parent folders or other repositories. Caches and temp directories that tools manage themselves are fine; do not inspect them.
2. NEVER run Git, with one exception: `git --no-optional-locks -C "<PROJECT_ROOT>" status --short --branch`, to confirm the branch and see changed files. Everything else is forbidden, including other read-only commands (`diff`, `log`, `show`, `branch`, `rev-parse`, `ls-files`) and any tool that invokes Git (VCS-derived versions, `gitleaks git`, pre-commit). Discover files with `rg`, `rg --files` and your file tools.
3. NEVER write to GitHub: no mutating `gh` command or API call (create, edit, comment, label, close, merge, release, dispatch, settings). Prepare such commands for the maintainer. Read-only `gh` (`view`, `list`, `api` GET) is allowed only when the maintainer asks you to check something, or when the current task needs current state (labels, milestones, a run the maintainer reported failing). Never poll or watch.
4. NEVER change identity or security configuration: Git config at any scope, signing or SSH keys, `gh auth`, credentials, or account, organization or repository settings. The maintainer also contributes upstream under a separate setup that nothing here may affect.
5. NEVER edit tracked files on `main`. Edit tracked files only after the maintainer confirms `Ready on branch: <branch>` for the current issue. Scratch work in ignored `.tmp/` is always allowed.
6. NEVER push, merge, tag, release, publish, delete branches or approve deployments. Install nothing globally, and contact no paid service. Project-local installs from the declared dependency groups or lockfiles are fine.
7. NEVER put secrets, tokens, personal or customer data, private paths or undisclosed vulnerability details in tracked files, issues, PRs, logs, fixtures or release notes. Write home paths as `~`. Never open or print `.env` files, credential stores or key files.
8. NEVER weaken a gate to get green: no lowered thresholds, blanket ignores, new skips, deleted tests or `continue-on-error`, and no suppression without its exact code and a reason. Weakening a gate needs its own approved issue.
9. NEVER claim a check passed unless you ran it in this session and saw it pass, or CI shows it. Report skips and failures as such. Never declare work done because time or context is short.
10. Preserve unrelated changes in the working tree. Never delete broad, unresolved or variable-built paths.

### B2. Working with the maintainer

- Lead every reply with the outcome and the next action. Give short progress updates during long work.
- Stop and ask before any choice that would change the public API, license, compatibility promise, security posture, release policy or repository administration. Otherwise make reasonable in-scope assumptions and state them.
- Write commands for the maintainer's OS: PowerShell on Windows, bash on Linux and macOS. Put one command per code block, on a single line, with no chaining (`&&`, `;`, pipes into another command), no continuations and no comments. Use `git -C "<PROJECT_ROOT>"` for every Git command.
- A multi-step action that needs verification (commit, PR, bulk issues, settings) goes in a helper under `.tmp/`: `.sh` run as `bash "<abs path>"`, or `.ps1` run as `& '<abs path>'`. A helper stops on the first error (`set -euo pipefail` or `$ErrorActionPreference = 'Stop'`), prints each action, is safe to re-run, verifies its result, and never pushes or merges. You never execute helpers.
- Say what output to expect, then wait, and read the pasted output before continuing. If a helper fails, diagnose the exact error and repair that helper. Never switch approach silently, and never create a replacement issue or PR.

### B3. Starting a session

1. Read Part A. If a value the current task needs is `TBD`, ask for that value only.
2. Read `.tmp/session-state.md` if it exists: confirmed decisions, the current issue and branch, and the checkpoint. Update it at every checkpoint.
3. Restate in at most eight lines: the project goal, the checkpoint, the smallest next step, and the one decision you need, if any.
4. When the maintainer reports a merge, continue with the next agreed issue. Do not recheck finished work unless asked.
5. Never carry assumptions, names or scope over from another project or session.

### B4. Planning

- Propose a short, outcome-based roadmap and get approval before creating a backlog. Never create issues for appearance. Keep the foundation to one or two setup PRs. After that, every PR delivers user-visible value or a needed fix.
- Each release has a milestone named after its version (`0.2.0`, `0.1.0a2`), whose description is the user-visible outcome. Milestones hold issues, never PRs, and are the single source of release scope. A Projects board is optional and never a second source of truth.
- Each version milestone has a `release: VERSION` issue that stays open until post-release verification is recorded on it.
- Split XL work into sub-issues before starting. An XXL item is an epic: a tracking issue with sub-issues, never implemented directly. Record ordering with GitHub sub-issues and "blocked by" links.
- To create more than one issue, write `.tmp/issues-plan.md` (titles, bodies, labels, size, milestone, type) for review, then an idempotent helper. The helper:
  - skips titles that already exist;
  - assigns `MAINTAINER`;
  - sets labels, milestone and type;
  - waits a random 3 to 6 minutes between creations (none for a single issue);
  - verifies the final state.

  If the maintainer says "only create issues", do nothing else.

### B5. Issues

- No PR without an open issue. Dependabot PRs are the only exception.
- Use the issue forms. The form sets the title prefix and the type:

| Form | Title prefix | Type | For |
|---|---|---|---|
| Bug report | `bug: ` | Bug | incorrect behavior |
| Feature proposal | `feature: ` | Feature | new user-visible behavior or content |
| Design proposal | `design: ` | Feature | a decision listed in B7 |
| Maintenance task | `maintenance: ` | Task | CI, tooling, dependencies, upkeep |
| Release checklist | `release: VERSION` | Task | one version, through to verification |

- To create an issue from the CLI:
  1. Write the body to `.tmp/issue-<slug>.md`, using the form's `### Heading` sections with real content.
  2. Give one `gh api --method POST repos/<owner>/<repo>/issues` command that sets the title, `body=@file`, `type`, `labels[]`, `assignees[]` and the milestone number. Use this, not `gh issue create`, which cannot set the type.

  Metadata lives only in GitHub's fields, never in the body.
- Every issue states the problem, motivation, scope, observable acceptance criteria, non-goals, dependencies, and risk and rollback where relevant.
- Assign the maintainer's own issues and PRs to `MAINTAINER`. Outside contributions stay unassigned until triage. Triage moves an issue from `needs-triage` to `ready`, `needs-decision` or `blocked`, and sets its kind, area, size and milestone.
- Never rewrite closed issues or merged PRs for uniformity. Never add automation that rejects or closes issues or PRs because of their prose: templates guide, and review catches gaps.

### B6. Labels

Use only the organization label set, plus the `area:` labels in Part A. Propose a new label through a `maintenance:` issue.

| Group | Labels | Rule |
|---|---|---|
| Kind | `bug`, `enhancement`, `documentation`, `maintenance`, `testing`, `performance`, `security`, `dependencies` | exactly one |
| Area | `area: core`, `area: ci`, `area: docs`; the profile's areas (`area: packaging`, `area: content` or `area: ui`); plus Part A | at least one |
| Size | `size: XS`, `size: S`, `size: M`, `size: L`, `size: XL`, `size: XXL` | exactly one |
| State | `needs-triage`, `needs-decision`, `blocked`, `ready` | at most one, open issues only |
| Release notes | `breaking-change`, `skip-release-notes` | when they apply |
| Other | `release`, `good first issue`, `help wanted`, `duplicate`, `invalid`, `wontfix` | when they apply |

`security` is for hardening that is safe to discuss in public. Vulnerabilities go to private reporting.

Size is measured on one scale: changed lines (added plus deleted), excluding lockfiles and generated files. CI sizes PRs automatically. At triage, an issue gets the size of the PR it should produce.

| Size | Lines | Rule |
|---|---|---|
| XS | 0–9 | — |
| S | 10–49 | — |
| M | 50–249 | — |
| L | 250–499 | one concern only |
| XL | 500–999 | the PR explains under "Why" why it cannot be split |
| XXL | 1000+ | split it, unless the change is mechanical (generated, renamed, vendored, bulk content); the PR says which |

### B7. Design decisions

Open a `design:` issue (`needs-decision`) before changing any of these:
- a public API, CLI, file format or output schema
- supported runtime or integration versions
- architecture, lifecycle, concurrency or ownership
- network, filesystem, credential or other security-sensitive behavior
- collecting, storing or sending user data, including telemetry
- dependency policy
- the release or supply chain
- the license or governance

Record the decision as `docs/design/NNNN-short-title.md`, numbered sequentially, with the sections Status, Context, Decision, Alternatives considered, Consequences, Compatibility and migration, Validation and failure semantics, and Follow-up issues. Merging the record accepts the decision. Implementation follows in separate linked issues. Small internal choices need no record. A license or governance change stays open for public comment for at least seven days before merge.

### B8. Branches, commits, pull requests

- Use one issue, one branch, one PR. Name the branch `<type>/<issue>-<slug>`, with type `feat`, `fix`, `docs`, `test`, `ci`, `build`, `chore`, `perf` or `refactor`, and a kebab-case slug of at most five words.
- Commit messages use Conventional Commits: `type(scope): summary`, imperative, at most 72 characters. Mark breaking changes with `!` and a `BREAKING CHANGE:` footer. When you prepared the change, add an `Assisted-by: <agent name>` trailer. Only the maintainer signs off; never add a `Signed-off-by` for yourself.
- Every commit is DCO-signed-off and cryptographically signed. Write the message to `.tmp/commit-msg-<issue>.txt` and give a commit helper that:
  1. checks the branch;
  2. checks `git config user.name` equals `COMMIT_NAME`, and stops if not, changing nothing;
  3. refuses paths outside the expected list, and runs `git diff --check`;
  4. shows the diff stat, stages only the named paths, and shows the staged summary;
  5. runs `git commit --signoff --gpg-sign --file <msg>`;
  6. requires `git log -1 --format=%G?` to print `G` or `U`, and requires the sign-off to be present;
  7. prints the short status.

  If signing fails, stop and tell the maintainer. Never offer an unsigned fallback.
- After the PR is open, add fixes as new signed commits on the same branch. Do not force-push or rebase unless the maintainer asks. Update the branch with GitHub's "Update branch" button.
- The PR title is a Conventional Commit of at most 72 characters, with no issue number. It becomes the commit on `main`, so it must state the change exactly.
- The PR body goes in `.tmp/pr-<issue>-<slug>.md`. It follows the repository's PR template exactly: every section, in order, with real content, no HTML comments or placeholders, and a box ticked only when true. Check it against the tracked template before handing it over.
- The PR helper:
  - sets base `main`, the head branch, the title and the body file;
  - sets the kind, area and release-note labels (size is automatic);
  - sets assignee `MAINTAINER`, and no milestone;
  - if a PR already exists for the branch, prints its URL and stops.
- After implementing, give three separate blocks in one response: the commit helper, `git push -u origin <branch>`, and the PR helper. Then stop. Do not monitor.
- If the maintainer reports a CI failure: read only the failed jobs' logs (`gh run view <id> --log-failed`), make the smallest fix, rerun that check locally, and give a signed follow-up commit plus `git push`. Never open a replacement PR.
- The maintainer merges with **Squash and merge** in the GitHub UI, after the required checks pass and the full diff has been self-reviewed. You never merge.
- After a merge (first confirm the URL belongs to `REPOSITORY`), give separate blocks: `git -C "<root>" switch main`, then `git -C "<root>" pull --ff-only`, then `git -C "<root>" branch -D <old-branch>` (`-D` because squashed branches are not ancestors), then `git -C "<root>" switch -c <next-branch>` for the next agreed issue.

### B9. Quality and tests

- Each change ships with its tests, docs and examples in the same PR, and stays within the issue's scope: no unrelated refactors or speculative abstractions.
- A new runtime dependency needs the maintainer's approval on the issue. State why the standard library or existing dependencies are not enough, its license (it must be compatible with the project's), and its maintenance health. Code copied from elsewhere keeps its license notice and is credited in `NOTICE`.
- Tests are deterministic and offline: no network, no sleeps, no machine-global state, no real credentials, no dependence on order. Integration tests are marked and run in their own CI lane.
- Test the artifact users receive (the built package or site), not only the source tree.
- Before handing over a commit, run every check CI runs, over the same paths. The PR records the exact commands and actual results, kept apart from what only CI will show.

### B10. Continuous integration

- Every workflow:
  - sets top-level `permissions: {}` or `contents: read`, with job-level grants only where needed;
  - uses `concurrency` with cancel-in-progress for PRs;
  - sets `timeout-minutes` on every job;
  - checks out with `persist-credentials: false`;
  - pins every action to a full commit SHA with a `# vX.Y.Z` comment from the official release tag;
  - uses no secrets in PR workflows;
  - uses `pull_request_target` only for metadata jobs that never check out or run PR code.
- CI ends with an aggregate job named `CI result`, which needs every other job and fails if any failed or was cancelled. `REQUIRED_CHECKS` stays stable as jobs change.
- The org checks (`Org checks / DCO`, `Org checks / Dependency review`) and the `PR size` labeler come from caller workflows that reuse `Diafyx/.github` workflows. Never copy their logic into the repository.
- CI runs on PRs, on pushes to `main`, and weekly on a schedule to catch upstream breakage.
- **Keeping CI fit as the project grows:**
  1. When a PR adds something CI does not exercise (a language or file type, a dependency ecosystem, a supported version or OS, an integration, an entry point, an artifact, a docs build), extend CI in that PR if the change is small. Otherwise open a linked `maintenance:` issue labeled `area: ci`, and claim no support until CI covers it. Add new ecosystems to `.github/dependabot.yml`.
  2. Every compatibility claim, in the README, metadata or docs, maps to a CI job that tests it.
  3. Every release issue includes a CI review:
     - the matrix matches the support policy;
     - Dependabot updates are merged;
     - the required checks match the job names;
     - no skips or `continue-on-error` have crept in;
     - median CI time over 10 minutes is flagged;
     - a test that passed only on rerun gets a `bug` issue.
  4. A red `main` or a red scheduled run comes before feature work: open a `bug:` issue labeled `area: ci`.
  5. Review Dependabot PRs within a week. Read the changelog of any major bump before merging.

### B11. Versioning and releases

- Follow Semantic Versioning for intent. The tag is `v` plus the exact version (`v0.3.1`). Tags exist only for releases.
- **The next version**, from the changes merged since the last tag:

| Merged since last release | Before 1.0 (`0.y.z`) | From 1.0 (`x.y.z`) |
|---|---|---|
| any `breaking-change` | minor `0.y+1.0` | major `x+1.0.0` |
| any new feature (`enhancement`) | minor `0.y+1.0` | minor `x.y+1.0` |
| only fixes, docs, internal or dependency work | patch `0.y.z+1` | patch `x.y.z+1` |

- **Pre-releases**, where the profile publishes them:
  - alpha: the scope is incomplete and the API may change;
  - beta: the scope is complete, in testing;
  - release candidate: blocker fixes only.

  Use them while an API is settling. Patch releases skip them.
- **Moving to `1.0.0`** takes a `design:` issue showing all of these:
  1. the core use case is complete and its public API is documented;
  2. the last two minor releases needed no breaking change;
  3. there is real use beyond the maintainer's tests;
  4. a support policy and a deprecation policy are written;
  5. every claimed platform and version is tested in CI;
  6. no open bug is marked blocking.
- **After `1.0`**: remove public items only after a deprecation warning has shipped for at least one minor release. Dropping a runtime version that has reached end of life is a minor release with a release note. Only the latest minor release gets fixes, unless the support policy says otherwise.
- **Release flow:**
  1. Merge all scope issues in the milestone.
  2. Merge a release-preparation PR with the version, metadata, `CHANGELOG.md` (Keep a Changelog, curated from PR labels) and compatibility notes.
  3. Confirm CI is green on that exact commit and the B10 review is done.
  4. The maintainer creates a signed, annotated tag (`git tag -s vX.Y.Z -m "vX.Y.Z"`) on that commit, then pushes it as a separate command.
  5. Run the profile's publish steps.
  6. Record verification on the release issue, then close the issue and the milestone.

  Never move or reuse a published tag.
- `CHANGELOG.md` changes only in release-preparation PRs, never as a per-PR gate. Each PR records its user impact in the template. Internal-only PRs get `skip-release-notes`. `.github/release.yml` groups generated notes by label.

### B12. Security and supply chain

- Keep private vulnerability reporting on. Never ask for vulnerability details in public.
- Dependabot runs weekly and grouped, with `open-pull-requests-limit: 5`, a 7-day `cooldown`, and explicit labels (`dependencies` plus an area). Security updates and CodeQL come from the org security configuration.
- Publish only from CI:
  - OIDC or Trusted Publishing, with no stored long-lived tokens where OIDC exists;
  - a protected environment that needs the maintainer's approval;
  - artifacts built once and published unchanged;
  - attestations where the publisher supports them.

  Never publish from a workstation.
- Before a private repository goes public, the maintainer runs a full-history secret scan, and the B13 baseline is applied.

### B13. Repository baseline

Every repository is created from `Diafyx/repo-template` and kept at the baseline in `Diafyx/.github` `standards/repository-baseline.md`. When setting up or retrofitting a repository, read that file (read-only, allowed for this purpose) with `gh api repos/Diafyx/.github/contents/standards/repository-baseline.md -H "Accept: application/vnd.github.raw"`. Then prepare one helper for the gaps; the maintainer runs it and verifies by read-back. A retrofit is one `maintenance:` issue per repository.

With one maintainer, required approvals are 0, and self-review is mandatory: a scoped issue, a fully read diff, green required checks, and resolved conversations.

### B14. The cycle for each issue

1. Confirm the issue is open and ready, and that its prerequisites are merged.
2. Give the branch command, then wait for `Ready on branch: <branch>`. Confirm it with the allowed `git status` command before editing.
3. Read the issue and every file you will touch, completely.
4. State the exact scope and your most important assumption.
5. Implement only that scope, with its tests and docs.
6. Run every relevant check locally.
7. Write the PR body and commit message files.
8. Give the commit helper, the push and the PR helper as three blocks. Stop.
9. On a reported CI failure, follow B8. On a reported merge, give the cleanup and next-branch blocks, then return to step 1.

**Done means all of these:**
- the acceptance criteria are met and the non-goals are untouched;
- the change is tested at the right layer;
- every gate is green, locally and in CI;
- docs, compatibility and user impact are handled or marked not applicable;
- no private data is included;
- commits are signed and signed off;
- the PR template is complete;
- conversations are resolved;
- the maintainer has merged;
- issue and milestone states are accurate.

### B15. Changing this standard

Parts B and C are synced from `Diafyx/.github/standards/`. Never edit them here. If a rule is wrong, missing or in conflict with the project, tell the maintainer and propose the change for `Diafyx/.github`. Until it lands, follow the rule as written, or the maintainer's explicit instruction.
