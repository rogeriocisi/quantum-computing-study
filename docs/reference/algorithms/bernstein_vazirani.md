# Bernstein-Vazirani Algorithm

## Overview
The Bernstein-Vazirani algorithm is a quantum algorithm that finds a hidden bitstring $s$ in a single query to a black-box function $f(x) = s \cdot x \pmod 2$.

- **Classical Complexity**: A classical computer requires $n$ queries (one for each bit of the string $s$) by querying $x = 2^i$ for $i=0, \dots, n-1$.
- **Quantum Complexity**: A quantum computer requires exactly **1 query**.

---

## Algorithm Logic
The algorithm is a variation of the Deutsch-Jozsa algorithm and uses the same circuit structure:

1.  **State Preparation**: Initialize $n$ qubits to $|0\rangle$ and 1 ancilla to $|1\rangle$.
2.  **Superposition**: Apply Hadamard gates to all $n+1$ qubits.
3.  **Oracle Application**: Apply the oracle $U_f$ which implements $f(x) = s \cdot x$. Due to Phase Kickback, the state becomes:
    $$\frac{1}{\sqrt{2^n}} \sum_{x \in \{0,1\}^n} (-1)^{s \cdot x} |x\rangle |-\rangle$$
4.  **Interference**: Apply Hadamard gates to the $n$ input qubits.
5.  **Measurement**: The result of the measurement is exactly the string $s$.

---

## API Reference

The module `src.algorithms.deutsch_jozsa` provides the implementation.

### `build_bv_oracle(s: str) -> QuantumCircuit`
Helper function to generate an oracle for a given secret string $s$.
- **Parameters**:
  - `s`: The secret bitstring (e.g., `"1011"`).

### `create_query_circuit(oracle: QuantumCircuit) -> QuantumCircuit`
Constructs the full quantum circuit. (Shared with Deutsch-Jozsa).

### `run_simulation(qc: QuantumCircuit) -> Optional[Dict[str, int]]`
Executes the circuit on a local simulator.

---

## Usage Example
```python
from src.algorithms.deutsch_jozsa import build_bv_oracle, create_query_circuit, run_simulation

# 1. Define secret string
secret = "1101"

# 2. Build the oracle
oracle = build_bv_oracle(secret)

# 3. Create and run circuit
qc = create_query_circuit(oracle)
counts = run_simulation(qc)

# 4. Extract result
measured = max(counts, key=counts.get)
print(f"Hidden string found: {measured}")
assert measured == secret
```

## Implementation Details
- **Module**: [`src/algorithms/deutsch_jozsa.py`](../../../src/algorithms/deutsch_jozsa.py)
- **Test Suite**: [`tests/test_deutsch_jozsa.py`](../../../tests/test_deutsch_jozsa.py)
- **Specification**: [`docs/system/specs/06-query_algorithms.md`](../../system/specs/06-query_algorithms.md)
