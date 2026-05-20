# Grover's Search Algorithm

## Overview
**Grover's Search** is a quantum search algorithm that finds a specific item (or multiple items) in an unstructured database of size $N = 2^n$ in $O(\sqrt{N})$ queries. 

Unlike classical search which requires searching through each element one-by-one in the worst case (running in $O(N)$ linear time), Grover's search provides a **quadratic quantum speedup**. While not exponential, quadratic speedup is incredibly versatile and can be applied to speed up NP-complete and combinatorial optimization problems.

- **Classical Complexity**: $O(N)$ queries.
- **Quantum Complexity**: $O(\sqrt{N})$ queries.

---

## Core Concepts & Amplitude Amplification
The algorithm does not search by "looking" at values. Instead, it uses **Amplitude Amplification** to systematically increase the probability amplitude of the target state(s) while decreasing the amplitudes of non-target states.

The algorithm consists of three main phases repeated iteratively:

### 1. State Initialization
All $n$ qubits are initialized to $|0\rangle^{\otimes n}$ and put into a uniform superposition using Hadamard gates:

$$|s\rangle = H^{\otimes n} |0\rangle^{\otimes n} = \frac{1}{\sqrt{N}} \sum_{x=0}^{N-1} |x\rangle$$

This distributes equal amplitude $\frac{1}{\sqrt{N}}$ to all possible search states.

### 2. The Grover Iteration
The Grover iteration is repeated approximately $R \approx \frac{\pi}{4}\sqrt{N}$ times and consists of two operators:

#### A. The Oracle ($U_\omega$)
The oracle identifies the target state $|\omega\rangle$ and flips its sign (phase) while leaving other states unchanged:

$$U_\omega |x\rangle = \begin{cases} -|x\rangle & \text{if } x = \omega \\ |x\rangle & \text{if } x \neq \omega \end{cases}$$

This reflects the quantum state vector about the hyperplane perpendicular to the target state.

#### B. The Diffuser ($U_s$)
The diffuser (also known as the "reflection about the mean" operator) reflects all amplitudes about the average (mean) amplitude:

$$U_s = 2|s\rangle\langle s| - I$$

Geometrically, this increases the positive amplitude of the target state (which was made negative by the oracle) while lowering the amplitudes of all non-target states.

---

## Execution Workflow
```mermaid
graph TD
    A[Start: |00...0>] --> B[H^⊗n Superposition]
    B --> C[Oracle: Flip Target Phase]
    C --> D[Diffuser: Reflect About Mean]
    D --> E{Iterated R times?}
    E -- No --> C
    E -- Yes --> F[Measure Qubits]
    F --> G[Target state found with high probability]
```

---

## Implementation Details & API Reference

The algorithm is fully implemented in [grover.py](file:///c:/Antigravity/quantum-computing-study/src/algorithms/grover.py) as a first-class, standalone, tested Python module.

### Core API Functions

*   `build_grover_oracle(target: str) -> QuantumCircuit`
    *   Constructs a phase oracle for a specific binary target string (e.g. `"101"`).
    *   Applies a multi-controlled $Z$ phase flip dynamically. To align with Qiskit's little-endian bit ordering convention, the target string is reversed. For qubits where the target bit is `'0'`, $X$ gates are applied before and after the controlled $Z$ gate to selectively invert only the target state's phase.
*   `build_grover_diffuser(n_qubits: int) -> QuantumCircuit`
    *   Constructs the standard $n$-qubit amplitude amplification operator (diffuser): $H^{\otimes n} (2|0\rangle\langle 0| - I) H^{\otimes n}$.
    *   Utilizes a multi-controlled $Z$ phase flip on the zero state.
*   `optimal_iterations(n_qubits: int) -> int`
    *   Calculates the mathematically optimal number of query iterations: $R = \lfloor \frac{\pi}{4}\sqrt{2^n} \rfloor$.
*   `create_grover_circuit(target: str, iterations: Optional[int] = None) -> QuantumCircuit`
    *   Orchestrates the entire Grover search circuit. Prepares the equal superposition, runs the oracle and diffuser pair $R$ times, and appends measurements to all qubits.
*   `run_simulation(qc: QuantumCircuit, shots: int = 1024) -> Optional[Dict[str, int]]`
    *   Simulates the compiled circuit using modern Qiskit Aer `AerSimulator` and the high-fidelity `SamplerV2` primitive.

---

## Usage Example

```python
from src.algorithms.grover import create_grover_circuit, run_simulation, optimal_iterations

# 1. Define target search state
target_state = "101"
n = len(target_state)

# 2. Compute optimal number of iterations (R = 2 for 3 qubits)
r = optimal_iterations(n)

# 3. Create full circuit
qc = create_grover_circuit(target_state, r)

# 4. Simulate locally
counts = run_simulation(qc)
print("Measured counts:", counts)
# Output will show '101' with >90% success probability!
```

---

## Verification & Automated Tests

A comprehensive unit test suite is implemented in [test_grover.py](file:///c:/Antigravity/quantum-computing-study/tests/test_grover.py) verifying the mathematical correctness and physical success criteria:
*   `test_optimal_iterations`: Verifies the theoretical iterations calculator for $n \in \{1, 2, 3, 4\}$.
*   `test_oracle_structure` & `test_diffuser_structure`: Asserts exact qubit bounds and register names.
*   `test_end_to_end_2_qubits`: Simulates searches for all 4 states (`"00"`, `"01"`, `"10"`, `"11"`) confirming success rates $\ge 98\%$.
*   `test_end_to_end_3_qubits` & `test_end_to_end_4_qubits`: Validates target state searches (e.g. `"101"`, `"1100"`) confirming success rates $\ge 90\%$.

