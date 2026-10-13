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
  `template/.config/mise.toml.jinja`, hk's package version is `LATEST` in
  `template/.config/hk.pkl.jinja`, Python dependencies are bare names, GitHub
  Actions use major tags (`@v6`), and the Renovate preset has no tag. The
  generated project's `mise run pin` (`template/.config/mise/tasks/pin.py`)
  pins them, using pinact for actions and the latest release tag for the
  preset. Changing those lines later would conflict with versions projects
  have since pinned.
- Tool config goes in `.config/`, in the template as in this repo, except
  `.typos.toml`: typos only reads config from the root.
- Don't add copier `_tasks`: they make copier and Renovate need `--trust`.
- Write each mise tool as its own `[tools.<name>]` table, so `copier update`
  can add or remove one without conflicting with neighbouring pins.
- Renovate ignores `template/`; this repo's own tools in `.config/mise.toml`
  are pinned and updated by Renovate.
- Renovate rules shared by generated projects go in the
  `CallumKerson/renovate-config` preset, not the template's `renovate.json`.
- Files ending `.jinja` are rendered; others are copied as they are, so GitHub
  workflow `${{ }}` expressions only need escaping in `.jinja` files.
- Generated projects must pass their own `mise run check-all` and
  `mise run test` straight after copying.
