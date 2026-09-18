---
id: grok
adapter: claude_markdown
support_tier: compatibility
skill_layout: flat
destinations:
  skills: .grok/skills
  agents: .grok/agents
---

# Grok Installation Target

Grok CLI is a maintained compatibility installation target without a runtime behavior guarantee.
Grok reads Claude-format skills and Markdown agents natively, so this target links the canonical
skills flat beneath `.grok/skills` and links the authored Claude Markdown agents beneath
`.grok/agents`. Grok also scans `~/.claude/skills` and `~/.claude/agents` on its own; installing
this target gives Grok its own copies when the Claude target is not installed.
