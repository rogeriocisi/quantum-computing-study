# SPEC-10: Quantum Phase Estimation (QPE)

## 1. Overview
Quantum Phase Estimation (QPE) is a key subroutine in quantum computing, designed to estimate the phase $\phi$ of an eigenvalue $e^{2\pi i \phi}$ for a unitary operator $U$ given its eigenstate $|\psi\rangle$. It forms the core quantum engine for Shor's factoring algorithm, the HHL solver, and quantum chemistry.

## 2. Problem Statement
-   **Input**: A unitary operator $U$ and an eigenstate $|\psi\rangle$ such that $U|\psi\rangle = e^{2\pi i \phi}|\psi\rangle$, where $0 \le \phi < 1$.
-   **Goal**: Estimate the phase $\phi$ to high precision.
-   **Classical Complexity**: Exponential in the required precision bits.
-   **Quantum Complexity**: Polynomial in the precision (controlled by the number of counting qubits $t$).

## 3. Implementation Strategy

### 3.1. Quantum Circuit
The circuit requires $t$ counting qubits and $m$ target qubits (1 target qubit for single-qubit unitaries):
1.  **State Preparation**: 
    - Initialize counting register to $|0\rangle^{\otimes t}$ and apply Hadamards to put it in a uniform superposition.
    - Prepare the target register in the eigenstate $|\psi\rangle$. For $U = P(2\pi\phi)$, the target qubit is prepared in $|1\rangle$ using an $X$ gate.
2.  **Controlled-Unitary evolution**: Apply controlled-$U^{2^j}$ gates where qubit $j$ of the counting register acts as control on the target. This encodes the phase values directly onto the counting qubits through **Phase Kickback**:
    $$\frac{1}{\sqrt{2^t}}\sum_{x=0}^{2^t-1} e^{2\pi i \phi x} |x\rangle |\psi\rangle$$
3.  **Inverse Fourier Transform (IQFT)**: Apply the Inverse Quantum Fourier Transform to the counting register using `QFTGate(t).inverse()` to transform the phase amplitudes back into computational basis states.
4.  **Measurement**: Measure the counting register to obtain bitstring $b$.

### 3.2. Phase Decoding
-   Convert the most frequent bitstring $b$ to decimal fraction:
    $$\phi_{est} = \frac{\text{int}(b, 2)}{2^t}$$

## 4. Code Structure
-   **File**: `src/algorithms/qpe.py`
-   **Key Functions**:
    -   `create_qpe_circuit(phi: float, n_counting: int) -> QuantumCircuit`: Constructs the complete QPE circuit with $t$ counting qubits and a single-qubit phase rotation operator $P(2\pi\phi)$ on target $|1\rangle$.
    -   `run_simulation(qc: QuantumCircuit, shots: int = 2048) -> Optional[Dict[str, int]]`: Simulates the circuit using `SamplerV2` and `AerSimulator`.
    -   `solve_qpe(counts: Dict[str, int], n_counting: int) -> Tuple[float, str]`: Decodes measurement counts to return the estimated phase $\phi_{est}$ and the corresponding bitstring.

## 5. Success Criteria
-   Exact phase estimation for binary-expressible phases (e.g. $\phi \in \{0.5, 0.25, 0.125, 0.75\}$) where $\phi_{est} = \phi$ with 100% precision in simulation.
-   Rational convergence with bounded error ($\le \frac{1}{2^t}$) and correct peak probability distribution for irrational phases (e.g. $\phi = 1/3 \approx 0.33333$).
-   Full unit test coverage in `tests/test_qpe.py` with passing assertions.
