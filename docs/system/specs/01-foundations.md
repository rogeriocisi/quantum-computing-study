# SPEC-01: Foundations & Qubits 🧪

## 1. Overview
The goal of this phase is to implement and visualize the most fundamental quantum states and protocols to build "Quantum Intuition". This includes entanglement, teleportation, and superdense coding.

## 2. Technical Requirements

### 2.1 Bell State Preparation
- **Requirement**: Create a function that generates the four Bell States.
- **Circuit**: 2 Qubits, 2 Classical Bits.
- **Verification**: Counts should show expected correlations (e.g., 50/50 for |00> and |11> in Phi+).

### 2.2 Quantum Teleportation
- **Requirement**: Implement the teleportation protocol to transmit a qubit state from Alice to Bob.
- **Verification**: Measure Bob's qubit and confirm it matches Alice's original state.
- **Primitives**: Use `SamplerV2` for result extraction.

### 2.3 Superdense Coding
- **Requirement**: Send 2 classical bits using 1 qubit and pre-shared entanglement.
- **Verification**: Confirm that Bob retrieves the exact 2-bit message sent by Alice.

### 2.4 Visualization Standards
- Every circuit must be exportable as a PNG using `qc.draw(output='mpl')`.
- Bloch sphere visualizations for single-qubit states.

## 3. Implementation Strategy
- **Module**: `src/algorithms/quantum_teleportation.py`, `src/algorithms/superdense_coding.py`
- **Execution**: All simulations MUST use `SamplerV2` primitives for count retrieval.

## 4. Success Criteria
- [x] Bell State implementation.
- [x] Quantum Teleportation implementation.
- [x] Superdense Coding implementation.
- [x] All simulations run on `AerSimulator`.
- [x] 100% test coverage in `tests/`.
