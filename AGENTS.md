# AGENTS.md

A copier template for Python projects. `copier.yaml` holds the questions and
tasks, and `template/` is what gets copied.

## Commands

- `mise run test` (or `uv run pytest`) generates projects from the working
  tree and runs their checks and tests, and checks `copier update` keeps a
  project's versions. It needs mise and network access, and takes a few
  minutes.
- `mise run check-all` runs all linters, formatters and type checks through hk;
  `mise run fix-all` applies fixes. Run both checks and tests before
  committing.

## Rules

- Never put a version in `template/`. Tools are `"latest"` in
  `template/mise.toml.jinja`, hk's package version is `LATEST` in
  `template/hk.pkl.jinja`, and Python dependencies are bare names.
  `tasks/pin_placeholders.py` pins them in the generated project. Changing
  those lines later would conflict with versions projects have since pinned.
- Renovate ignores `template/`; this repo's own tools in the root `mise.toml`
  are pinned and updated by Renovate.
- Files ending `.jinja` are rendered; others are copied as they are.
- Generated projects must pass their own `mise run check-all` and
  `mise run test` straight after copying.
