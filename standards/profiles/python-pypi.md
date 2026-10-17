## Part C: Profile `python-pypi` (standard v1.0.0)

A Python library or CLI published to PyPI. This adds to Part B.

### C1. Layout and packaging

- Package code goes in `src/<IMPORT_NAME>/`, tests in `tests/`, maintained scripts in `tools/`.
- `pyproject.toml` holds PEP 621 metadata with a PEP 517 backend (setuptools ≥ 77 or hatchling; record the choice). Use an SPDX `license` expression plus `license-files`, accurate classifiers (C5), `requires-python`, keywords, and `[project.urls]` (Homepage, Issues, Source, and Changelog once one exists).
- Exactly one version source: the literal `__version__` in `src/<IMPORT_NAME>/_version.py`, which the backend reads. No VCS-derived versions (they need Git, B1).
- Keep runtime dependencies minimal, with lower bounds only. An upper cap needs a known incompatibility, recorded in a comment. Integrations live behind extras (`OPTIONAL_INTEGRATIONS`). A test proves `import <IMPORT_NAME>` works without them.
- Development tools go in the PEP 735 `[dependency-groups] dev`, never in runtime dependencies. Set up with `python -m venv .venv`, then `python -m pip install --group dev -e .` (pip ≥ 25.1).
- Ship `py.typed`, and fully annotate the public API. Every public function, class and module has a docstring. Commands differ by OS: `.venv/bin/` on Linux and macOS, `.venv\Scripts\` on Windows.
- The public API is the set of names in `__all__` of documented modules. Modules starting with `_` are private. Any change to the public API follows B7.

### C2. Quality gates (identical locally and in CI)

- `ruff format --check .` and `ruff check .` over the whole repository.
- `mypy` in strict mode over `src`, `tests` and `tools`.
- `pytest` with `-ra --strict-markers --strict-config`, and `filterwarnings = ["error"]` so deprecations surface.
- Branch coverage of package source at 100% (`--cov-branch --cov-fail-under=100`). Lowering it needs its own issue with evidence. `# pragma: no cover` is only for genuinely unreachable lines, with a comment saying why.

### C3. Supported Python

- Support every CPython version from `PYTHON_FLOOR` up that has not reached end of life. Check https://devguide.python.org/versions/ at every release preparation.
- A new CPython version (released each October) is added to CI and classifiers in the next minor release, through a `maintenance:` issue. A pre-release CPython may run in a separate non-required job; when it fails, open an issue.
- An end-of-life version is dropped in the next minor release: raise `requires-python`, update the classifiers and the matrix, and add a release note.
- CI matrix: every supported version on Ubuntu, plus the oldest and newest on Windows and macOS.

### C4. Artifact checks (CI `package` job, and before every release)

1. Build into a fresh `dist/`: `python -m build --sdist --wheel --outdir dist`.
2. Run `python -m twine check --strict dist/*`.
3. Inspect the contents:
   - the wheel holds the package, `py.typed` and the license files;
   - the sdist holds `src`, `tests`, `README`, `LICENSE` and `pyproject.toml`;
   - neither holds `.tmp`, caches, editor files or secrets.
4. Install the wheel into a clean venv outside the checkout. Check:
   - the import works;
   - `__version__` equals `importlib.metadata.version(DISTRIBUTION_NAME)`;
   - the CLI `--help` and `--version` work, if there is a CLI;
   - one minimal real use works.
5. Upload `dist/` as a workflow artifact.

### C5. Versions (PEP 440)

- Versions look like `0.1.0a1`, `0.1.0b1`, `0.1.0rc1`, `0.1.0` or `0.1.1`. The tag is `v` plus that string. GitHub releases for `a`, `b` and `rc` versions are marked as pre-releases.
- The `Development Status` classifier follows the version:

| Stage | Classifier |
|---|---|
| Before the first release | `2 - Pre-Alpha` |
| Alpha releases | `3 - Alpha` |
| Final `0.x` releases | `4 - Beta` |
| From `1.0.0` | `5 - Production/Stable` |

- Deprecate with `warnings.warn(..., DeprecationWarning, stacklevel=2)` and a "Deprecated" changelog entry. Remove only as B11 allows.

### C6. Publishing through PyPI Trusted Publishing

Before the first release, a `design:` issue and ADR define `.github/workflows/release.yml`. Guide the maintainer through each stage separately, and wait for confirmation after every irreversible step: tag push, dispatch, environment approval. The workflow must have:

1. **Trigger:** `workflow_dispatch` on `main`, with inputs `tag` and `confirm`, where `confirm` must equal `publish <version>`. Creating a tag or a GitHub release never publishes.
2. **Preflight** (read-only; fails closed on any mismatch):
   - the tag exists and points to a commit on `main`;
   - the tag equals `v` plus `__version__`;
   - `CI result` passed on that commit;
   - the only open issue in the version milestone is the release issue;
   - `confirm` matches.
3. **Build:** check out the tag and build once. Run the C4 checks, write `SHA256SUMS`, and upload the artifact.
4. **Publish:** environment `pypi` (the maintainer is the required reviewer; deployments only from `main`), `permissions: id-token: write`, and the same downloaded artifact published with `pypa/gh-action-pypi-publish` (SHA-pinned; it produces attestations). No API token.
5. **GitHub release**, after the publish step succeeds: `gh release create <tag> dist/* --verify-tag --notes-file <curated notes>`, with `--prerelease` for `a`, `b` and `rc` versions.

**First publication:** the maintainer confirms the name is free on PyPI, then registers a pending Trusted Publisher (owner `Diafyx`, the repository, workflow `release.yml`, environment `pypi`). A TestPyPI rehearsal through a separate `testpypi` environment is optional.

**Post-release verification** goes on the release issue, with evidence:
- the PyPI version page, its metadata and both files are correct;
- the PyPI file hashes equal `SHA256SUMS`;
- the attestations are present;
- `pip install DISTRIBUTION_NAME==VERSION` into a fresh venv outside the checkout imports, reports the version and runs the minimal example;
- the extras install;
- the GitHub release has the same files and notes.

**Failure:** confirm a run's terminal state before dispatching again. A version that reached PyPI is immutable: never upload different bytes under it. Fix forward with a new version. Yank only a broken or dangerous release, with a stated reason.

### C7. Profile security

- Test fixtures are synthetic. Tests never touch the network.
- Dependabot covers the `pip` and `github-actions` ecosystems.
- Add a `pip-audit` CI job once the package has runtime dependencies.
