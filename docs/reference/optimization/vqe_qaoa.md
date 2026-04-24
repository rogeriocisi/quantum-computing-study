# Hybrid Quantum-Classical Optimization (VQE & QAOA)

## Overview
This module provides a foundation for hybrid quantum-classical algorithms, which are the cornerstone of the NISQ (Noisy Intermediate-Scale Quantum) era. It focuses on two primary paradigms:

- **VQE (Variational Quantum Eigensolver)**: Used to find the ground state energy of a Hamiltonian (essential for quantum chemistry and material science).
- **QAOA (Quantum Approximate Optimization Algorithm)**: A specialized version of VQE designed to solve combinatorial optimization problems (e.g., Max-Cut).

---

## Technical Details

### Variational Workflow
Both algorithms follow a similar iterative loop:
1.  **Ansatz Preparation**: A parametrized quantum circuit is prepared on the quantum device.
2.  **Measurement**: The expectation value of a cost function (Hamiltonian) is measured.
3.  **Classical Optimization**: A classical optimizer (e.g., COBYLA, SPSA) updates the circuit parameters to minimize the cost.

---

## API Reference

The module `src.optimization.vqe_qaoa` defines the interfaces for these workflows.

### `build_qaoa_ansatz(n_qubits: int = 4, p: int = 1) -> QuantumCircuit`
Generates a parametrized QAOA circuit.
- **Parameters**:
  - `n_qubits`: Number of qubits in the problem.
  - `p`: Number of layers (depth) of the ansatz. Higher $p$ usually leads to better approximations.
- **Returns**: A `qiskit.QuantumCircuit` with symbolic parameters.

### `vqe_workflow(ansatz: QuantumCircuit, hamiltonian: Any = None) -> np.ndarray`
Executes the hybrid optimization loop.
- **Parameters**:
  - `ansatz`: The variational circuit to optimize.
  - `hamiltonian`: The operator representing the problem to solve.
- **Returns**: A NumPy array of the optimized parameters.

---

## Usage Example
```python
from src.optimization.vqe_qaoa import build_qaoa_ansatz, vqe_workflow

# 1. Build a 4-qubit QAOA circuit
ansatz = build_qaoa_ansatz(n_qubits=4, p=2)

# 2. Run the optimization workflow
optimal_params = vqe_workflow(ansatz)

print(f"Optimal Parameters: {optimal_params}")
```

## Implementation Details
- **Module**: [`src/optimization/vqe_qaoa.py`](../../../src/optimization/vqe_qaoa.py)
- **Test Suite**: [`tests/test_vqe_qaoa.py`](../../../tests/test_vqe_qaoa.py)
