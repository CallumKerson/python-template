#!/usr/bin/env -S uv run --script
# [MISE] description="Pin tools and dependencies the template left unversioned"
"""
Pin the unversioned placeholders python-template writes to concrete versions.

Only placeholders are touched: tools set to "latest" in mise.toml, the LATEST
sentinel in hk.pkl, a bare uv_build and Python dependencies without a version.
Versions already pinned are left alone.
"""

import re
import subprocess
import tomllib
from pathlib import Path

MISE_TOML = Path("mise.toml")
HK_PKL = Path("hk.pkl")
PYPROJECT = Path("pyproject.toml")
UV_LOCK = Path("uv.lock")
WORKFLOWS = Path(".github/workflows")


def run(*args: str) -> str:
    """Run a command, returning its output."""
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout.strip()


def tool_version(value: object) -> object:
    """Return the version of a mise [tools] entry, which may be a table."""
    return value.get("version") if isinstance(value, dict) else value


def pin_mise_tools() -> None:
    """Replace "latest" with the current version for each mise tool still using it."""
    text = MISE_TOML.read_text()
    for name, value in tomllib.loads(text).get("tools", {}).items():
        if tool_version(value) != "latest":
            continue
        version = run("mise", "latest", name)
        # Either version = "latest" in a [tools.<name>] table, or <name> = "latest"
        key = rf'"?{re.escape(name)}"?'
        placeholder = re.compile(rf'^((?:\[tools\.{key}\][^\[]*?version|{key})\s*=.*?)"latest"', re.MULTILINE)
        text = placeholder.sub(rf'\g<1>"{version}"', text, count=1)
        print(f"Pinned {name} to {version} in {MISE_TOML}")
    MISE_TOML.write_text(text)


def pin_hk_pkl() -> None:
    """Replace the LATEST sentinel in hk.pkl with the installed hk version."""
    text = HK_PKL.read_text()
    if "LATEST" not in text:
        return
    version = run("mise", "exec", "--", "hk", "--version").split()[-1]
    HK_PKL.write_text(text.replace("LATEST", version))
    print(f"Pinned hk.pkl to hk {version}")


def pin_uv_build() -> None:
    """Bound a bare uv_build requirement to the installed uv's minor version."""
    text = PYPROJECT.read_text()
    if 'requires = ["uv_build"]' not in text:
        return
    version = run("mise", "exec", "--", "uv", "--version").split()[1]
    major, minor, _ = version.split(".", 2)
    requirement = f"uv_build>={major}.{minor}.0,<{major}.{int(minor) + 1}.0"
    PYPROJECT.write_text(text.replace('requires = ["uv_build"]', f'requires = ["{requirement}"]'))
    print(f"Pinned build backend to {requirement}")


def normalise(name: str) -> str:
    """Normalise a package name as PEP 503 does."""
    return re.sub(r"[-_.]+", "-", name).lower()


def pin_python_dependencies() -> None:
    """Give each dependency without a version a lower bound of its locked version."""
    pyproject = tomllib.loads(PYPROJECT.read_text())
    requirements = list(pyproject.get("project", {}).get("dependencies", []))
    for group in pyproject.get("dependency-groups", {}).values():
        requirements += [r for r in group if isinstance(r, str)]
    bare = [r for r in requirements if re.fullmatch(r"[A-Za-z0-9._-]+", r)]

    run("mise", "exec", "--", "uv", "lock")
    if bare:
        locked = {normalise(p["name"]): p["version"] for p in tomllib.loads(UV_LOCK.read_text())["package"]}
        text = PYPROJECT.read_text()
        for name in bare:
            version = locked[normalise(name)]
            text = text.replace(f'"{name}"', f'"{name}>={version}"')
            print(f"Pinned {name} to >={version} in {PYPROJECT}")
        PYPROJECT.write_text(text)
    # Locks again with the new bounds, and creates .venv for ty
    run("mise", "exec", "--", "uv", "sync")


def main() -> None:
    """Pin every placeholder, then lock the tools."""
    pin_mise_tools()
    run("mise", "install", "--quiet")
    pin_hk_pkl()
    pin_uv_build()
    pin_python_dependencies()
    if WORKFLOWS.is_dir():
        # Pins actions given by tag, e.g. actions/checkout@v6, to their commit
        run("mise", "exec", "--", "pinact", "run")
    run("mise", "lock")


if __name__ == "__main__":
    main()
