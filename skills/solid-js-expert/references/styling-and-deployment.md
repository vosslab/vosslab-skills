# Styling and deployment

## Mini-index

- [Tailwind CSS v4](#tailwind-css-v4)
- [CSS modules](#css-modules)
- [Deployment provider matrix](#deployment-provider-matrix)

---

## Tailwind CSS v4

> **Note:** For Tailwind CSS v3 see the `tailwind-v3` guide.

### Installation

```bash
npm install --save-dev tailwindcss @tailwindcss/postcss postcss
```

Create `postcss.config.mjs`:

```js
export default {
    plugins: {
        "@tailwindcss/postcss": {},
    },
};
```

### Import Tailwind

`src/index.css`:

```css
@import "tailwindcss";
```

Root entry `index.jsx` / `index.tsx`:

```jsx
import { render } from "solid-js/web";
import App from "./App";
import "./index.css";

render(() => <App />, document.getElementById("root"));
```

### Usage

Use Tailwind utility classes on `class` (not `className`) in Solid JSX:

```jsx
function Card() {
    return (
        <div class="grid min-h-screen place-items-center">
            <div class="aspect-[2] h-[160px] rounded-[16px] shadow-[0_0_0_4px_hsl(0_0%_0%/15%)]">
                Hello, world!
            </div>
        </div>
    );
}
```

---

## CSS modules

CSS Modules scope class names locally, preventing global conflicts.

### Creating a module file

```css
/* styles.module.css */
.foo { color: red; }
.bar { background-color: blue; }
```

Do not use bare HTML tag selectors in CSS modules (specificity issues).

### Using modules in components

```jsx
import styles from "./styles.module.css";

function Component() {
    return (
        <>
            {/* single class */}
            <div class={styles.foo}>Hello</div>

            {/* multiple classes */}
            <div class={`${styles.foo} ${styles.bar}`}>Hello</div>

            {/* mix with plain class names */}
            <div class={`${styles.foo} container`}>Hello</div>

            {/* dashed names -- use bracket notation */}
            <div class={styles["foo-with-dash"]}>Hello</div>
        </>
    );
}
```

---

## Deployment provider matrix

Build output directory is `dist` for all providers unless noted.

| Provider | Type | CLI tool | Key notes |
| --- | --- | --- | --- |
| Vercel | Edge / serverless | `vercel` | Import repo via dashboard or run `vercel` in project dir |
| Netlify | Static / serverless | `netlify-cli` | Set publish dir to `dist`; run `netlify init` |
| Cloudflare Pages | Edge / JAMstack | `wrangler` | Set `NODE_VERSION` env var; output `dist`; `wrangler pages deploy dist` |
| Firebase | Static (Google) | `firebase-tools` | Add `firebase.json` with `"public": "dist"`; run `firebase deploy` |
| Railway | Container / static | `@railway/cli` | Set start script to `npx http-server ./dist`; `railway up` |
| AWS via SST | Lambda / container | `sst` | Set preset `aws-lambda-streaming`; `sst deploy --stage production` |
| AWS via Flightcontrol | AWS static / service | GUI or `flightcontrol.json` | Link GitHub; output dir `dist`; connect AWS account |
| Stormkit | Static / SPA | GUI | Import from GitHub/GitLab/Bitbucket; verify output folder |
| Zerops | Static + SSR Node.js | `zcli` | Add `zerops.yml`; supports static and SSR Node.js 20 |

### Flightcontrol code-based config

```json
{
    "$schema": "https://app.flightcontrol.dev/schema.json",
    "environments": [{
        "id": "production",
        "name": "Production",
        "region": "us-west-2",
        "source": { "branch": "main" },
        "services": [{
            "id": "my-solid-app",
            "buildType": "nixpacks",
            "type": "static",
            "outputDirectory": "dist",
            "singlePageApp": true
        }]
    }]
}
```

### Zerops SSR config

```yaml
zerops:
  - setup: app
    build:
      base: nodejs@latest
      buildCommands:
        - pnpm i
        - pnpm build
      deployFiles:
        - .output
        - node_modules
        - package.json
    run:
      base: nodejs@latest
      ports:
        - port: 3000
          httpSupport: true
      start: pnpm start
```

### Zerops static config

```yaml
zerops:
  - setup: app
    build:
      base: nodejs@latest
      buildCommands:
        - pnpm i
        - pnpm build
      deployFiles:
        - dist/~
    run:
      base: static
```
