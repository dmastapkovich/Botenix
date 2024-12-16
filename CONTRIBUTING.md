# Contributing to Botenix

Thank you for considering contributing to Botenix! We appreciate your time and effort. Below are the guidelines to help you contribute effectively.

## Process

1. **Fork the repository**:
   - Clone your fork locally.

2. **Create a feature branch**:
   - Name your branch descriptively (e.g., `feature/add-router` or `bugfix/fix-logging`).

3. **Make changes**:
   - Follow the coding style (PEP 8, `ruff`, and `mypy`).
   - Add or update tests to cover your changes.
   - Ensure all tests pass (`uv run pytest`).

4. **Commit your changes**:
   - Use [Conventional Commits](https://www.conventionalcommits.org/):

     ```
     feat/router: add message routing by regex
     fix/logger/: resolve issue with missing timestamps
     ```

5. **Open a Pull Request**:
   - Target the `develop` branch.
   - Provide a clear description of your changes.

## Requirements

- **Tests**: All changes must include tests.
- **Linting**: Code must pass `ruff` and `mypy` checks.
- **Pull Request Reviews**: At least one reviewer must approve your Pull Request.
