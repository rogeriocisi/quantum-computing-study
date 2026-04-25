# Quantum Computing Study: Roadmap & Resource Portal 🌌

This repository contains a comprehensive **12-month study roadmap** and practical implementations for transitioning from classical software engineering to **Quantum Computing Developer**, specifically targeting the **IBM Certified Associate Developer - Quantum Computation using Qiskit v2.X**.

---

## 🚀 The Mission
To transform software engineers and scientists into quantum-ready developers by mastering **Linear Algebra**, **Quantum Algorithms**, and **Hardware-Conscious Development** using the latest **Qiskit v2.x** framework.

---

## 📚 Academic Resource Portal
A curated selection of the best educational materials in the field. For the full list of books, courses, and papers, see the **[Detailed Resource Guide](docs/roadmap/resources.md)**.

### 📖 Essential Books
*   **The Best Starting Point**: *Introduction to Classical and Quantum Computing* by Thomas G. Wong.
*   **The Official Guide**: *Learn Quantum Computing using Qiskit* by IBM Qiskit Community.
*   **The "Bible" of the Field**: *Quantum Computation and Quantum Information* ("Mike & Ike") by Nielsen & Chuang.

---

## ✨ Core Implementations
Practical algorithms implemented from scratch with full technical documentation and unit testing.

*   **[Vedral-Barenco-Ekert (VBE) Adder](docs/reference/algorithms/vbe_adder.md)**: A reversible ripple-carry quantum adder. Implementation follows the 1996 seminal paper.
*   **[Bell State Generation](docs/reference/algorithms/bell_state.md)**: Fundamental 2-qubit entanglement circuit ($|\Phi^+\rangle$).
*   **[Deutsch-Jozsa Algorithm](docs/reference/algorithms/deutsch_jozsa.md)**: First algorithm to show exponential quantum speedup for black-box problems.
*   **[VQE & QAOA Optimization](docs/reference/optimization/vqe_qaoa.md)**: Hybrid workflows for chemistry and combinatorial problems.
*   **[Variational Quantum Classifier](docs/reference/qml/vqc.md)**: Supervised learning using PennyLane-Qiskit integration.
*   **[NISQ Error Mitigation](docs/reference/utils/nisq_mitigation.md)**: Zero Noise Extrapolation (ZNE) tools for noisy devices.

---

## 📅 Realistic Part-Time Roadmap (12 Months)
*Optimized for 6-10 hours/week. Refined for developers focusing on core logic and professional delivery. See the **[Full Roadmap Document](docs/roadmap/quantum-dev-roadmap.md)** for detailed phase-by-phase milestones.*

### Phase 1: Foundations & Qubits (Month 1)
*   **Goal**: Transition from classical logic to quantum state representation (Dirac & Bloch).

### Phase 2: Core Quantum Logic — Algorithms I (Months 2-4)
*   **Topics**: Oracles, Phase Kickback, Deutsch-Jozsa, Bernstein-Vazirani, Simon's Algorithm.
*   **Focus**: Mastery of the "Quantum Intuition" — where most developers face the steepest learning curve.

### Phase 3: Intro to QML with PennyLane (Month 5)
*   **Topics**: Variational Quantum Circuits (VQC) as "Quantum Neural Networks", PennyLane setup.
*   **Focus**: Early introduction to the "learnable" part of quantum computing.

### Phase 4: Advanced Algorithms II (Month 6)
*   **Topics**: Grover's Search, Quantum Fourier Transform (QFT), Phase Estimation (QPE), Shor's Algorithm.
*   **Goal**: Understanding the mathematical foundations and Qiskit implementations of complex routines.

### Phase 5: Applied QML & Optimization (Months 7-8)
*   **Topics**: QAOA for optimization, VQE for molecular simulation, Hybrid workflows.
*   **Focus**: Practical use of **PennyLane** and Qiskit for real-world problem solving.

### Phase 6: The NISQ Era & Noise Reality (Month 9)
*   **Topics**: Conceptual Noise, Decoherence, high-level Error Mitigation (ZNE/M3).
*   **Focus**: Understanding hardware limitations without diving too deep into physics.

### Phase 7: Buffer Month & Exam Deep Review (Month 10)
*   **Objective**: Identify and fill knowledge gaps, review all previous phases, and start targeted IBM C1000-179 prep.
*   **Focus**: Consolidation and "house cleaning" before the final push.

### Phase 8: Industrial Capstone & IBM Certification (Months 11-12)
*   **Final Project**: A professional-grade hybrid application with a full CI/CD pipeline and technical documentation.
*   **Certification**: Completion of the **IBM C1000-179 Exam**.

---

## 💻 Hardware Requirements

To bridge the gap between classical simulation and real-world execution, the following hardware setup is recommended:

### 🖥️ Local Simulation (High-Performance Workstation)
*Optimized for Quantum Simulation (Qiskit Aer GPU) and AI/LLM local workloads — no mining overhead.*

*   **CPU**: AMD Ryzen 7 9700X — High single-core clock speeds are essential for the classical optimization loops in QAOA/VQE. More energy-efficient than previous gen with no mining demand.
*   **RAM**: 32 GB DDR5-6000 (2x16 GB, Dual Channel) — The most critical component; quantum state-vector simulations are memory-intensive. Expandable to 64 GB if needed in later roadmap phases (QML/VQE).
*   **GPU**: NVIDIA RTX 4060 Ti 16 GB — Preferred over the 4070 12 GB for this use case: the extra VRAM enables simulation of ~28–30 qubits locally with `qiskit-aer-gpu` and `PennyLane Lightning-GPU`, vs. ~26 qubits with 12 GB.
*   **Storage**: 1 TB NVMe SSD — Sufficient for system, dev environments, and all roadmap projects.
*   **Motherboard**: AMD B650 — Reliable and cost-effective chipset, fully compatible with Ryzen 9000 series.
*   **PSU**: 650W 80+ Gold — Efficient power delivery; adequate without 24/7 mining load.
*   **Cooling**: High-performance Tower Air Cooler (e.g., DeepCool AK620) — Silent and stable for sustained simulation workloads.


### ☁️ Remote Quantum Access (Real Hardware)
*   **IBM Quantum Platform**: Access to utility-scale processors (127-qubit Eagle/Heron) via **IBM Quantum Runtime API**.
*   **AWS Braket**: Access to diverse architectures (IonQ, Rigetti, QuEra) using the Braket SDK.

---

## 🛠️ Tech Stack & Setup

### Requirements
*   **Python**: 3.10+
*   **SDK**: Qiskit 2.x (v2.3+)
*   **Tools**: PennyLane (QML), Qiskit Aer (Simulation), Qiskit Runtime (Cloud).

### Quick Setup

#### 🪟 Windows (PowerShell)
```powershell
# Create environment
python -m venv quantum_env
.\quantum_env\Scripts\activate

# Install dependencies
pip install qiskit qiskit-aer qiskit-ibm-runtime pennylane matplotlib
```

#### 🐧 Linux / WSL2 (Bash)
```bash
# Create environment
python3 -m venv quantum_env
source quantum_env/bin/activate

# Install dependencies
pip install qiskit qiskit-aer qiskit-ibm-runtime pennylane matplotlib
```

---

## 🏆 Certification Goals

### 🎯 Primary: IBM C1000-179
The main objective is 100% coverage of the IBM Certified Developer exam:
*   **Circuit Operations (47%)**
*   **Visualization (19%)**
*   **Primitives (15%)**
*   **Quantum Information (10%)**
*   **OpenQASM & Tooling (9%)**

### 🌟 The "Plus" (Complementary Badges)
*   **AWS Braket**: For cloud-native infrastructure mastery.
*   **MIT xPRO**: For executive strategy and theoretical depth.
*   **PennyLane (Xanadu)**: For advanced Quantum Machine Learning.

## 🧪 Quality Assurance & Developer Tooling
To maintain high standards for quantum code, this project enforces strict formatting, linting, and test coverage.

*   **Linting & Style:** Configured via `flake8` (see [.flake8](.flake8)) and `black` for PEP 8 compliance.
*   **Code Cleanup:** Automatic unused import removal via `autoflake`.
*   **Testing Suite:** Built using `pytest` with coverage tracking.
*   **Developer Guide:** See [CHEATSHEET.md](CHEATSHEET.md) for activation and command references.

### Quick Commands
*   **Run tests:** `pytest --cov=src`
*   **Format code:** `black .`
*   **Lint check:** `flake8`
*   **Clean imports:** `autoflake --in-place --remove-all-unused-imports --recursive src tests scripts`

---

## 📂 Project Structure
*   `src/`: Quantum code implementations (.py).
*   `tests/`: Unit test suite for verification.
*   `scripts/`: Demonstration and execution scripts.
*   `docs/`: Resource portal, roadmap details, and technical reference.
*   `.github/`: Community templates (Issue/PR forms) and standards.
*   `outputs/`: Circuits, diagrams, and simulation results.
*   **Configuration Files:**
    *   [.flake8](.flake8): Style rules and execution settings.
    *   [.env.example](.env.example): Secrets and API key templates.


---

*Built for the **Quantum Utility** era. Focused on code that runs on real hardware.*
