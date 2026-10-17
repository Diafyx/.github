# Prompts for coding agents (standard v1.0.0)

The rules live in each repository's `AGENTS.md`. Codex loads that file automatically, and Claude Code loads it through `CLAUDE.md`. These prompts only start or steer a session, so keep them short. Replace `<...>` before pasting.

## 1. Start any session

```text
Read AGENTS.md completely and follow it exactly for this whole session. Then do B3: restate the project goal, the checkpoint from .tmp/session-state.md (create it if missing), the smallest next step, and the one decision you need from me. Do not edit tracked files, run Git (except the allowed git status), or write to GitHub.
```

## 2. New project, right after the repository is created from the template and the standard is synced

```text
This is a new Diafyx project. Read AGENTS.md completely and follow it exactly. Part A still has TBD values: ask me only for the ones you need, as one short list. Then propose a roadmap (B4): 3 to 6 milestones, each with a user-visible outcome, and the single foundation issue that comes first. Create nothing and edit no tracked file until I approve.
```

## 3. Existing repository adopting the standard (retrofit)

```text
This repository is adopting the Diafyx standard. I synced AGENTS.md on branch <branch> for issue #<N>. Read AGENTS.md completely and follow it. Then: (1) fill Part A from the repository's real files (build config, CI, README), marking anything uncertain TBD and asking me; (2) read the baseline as B13 allows and list every gap in one table: item, current state, required state, and how to fix it (file, setting, ruleset or label); (3) wait for my approval before changing anything.
```

## 4. Work on the next issue

```text
Next: issue #<N>. Follow B14.
```

## 5. CI failed on a PR

```text
CI failed on PR #<N>: <url>. Follow B8: read only the failed jobs' logs, make the smallest fix on the same branch, rerun that check locally, then give me the signed follow-up commit and git push.
```

## 6. A PR was merged

```text
PR #<N> is merged: <url>. Give me the cleanup and next-branch commands (B8), then continue with the next agreed issue.
```

## 7. Create planned issues only

```text
Only create issues: <list or "the approved roadmap for milestone X">. Follow B4 and B5: write .tmp/issues-plan.md for my review first, then the idempotent helper. Do not branch or implement anything.
```

## 8. Prepare a release

```text
Start release <VERSION>. Follow B11 and the Part C release steps one stage at a time. Begin with the B10 CI review and the release-preparation issue, and wait for my confirmation after every irreversible step.
```

## 9. Resume after a break or a new chat

```text
Resume. Re-read AGENTS.md and .tmp/session-state.md, check the branch with the allowed git status, and tell me where we are and the next step. Do not redo finished work.
```

## 10. The agent drifted from the rules

```text
Stop. That breaks AGENTS.md <rule, e.g. B1.2>. Re-read Part B, tell me what you did wrong in one line, undo only your own uncommitted edits if any, and continue by the rules.
```
