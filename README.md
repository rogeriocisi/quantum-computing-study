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

## 📅 High-Intensity Roadmap (12 Months)
*Optimized for developers with a strong mathematical background.*

### Phase 1: Fast Foundations (Month 1)
*   **Topics**: Linear Algebra, Dirac Notation (|ψ⟩, ⟨ψ|), Unitary Matrices, Bloch Sphere.
*   **Goal**: Master the mathematical representation of qubits and single/multi-qubit gates.

### Phase 2: Quantum Logic & Algorithms (Months 2-3)
*   **Topics**: Deutsch-Jozsa, Phase Kickback, Bernstein-Vazirani, Simon's Algorithm.
*   **Advanced**: Grover's Search (Amplitude Amplification) and QFT (Quantum Fourier Transform).

### Phase 3: NISQ Era & Variational Algorithms (Months 4-5)
*   **Topics**: VQE (Variational Quantum Eigensolver), QAOA (Optimization).
*   **Focus**: Quantum Machine Learning (QML) using PennyLane and Qiskit.

### Phase 4: Hardware Control & Error Mitigation (Months 6-8)
*   **Topics**: Noise Models, ZNE (Zero-Noise Extrapolation), M3 Mitigation.
*   **Specialization**: Open Pulse and low-level hardware control.

### Phase 5: DevOps, Research & Certification (Months 9-12)
*   **Portfolio**: Quantum Serverless Pipelines, Dockerized Hybrid Workflows.
*   **Certification**: **IBM C1000-179 Exam Prep**.
*   **Mastery**: Quantum Error Correction (QEC) and final Capstone Project.

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
