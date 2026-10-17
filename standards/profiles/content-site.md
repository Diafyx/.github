## Part C: Profile `content-site` (standard v1.0.0)

A prose-first repository (articles, notes, a studio site) built into a static site and deployed to GitHub Pages. This adds to Part B.

### C1. Licensing and originality

- `LICENSE` is CC BY 4.0, covering the text and images. Build code and code samples are Apache-2.0: put that text in `LICENSE-CODE`. The README states which license applies to what.
- All content is original wording. Quote briefly, with attribution and a link. Never copy text, figures, problem sets or diagrams from books, courses, exam papers or other sites. Draw your own diagrams, or use properly licensed ones and credit them.
- Factual claims cite primary sources where they exist (specifications, official documentation, the original paper). Name the version a claim applies to when behavior varies by version.

### C2. Content rules

- `CONTENT_GUIDE` holds the house style:
  - file naming and front matter;
  - heading structure;
  - tone and reading level;
  - diagram and code-sample conventions;
  - how sources are cited.

  Follow it, and change it only through a `maintenance:` issue.
- One article, or one tightly related set, per issue and PR. New content is a `feature:` issue labeled `enhancement` and `area: content`. A factual error is a `bug:` issue labeled `bug` and `area: content`.
- Accessibility: every image has meaningful alt text, headings never skip a level, link text says where it goes, and color is never the only carrier of meaning.
- A substantive correction to a published page gets a short dated "Updated" note on that page.

### C3. Build and quality gates (identical locally and in CI)

- The build script is deterministic and runs offline: same input, same output, no network calls.
- PR CI builds the site, then checks:
  - every internal link and anchor resolves (blocking);
  - Markdown lint passes (blocking);
  - spelling passes against a tracked project word list (blocking).

  CI uploads the built site as an artifact.
- External links are checked by a weekly scheduled job. A broken link opens a `bug:` issue and never blocks PRs.
- Build-script code follows B9. If the script has logic beyond templating, it has unit tests.

### C4. Deploying

- Deploy only from `main`, through the GitHub Pages Actions flow (`actions/upload-pages-artifact`, then `actions/deploy-pages` in the `github-pages` environment). PR runs build and check, but never deploy.
- The `deploy` job has `pages: write` and `id-token: write`. Every other job is read-only.
- After a merge, verify that the deploy run passed and that the changed pages are live at `SITE_URL`.

### C5. Versions and milestones

- Content sites have no version numbers, tags or releases. Each merge to `main` publishes. B11 does not apply, and there is no `CHANGELOG.md`.
- Milestones are named for outcomes (for example `OS: CPU scheduling`), with a description saying what readers will be able to learn or do. Close a milestone when its pages are live and verified.
- Packaging content as a versioned product (a book, a PDF, a course) needs a `design:` issue first.

### C6. Size labels for content

Size follows B6. An `L` or larger PR that adds a single article is acceptable when the PR says so under "Why". Splitting one article across PRs to lower the size is not required.
