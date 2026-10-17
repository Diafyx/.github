## Part C: Profile `web-app` (standard v1.0.0)

A browser application (for example TypeScript, React and Vite), deployed as a static site. It is not published as a package. This adds to Part B.

### C1. Toolchain

- Pin the Node.js version in `.nvmrc`, use the current LTS line, and keep `engines` in `package.json` in step with it. CI reads `.nvmrc`.
- Use npm with a committed `package-lock.json`. Set up and run CI with `npm ci`, never `npm install`. Set `"private": true` so the app cannot be published to npm by accident.
- `package.json` scripts are the single entry points, and Part A's local commands call them: `lint`, `typecheck`, `test`, `build`.
- TypeScript runs in `strict` mode. Runtime dependencies stay minimal, and build-only tools go in `devDependencies`.

### C2. Quality gates (identical locally and in CI)

- `npm run lint`, `npm run typecheck`, `npm test` and `npm run build`. The build must succeed with no type errors.
- Unit tests cover logic, state and data. Component tests cover interactive behavior and accessibility roles. Tests never touch the network.
- Pure logic and data modules (simulation steps, parsers, stores) need meaningful coverage. Record the threshold in Part A, and lower it only through an issue.
- Accessibility: everything works from the keyboard, focus is visible, images and icons have text alternatives or `aria-hidden`, color contrast meets WCAG 2.2 AA, and `prefers-reduced-motion` is respected.

### C3. Supported environments

- Support the current and previous major versions of Chrome, Firefox, Safari and Edge. State this in the README.
- Desktop is the baseline. Phone or tablet support is claimed only after a dedicated issue makes it work and CI or a documented manual check covers it.

### C4. Deploying

- Production deploys only from `main`, through the hosting provider's Git integration or a GitHub Actions workflow. Record which one, and the production URL, in Part A. Pull requests get preview deploys where the provider offers them.
- The build output is static and reproducible from the lockfile. Secrets never enter the client bundle. Anything shipped to the browser is public.
- After a merge, verify that the production deploy ran on the merged commit and that the changed behavior is live.
- `index.html` keeps accurate metadata: description, canonical URL, theme color, Open Graph and Twitter tags with a real preview image, and favicons.

### C5. Versions and releases

- B11 applies: SemVer in `package.json` `version`, the tag `vX.Y.Z`, a `CHANGELOG.md` curated in the release-preparation PR, and the release flow.
- In this profile, the B11 publish step means:
  1. confirm production is serving the tagged commit;
  2. create the GitHub release from the tag, with the curated notes (`gh release create vX.Y.Z --verify-tag --notes-file <notes>`).

  There is no package registry and no pre-release versions.
- Post-release verification on the release issue: the production URL serves the tagged commit, the main user flows work, and the release notes are correct.

### C6. Profile security

- Dependabot covers the `npm` and `github-actions` ecosystems. Group development dependencies separately from runtime ones.
- Keep a strict Content Security Policy where the host allows it. Never load third-party scripts without a `design:` issue.
- Do not add analytics, tracking or cookies without a `design:` issue (B7).
