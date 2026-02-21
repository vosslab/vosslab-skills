## Coding Style
See Python coding style in docs/PYTHON_STYLE.md.
See Markdown style in docs/MARKDOWN_STYLE.md.
See repo style in docs/REPO_STYLE.md.
When making edits, document them in docs/CHANGELOG.md.
When in doubt, implement the changes the user asked for rather than waiting for a response; the user is not the best reader and will likely miss your request and then be confused why it was not implemented or fixed.
When changing code always run focused tests on changed code, documentation does not require tests.
Agents may find pytest programs to run in the tests folder, including smoke tests and pyflakes runner scripts. These should all be capable of the -k flag, such as pytest test_feature.py -k changed_file.py

## Python Environment
AI agents (Codex/Claude) must run Python using `source source_me.sh && python3` (use Python 3.12 only).
AI agents should execute shell commands with Bash (`bash -lc`) instead of Zsh because `source_me.sh` and this repo's environment assumptions target Bash semantics.
This is only for AI agents runtime, not a requirement for repo scripts.
On this user's macOS (Homebrew Python 3.12), Python modules are installed to `/opt/homebrew/lib/python3.12/site-packages/`.
