# SPEC-06: Query Algorithms (Deutsch-Jozsa & Bernstein-Vazirani)

## 1. Overview
Query algorithms are a class of quantum algorithms that solve problems involving a "black-box" function (oracle) with fewer queries than any classical algorithm. This specification covers two foundational query algorithms:
1.  **Deutsch-Jozsa (DJ)**: Determines if a function is constant or balanced.
2.  **Bernstein-Vazirani (BV)**: Finds a hidden bitstring $s$ used in a dot-product function.

## 2. Problem Statements

### 2.1. Deutsch-Jozsa
-   **Input**: A function $f: \{0,1\}^n \to \{0,1\}$ guaranteed to be either **constant** (same output for all inputs) or **balanced** (output 0 for half of inputs, 1 for the other half).
-   **Goal**: Determine if $f$ is constant or balanced.
-   **Classical Complexity**: $O(2^{n-1} + 1)$ queries in the worst case.
-   **Quantum Complexity**: Exactly **1 query**.

### 2.2. Bernstein-Vazirani
-   **Input**: A function $f: \{0,1\}^n \to \{0,1\}$ defined as $f(x) = s \cdot x \pmod 2$, where $s$ is a hidden bitstring.
-   **Goal**: Find the hidden string $s$.
-   **Classical Complexity**: $n$ queries (querying each bit position).
-   **Quantum Complexity**: Exactly **1 query**.

## 3. Implementation Strategy

### 3.1. Unified Circuit Structure
Both algorithms share the same circuit template:
1.  **Initialize**: $n$ input qubits in $|0\rangle$ and 1 ancilla qubit in $|1\rangle$.
2.  **Superposition**: Apply Hadamard gates ($H$) to all $n+1$ qubits. This puts the ancilla in the $|-\rangle$ state, enabling **Phase Kickback**.
3.  **Oracle**: Apply the unitary $U_f$ that implements the function $f$.
4.  **Interference**: Apply Hadamard gates to the $n$ input qubits.
5.  **Measure**: Measure the $n$ input qubits.

### 3.2. Result Interpretation
-   **DJ**: If the result is the all-zeros string ($|00...0\rangle$), the function is **constant**. Otherwise, it is **balanced**.
-   **BV**: The measured bitstring is exactly the hidden string $s$.

## 4. Code Structure
-   **File**: `src/algorithms/deutsch_jozsa.py`
-   **Key Functions**:
    - `build_dj_oracle(n_qubits, balanced)`: Constructs a DJ oracle.
    - `build_bv_oracle(s)`: Constructs a BV oracle.
    - `create_query_circuit(oracle)`: Builds the unified quantum circuit.
    - `run_simulation(qc)`: Simulates execution and returns counts.

## 5. Success Criteria
-   DJ must correctly identify constant/balanced functions with 100% accuracy in simulation.
-   BV must retrieve the secret string $s$ with 100% accuracy in simulation.
-   Full unit test coverage in `tests/test_deutsch_jozsa.py`.
