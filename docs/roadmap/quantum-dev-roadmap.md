# Quantum Developer Roadmap — 12-Month Detailed Plan

| **Month** | **Focus** | **Weekly Milestones (summary)** | **Monthly Deliverable** |
| --- | --- | --- | --- |
| **Month 1** | Foundations & Qubits | Wk 1: Dirac/Bloch; Wk 2: Applied linear algebra; Wk 3: Gates & measurements; Wk 4: Simulator setup | Notes + 5 basic notebooks |
| **Month 2** | Algorithms I — Core Logic | Wk 5: Oracles & kickback; Wk 6: Deutsch-Jozsa; Wk 7: Bernstein-Vazirani; Wk 8: Simon's implementation | 3 algorithms from scratch |
| **Month 3** | Advanced Algorithms II | Wk 9: Grover's Search; Wk 10: QFT; Wk 11: Phase Estimation (QPE); Wk 12: Shor's implementation | 3 advanced algorithms + tests |
| **Month 4** | QML with PennyLane I | Wk 13: VQC concepts; Wk 14: PennyLane setup; Wk 15: PennyLane-Qiskit; Wk 16: Device optimization | Simple VQC skeleton |
| **Month 5** | QML with PennyLane II | Wk 17: VQC training; Wk 18: Loss & gradients; Wk 19: Classification tests; Wk 20: Baseline comparison | Trained QML classifier |
| **Month 6** | Applied QML & Optimization I | Wk 21: QAOA theory & setup; Wk 22: QAOA implementation; Wk 23: VQE theory; Wk 24: VQE molecular run | QAOA/VQE optimization workflows |
| **Month 7** | Applied QML & Optimization II | Wk 25: Hybrid PennyLane+Qiskit; Wk 26: Classical optimizers; Wk 27: CI for experiments; Wk 28: Documentation | Hybrid QML pipeline + CI |
| **Month 8** | Industrial Capstone — Plan & Base | Wk 29: Problem definition; Wk 30: Architecture; Wk 31: Skeletons; Wk 32: Core unit testing | Capstone spec & skeletons |
| **Month 9** | Industrial Capstone — Noise | Wk 33: Noise modeling; Wk 34: ZNE mitigation; Wk 35: Calibration maps; Wk 36: Simulating real noise | Noise-resilient prototype |
| **Month 10** | Industrial Capstone — Launch | Wk 37: Cloud run; Wk 38: Performance profiling; Wk 39: Post-processing; Wk 40: Technical docs | Production capstone repo |
| **Month 11** | Exam Prep — SDK & Mock 1 | Wk 41: Algorithm review; Wk 42: Qiskit Primitives; Wk 43: Mock Exam 1; Wk 44: Gap fixing | Gap analysis & checklist |
| **Month 12** | Exam Prep & IBM Certification | Wk 45: Mock Exam 2; Wk 46: Final SDK practice; Wk 47: Official IBM C1000-179 Exam; Wk 48: Portfolio polishing | IBM Certified Developer Badge |

---

## Detailed Weekly Breakdown

### Month 1 — Foundations & Qubits (Weeks 1–4)
*   **Week 1 — Core Concepts**: Dirac notation, pure/mixed states, Bloch sphere.
*   **Week 2 — Applied Linear Algebra**: Vectors, matrices, inner products, tensors, eigenvalues.
*   **Week 3 — Gates & Measurements**: Pauli, Hadamard, CNOT, phase gates; measurement and probabilities.
*   **Week 4 — Local Simulator Setup**: Qiskit v2.x environment; running statevector and qasm simulators.

### Month 2 — Core Quantum Logic (Algorithms I) (Weeks 5–8)
*   **Week 5 — Oracles & Phase Kickback**: Understanding how classical functions are mapped to quantum operators.
*   **Week 6 — Deutsch-Jozsa**: First demonstration of exponential quantum speedup for constant/balanced functions.
*   **Week 7 — Bernstein-Vazirani**: Learning about the hidden string problem and single-query search complexity.
*   **Week 8 — Simon's Algorithm**: Period finding, quantum circuit compilation, and classical post-processing.

### Month 3 — Advanced Algorithms II (Weeks 9–12)
*   **Week 9 — Grover's Search**: Amplitude amplification, database search, oracle and diffuser construction.
*   **Week 10 — Quantum Fourier Transform (QFT)**: Mathematical definition and manual gate implementation.
*   **Week 11 — Quantum Phase Estimation (QPE)**: Estimating eigenvalues of unitaries via QFT and phase kickback.
*   **Week 12 — Shor's Algorithm**: Modular exponentiation, QPE execution, and continued fractions factorization.

### Month 4 — Quantum Machine Learning with PennyLane I (Weeks 13–16)
*   **Week 13 — VQC Concepts**: Variational Quantum Circuits as "learnable" blocks and quantum neural networks.
*   **Week 14 — PennyLane Setup**: Installation, backend configuration, and PennyLane-Qiskit integration.
*   **Week 15 — Device Integration**: Configuring Qiskit devices within the PennyLane ecosystem.
*   **Week 16 — Advanced Embedding**: Data encoding and feature maps (Angle/Amplitude embedding).

### Month 5 — Quantum Machine Learning with PennyLane II (Weeks 17–20)
*   **Week 17 — VQC Training**: Setting up cost functions and gradient descents in PennyLane.
*   **Week 18 — Optimization Loops**: Implementing basic training loops for synthetic datasets.
*   **Week 19 — Classification Evaluation**: Evaluating metrics (accuracy, precision) of VQC classifiers.
*   **Week 20 — Comparison with Classical Baseline**: Benchmarking against standard classical neural networks.

### Months 6–7 — Applied QML & Optimization (Weeks 21–28)
*   **Week 21 — QAOA Theory**: Quantum Approximate Optimization Algorithm for combinatorial problems (Max-Cut).
*   **Week 22 — QAOA Implementation**: Solving optimization models on local CPU simulators.
*   **Week 23 — VQE Theory**: Variational Quantum Eigensolver for molecular simulations and Hamiltonian ground states.
*   **Week 24 — VQE Implementation**: Simulating the ground state of small molecules (e.g., $H_2$).
*   **Week 25 — Hybrid Workflows**: Advanced integration between PennyLane and Qiskit Runtime APIs.
*   **Week 26 — Classical Optimizers**: Exploring `scipy`, `optuna`, and learning rate scheduling.
*   **Week 27 — CI for Experiments**: Setting up GitHub Actions to run experiments automatically via `papermill`.
*   **Week 28 — Technical Documentation**: Drafting technical reports and API references.

### Months 8–10 — Industrial Capstone (Weeks 29–40)
*   **Week 29 — Problem Definition**: Selecting project scope, industrial applications, and success metrics.
*   **Week 30 — Architecture Design**: Structuring the hybrid quantum-classical software architecture.
*   **Week 31 — Workspace Setup**: Initializing directories, dependencies, and configuration maps.
*   **Week 32 — Initial Code Skeletons**: Creating basic function definitions and structural layouts.
*   **Week 33 — Core Quantum Algorithms**: Implementing specific quantum modules of the capstone project.
*   **Week 34 — Classical Orchestration**: Building classical pre- and post-processing adapters.
*   **Week 35 — Pytest Unit Testing**: Writing thorough automated test suites.
*   **Week 36 — Integration**: Completing the baseline hybrid quantum-classical workflow.
*   **Week 37 — Noise & Decoherence Modeling**: Injecting realistic backend noise models (T1, T2 relaxation).
*   **Week 38 — Zero Noise Extrapolation (ZNE)**: Implementing error mitigation techniques on noisy data.
*   **Week 39 — Backend Calibration**: Processing backend calibration reports to optimize qubit routing.
*   **Week 40 — Launch & Report**: Performance profiling, cloud hardware run, and compiling the final technical report.

### Months 11–12 — Exam Prep & IBM Certification (Weeks 41–48)
*   **Week 41 — Algorithm Review**: Deep-dive theoretical and mathematical review of all algorithms.
*   **Week 42 — Qiskit SDK Primitives**: Comprehensive review of Qiskit v2.x (Sampler, Estimator, Transpiler).
*   **Week 43 — Mock Exam 1**: Attempting the first full-length practice exam for the IBM C1000-179.
*   **Week 44 — Gap Fixing**: Targeting weak areas identified in Mock Exam 1.
*   **Week 45 — Mock Exam 2**: Attempting the second full-length practice exam.
*   **Week 46 — Final Practice**: Quick-fire code syntax review and flashcards.
*   **Week 47 — IBM Exam**: Taking the official **IBM Certified Associate Developer - Quantum Computation using Qiskit v2.X** exam.
*   **Week 48 — Portfolio Polishing**: Finalizing the GitHub repository for public presentation.