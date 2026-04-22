# Commit Conventions

Format: `<type>(<scope>): <short description in English>`

## Types

| Type       | Use                                              |
|------------|--------------------------------------------------|
| `feat`     | New feature or implementation                    |
| `fix`      | Bug fix                                          |
| `docs`     | Documentation only                               |
| `refactor` | Code change without behavior change              |
| `test`     | Adding or fixing tests                           |
| `chore`    | Dependencies, config, tooling                    |
| `style`    | Formatting, linting (no logic change)            |
| `perf`     | Performance improvement                          |
| `ci`       | CI/CD pipeline changes                           |

## Scopes (this project)

| Scope          | Maps to                          |
|----------------|----------------------------------|
| `bell-state`   | `src/algorithms/bell_state.py`   |
| `vqe`          | `src/optimization/vqe_qaoa.py`   |
| `qml`          | `src/qml/qml_vqc.py`             |
| `nisq`         | `src/utils/nisq_mitigation.py`   |
| `algorithms`   | `src/algorithms/`                |
| `src`          | multiple modules under `src/`    |
| `scripts`      | `scripts/`                       |
| `docs`         | `docs/`                          |
| `deps`         | `requirements.txt`               |
| `git`          | `.pre-commit-config.yaml`, hooks |
| `landing`      | `landing/`                       |
| `readme`       | `README.md`                      |

## Examples

```bash
# New implementation
feat(bell-state): implement 3-qubit GHZ state circuit

# Bug fix
fix(vqe): correct QAOA layer parameter initialization

# Documentation
docs(readme): update hardware requirements for RTX 4060 Ti
docs(roadmap): add week-by-week breakdown for month 3

# Tests
test(bell-state): add unit tests for entanglement verification
test(vqe): add unit tests for QAOA cost function
test(src): add initial unit test suite for quantum algorithms

# Refactor
refactor(nisq): extract noise scaling into helper function

# Dependencies
chore(deps): pin qiskit to >=2.3
chore(deps): add scipy for classical optimization

# Config / tooling
chore(git): add conventional commits pre-commit hook

# Performance
perf(vqe): reduce circuit depth in QAOA ansatz

# Multiple modules (single commit)
test(src): add unit tests for bell-state, vqe and qml modules
```

## Rules

- Use **English** for all commit messages
- Keep the description **short** (under 72 characters)
- Use **imperative mood**: "add", "fix", "update" — not "added", "fixed"
- One responsibility per commit when possible
- For multiple files in one commit, use a broader scope (`src`, `docs`)
