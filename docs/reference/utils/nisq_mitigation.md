# NISQ Error Mitigation (ZNE)

## Overview
Current quantum hardware is noisy and lacks error correction. **Error Mitigation** techniques aim to reduce the impact of noise on the final result without requiring full fault tolerance.

This module focuses on **Zero Noise Extrapolation (ZNE)**, a method where the noise of a circuit is artificially increased to extrapolate back to the "zero noise" limit.

---

## Technical Details

### Zero Noise Extrapolation (ZNE)
1.  **Noise Scaling**: The circuit is executed multiple times with increasing noise levels. This is typically achieved via **Gate Folding** (replacing a gate $G$ with $G G^\dagger G$).
2.  **Data Collection**: Expectation values are recorded for each noise scale factor.
3.  **Extrapolation**: A curve (linear, polynomial, or exponential) is fitted to the results to estimate the value at $scale = 0$.

---

## API Reference

The module `src.utils.nisq_mitigation` provides tools for experiment preparation.

### `apply_zne(circuit: QuantumCircuit, scale_factors: Tuple[float, ...]) -> Dict`
Prepares a series of experiments for ZNE.
- **Parameters**:
  - `circuit`: The baseline `QuantumCircuit` to be mitigated.
  - `scale_factors`: A tuple of factors (e.g., 1.0, 1.5, 2.0) defining how much to scale the noise.
- **Returns**: A dictionary mapping each scale factor to its results.

### `build_test_circuit() -> QuantumCircuit`
A helper function that returns a simple Bell-state circuit used for testing the mitigation logic.

---

## Usage Example
```python
from src.utils.nisq_mitigation import build_test_circuit, apply_zne

# 1. Create a circuit
qc = build_test_circuit()

# 2. Prepare ZNE experiments
results = apply_zne(qc, scale_factors=(1.0, 2.0, 3.0))

for scale, data in results.items():
    print(f"Scale {scale}: {data}")
```

## Implementation Details
- **Module**: [`src/utils/nisq_mitigation.py`](../../../src/utils/nisq_mitigation.py)
- **Test Suite**: [`tests/test_nisq_mitigation.py`](../../../tests/test_nisq_mitigation.py)
