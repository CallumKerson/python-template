# Python Project Template

A [Copier](https://copier.readthedocs.io/) template for Python projects using
modern tools and best practices.

## Features

- **Python 3.12+** with modern tooling
- **[uv](https://docs.astral.sh/uv/)** for fast dependency management
- **[mise](https://mise.jd.dev/)** for environment and task management
- **[Ruff](https://docs.astral.sh/ruff/)** for linting and formatting
- **[pytest](https://pytest.org/)** for testing
- **Automated project setup** with post-generation tasks

## Usage

### Prerequisites

- [mise](https://mise.jd.dev/getting-started.html)

### Generate a new project

```bash
copier copy https://github.com/your-username/python-template my-project
cd my-project
```

The template will:

1. Ask for your project name and description
2. Generate the project structure
3. Set up mise configuration
4. Install dependencies with uv
5. Format and lint the generated code

### Manual setup (if needed)

```bash
# Trust and install mise configuration
mise trust ./.config/mise.toml
mise install

# Install dependencies
uv lock

# Format and lint
mise run format
mise run lint
```

## Project Structure

The generated project includes:

```text
my-project/
├── .config/
│   └── mise.toml          # Task runner configuration
├── my_project/            # Main Python package
│   ├── __init__.py
│   └── main.py           # Entry point
├── tests/
├── .gitignore
├── .template-answers.yaml # Copier answers (for updates)
├── pyproject.toml         # Project metadata and dependencies
└── README.md
```

## Available Tasks

```bash
mise run format    # Format code with ruff
mise run lint      # Lint code with ruff
mise run test      # Run tests with pytest
```

## Development

This template includes:

- Parameterized tests with pytest
- Automated formatting and linting
- Project validation

### Running tests

```bash
mise run test  # Unit tests
```
