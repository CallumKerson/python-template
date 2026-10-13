"""
Generate projects from the template and check they work.

These run the template's tasks for real, so they need mise and network access.
"""

import json
import re
import shutil
import subprocess
import tomllib
from pathlib import Path

import pytest
from copier import run_copy

TEMPLATE = Path(__file__).parent.parent
ANSWERS_FILE = ".copier-answers.yaml"
# Longer than every line limit, to check generated files wrap it
LONG_DESCRIPTION = (
    "Check that a description longer than any line limit, with hyphenated words like copier-template, "
    "is wrapped in every generated file"
)
IGNORED = shutil.ignore_patterns(".git", ".venv", "*_cache", "__pycache__")


def run(cwd: Path, *args: str) -> str:
    """Run a command in cwd, returning its output."""
    result = subprocess.run(args, cwd=cwd, check=False, capture_output=True, text=True)
    assert result.returncode == 0, f"{' '.join(args)} failed:\n{result.stdout}\n{result.stderr}"
    return result.stdout


def commit_all(repo: Path, message: str) -> None:
    """Commit every change in repo, skipping hooks."""
    run(repo, "git", "add", "--all")
    run(repo, "git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qnm", message)


@pytest.fixture(autouse=True)
def _outside_virtual_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Stop uv and ty in generated projects using this repo's virtual environment."""
    monkeypatch.delenv("VIRTUAL_ENV", raising=False)


@pytest.fixture
def template(tmp_path: Path) -> Path:
    """Return a git repository holding the template's working tree, tagged v1.0.0."""
    repo = tmp_path / "template"
    shutil.copytree(TEMPLATE, repo, ignore=IGNORED)
    run(repo, "git", "init", "-q")
    commit_all(repo, "feat: template")
    run(repo, "git", "tag", "v1.0.0")
    return repo


def generate(template: Path, project: Path, **data: object) -> None:
    """Generate a project from the template with default answers, then set it up."""
    # Without unsafe=True, copier refuses templates with tasks, as it would for Renovate
    data = {"project_name": "demo-app", "project_description": LONG_DESCRIPTION, **data}
    run_copy(str(template), project, data=data, defaults=True)
    run(project, "mise", "trust", "--quiet")
    run(project, "mise", "run", "setup")
    commit_all(project, "feat: initial commit")


def mise_tools(project: Path) -> dict:
    """Return the [tools] table of the project's .config/mise.toml."""
    return tomllib.loads((project / ".config/mise.toml").read_text())["tools"]


def tool_version(value: str | dict) -> str:
    """Return the version of a mise [tools] entry, which may be a table."""
    return value["version"] if isinstance(value, dict) else value


@pytest.mark.parametrize("github", [False, True], ids=["local", "github"])
@pytest.mark.parametrize("project_type", ["library", "cli"])
def test_copy(template: Path, tmp_path: Path, project_type: str, *, github: bool) -> None:
    project = tmp_path / "demo-app"
    generate(template, project, project_type=project_type, github=github)

    # Every placeholder is pinned
    versions = [tool_version(v) for v in mise_tools(project).values()]
    assert all(re.fullmatch(r"\d+(\.\d+)+", v) for v in versions), versions
    assert "LATEST" not in (project / ".config/hk.pkl").read_text()
    pyproject = tomllib.loads((project / "pyproject.toml").read_text())
    assert re.fullmatch(r"uv_build>=\d+\.\d+\.0,<\d+\.\d+\.0", pyproject["build-system"]["requires"][0])
    requirements = pyproject["project"]["dependencies"] + pyproject["dependency-groups"]["dev"]
    assert all(">=" in r for r in requirements), requirements
    assert (project / ".config/mise.lock").is_file()
    assert (project / ANSWERS_FILE).is_file()
    assert (project / ".github").is_dir() == github
    if github:
        for workflow in (project / ".github/workflows").iterdir():
            assert "@v" not in workflow.read_text().replace("# v", ""), workflow.name
        renovate = json.loads((project / ".github/renovate.json").read_text())
        assert re.fullmatch(r"github>CallumKerson/renovate-config#v\d+\.\d+\.\d+", renovate["extends"][0])

    # The generated project passes its own checks and tests, even from a fresh clone
    shutil.rmtree(project / ".venv")
    run(project, "mise", "run", "check-all")
    run(project, "mise", "run", "test")
    if project_type == "cli":
        assert run(project, "uv", "run", "demo-app", "hello", "--name", "Ada") == "Hello, Ada!\n"


def test_update_keeps_project_versions(template: Path, tmp_path: Path) -> None:
    project = tmp_path / "demo-app"
    generate(template, project)

    # The project manages its own versions
    mise_toml = project / ".config/mise.toml"
    pinned_ruff = tool_version(mise_tools(project)["ruff"])
    ruff = '[tools.ruff]\nversion = "{}"'
    mise_toml.write_text(mise_toml.read_text().replace(ruff.format(pinned_ruff), ruff.format("0.15.0")))
    pyproject = project / "pyproject.toml"
    pyproject.write_text(pyproject.read_text().replace("dev = [\n", 'dev = [\n  "pytest-cov>=7.0.0",\n'))
    run(project, "mise", "exec", "--", "uv", "lock")
    init = project / "src/demo_app/__init__.py"
    init.write_text('"""Code the project wrote."""\n')
    commit_all(project, "build: pin ruff and add pytest-cov")

    # The template adds a tool and changes another file
    tools = template / "template/.config/mise.toml.jinja"
    tools.write_text(
        tools.read_text().replace("[tools.rumdl]", '[tools.shellcheck]\nversion = "latest"\n\n[tools.rumdl]')
    )
    readme = template / "template/README.md.jinja"
    readme.write_text(readme.read_text() + "\nA new paragraph from the template.\n")
    example = template / "template/src/{{ package_name }}/__init__.py.jinja"
    example.write_text(example.read_text() + "\n# A change to the example code\n")
    commit_all(template, "feat: add shellcheck")
    run(template, "git", "tag", "v2.0.0")

    run(project, "mise", "run", "update-template")

    tools = mise_tools(project)
    assert tool_version(tools["ruff"]) == "0.15.0"
    assert re.fullmatch(r"\d+(\.\d+)+", tool_version(tools["shellcheck"]))
    assert '"pytest-cov>=7.0.0"' in pyproject.read_text()
    assert "A new paragraph from the template." in (project / "README.md").read_text()
    assert init.read_text() == '"""Code the project wrote."""\n'
    assert not list(project.rglob("*.rej"))
    assert "<<<<<<<" not in mise_toml.read_text() + pyproject.read_text()
