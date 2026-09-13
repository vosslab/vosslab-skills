# Repository indexing

This directory owns commands that validate canonical skill and agent metadata and generate tracked
indexes or plugin projections. Indexing is a first-class repository domain beside `install_lib/`
and owns the canonical metadata and discovery models that installation also uses.

Run the merged command from the repository root through the Python bootstrap:

```bash
source source_me.sh && python3 index_lib/build_all.py
source source_me.sh && python3 index_lib/build_all.py --check
```

The focused modules remain directly runnable when maintaining one projection. Each generator also
supports `--check`; `openai_sidecars.py` is validation-only and requires that flag. Edit canonical
sources, then run `build_all.py`; generated files identify the focused module that owns them.
