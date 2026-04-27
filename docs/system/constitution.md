# Project Constitution — Quantum Computing Study 📜

> **Rule 0: Governing Authority**
> Antigravity AI (and any other agentic tools) MUST read and adhere to the standards defined in this document for every code generation, architectural decision, or repository modification.

---

## 1. Mission & Vision
- **Primary Goal**: Successfully pass the **IBM Certified Associate Developer - Quantum Computation using Qiskit v2.x** (Exam C1000-179).
- **Vision**: Transform a Software Developer's mindset into a **Quantum Software Engineer** by mastering the hybrid classical-quantum paradigm.

## 2. Tech Stack Constraints
- **Language**: Python 3.10+
- **Primary SDK**: **Qiskit 2.x** (v2.3+ as of 2026). This is mandatory for the C1000-179 exam. Use `SamplerV2` and `EstimatorV2` primitives. Do NOT use deprecated patterns from v0.x or v1.x (e.g., `execute()`, Qiskit Pulse was removed in 2.0).
- **QML Framework**: PennyLane (integration with Qiskit).
- **Simulation**: Qiskit Aer (local), IBM Quantum Runtime (remote).
- **Environment**: Virtual environment managed via `pip` and `requirements.txt`.

## 3. Communication & Language
- **Primary Language**: English. All code comments, documentation, and commit messages must be in English.
- **Audience**: International researchers and professional developers.

## 4. Repository Structure & Standards
- **Source Code (`src/`)**: Reusable modules organized by domain (`algorithms/`, `qml/`, `optimization/`, `utils/`).
- **Scratch / Prototypes (`src/scratch/`)**: Fast prototyping, isolated concept testing, and experimental code. Visible and tracked in Git for knowledge sharing.
- **Execution Scripts (`scripts/`)**: Standalone runners that import from `src/` (e.g., `capstone_demo.py`). These are not importable modules.
- **Notebooks (`notebooks/`)**: Used for Phase 1-6 learning and prototyping.
- **Governance (`docs/system/`)**:
    - `constitution.md`: This document.
    - `specs/`: Detailed technical specifications for every major module.
    - `architecture.md`: High-level design and workflows.

## 5. Coding Standards
- **Style**: Adhere to PEP 8.
- **Documentation**: Every function must have a Google-style docstring.
- **Types**: Use Python Type Hints for all function signatures.
- **Testing**: Every module in `src/` should have a corresponding test in `tests/`.

## 6. SDD Workflow (Spec-Driven Development)
1. Define intent in a new `docs/system/specs/*.md` file.
2. Review architecture in `docs/system/architecture.md` if the change is structural.
3. Implement in `src/`.
4. Validate with `tests/`.

---
*Authorized by Antigravity AI & The User — April 2026*
