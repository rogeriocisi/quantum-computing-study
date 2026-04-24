# Quantum Developer Roadmap — 12-Month Detailed Plan

| **Month** | **Focus** | **Weekly Milestones (summary)** | **Monthly Deliverable** |
| --- | --- | --- | --- |
| **Month 1** | Foundations & Qubits | Wk 1: Dirac/Bloch; Wk 2: Applied linear algebra; Wk 3: Gates & measurements; Wk 4: Simulator setup | Notes + 5 basic notebooks |
| **Month 2** | Algorithms I — Part A | Wk 5: Oracles; Wk 6: Phase kickback; Wk 7: Deutsch; Wk 8: Deutsch-Jozsa | 3 notebooks with visualizations |
| **Month 3** | Algorithms I — Part B | Wk 9: Bernstein-Vazirani; Wk 10: Simon's theory; Wk 11: Simon's implementation; Wk 12: Debugging | Mini-project: pattern detection |
| **Month 4** | Algorithms I — Part C | Wk 13: Core Logic Review; Wk 14: Qiskit v2 SDK; Wk 15: OpenQASM; Wk 16: Unit Testing | Utility library + examples |
| **Month 5** | Intro to QML (PennyLane) | Wk 17: VQC concepts; Wk 18: PennyLane setup; Wk 19: Simple training; Wk 20: Baseline comparison | Comparative QML notebook |
| **Month 6** | Advanced Algorithms II | Wk 21: Grover's Search; Wk 22: QFT; Wk 23: Phase Estimation (QPE); Wk 24: Shor's (Conceptual) | 3 advanced notebooks |
| **Month 7** | Applied QML — Part A | Wk 25: QAOA theory; Wk 26: QAOA implementation; Wk 27: VQE theory; Wk 28: VQE implementation | Small optimization project |
| **Month 8** | Applied QML — Part B | Wk 29: Hybrid PennyLane+Qiskit; Wk 30: Classical optimizers; Wk 31: CI for experiments; Wk 32: Documentation | Hybrid pipeline + CI |
| **Month 9** | NISQ & Noise Reality | Wk 33: Conceptual noise; Wk 34: ZNE/M3 mitigation; Wk 35: Calibration; Wk 36: Hardware tests | Mitigation report |
| **Month 10** | Buffer & Review | Wk 37: Algorithm review; Wk 38: Qiskit SDK review; Wk 39: Mock exams; Wk 40: Gap fixing | C1000-179 topic checklist |
| **Month 11** | Capstone & Exam — Part A | Wk 41: Problem definition; Wk 42: Architecture; Wk 43: Implementation; Wk 44: Hardware runs | Capstone MVP |
| **Month 12** | Capstone & Exam — Part B | Wk 45: CI/CD; Wk 46: Tech documentation; Wk 47: Final practice; Wk 48: IBM Exam | Final App + Certification |

---

## Detailed Weekly Breakdown

### Month 1 — Foundations & Qubits
*   **Week 1 — Core Concepts**: Dirac notation, pure/mixed states, Bloch sphere.
*   **Week 2 — Applied Linear Algebra**: Vectors, matrices, inner products, tensors, eigenvalues.
*   **Week 3 — Gates & Measurements**: Pauli, Hadamard, CNOT, phase gates; measurement and probabilities.
*   **Week 4 — Local Simulator Setup**: Qiskit v2.x environment; running statevector and qasm simulators.

### Months 2–4 — Core Quantum Logic (Algorithms I)
*   **Week 5 — Oracles & Phase Kickback**: Understanding how classical functions are mapped to quantum operators.
*   **Week 6 — Deutsch & Deutsch-Jozsa**: The first demonstration of quantum speedup.
*   **Week 7 — Bernstein-Vazirani**: Learning about the hidden string problem and query complexity.
*   **Week 8 — Logic Review**: Consolidating oracle design and interference logic.
*   **Week 9 — Simon's Theory**: Period finding and the bridge to Shor's algorithm.
*   **Week 10 — Simon's Implementation**: Building the circuit and classical post-processing.
*   **Week 11 — Debugging & Unit Testing**: Learning how to test quantum code and handle probabilistic outputs.
*   **Week 12 — Mini-project: Pattern Detection**: A small project using Simon's logic.
*   **Week 13 — Core Logic Refinement**: Deep dive into state transformation and unitary matrices.
*   **Week 14 — Qiskit v2 SDK Patterns**: Primitives (Sampler, Estimator) and session management.
*   **Week 15 — OpenQASM 3.0**: Exporting circuits and low-level circuit description.
*   **Week 16 — Advanced Unit Testing**: Using `pytest` with Qiskit Aer for regression testing.

### Month 5 — Introduction to QML with PennyLane
*   **Week 17 — VQC Concepts**: Variational Quantum Circuits as "learnable" blocks.
*   **Week 18 — PennyLane Setup**: Installation and integration with Qiskit backends.
*   **Week 19 — Simple VQC Training**: Implementing a basic classifier for synthetic data.
*   **Week 20 — Comparison with Classical Baseline**: Benchmarking against standard Neural Networks.

### Month 6 — Advanced Algorithms II
*   **Week 21 — Grover's Search**: Amplitude amplification and database search.
*   **Week 22 — Quantum Fourier Transform (QFT)**: Mathematical core and implementation.
*   **Week 23 — Phase Estimation (QPE)**: Estimating eigenvalues of unitaries.
*   **Week 24 — Shor's (Conceptual)**: Understanding the factoring algorithm components without full implementation.

### Months 7–8 — Applied QML & Optimization
*   **Week 25 — QAOA Theory**: Quantum Approximate Optimization Algorithm for combinatorial problems.
*   **Week 26 — QAOA Implementation**: Solving MaxCut or similar optimization problems.
*   **Week 27 — VQE Theory**: Variational Quantum Eigensolver for chemistry and physics.
*   **Week 28 — VQE Implementation**: Simulating the ground state of a small molecule (e.g., H2).
*   **Week 29 — Hybrid Workflows**: Advanced integration between PennyLane and Qiskit Runtime.
*   **Week 30 — Classical Optimizers**: Exploring `scipy`, `optuna`, and other optimization loops.
*   **Week 31 — CI for Experiments**: Setting up GitHub Actions to run notebooks via `papermill`.
*   **Week 32 — Documentation & Reproducibility**: Creating experiment templates and technical logs.

### Month 9 — NISQ Era & Noise Reality
*   **Week 33 — Noise & Decoherence Concepts**: Relaxation (T1) and dephasing (T2) times.
*   **Week 34 — Mitigation Techniques (ZNE, M3)**: Conceptual understanding of error suppression.
*   **Week 35 — Backend Calibration**: Learning to read and interpret backend properties (error rates).
*   **Week 36 — Real Hardware Tests**: Submitting small jobs to IBM Quantum systems and analyzing results.

### Month 10 — Buffer & Deep Review
*   **Week 37 — Algorithm Review**: Flashcards and deep dives into weak areas.
*   **Week 38 — Qiskit SDK Review**: Finalizing mastery of the latest API patterns.
*   **Week 39 — Practice Exams**: Taking full-length mock exams for C1000-179.
*   **Week 40 — Gap Fixing**: Addressing specific topics revealed by practice exams.

### Months 11–12 — Capstone & IBM Certification
*   **Week 41 — Problem Definition**: Scope and success criteria for the final project.
*   **Week 42 — Architecture & CI/CD Plan**: Designing the hybrid pipeline.
*   **Week 43 — Implementation Phase 1**: Core quantum code and classical integration.
*   **Week 44 — Local Testing & Profiling**: Ensuring performance and correctness.
*   **Week 45 — Real Hardware Execution**: Submitting the final project to IBM systems.
*   **Week 46 — Post-processing & Visualization**: Analyzing hardware results vs. simulators.
*   **Week 47 — Final Tech Documentation**: Creating a professional README and technical report.
*   **Week 48 — IBM Certification Exam**: Attempting the C1000-179 certification.
*   **Week 49–50 — Portfolio Polishing**: Finalizing the GitHub repository for public view.
*   **Week 51–52 — Final Review & Post-Mortem**: Lessons learned and next steps in the quantum career.