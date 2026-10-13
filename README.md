# python-template

A [copier](https://copier.readthedocs.io) template for my Python projects:
[uv](https://docs.astral.sh/uv/) for Python and dependencies,
[mise](https://mise.jdx.dev) for tools and tasks, and [hk](https://hk.jdx.dev)
running ruff, ty, rumdl, ryl, tombi and typos as git hooks.

## Usage

Projects need [mise](https://mise.jdx.dev/getting-started.html):

```sh
uvx copier copy gh:CallumKerson/python-template my-project
cd my-project
mise run setup    # pin versions and install the git hooks
```

It asks for:

- the project's name, description and author;
- the minimum Python version;
- whether mise should run `uv sync` automatically.

Answers are saved to `.copier-answers.yaml`. Pull in later template
changes from the project with `mise run update-template`.

## Versions belong to the project

The template never sets tool or dependency versions. It writes them
unversioned: `"latest"` in `mise.toml`, `LATEST` in `hk.pkl`, and bare
`uv_build` and `pytest` in `pyproject.toml`.

The project's `mise run pin` task (`template/.mise/tasks/pin.py`) pins only
those placeholders to the current versions and locks them with `mise lock`
and `uv sync`; `mise run setup` and `mise run update-template` run it.
Versions the project has already pinned are left alone.

The template has no copier tasks, so neither copier nor Renovate's copier
manager needs `--trust`. The catch is that `copier update` merges against
the unpinned template, so it sees every pinned line as the project's own
change, and a template change next to one conflicts. Each mise tool is its
own `[tools.<name>]` table so that adding or removing a tool merges cleanly.
Changes beside the versions in `hk.pkl` or `pyproject.toml` can still
conflict.

When adding a tool or dependency to the template, add it unversioned.

## Development

```sh
mise run test         # generate projects and check them; needs network access
mise run fix-all      # apply linter and formatter fixes
mise run check-all    # run all linters, formatters and type checks
```
