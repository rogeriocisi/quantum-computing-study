# Specification: Phase 2 — Quantum Arithmetic (VBE Adder) 🧮

- **Module**: `src/algorithms/vbe_adder.py`
- **Phase**: 2
- **Status**: Implemented (Retroactive Spec)

## 1. Overview
Implementation of a reversible ripple-carry adder based on the Vedral, Barenco, and Ekert (VBE) design. The primary goal is to perform in-place addition of two $n$-bit integers.

## 2. Technical Requirements

### 2.1 Circuit Topology
- **Input**: Two $n$-bit registers $A$ and $B$, and $n+1$ carry ancillae $C$.
- **In-place Addition**: The circuit must compute $B = A + B \pmod{2^{n+1}}$.
- **Reversibility**:
    - Register $A$ must be restored to its initial state.
    - Carry ancillae $c_0 \dots c_{n-1}$ must be restored to $|0\rangle$.
- **Bit Order**: Implementation must follow the LSB-first convention (Least Significant Bit at index 0).

### 2.2 Gate Requirements
- Use the standard VBE `CARRY` and `SUM` gates composed of Toffoli (CCX) and CNOT (CX) gates.
- Total qubit count: $3n + 1$.
- Total Toffoli count: $2n$.

## 3. Implementation Constraints
- **Validation**: The circuit must be validated against the seminal 1996 paper and modern simulators (Quirk).
- **MSB Handling**: The most significant bit of the sum must be correctly stored in the last carry qubit ($c_n$).

## 4. Success Criteria
- [x] Correctly adds numbers up to $2^n - 1$.
- [x] Handles carry-out (overflow) correctly.
- [x] Passes all 55 unit tests in `tests/test_vbe_adder.py`.
- [x] Documentation exists in `docs/code/algorithms/vbe_adder.md`.
