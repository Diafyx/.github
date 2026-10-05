# .github

Organization-wide defaults for [GlassBoxStudio](https://github.com/GlassBoxStudio).

GitHub uses the files in this repository for every GlassBoxStudio repository that doesn't define its own:

| File | Purpose |
|---|---|
| [`profile/README.md`](profile/README.md) | The organization's profile page |
| [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) | Contributor Covenant 3.0 |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute |
| [`SECURITY.md`](SECURITY.md) | How to report a vulnerability |
| [`SUPPORT.md`](SUPPORT.md) | Where to get help |
| [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE) | Bug report and feature request forms |
| [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) | Pull request checklist |
| [`workflow-templates/`](workflow-templates) | CI starter workflows (Node.js, Python, Gradle, Maven, Go, Rust), offered under **Actions → New workflow** in every repository |

All starter workflows pin actions to full commit SHAs, as required by the organization's Actions policy. Dependabot does not update this folder, so refresh the pinned SHAs here when a workflow in a repository is updated.

See GitHub's documentation on [default community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).
