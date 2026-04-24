# Bell State Generation (Entanglement)

## Overview
A Bell state is a specific type of quantum state representing the simplest form of **quantum entanglement** between two qubits. The state implemented here is the $|\Phi^+\rangle$ state:

$$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

When measured, both qubits will yield the same result (either both 0 or both 1) with 50% probability each, demonstrating a perfect correlation that cannot be explained by classical physics.

---

## Technical Circuit Logic
The Bell state is generated using two fundamental quantum gates:

1.  **Hadamard Gate (H)**: Applied to the first qubit to create a uniform superposition:
    $$|00\rangle \xrightarrow{H_0} \frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes |0\rangle = \frac{|00\rangle + |10\rangle}{\sqrt{2}}$$

2.  **CNOT Gate (CX)**: Applied with the first qubit as control and the second as target. This "links" the states:
    $$\frac{|00\rangle + |10\rangle}{\sqrt{2}} \xrightarrow{CX_{0,1}} \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

---

## API Reference

The module `src.algorithms.bell_state` provides functions to create and simulate the entanglement.

### `create_bell_state() -> QuantumCircuit`
Constructs a 2-qubit circuit that generates the $|\Phi^+\rangle$ state.
- **Returns**: A `qiskit.QuantumCircuit` with 2 qubits and 2 classical bits, including measurement operations.

### `run_simulation(qc: QuantumCircuit) -> Dict[str, int]`
Simulates the circuit locally and generates visual outputs.
- **Side Effects**:
    - Saves the circuit diagram to `outputs/bell_circuit.png`.
    - Saves the result histogram to `outputs/bell_histogram.png`.
- **Returns**: A dictionary of measurement counts (expected to contain only `'00'` and `'11'`).

---

## Usage Example
```python
from src.algorithms.bell_state import create_bell_state, run_simulation

# Create the entangled circuit
qc = create_bell_state()

# Run and visualize
counts = run_simulation(qc)

print(f"Entanglement Results: {counts}")
# Expected output: {'00': ~512, '11': ~512}
```

## Implementation Details
- **Module**: [`src/algorithms/bell_state.py`](../../../src/algorithms/bell_state.py)
- **Test Suite**: [`tests/test_bell_state.py`](../../../tests/test_bell_state.py)
