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

The module `src.algorithms.deutsch_jozsa` provides a template-like implementation.

### `deutsch_jozsa(n_qubits: int = 2, balanced: bool = True) -> Optional[Dict[str, int]]`
Executes the full Deutsch-Jozsa algorithm.
- **Parameters**:
  - `n_qubits`: Number of input bits (excluding the ancilla).
  - `balanced`: Whether the mock oracle generated should be balanced (True) or constant (False).
- **Returns**: A dictionary of counts. If the function is constant, you will observe `'0...0'` with 100% probability.

### `build_oracle(n_qubits: int, balanced: bool = True) -> QuantumCircuit`
A helper function to generate mock oracles for testing.
- **Note**: In a real-world scenario, the oracle would be a "black box" provided to the algorithm.

---

## Usage Example
```python
from src.algorithms.deutsch_jozsa import deutsch_jozsa

# Test with 3 input qubits and a balanced oracle
counts = deutsch_jozsa(n_qubits=3, balanced=True)

print(f"Results: {counts}")
# Since it's balanced, we expect a non-zero bitstring result.
```

## Implementation Details
- **Module**: [`src/algorithms/deutsch_jozsa.py`](../../../src/algorithms/deutsch_jozsa.py)
- **Test Suite**: [`tests/test_deutsch_jozsa.py`](../../../tests/test_deutsch_jozsa.py)
