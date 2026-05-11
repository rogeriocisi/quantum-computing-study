# SPEC-07: Simon's Algorithm

## 1. Overview
Simon's algorithm provides an exponential speedup over classical probabilistic algorithms for finding a hidden period in a specific class of functions. It is a foundational query algorithm that demonstrates the power of quantum interference.

## 2. Problem Statement
-   **Input**: A black-box function $f: \{0,1\}^n \to \{0,1\}^m$.
-   **Promise**: There exists a hidden string $s \in \{0,1\}^n$ such that $f(x) = f(y)$ if and only if $x \oplus y \in \{0, s\}$.
-   **Goal**: Find the hidden string $s$.
-   **Classical Complexity**: $O(2^{n/2})$ queries.
-   **Quantum Complexity**: $O(n)$ queries + classical linear algebra (Gaussian elimination).

## 3. Implementation Strategy

### 3.1. Quantum Circuit
The circuit requires $2n$ qubits:
1.  **State Preparation**: $n$ input qubits in $|0\rangle$, $n$ output qubits in $|0\rangle$.
2.  **Superposition**: Hadamard gates on the first $n$ qubits.
3.  **Oracle**: Apply $U_f: |x\rangle|0\rangle \to |x\rangle|f(x)\rangle$.
4.  **Interference**: Hadamard gates on the first $n$ qubits.
5.  **Measurement**: Measure the first $n$ qubits.

### 3.2. Classical Post-processing
-   Each measurement returns a bitstring $y$ such that $y \cdot s = 0 \pmod 2$.
-   Collect $n-1$ linearly independent bitstrings to form a system of equations.
-   Solve for $s$ using Gaussian elimination over $GF(2)$.

## 4. Code Structure
-   **File**: `src/algorithms/simon.py`
-   **Key Functions**:
    - `build_simon_oracle(s: str) -> QuantumCircuit`: Constructs the Simon oracle.
    - `create_simon_circuit(oracle: QuantumCircuit) -> QuantumCircuit`: Builds the quantum circuit.
    - `solve_simon(counts: Dict[str, int], n: int) -> str`: Classical solver for the hidden period.
    - `run_simulation(qc: QuantumCircuit) -> Dict[str, int]`: Executes simulation using `SamplerV2`.

## 5. Success Criteria
-   Correctly retrieve $s$ for varying lengths (2 to 6 qubits).
-   Correctly handle the $s=0^n$ case (one-to-one function).
-   Full unit test coverage in `tests/test_simon.py`.
