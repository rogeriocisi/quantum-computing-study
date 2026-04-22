# Quantum Computing Study: Roadmap & Resource Portal 🌌

This repository contains a comprehensive **12-month study roadmap** and practical implementations for transitioning from classical software engineering to **Quantum Computing Developer**, specifically targeting the **IBM Certified Associate Developer - Quantum Computation using Qiskit v2.X**.

---

## 🚀 The Mission
To transform software engineers and scientists into quantum-ready developers by mastering **Linear Algebra**, **Quantum Algorithms**, and **Hardware-Conscious Development** using the latest **Qiskit v2.x** framework.

---

## 📚 Academic Resource Portal
A curated selection of the best educational materials in the field, categorized by difficulty and focus.

### 📖 Essential Books
*   **The Best Starting Point**: *Introduction to Classical and Quantum Computing* by Thomas G. Wong.
*   **The Official Guide**: *Learn Quantum Computing using Qiskit* by IBM Qiskit Community.
*   **The "Bible" of the Field**: *Quantum Computation and Quantum Information* ("Mike & Ike") by Nielsen & Chuang.
*   **The Essential Bridge**: *Quantum Computing: A Gentle Introduction* by Rieffel & Polak (Focus on Linear Algebra).
*   **Applied Mastery**: *Quantum Computing: An Applied Approach* by Jack Hidary (Qiskit + Cirq).

### 🎓 Top-Tier Courses
*   **IBM Quantum Learning**: Official interactive path for Qiskit v2 certification.
*   **MIT 8.370x**: Quantum Information Science by Peter Shor & Isaac Chuang.
*   **QuTech Academy (TU Delft)**: Advanced modules on Quantum Internet and Hardware.

### ▶️ Video Playlists
*   **Michael Nielsen**: "Quantum Computing for the Determined" (Short, rigorous conceptual videos).
*   **John Watrous (IBM)**: "Understanding Quantum Information" (Advanced university-level course).
*   **Abraham Asfaw (IBM)**: "Coding with Qiskit" (Practical Python implementation).

### 📄 Key Research Papers (ArXiv)
*   **Preskill (arXiv:1801.00862)**: Quantum Computing in the NISQ Era and Beyond.
*   **QML Survey (arXiv:2310.10315)**: A Survey on Quantum Machine Learning.
*   **NISQ Tutorial (arXiv:2310.12571)**: Quantum Computing through the Lens of Control.

---

## 📅 Realistic Part-Time Roadmap (12 Months)
*Optimized for 6-10 hours/week. Developer-centric approach with a focus on QML and software patterns.*

### Phase 1: Foundations & Qubits (Month 1)
*   **Topics**: Linear Algebra, Dirac Notation, Bloch Sphere, Single & Multi-qubit Gates.
*   **Goal**: Transition from classical logic to quantum state representation.

### Phase 2: Algorithms I & Logic Gates (Months 2-3)
*   **Topics**: Oracles, Phase Kickback, Deutsch-Jozsa, Bernstein-Vazirani, Simon's Algorithm.
*   **Focus**: Mastering the core logic that powers quantum speedups.

### Phase 3: Intro to QML with PennyLane (Month 4)
*   **Topics**: Variational Quantum Circuits (VQC) as "Quantum Neural Networks", PennyLane setup.
*   **Focus**: Early introduction to the "learnable" part of quantum computing for developers.

### Phase 4: Advanced Algorithms II (Months 5-6)
*   **Topics**: Grover's Search, Quantum Fourier Transform (QFT), Phase Estimation (QPE), Shor's Algorithm.
*   **Goal**: Understanding the mathematical foundations of the most famous algorithms.

### Phase 5: Applied QML & Optimization (Months 7-8)
*   **Topics**: QAOA for optimization, VQE for simple molecular simulation, Hybrid workflows.
*   **Focus**: Practical use of **PennyLane** and Qiskit for real-world problem solving.

### Phase 6: The NISQ Era & Noise Reality (Month 9)
*   **Topics**: Conceptual Noise, Decoherence, Fidelity, high-level Error Mitigation (ZNE/M3).
*   **Focus**: Understanding the limitations of current hardware without diving too deep into transpilation physics.

### Phase 7: IBM Certification Mastery (Months 10-11)
*   **Objective**: **IBM C1000-179 Exam Prep**.
*   **Practice**: Intensive focus on the official curriculum, mock exams, and Qiskit SDK v2 best practices.

### Phase 8: Industrial Capstone & Portfolio (Month 12)
*   **Final Project**: A hybrid quantum-classical application (e.g., Portfolio Optimization or QML Signal Processing) with a full CI/CD pipeline.

---

## 💻 Hardware Requirements

To bridge the gap between classical simulation and real-world execution, the following hardware setup is recommended:

### 🖥️ Local Simulation (High-Performance Workstation)
*Optimized for both Quantum Simulation (Qiskit Aer GPU) and high-end gaming (because you deserve some 4K FPS after solving Dirac equations) 🎮.*

*   **CPU**: AMD Ryzen 7 7700X or Intel Core i7-13700K — High clock speeds are essential for the classical optimization loops in QAOA/VQE.
*   **RAM**: 32 GB DDR5 — The most critical component; quantum state-vector simulations are memory-intensive.
*   **GPU**: NVIDIA RTX 4070 12 GB — Supports `qiskit-aer-gpu` and `PennyLane Lightning-GPU` for massive simulation speedups.
*   **Storage**: 1 TB NVMe SSD (System & Dev Environments) + 1 TB HDD (Large datasets).
*   **Motherboard**: AMD B650 or Intel B760 — Reliable and cost-effective chipsets.
*   **PSU**: 650W 80+ Gold — Efficient power delivery for stable performance.
*   **Cooling**: High-performance Tower Air Cooler (e.g., DeepCool AK620) for silent and stable operation.

### ☁️ Remote Quantum Access (Real Hardware)
*   **IBM Quantum Platform**: Access to utility-scale processors (127-qubit Eagle/Heron) via **IBM Quantum Runtime API**.
*   **AWS Braket**: Access to diverse architectures (IonQ, Rigetti, QuEra) using the Braket SDK.

---

## 🛠️ Tech Stack & Setup

### Requirements
*   **Python**: 3.10+
*   **SDK**: Qiskit v2.x
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

---

## 📂 Project Structure
*   `src/`: Quantum code implementations (.py).
*   `docs/`: Resource portal, roadmap details, and theoretical material.
*   `landing/`: Web visualization of the study progress.
*   `outputs/`: Circuits, diagrams, and simulation results.

---

*Built for the **Quantum Utility** era. Focused on code that runs on real hardware.*
