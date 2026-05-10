# Deutsch-Jozsa Algorithm

## Overview
The Deutsch-Jozsa algorithm was the first example of a quantum algorithm that performs better than the best possible classical algorithm. It determines whether a black-box function (oracle) $f: \{0,1\}^n \rightarrow \{0,1\}$ is **constant** (same output for all inputs) or **balanced** (output 1 for exactly half of the inputs).

- **Classical Complexity**: In the worst case, a classical computer needs $2^{n-1} + 1$ queries.
- **Quantum Complexity**: A quantum computer needs exactly **1 query**.

---

## Algorithm Logic
The algorithm leverages **superposition** and **phase kickback** to analyze the function's global property in a single step:

1.  **State Preparation**: Initialize $n$ input qubits to $|0\rangle$ and 1 ancilla qubit to $|1\rangle$.
2.  **Superposition**: Apply Hadamard gates to all qubits to create a uniform superposition.
3.  **Oracle Application**: Apply the oracle $U_f$. Due to the ancilla being in $|-\rangle$, the phase kickback effect stores the function output in the phase:
    $$U_f |x\rangle |-\rangle = (-1)^{f(x)} |x\rangle |-\rangle$$
4.  **Interference**: Apply Hadamard gates to the $n$ input qubits again.
5.  **Measurement**: Measure the input qubits.
    - If the result is **all zeros** ($|00\dots0\rangle$), the function is **constant**.
    - If the result is **anything else**, the function is **balanced**.

---

## API Reference

The module `src.algorithms.deutsch_jozsa` provides implementations for query-based algorithms.

### `create_query_circuit(oracle: QuantumCircuit) -> QuantumCircuit`
Constructs the full quantum circuit for a query algorithm (DJ or BV).
- **Parameters**:
  - `oracle`: A `QuantumCircuit` representing the black-box function $f(x)$.
- **Returns**: A `qiskit.QuantumCircuit` with Phase Kickback preparation and final interference.

### `build_dj_oracle(n_qubits: int, balanced: bool = True) -> QuantumCircuit`
Helper function to generate oracles for the Deutsch-Jozsa problem.
- **Parameters**:
  - `n_qubits`: Number of input qubits.
  - `balanced`: If True, returns a balanced function; if False, returns a constant function.

### `run_simulation(qc: QuantumCircuit) -> Optional[Dict[str, int]]`
Executes the circuit on a local simulator.
- **Returns**: A dictionary of counts. If the function is constant, you will observe `'0...0'` with 100% probability.

---

## Usage Example
```python
from src.algorithms.deutsch_jozsa import build_dj_oracle, create_query_circuit, run_simulation

# 1. Build a balanced oracle for 3 qubits
oracle = build_dj_oracle(n_qubits=3, balanced=True)

# 2. Create the algorithm circuit
qc = create_query_circuit(oracle)

# 3. Simulate
counts = run_simulation(qc)
print(f"Results: {counts}")
# Since it's balanced, we expect a non-zero bitstring result (e.g., '111').
```

## Implementation Details
- **Module**: [`src/algorithms/deutsch_jozsa.py`](../../../src/algorithms/deutsch_jozsa.py)
- **Test Suite**: [`tests/test_deutsch_jozsa.py`](../../../tests/test_deutsch_jozsa.py)
- **Specification**: [`docs/system/specs/06-query_algorithms.md`](../../system/specs/06-query_algorithms.md)
