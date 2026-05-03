# Superdense Coding

## Overview
Superdense Coding is a quantum communication protocol that allows a sender (Alice) to send two classical bits of information to a receiver (Bob) by transmitting only a **single qubit**. This protocol demonstrates the power of pre-shared **quantum entanglement** as a resource.

For the protocol to work, Alice and Bob must initially share an entangled pair of qubits (a Bell pair).

---

## Technical Circuit Logic
The protocol involves 2 qubits and the following stages:

1.  **Entanglement Sharing**: Alice and Bob share a Bell pair $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$. Alice holds qubit $q_0$ and Bob holds qubit $q_1$.
2.  **Alice's Encoding**: Alice wants to send a 2-bit message $m_1 m_0$. She applies local gates to her qubit $q_0$:
    - To send `00`: Apply $I$ (do nothing).
    - To send `01`: Apply $Z$ gate.
    - To send `10`: Apply $X$ gate.
    - To send `11`: Apply $X$ and $Z$ gates.
3.  **Transmission**: Alice sends her qubit $q_0$ to Bob.
4.  **Bob's Decoding**: Bob now has both qubits. He performs a Bell basis measurement by reversing the entanglement steps:
    - Apply CNOT($q_0, q_1$).
    - Apply $H(q_0)$.
    - Measure both qubits. The result $q_1 q_0$ corresponds exactly to the 2-bit message Alice intended to send.

---

## API Reference

The module `src.algorithms.superdense_coding` provides functions to demonstrate the protocol.

### `create_superdense_circuit(message: str) -> QuantumCircuit`
Constructs a 2-qubit circuit that encodes a 2-bit classical message into a shared Bell pair.
- **Args**: `message` (str) - One of `'00'`, `'01'`, `'10'`, or `'11'`.
- **Returns**: A `qiskit.QuantumCircuit` implementing the encoding and decoding.

### `run_simulation(qc: QuantumCircuit, message: str) -> Dict[str, int]`
Simulates the circuit locally and generates visual outputs.
- **Side Effects**:
    - Saves the circuit diagram to `outputs/superdense_circuit_<message>.png`.
    - Saves the result histogram to `outputs/superdense_histogram_<message>.png`.
- **Returns**: A dictionary of measurement counts.

---

## Usage Example
```python
from src.algorithms.superdense_coding import create_superdense_circuit, run_simulation

# Send the message '10'
msg = '10'
qc = create_superdense_circuit(msg)

# Run and visualize
counts = run_simulation(qc, msg)

print(f"Original Message: {msg}")
print(f"Decoded Message: {counts}")
# Expected output: {'10': 1024}
```

## Implementation Details
- **Module**: [`src/algorithms/superdense_coding.py`](../../../src/algorithms/superdense_coding.py)
