"""Tests for the Copier template"""

from pathlib import Path

import pytest
from copier import run_copy

template = Path(__file__).parent.parent.resolve()


@pytest.mark.parametrize(
    "test_case",
    [
        {
            "name": "defaults",
            "data": {},
            "defaults": True,
            "expected_project_name": "test-project",
            "expected_package_name": "test_project",
            "expected_description": "A cool new Python project",
        },
        {
            "name": "custom_project_name",
            "data": {"project_name": "my-cool-app"},
            "defaults": True,
            "expected_project_name": "my-cool-app",
            "expected_package_name": "my_cool_app",
            "expected_description": "A cool new Python project",
        },
        {
            "name": "custom_both",
            "data": {
                "project_name": "amazing-tool",
                "project_description": "An amazing development tool",
            },
            "defaults": True,
            "expected_project_name": "amazing-tool",
            "expected_package_name": "amazing_tool",
            "expected_description": "An amazing development tool",
        },
    ],
)
def test_template_generation(tmp_path: Path, test_case: dict) -> None:
    """Test copier template with different input combinations."""
    target = tmp_path / "test-project"

    run_copy(
        str(template),
        target,
        data=test_case["data"],
        defaults=test_case["defaults"],
        unsafe=True,
        vcs_ref="HEAD",
    )

    _assert_essential_files_exist(target)
    _assert_package_structure(target, test_case["expected_package_name"])
    _assert_template_substitution(
        target, test_case["expected_project_name"], test_case["expected_description"]
    )


def _assert_essential_files_exist(target: Path) -> None:
    """Check that all essential files were created."""
    required_files = [
        "pyproject.toml",
        "README.md",
        ".gitignore",
        ".config/mise.toml",
        ".template-answers.yaml",
    ]

    for file_path in required_files:
        assert (target / file_path).exists(), f"Required file {file_path} not found"


def _assert_package_structure(target: Path, expected_package_name: str) -> None:
    """Check that the package directory has the correct structure."""
    package_dir = target / expected_package_name
    assert package_dir.exists() and package_dir.is_dir(), (
        f"Expected package directory '{expected_package_name}', found: {[d.name for d in target.iterdir() if d.is_dir()]}"
    )

    main_file = package_dir / "main.py"
    assert main_file.exists(), (
        f"Expected main.py in {package_dir.name}, found: {[f.name for f in package_dir.iterdir()]}"
    )


def _assert_template_substitution(
    target: Path, expected_project_name: str, expected_description: str
) -> None:
    """Check that template variables were properly substituted."""
    pyproject_content = (target / "pyproject.toml").read_text()
    assert expected_project_name in pyproject_content
    assert expected_description in pyproject_content
    assert "{{ project_name }}" not in pyproject_content
    assert "{{ project_description }}" not in pyproject_content

    readme_content = (target / "README.md").read_text()
    assert expected_project_name in readme_content
    assert "{{ project-name }}" not in readme_content
