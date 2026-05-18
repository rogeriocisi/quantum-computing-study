# Quantum Developer Roadmap — 12-Month Detailed Plan

| **Month** | **Focus** | **Weekly Milestones (summary)** | **Monthly Deliverable** |
| --- | --- | --- | --- |
| **Month 1** | Foundations & Qubits | Wk 1: Dirac/Bloch; Wk 2: Applied linear algebra; Wk 3: Gates & measurements; Wk 4: Simulator setup | Notes + 5 basic notebooks |
| **Month 2** | Algorithms I — Core Logic | Wk 5: Oracles & kickback; Wk 6: Deutsch-Jozsa; Wk 7: Bernstein-Vazirani; Wk 8: Simon's implementation | 3 algorithms from scratch |
| **Month 3** | Advanced Algorithms II | Wk 9: Grover's Search; Wk 10: QFT; Wk 11: Phase Estimation (QPE); Wk 12: Shor's implementation | 3 advanced algorithms + tests |
| **Month 4** | Intro to QML (PennyLane) | Wk 13: VQC concepts; Wk 14: PennyLane setup; Wk 15: Simple VQC training; Wk 16: Baseline comparison | Simple VQC classifier |
| **Month 5** | Applied QML & Optimization I | Wk 17: QAOA theory & setup; Wk 18: QAOA implementation; Wk 19: VQE theory; Wk 20: VQE molecular run | QAOA/VQE optimization workflows |
| **Month 6** | Applied QML & Optimization II | Wk 21: Hybrid PennyLane+Qiskit; Wk 22: Classical optimizers; Wk 23: CI for experiments; Wk 24: Documentation | Hybrid QML pipeline + CI |
| **Month 7** | Industrial Capstone — Plan | Wk 25: Problem definition; Wk 26: Architecture design; Wk 27: Workspace & setup; Wk 28: Initial code skeletons | Capstone specification document |
| **Month 8** | Industrial Capstone — Build I | Wk 29: Core quantum algorithms; Wk 30: Classical orchestration; Wk 31: Pytest unit testing; Wk 32: Integration | Working local prototype |
| **Month 9** | Industrial Capstone — Build II | Wk 33: Noise & decoherence modeling; Wk 34: ZNE error mitigation; Wk 35: Backend calibration; Wk 36: Simulating real noise | Noise-resilient implementation |
| **Month 10** | Industrial Capstone — Launch | Wk 37: Cloud run; Wk 38: Performance profiling; Wk 39: Result post-processing; Wk 40: Technical docs | Production-grade Capstone portfolio |
| **Month 11** | Exam Prep — Review | Wk 41: Algorithm deep review; Wk 42: Qiskit Primitives & API; Wk 43: Mock Exam 1; Wk 44: Gap fixing | C1000-179 topic review checklist |
| **Month 12** | Exam Prep & Certification | Wk 45: Mock Exam 2; Wk 46: Final SDK practice; Wk 47: Official IBM C1000-179 Exam; Wk 48: Portfolio polishing | IBM Certified Developer Badge |

---

## Detailed Weekly Breakdown

### Month 1 — Foundations & Qubits
*   **Week 1 — Core Concepts**: Dirac notation, pure/mixed states, Bloch sphere.
*   **Week 2 — Applied Linear Algebra**: Vectors, matrices, inner products, tensors, eigenvalues.
*   **Week 3 — Gates & Measurements**: Pauli, Hadamard, CNOT, phase gates; measurement and probabilities.
*   **Week 4 — Local Simulator Setup**: Qiskit v2.x environment; running statevector and qasm simulators.

### Month 2 — Core Quantum Logic (Algorithms I)
*   **Week 5 — Oracles & Phase Kickback**: Understanding how classical functions are mapped to quantum operators.
*   **Week 6 — Deutsch-Jozsa**: First demonstration of exponential quantum speedup for constant/balanced functions.
*   **Week 7 — Bernstein-Vazirani**: Learning about the hidden string problem and single-query search complexity.
*   **Week 8 — Simon's Algorithm**: Period finding, quantum circuit compilation, and classical post-processing.

### Month 3 — Advanced Algorithms II
*   **Week 9 — Grover's Search**: Amplitude amplification, database search, oracle and diffuser construction.
*   **Week 10 — Quantum Fourier Transform (QFT)**: Mathematical definition and manual gate implementation.
*   **Week 11 — Quantum Phase Estimation (QPE)**: Estimating eigenvalues of unitaries via QFT and phase kickback.
*   **Week 12 — Shor's Algorithm**: Modular exponentiation, QPE execution, and continued fractions factorization.

### Month 4 — Introduction to QML with PennyLane
*   **Week 13 — VQC Concepts**: Variational Quantum Circuits as "learnable" blocks and quantum neural networks.
*   **Week 14 — PennyLane Setup**: Installation, backend configuration, and PennyLane-Qiskit integration.
*   **Week 15 — Simple VQC Training**: Implementing a basic classifier for synthetic datasets.
*   **Week 16 — Comparison with Classical Baseline**: Benchmarking against standard classical neural networks.

### Months 5–6 — Applied QML & Optimization
*   **Week 17 — QAOA Theory**: Quantum Approximate Optimization Algorithm for combinatorial problems (Max-Cut).
*   **Week 18 — QAOA Implementation**: Solving optimization models on local CPU simulators.
*   **Week 19 — VQE Theory**: Variational Quantum Eigensolver for molecular simulations and Hamiltonian ground states.
*   **Week 20 — VQE Implementation**: Simulating the ground state of small molecules (e.g., $H_2$).
*   **Week 21 — Hybrid Workflows**: Advanced integration between PennyLane and Qiskit Runtime APIs.
*   **Week 22 — Classical Optimizers**: Exploring `scipy`, `optuna`, and learning rate scheduling.
*   **Week 23 — CI for Experiments**: Setting up GitHub Actions to run experiments automatically via `papermill`.
*   **Week 24 — Technical Documentation**: Drafting technical reports and API references.

### Months 7–10 — Industrial Capstone
*   **Week 25 — Problem Definition**: Selecting project scope, industrial applications, and success metrics.
*   **Week 26 — Architecture Design**: Structuring the hybrid quantum-classical software architecture.
*   **Week 27 — Workspace Setup**: Initializing directories, dependencies, and configuration maps.
*   **Week 28 — Initial Code Skeletons**: Creating basic function definitions and structural layouts.
*   **Week 29 — Core Quantum Algorithms**: Implementing specific quantum modules of the capstone project.
*   **Week 30 — Classical Orchestration**: Building classical pre- and post-processing adapters.
*   **Week 31 — Pytest Unit Testing**: Writing thorough automated test suites.
*   **Week 32 — Integration**: Completing the baseline hybrid quantum-classical workflow.
*   **Week 33 — Noise & Decoherence Modeling**: Injecting realistic backend noise models (T1, T2 relaxation).
*   **Week 34 — Zero Noise Extrapolation (ZNE)**: Implementing error mitigation techniques on noisy data.
*   **Week 35 — Backend Calibration**: Processing backend calibration reports to optimize qubit routing.
*   **Week 36 — Real Noise Simulation**: Comparing noisy simulator runs against noiseless baselines.
*   **Week 37 — Cloud Run**: Preparing jobs for real hardware submission.
*   **Week 38 — Performance Profiling**: Profiling classical runtime bottlenecks and quantum gate counts.
*   **Week 39 — Result Post-processing**: Statistically decoding output measurements.
*   **Week 40 — Technical Documentation**: Compiling professional README files, charts, and final reports.

### Months 11–12 — Exam Prep & IBM Certification
*   **Week 41 — Algorithm Review**: Deep-dive theoretical and mathematical review of all algorithms.
*   **Week 42 — Qiskit SDK Primitives**: Comprehensive review of Qiskit v2.x (Sampler, Estimator, Transpiler).
*   **Week 43 — Mock Exam 1**: Attempting the first full-length practice exam for the IBM C1000-179.
*   **Week 44 — Gap Fixing**: Targeting weak areas identified in Mock Exam 1.
*   **Week 45 — Mock Exam 2**: Attempting the second full-length practice exam.
*   **Week 46 — Final Practice**: Quick-fire code syntax review and flashcards.
*   **Week 47 — IBM Exam**: Taking the official **IBM Certified Associate Developer - Quantum Computation using Qiskit v2.X** exam.
*   **Week 48 — Portfolio Polishing**: Finalizing the GitHub repository for public presentation.