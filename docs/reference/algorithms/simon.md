# Simon's Algorithm

## Overview
Simon's algorithm is a quantum query algorithm that solves *Simon's problem* with exponential speedup over classical probabilistic algorithms. It finds a hidden bitstring $s$ (the period) for a function $f: \{0,1\}^n \to \{0,1\}^m$ such that $f(x) = f(y)$ if and only if $y = x \oplus s$.

- **Classical Complexity**: $O(2^{n/2})$ queries (Birthday Paradox bound).
- **Quantum Complexity**: $O(n)$ queries + classical linear algebra.

This algorithm is historically significant as it inspired Peter Shor to develop his factoring algorithm.

---

## Algorithm Logic
The algorithm consists of a quantum part to gather linear equations and a classical part to solve them.

### 1. Quantum Part
1.  **Initialize**: $n$ qubits in $|0\rangle$ (input) and $n$ qubits in $|0\rangle$ (output).
2.  **Superposition**: Apply Hadamard gates ($H$) to the first $n$ qubits.
3.  **Oracle**: Apply $U_f$ which maps $|x\rangle |0\rangle \to |x\rangle |f(x)\rangle$.
4.  **Interference**: Apply Hadamard gates to the first $n$ qubits.
5.  **Measure**: Measure the first $n$ qubits to obtain a string $y$.
    - The interference ensures that only strings $y$ satisfying $y \cdot s = 0 \pmod 2$ are measured.

### 2. Classical Part
Repeat the quantum part until $n-1$ linearly independent strings $y_1, y_2, \dots, y_{n-1}$ are found. Solve the system of linear equations $M s = 0$ over $GF(2)$ to find the non-zero hidden string $s$.

---

## API Reference

The module `src.algorithms.simon` provides the implementation.

### `build_simon_oracle(s: str) -> QuantumCircuit`
Helper function to generate a Simon oracle for a secret string $s$.
- **Parameters**:
  - `s`: The secret bitstring (e.g., `"110"`).

### `create_simon_circuit(oracle: QuantumCircuit) -> QuantumCircuit`
Constructs the quantum circuit part of the algorithm.
- **Returns**: A `qiskit.QuantumCircuit` that performs the query and returns $y$.

### `solve_simon(counts: Dict[str, int], n: int) -> str`
Performs the classical post-processing to retrieve $s$ from the measured samples.

---

## Usage Example
```python
from src.algorithms.simon import build_simon_oracle, create_simon_circuit, solve_simon, run_simulation

# 1. Define secret
secret = "101"

# 2. Build and run
oracle = build_simon_oracle(secret)
qc = create_simon_circuit(oracle)
counts = run_simulation(qc)

# 3. Solve
found_s = solve_simon(counts, len(secret))
print(f"Secret: {found_s}")
```

## Implementation Details
- **Module**: [`src/algorithms/simon.py`](../../../src/algorithms/simon.py)
- **Test Suite**: [`tests/test_simon.py`](../../../tests/test_simon.py)
