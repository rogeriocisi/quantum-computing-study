# Quantum Teleportation

## Overview
Quantum Teleportation is a fundamental protocol in quantum computing and quantum communication. It allows for the transmission of unknown quantum states from one location (Alice) to another (Bob) without physically transmitting the qubit itself. This is achieved using **quantum entanglement** (a shared Bell state) and classical communication.

The protocol destroys the original state at the sender's location due to the no-cloning theorem, successfully "teleporting" it to the receiver.

---

## Technical Circuit Logic
The teleportation protocol operates using 3 qubits and involves the following steps:

1.  **State Preparation**: Alice possesses a qubit $q_0$ in an arbitrary state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ that she wishes to teleport to Bob.
2.  **Entanglement (Bell Pair)**: Alice and Bob share an entangled pair of qubits ($q_1$ and $q_2$) in the $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$ state. Alice holds $q_1$, and Bob holds $q_2$.
3.  **Alice's Operations**: Alice applies a CNOT gate with $q_0$ as the control and $q_1$ as the target, followed by a Hadamard gate on $q_0$. She then measures both of her qubits ($q_0 \to c_z, q_1 \to c_x$).
4.  **Bob's Conditional Operations**: Depending on the classical bits ($c_x, c_z$) Alice sends to Bob, he applies Pauli gates to his qubit $q_2$ to recover the original state:
    - If $c_x = 1$, Bob applies an **X gate** to $q_2$.
    - If $c_z = 1$, Bob applies a **Z gate** to $q_2$.
5.  **Verification**: After Bob's operations, his qubit $q_2$ is in the exact state $|\psi\rangle$ initially held by $q_0$.

---

## API Reference

The module `src.algorithms.quantum_teleportation` provides functions to create and simulate the teleportation protocol.

### `create_teleportation_circuit(theta: float = np.pi / 3) -> QuantumCircuit`
Constructs a 3-qubit circuit that prepares an initial state via an $R_x(\theta)$ rotation and teleports it.
- **Args**: `theta` (float) - The angle for the initial state preparation.
- **Returns**: A `qiskit.QuantumCircuit` implementing the protocol, including Bob's verification measurement.

### `run_simulation(qc: QuantumCircuit) -> Dict[str, int]`
Simulates the circuit locally using Qiskit Aer and generates visual outputs.
- **Side Effects**:
    - Saves the circuit diagram to `outputs/teleportation_circuit.png`.
    - Saves the result histogram to `outputs/teleportation_histogram.png`.
- **Returns**: A dictionary of measurement counts. The verification qubit should always yield `0`, confirming the state was accurately teleported and reversed.

---

## Usage Example
```python
import numpy as np
from src.algorithms.quantum_teleportation import create_teleportation_circuit, run_simulation

# Create the teleportation circuit with an initial state rotation of pi/3
qc = create_teleportation_circuit(theta=np.pi / 3)

# Run and visualize
counts = run_simulation(qc)

print(f"Teleportation Results: {counts}")
# Expected output: Verification measurement (leftmost bit) should always be '0'
# e.g., {'0 1 1': 255, '0 0 0': 255, '0 0 1': 255, '0 1 0': 255}
```

## Implementation Details
- **Module**: [`src/algorithms/quantum_teleportation.py`](../../../src/algorithms/quantum_teleportation.py)
