# Coding Standards & Development Workflow

This document defines the mandatory standards for all implementations in the Quantum Computing Study project.

## 1. Development Workflow (The Five Steps)
Every new implementation (algorithm, utility, or module) must follow these steps in order:

1.  **SPECIFICATION**: Create a detailed spec in `docs/system/specs/` (e.g., `05-chsh_game.md`).
2.  **IMPLEMENTATION**: Write the code in the appropriate `src/` subdirectory.
3.  **TESTING**: Create a unit test file in `tests/` and ensure 100% pass rate.
4.  **DOCUMENTATION**: Create a reference guide in `docs/reference/` for the new module.
5.  **ROADMAP UPDATE**: Add the implementation to the "Core Implementations" list in `README.md`.

---

## 2. Python Naming Conventions
To ensure consistency across the library, all quantum algorithms must implement the following core functions:

### `create_<name>_circuit(...)`
- **Purpose**: Purely responsible for constructing the `QuantumCircuit` object.
- **Input**: Configuration parameters (e.g., number of qubits, bitstrings, angles).
- **Output**: Returns a `qiskit.QuantumCircuit` object.
- **Restriction**: Should not run simulations or perform measurements unless they are part of the circuit logic.

### `run_simulation(qc, ...)`
- **Purpose**: Executes the circuit on a simulator (typically `AerSimulator`).
- **Input**: The `QuantumCircuit` and simulation parameters (e.g., shots).
- **Mandate**: MUST use `SamplerV2` (from `qiskit_aer.primitives` or `qiskit_ibm_runtime`) for count retrieval.
- **Output**: Returns measurement results (usually a `counts` dictionary).
- **Visuals**: May generate diagrams (`circuit.draw`) or histograms (`plot_histogram`) in the `outputs/` folder.

---

## 3. Structural Standards

### Execution Block
Every module in `src/` should be both a library and a runnable script. This is achieved using the `main()` pattern:
```python
def main() -> None:
    # 1. Create
    qc = create_example_circuit()
    # 2. Run
    results = run_simulation(qc)
    # 3. Analyze
    print(results)

if __name__ == "__main__":
    main()
```

### Quality Assurance
- **Formatting**: All code must be formatted with `black .`.
- **Linting**: Code must pass `flake8` checks.
- **Cleanup**: Unused imports must be removed using `autoflake`.
- **Imports**: Modules within the project should use absolute imports from `src`.
- **Documentation**: Every function must have a **Google-style** or **NumPy-style** docstring with type annotations.
