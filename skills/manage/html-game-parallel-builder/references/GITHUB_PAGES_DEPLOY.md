# Deploying the dist/ build to GitHub Pages

This guide explains how to publish the canonical production build from
`dist/` to GitHub Pages.

The expected workflow is:

1. Build the game into `dist/`.
2. Publish the `dist/` contents to GitHub Pages.
3. Configure GitHub Pages to serve the build.

## What `dist/` is

The `dist/` folder is the finished website that GitHub Pages will serve.
GitHub Pages does not need your TypeScript source files. It needs the
final browser-ready files: `index.html`, JavaScript, CSS, images, and
other assets.

A typical `dist/` after `./build_github_pages.sh` runs:

```text
dist/
  index.html
  main.js
  style.css
  .nojekyll
```

`dist/index.html` must exist. The skill's `build_github_pages.sh` asserts
this before exiting.

## Recommended deployment path

If you are new to GitHub Pages, use **GitHub Actions** (described below).
GitHub Actions is usually easier because:

- You keep your source code on `main`.
- GitHub builds and publishes the site automatically on every push.
- You do not need to manually switch branches or force-push.

Use the `gh-pages` branch method only if you want to manually publish
the already-built `dist/` folder. That method is covered later in this
guide as the advanced alternative.

## Prerequisites

You need:

- A GitHub repository for the game.
- A working TypeScript build.
- A `build_github_pages.sh` script that creates a complete `dist/`
  directory.
- A `package-lock.json` committed to the repo (the workflow uses
  `npm ci`, which requires a lockfile). Running `setup_game.sh` once
  produces this lockfile; commit it before enabling the workflow.

## Build the GitHub Pages output

From the project root, run:

```bash
./build_github_pages.sh
```

The script:

1. Wipes `dist/` from scratch.
2. Type-checks via `npx tsc --noEmit`.
3. Bundles `src/init.ts` to `dist/main.js` with esbuild.
4. Copies `src/index.html` and `src/style.css` into `dist/`.
5. Creates `dist/.nojekyll`.
6. Asserts `dist/index.html` exists.

Type checking must pass; the script fails the build on any TypeScript
error. Do not deploy if type checking fails.

## Preview the production build locally

Before deploying, preview the `dist/` folder with a local static server.

```bash
python3 -m http.server 8000 --directory dist
```

Or with Node:

```bash
npx serve dist
```

Then open `http://localhost:8000` and check that:

- The game loads without console errors.
- Assets load correctly.
- Saves, settings, and `localStorage` behavior work as expected.
- The game still works after a browser refresh.
- Navigation does not depend on local file paths.

Serving through a static server is more reliable than opening
`index.html` directly because it catches path and browser-loading
issues that file-protocol pages hide.

## Deploy with GitHub Actions (recommended)

This workflow tells GitHub to do four things whenever you push to
`main`:

1. Download the repository.
2. Install the project dependencies.
3. Run the build script.
4. Publish the `dist/` folder to GitHub Pages.

The skill ships the workflow file at
`templates/deploy_pages_workflow.yml` (kept outside `.github/` so the
skill repo does not ship a hidden directory). Copy it to
`.github/workflows/deploy-pages.yml` in your project.

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: github-pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build GitHub Pages output
        run: ./build_github_pages.sh

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

Then configure GitHub Pages:

1. Open the repository on GitHub.
2. Go to **Settings**.
3. Open **Pages**.
4. Under **Build and deployment**, set **Source** to **GitHub Actions**.

After the next push to `main`, GitHub Actions will build and deploy the
site. GitHub Pages may take a minute or two to show the new version
after a successful deployment.

### Workflow file push permissions

GitHub may reject a push that creates or edits files under
`.github/workflows/` if the token used for `git push` does not have
permission to modify workflow files.

A common error looks like this:

```text
refusing to allow a Personal Access Token to create or update workflow
.github/workflows/deploy-pages.yml without workflow scope
```

This does not mean the workflow file is invalid. It means the current
Git credentials are not allowed to modify workflow files.

Use one of these fixes (in order of "least annoying"):

1. **Add the workflow through the GitHub web UI.** Open
   `https://github.com/<owner>/<repo>/new/main/.github/workflows`,
   create `deploy-pages.yml`, and paste the YAML above. After this
   one-time add, normal source edits push as usual without touching
   the workflow.
2. **Update the Personal Access Token so it has the workflow scope, or
   the equivalent permission to create and edit workflow files.**
   Classic PAT: enable the `workflow` scope. Fine-grained PAT: grant
   permission to update Actions / workflow files for that repo.
3. **Use SSH or `gh` auth.** If your local HTTPS token keeps causing
   this, switching the remote to SSH avoids stale-token problems
   entirely.

### First successful deploy checklist

After the workflow finishes, check:

1. The Actions tab shows a successful run.
2. Settings -> Pages shows **GitHub Actions** as the source.
3. The published site URL appears in Settings -> Pages.
4. The site loads in a browser.

## Use relative paths so files load correctly

GitHub Pages often serves project sites from a subpath:

```text
https://USERNAME.github.io/REPOSITORY_NAME/
```

Because of this, avoid root-relative asset paths like:

```html
<script src="/main.js"></script>
```

Use relative paths instead:

```html
<script src="./main.js"></script>
```

The same rule applies to CSS, images, audio, data files, and other
assets.

Good:

```html
<link rel="stylesheet" href="./style.css">
<img src="./assets/icon.png">
```

Risky for project pages:

```html
<link rel="stylesheet" href="/style.css">
<img src="/assets/icon.png">
```

The shipped `templates/src_index.html` already uses relative paths.

## .nojekyll

GitHub Pages otherwise treats the served directory as a Jekyll site,
which silently strips files starting with `_`. The shipped
`build_github_pages.sh` runs `touch dist/.nojekyll` to disable that
behavior.

## Recommended `build_github_pages.sh` contract

The script is the canonical production build path. It must:

- Remove stale output.
- Run TypeScript checks.
- Build the browser game.
- Write a complete GitHub Pages site to `dist/`.
- Ensure `dist/index.html` exists.
- Create `dist/.nojekyll`.

The shipped template at
``templates/build_github_pages.sh``
already follows this contract.

## Advanced alternative: deploy from a `gh-pages` branch

> **Warning:** Commit or stash all work before using this method.
> The commands below replace the contents of the `gh-pages` branch with
> the contents of `dist/`. Do not run these commands if you have
> uncommitted work.

This method keeps the source on `main` and the built site on
`gh-pages`. It does not require a GitHub Actions workflow, so it sidesteps
the workflow-scope push restriction. The trade-off is that you must
build locally and push the result yourself on every release.

A safer flow uses a sibling worktree so the built artifact never
touches the main working tree:

```bash
./build_github_pages.sh

# Set up the gh-pages branch in a sibling worktree (one-time).
git worktree add -B gh-pages ../<repo>-gh-pages origin/gh-pages 2>/dev/null \
	|| git worktree add ../<repo>-gh-pages -b gh-pages

cd ../<repo>-gh-pages
git rm -rf .
cp -R ../<repo>/dist/. .
touch .nojekyll
git add .
git commit -m "Deploy GitHub Pages build"
git push origin gh-pages
cd -
```

Then configure GitHub Pages:

1. Open the repository on GitHub.
2. Go to **Settings** -> **Pages**.
3. Under **Build and deployment**, set **Source** to
   **Deploy from a branch**.
4. Select the `gh-pages` branch and the root folder.
5. Save.

This skill's orchestrator should not pick this path automatically. Use
GitHub Actions unless the user explicitly asks for branch-based
deployment.

## Deployment checklist

Before publishing:

- `./build_github_pages.sh` finishes successfully.
- `dist/index.html` exists.
- The game works when served locally from `dist/`.
- Browser console has no missing-file errors.
- Asset paths are relative, not root-relative.
- `dist/.nojekyll` exists (the build script creates it).
- GitHub Pages source is set to either **GitHub Actions** or the
  `gh-pages` branch.

## Troubleshooting

### I see a blank page

1. Open the browser developer console.
2. Look for red errors.
3. If files like `main.js` or `style.css` are missing, check the asset
   paths.
4. Use relative paths like `./main.js`, not `/main.js`.

### Files load locally but not on GitHub Pages

1. Check for root-relative paths starting with `/`.
2. Switch them to `./file.js` or `./assets/file.png`.
3. Confirm the project URL includes the repository name as a subpath.

### The old version is still showing

1. GitHub Pages can take a minute or two to update after a successful
   deploy.
2. Hard-refresh the page (shift-reload).
3. Check the Actions tab to confirm the latest run actually succeeded.

### The workflow fails at `npm ci`

1. Make sure `package-lock.json` is committed.
2. If the project intentionally avoids lockfiles, swap `npm ci` for
   `npm install` in your copy of the workflow.

### The build passes but the game fails after refresh

1. The game may rely on local development paths or unbuilt files.
2. Confirm everything the game needs at runtime is copied into `dist/`
   by `build_github_pages.sh`.
3. Files outside `dist/` are not served by GitHub Pages.

### `git push` is rejected for the workflow file

See "Workflow file push permissions" above.
