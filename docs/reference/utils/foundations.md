# Quantum Foundations & Primitives

## Overview
This module contains fundamental quantum operations and state preparations that serve as building blocks for more complex algorithms. The primary focus is on **Quantum Entanglement** and standard state preparations.

### Bell States
A Bell state is a specific type of quantum state representing the simplest form of **quantum entanglement** between two qubits. The state implemented here is the $|\Phi^+\rangle$ state:

$$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

---

## Technical Logic

### Entanglement Generation
The Bell state is generated using two fundamental quantum gates:

1.  **Hadamard Gate (H)**: Creates a uniform superposition.
2.  **CNOT Gate (CX)**: Entangles the qubits.

---

## API Reference

The module `src.utils.foundations` provides functions to create, apply, and simulate fundamental states.

### `apply_bell_pair(qc: QuantumCircuit, a: int, b: int) -> None`
Applies the $|\Phi^+\rangle$ entanglement logic to two existing qubits in a circuit.
- **Parameters**:
    - `qc`: The target `QuantumCircuit`.
    - `a`: Index of the control qubit.
    - `b`: Index of the target qubit.

### `create_bell_state() -> QuantumCircuit`
Constructs a standalone 2-qubit circuit that generates the $|\Phi^+\rangle$ state.
- **Returns**: A `qiskit.QuantumCircuit` with 2 qubits and 2 classical bits.

### `run_simulation(qc: QuantumCircuit) -> Dict[str, int]`
Simulates a circuit locally and generates visual outputs.
- **Returns**: A dictionary of measurement counts.

---

## Usage Example

```python
from qiskit import QuantumCircuit
from src.utils.foundations import apply_bell_pair

# Use as a primitive in a larger circuit
qc = QuantumCircuit(3)
apply_bell_pair(qc, 1, 2)
print(qc)
```

## Implementation Details
- **Module**: [`src/utils/foundations.py`](../../../src/utils/foundations.py)
- **Test Suite**: [`tests/test_foundations.py`](../../../tests/test_foundations.py) (TBD)
