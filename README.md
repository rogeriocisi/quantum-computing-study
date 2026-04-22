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
*Optimized for 6-10 hours/week. A comprehensive journey from zero to hardware-ready mastery.*

### Phase 1: Foundations & Qubits (Month 1)
*   **Topics**: Linear Algebra, Dirac Notation, Bloch Sphere, Single & Multi-qubit Gates.
*   **Goal**: Transition from classical logic to quantum state representation.

### Phase 2: Quantum Logic & Algorithms I (Months 2-3)
*   **Topics**: Oracles, Phase Kickback, Deutsch-Jozsa, Bernstein-Vazirani, Simon's Algorithm.
*   **Focus**: Mastery of interference-based speedups.

### Phase 3: Advanced Algorithms II (Months 4-5)
*   **Topics**: Grover's Search, Quantum Fourier Transform (QFT), Phase Estimation (QPE), Shor's Algorithm.
*   **Goal**: Understanding the mathematical core of quantum complexity.

### Phase 4: NISQ Applications & QML (Months 6-7)
*   **Topics**: Variational Algorithms (VQE, QAOA), Quantum Kernels, Neural Networks (PennyLane).
*   **Focus**: Solving optimization and chemistry problems on near-term hardware.

### Phase 5: Hardware Control & Error Mitigation (Months 8-9)
*   **Topics**: Transpilation, Noise Models, Error Mitigation (ZNE, M3), Open Pulse.
*   **Goal**: Learning to run production-grade code on noisy systems.

### Phase 6: Specialization & Advanced Topics (Month 10)
*   **Topics**: Quantum Error Correction (QEC) basics, Surface Codes, or Quantum Communication protocols.
*   **Goal**: Expanding knowledge into the frontiers of Fault-Tolerant systems.

### Phase 7: IBM Certification Mastery (Month 11)
*   **Objective**: **IBM C1000-179 Exam Prep**.
*   **Practice**: Full-length mock exams and deep dive into Qiskit Primitives (v2).

### Phase 8: Industrial Capstone & Portfolio (Month 12)
*   **Final Project**: A hybrid quantum-classical application (e.g., Portfolio Optimization or Molecular Simulation) with a full CI/CD pipeline.

---

## 🛠️ Tech Stack & Setup

### Requirements
*   **Python**: 3.10+
*   **SDK**: Qiskit v2.x
*   **Tools**: PennyLane (QML), Qiskit Aer (Simulation), Qiskit Runtime (Cloud).

### Quick Setup
```powershell
# Create environment
python -m venv quantum_env
.\quantum_env\Scripts\activate

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
