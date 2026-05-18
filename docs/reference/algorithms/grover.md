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

## Technical Project Details
*   **Grover Roadmap**: Standalone implementation of Grover's search, including query-based oracles and automatic diffuser construction, is planned for Month 6 of the study curriculum.
    *   **Roadmap Details**: [`docs/roadmap/quantum-dev-roadmap.md`](../../roadmap/quantum-dev-roadmap.md)
*   **Relation to Shor's**: Along with Shor's algorithm, Grover's search represents the twin pillar of core quantum speedups featured in the IBM certification syllabus.
