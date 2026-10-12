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
- whether it's a library or a [cyclopts](https://cyclopts.readthedocs.io) CLI;
- whether to add GitHub CI, Renovate and release-please. release-please uses
  a GitHub App's token, read from the `RELEASE_APP_CLIENT_ID` variable and
  `RELEASE_APP_PRIVATE_KEY` secret, so release pull requests run CI.

Answers are saved to `.copier-answers.yaml`. Pull in later template
changes from the project with `mise run update-template`.

## Adopting an existing project

Copy the template over the project from a clean git tree, answering the
questions to match it, then review every change before running setup:

```sh
cd my-project
uvx copier copy --overwrite gh:CallumKerson/python-template .
git checkout HEAD -- uv.lock    # before setup, so it doesn't re-resolve
```

Copier leaves existing code in `src/<package>/` and the example test alone,
but replaces other files whole. Put back what was the project's own:

- dependencies, scripts, entry points and pytest settings in
  `pyproject.toml`;
- project-specific `.gitignore` entries, hk excludes, mise tasks and tools;
- anything else in `README.md` and `AGENTS.md`.

Delete any new example code or tests the project doesn't need; copier won't
add them back on update. Then run `mise run setup`, `mise run check-all` and
`mise run test`.

## Versions belong to the project

The template never sets tool or dependency versions. It writes them
unversioned: `"latest"` in `mise.toml`, `LATEST` in `hk.pkl`, and bare
`uv_build`, `pytest` and `cyclopts` in `pyproject.toml`.

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

## Renovate

Generated projects with GitHub on use Renovate's copier manager to open a pull
request for each new template release. Renovate has no mise, so anything new
from the template stays unpinned until `mise run pin` runs locally.

## Development

```sh
mise run test         # generate projects and check them; needs network access
mise run fix-all      # apply linter and formatter fixes
mise run check-all    # run all linters, formatters and type checks
```
