---
id: hermes
adapter: skills_only
support_tier: compatibility
skill_layout: category
destinations:
  skills: .hermes/skills
---

# Hermes Installation Target

Hermes Agent is a maintained compatibility installation target without a runtime behavior
guarantee. Hermes organizes `~/.hermes/skills` as `<category>/<skill>/SKILL.md`, so this target
links each canonical `skills/<category>` directory beneath `.hermes/skills`. Hermes has no
user-defined agent files, so the target declares no agents destination.
