# Specification: Phase 4 — NISQ Utilities & Mitigation 🛠️

- **Module**: `src/utils/`
- **Phase**: 4
- **Status**: Implemented (Retroactive Spec)

## 1. Overview
Tools for managing noise and error mitigation in Noisy Intermediate-Scale Quantum (NISQ) devices.

## 2. Technical Requirements

### 2.1 Zero Noise Extrapolation (ZNE)
- **Requirement**: Implement a skeleton for ZNE error mitigation.
- **Methodology**:
    1.  Execute circuit at different noise scale factors.
    2.  Collect expectation values.
    3.  Extrapolate to the zero-noise limit (theoretical).
- **Scale Factors**: Support configurable scaling (e.g., 1.0, 1.5, 2.0).

## 3. Success Criteria
- [x] ZNE interface supports variable noise scaling factors.
- [x] Test circuits (Bell state) are provided for verification.
- [x] Structure allows future integration with Mitiq or similar libraries.
