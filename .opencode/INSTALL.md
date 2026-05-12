# Installing Voss Lab Skills for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed

## Installation

Add vosslab-skills to the `plugin` array in your `opencode.json`
(global or project-level):

```json
{
  "plugin": ["vosslab-skills@git+https://github.com/vosslab/vosslab-skills.git"]
}
```

Restart OpenCode. The plugin installs through OpenCode's plugin manager
and registers all skills.

Verify by listing skills with the `skill` tool:

```
use skill tool to list skills
```

## Updating

OpenCode installs vosslab-skills through a git-backed package spec. To pick
up the newest commit, clear OpenCode's package cache or reinstall the plugin.

To pin a specific version:

```json
{
  "plugin": ["vosslab-skills@git+https://github.com/vosslab/vosslab-skills.git#v26.05.12"]
}
```

## Troubleshooting

### Plugin not loading

1. Check logs: `opencode run --print-logs "hello" 2>&1 | grep -i vosslab`
2. Verify the plugin line in your `opencode.json`
3. Make sure you are running a recent version of OpenCode

### Skills not found

1. Use `skill` tool to list what is discovered
2. Check that the plugin is loading (see above)

### Tool mapping

When skills reference Claude Code tools:
- `TodoWrite` -> `todowrite`
- `Task` with subagents -> `@mention` syntax
- `Skill` tool -> OpenCode's native `skill` tool
- File operations -> your native tools

## Getting Help

- Report issues: https://github.com/vosslab/vosslab-skills/issues
- Full documentation: https://github.com/vosslab/vosslab-skills/blob/main/README.md
