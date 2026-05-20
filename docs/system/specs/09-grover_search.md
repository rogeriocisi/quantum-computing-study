# SPEC-09: Grover's Search Algorithm

## 1. Overview
Grover's Search Algorithm provides a quadratic speedup over classical unstructured search. It locates a unique target item (or items) in an unstructured database of size $N = 2^n$ using amplitude amplification.

## 2. Problem Statement
-   **Input**: A black-box function (oracle) $f: \{0,1\}^n \to \{0,1\}$ such that $f(x) = 1$ if $x$ is the target state $\omega$, and $f(x) = 0$ otherwise.
-   **Goal**: Find the target state $\omega \in \{0,1\}^n$.
-   **Classical Complexity**: $O(2^n)$ queries (linear search).
-   **Quantum Complexity**: $O(\sqrt{2^n})$ queries (quadratic speedup).

## 3. Implementation Strategy

### 3.1. Quantum Circuit
The circuit operates on $n$ qubits without additional ancilla overhead:
1.  **State Preparation**: Initialize $n$ qubits in $|0\rangle^{\otimes n}$ and apply Hadamard gates $H^{\otimes n}$ to construct an equal superposition $|s\rangle$.
2.  **Oracle ($U_\omega$)**: Applies a phase flip to the target state $|\omega\rangle$, changing its amplitude sign:
    $$U_\omega |x\rangle = (-1)^{f(x)} |x\rangle$$
    This is implemented dynamically by applying $X$ gates to qubits that are `'0'` in the target string, performing a multi-controlled $Z$ phase flip, and reverting the $X$ gates.
3.  **Diffuser ($U_s$)**: Amplifies the target state amplitude by reflecting all amplitudes about the average (mean) amplitude:
    $$U_s = H^{\otimes n} (2|0\rangle\langle 0| - I) H^{\otimes n}$$
4.  **Iteration**: Repeat the pair $(U_\omega \to U_s)$ exactly $R = \lfloor \frac{\pi}{4}\sqrt{2^n} \rfloor$ times.
5.  **Measurement**: Measure all $n$ qubits.

## 4. Code Structure
-   **File**: `src/algorithms/grover.py`
-   **Key Functions**:
    -   `build_grover_oracle(target: str) -> QuantumCircuit`: Constructs the phase-inversion oracle for the target.
    -   `build_grover_diffuser(n_qubits: int) -> QuantumCircuit`: Constructs the amplitude amplification operator.
    -   `optimal_iterations(n_qubits: int) -> int`: Computes the mathematically optimal number of query iterations.
    -   `create_grover_circuit(target: str, iterations: Optional[int] = None) -> QuantumCircuit`: Assembles the full Grover quantum circuit with measurements.
    -   `run_simulation(qc: QuantumCircuit, shots: int = 1024) -> Optional[Dict[str, int]]`: Simulates the circuit using `SamplerV2` and `AerSimulator`.

## 5. Success Criteria
-   The optimal iteration count must be computed accurately (e.g. $R=1$ for $n=2$, $R=2$ for $n=3$, $R=3$ for $n=4$).
-   End-to-end simulations must yield a measurement probability of $>90\%$ for the target bitstring.
-   Support arbitrary target strings dynamically without hardcoded bounds or ancilla requirements.
-   Full unit test coverage in `tests/test_grover.py` with passing assertions on physical success criteria.
