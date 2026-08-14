# Spec quick reference

Condensed reference card for the Agent Skills open standard. Source: [agentskills.io/specification](https://agentskills.io/specification).

## Frontmatter fields

| Field | Required | Type | Constraints |
| --- | --- | --- | --- |
| `name` | Yes | string | 1-64 chars. Lowercase alphanumeric + hyphens. No leading/trailing/consecutive hyphens. Must match directory name. |
| `description` | Yes | string | 1-1024 chars. Non-empty. What the skill does + when to use it. |
| `license` | No | string | License name or reference to bundled file. |
| `compatibility` | No | string | 1-500 chars. Environment requirements. |
| `metadata` | No | map | String keys to string values. Arbitrary additional properties. |
| `allowed-tools` | No | string | Space-delimited tool list. Experimental. |

## Name rules

- Lowercase letters, digits, hyphens only (`a-z`, `0-9`, `-`).
- Must not start or end with `-`.
- Must not contain `--`.
- Must match parent directory name exactly.
- Max 64 characters.

Valid: `pdf-processing`, `data-analysis`, `code-review`

Invalid: `PDF-Processing` (uppercase), `-pdf` (leading hyphen), `pdf--processing` (consecutive hyphens)

## Description guidelines

- Describe what the skill does and when to use it.
- Include keywords that help agents match tasks.
- All trigger/activation context belongs here, not in the body.
- Body is only loaded after activation, so "When to use" sections in the body do not help with discovery.

## Directory conventions

```
skill-name/
+-- SKILL.md              # Required
+-- scripts/              # Optional: executable code
+-- references/           # Optional: on-demand documentation
+-- assets/               # Optional: static resources for output
+-- agents/
|   +-- openai.yaml       # Optional: UI metadata
```

## Progressive disclosure levels

| Level | Content | When loaded | Budget |
| --- | --- | --- | --- |
| 1. Metadata | name + description | Always (startup) | ~100 tokens |
| 2. Instructions | SKILL.md body | On activation | < 5000 tokens |
| 3. Resources | scripts/, references/, assets/ | On demand | Unlimited |

## Body guidelines

- No format restrictions on Markdown body.
- Keep under 500 lines.
- Move detailed content to `references/`.
- Reference files from SKILL.md with guidance on when to read them.
- Keep file references one level deep.
- Large reference files (100+ lines): add a table of contents.
- Very large files (10k+ words): add grep patterns in SKILL.md.

## Validation

Use the reference library to validate:

```bash
skills-ref validate ./my-skill
```

Source: [github.com/agentskills/agentskills/tree/main/skills-ref](https://github.com/agentskills/agentskills/tree/main/skills-ref)
