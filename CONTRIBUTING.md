# Contributing

Thanks for your interest in contributing to a GlassBoxStudio project. This guide applies to every repository in the organization unless that repository has its own `CONTRIBUTING.md`.

GlassBoxStudio is a small, independent studio, so reviews can take a few days. Every issue and pull request is read.

## Before you start

- **Bugs:** search the existing issues first. If it hasn't been reported, open one using the bug report form.
- **Features and larger changes:** open an issue describing the problem and your proposed approach *before* writing code, so the direction can be agreed up front. Pull requests for unagreed features may be closed.
- **Small fixes** (typos, docs, obvious one-line bugs) can go straight to a pull request.
- **Security vulnerabilities:** do **not** open a public issue. Follow the [security policy](https://github.com/GlassBoxStudio/.github/blob/main/SECURITY.md).

## Making a change

1. Fork the repository and create a branch from `main` with a descriptive name, e.g. `fix/step-rewind` or `feat/cassandra-batch`.
2. Follow the setup steps in the repository's README.
3. Keep the change focused: one logical change per pull request.
4. Add or update tests for any behavior you change.
5. Make sure lint, tests and build pass locally. They are the same checks CI runs.
6. Open the pull request against `main` and fill in the template.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>: <short summary in the imperative mood>
```

Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`. Examples:

```
feat: add Cassandra batch write scenario
fix: keep playback paused after rewinding past step 1
```

Signed commits are welcome but not required.

## Review and merging

- A maintainer reviews every pull request. CI must be green before merging.
- You may be asked for changes. Push them as new commits to the same branch rather than force-pushing, so the review history stays readable.
- Pull requests are merged with a merge commit, so your individual commits are preserved on `main` and credited to you.

## Use of AI tools

AI-assisted contributions are welcome, with the same bar as any other contribution:

- You are responsible for every line you submit. Review, test and understand it before opening a pull request.
- Be ready to explain the change in your own words when asked.
- Write issue descriptions, pull request descriptions and review replies yourself.
- Pull requests opened autonomously by agents, without a human who understands the change, will be closed.

## Licensing

By contributing, you agree that your contributions are licensed under the license of the repository you are contributing to (see its `LICENSE` file), and that you have the right to submit them under that license.

## Code of conduct

Everyone participating in GlassBoxStudio projects is expected to follow the [Code of Conduct](https://github.com/GlassBoxStudio/.github/blob/main/CODE_OF_CONDUCT.md).
