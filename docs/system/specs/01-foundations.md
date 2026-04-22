# Specification: Phase 1 — Foundations & Qubits 🧪

- **Module**: `src/algorithms/`
- **Phase**: 1
- **Status**: Draft

## 1. Overview
The goal of this phase is to implement and visualize the most fundamental quantum states and gates to build "Quantum Intuition".

## 2. Technical Requirements

### 2.1 Bell State Preparation
- **Requirement**: Create a function that generates the four Bell States.
- **Circuit**: 2 Qubits, 2 Classical Bits.
- **Verification**: Counts should show a 50/50 distribution between |00> and |11> (for the first Bell state).

### 2.2 Visualization Standards
- Every circuit created in this phase must be exportable as a PNG using `qc.draw(output='mpl')`.
- Bloch sphere visualizations must be generated for single-qubit gates (X, Y, Z, H).

## 3. Success Criteria
- [ ] Code follows PEP8 and contains docstrings.
- [ ] Simulation runs without errors on `AerSimulator`.
- [ ] Histograms are saved in the `outputs/` directory.

## 4. Dependencies
- `qiskit`
- `qiskit-aer`
- `matplotlib`
