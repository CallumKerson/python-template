# python-template

A [copier](https://copier.readthedocs.io) template for my Python projects:
[uv](https://docs.astral.sh/uv/) for Python and dependencies,
[mise](https://mise.jdx.dev) for tools and tasks, and [hk](https://hk.jdx.dev)
running ruff, ty, rumdl, ryl, tombi and typos as git hooks.

## Usage

Projects need [mise](https://mise.jdx.dev/getting-started.html). The template
runs tasks after copying, so it has to be trusted:

```sh
uvx copier copy --trust gh:CallumKerson/python-template my-project
```

It asks for:

- the project's name, description and author;
- the minimum Python version;
- whether mise should run `uv sync` automatically.

Answers are saved to `.config/copier-answers.yaml`. Pull in later template
changes from the project with `mise run update-template`.

## Versions belong to the project

The template never sets tool or dependency versions. It writes them
unversioned: `"latest"` in `mise.toml`, `LATEST` in `hk.pkl`, and bare
`uv_build` and `pytest` in `pyproject.toml`.

After every copy and update, `tasks/pin_placeholders.py` pins only those
placeholders to the current versions and locks them with `mise lock` and
`uv sync`. Versions the project has already pinned are left alone. Since the
template's lines don't change between releases, `copier update` never touches
a project's versions; keeping them up to date is the project's job.

When adding a tool or dependency to the template, add it unversioned.

## Development

```sh
mise run test         # generate projects and check them; needs network access
mise run fix-all      # apply linter and formatter fixes
mise run check-all    # run all linters, formatters and type checks
```
