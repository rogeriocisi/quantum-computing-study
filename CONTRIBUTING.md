# Contributing to Quantum Computing Study

Thank you for your interest in contributing! We welcome all contributions that improve the quality, correctness, and clarity of this quantum computing study repository.

## How to Contribute

### 1. Report Bugs or Request Features
Feel free to open an issue if you find a bug or have an idea for a new feature. Please use the provided templates.

### 2. Code Contributions
1. Fork the repository and create your branch from `main`.
2. Ensure you have the development environment set up (see [CHEATSHEET.md](CHEATSHEET.md)).
3. Make your changes, adhering to the project's coding standards.

## Development Standards

We enforce strict code quality to keep the repository professional and maintainable.

### Language Rule
All code documentation—including docstrings, comments, and commit messages—**MUST** be written in English.


### Environment Setup
```powershell
python -m venv quantum_env
.\quantum_env\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Code Style (PEP 8)
We use `black` for formatting and `flake8` for linting.
Before committing, please run:
```bash
# Format code
black .

# Clean unused imports
autoflake --in-place --remove-all-unused-imports --recursive src tests scripts

# Check for linting errors
flake8
```

### Testing
All new algorithms or features must include unit tests in the `tests/` directory.
Run tests with:
```bash
pytest --cov=src
```

## Commit Messages
We follow [Conventional Commits](https://www.conventionalcommits.org/):
* `feat:` for new quantum algorithms or features.
* `fix:` for bug fixes.
* `docs:` for documentation changes.
* `chore:` for maintenance tasks.

Thank you for helping advance quantum education!
