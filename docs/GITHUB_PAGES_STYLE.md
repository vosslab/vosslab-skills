# GitHub Pages style

> This file is vendored. Local changes can and will be overwritten by propagation.

This guide owns the GitHub Pages deployment contract for repositories with
`REPO_TYPE=githubpages`. It complements `docs/TYPESCRIPT_STYLE.md`,
which owns local TypeScript maintenance.

## Keep deployment small

Local maintenance establishes that the newest dependencies work. Pages publishes
the committed result and does not independently select newer dependencies.

- Run `./update_dependencies.sh` locally to refresh dependencies, audit them,
  run code checks, and validate the production build.
- Commit the reviewed `package.json` and `package-lock.json` together.
- The Pages workflow runs `npm ci --no-audit`, then
  `./build_github_pages.sh`, then uploads `dist/` and deploys it.
- `build_github_pages.sh` type-checks and builds the site. Keep broader lint,
  test, audit, and dependency update work in local maintenance.

The workflow uses an explicit Node major validated by local maintenance. Update
that value only after validating the newer major locally.

## Activate workflow seeds

The repository receives `deploy-pages.yml` at its root so propagation never overwrites
an active workflow. To activate it, move it to:

```text
.github/workflows/deploy-pages.yml
```

Keep custom workflows when they need a different build or artifact path. Update
the equivalent install, build, upload, and deploy steps instead of replacing a
working custom workflow.

Leave GitHub's defaults and the repository's existing Dependabot setup unchanged;
this template does not provide or recommend a replacement configuration.

## Build contract

`build_github_pages.sh` writes the complete publishable site to `dist/`. It must
use installed local tools, verify its required source files, and leave
`dist/index.html`, `dist/main.js`, and `dist/.nojekyll` ready for the Pages
artifact action.
