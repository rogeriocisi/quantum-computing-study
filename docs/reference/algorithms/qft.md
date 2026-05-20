# Quantum Fourier Transform (QFT)

## Overview
The **Quantum Fourier Transform (QFT)** is the quantum analog of the classical Discrete Fourier Transform (DFT). It is a linear transformation on qubits that maps a quantum state $|x\rangle$ in the computational basis to a superposition state $|\tilde{x}\rangle$ in the Fourier basis. 

The QFT is not used directly for speedups on classical data processing (since measuring the output collapses the state, and reading all amplitudes would take exponential time). Instead, it serves as a crucial building block in many advanced quantum algorithms:
*   **Shor's Algorithm** (for integer factorization)
*   **Quantum Phase Estimation (QPE)** (for finding eigenvalues of unitaries)
*   **Quantum Simulation** and solving systems of linear equations (HHL)

- **Classical DFT Complexity**: $O(N \log N)$ using Fast Fourier Transform (FFT) where $N = 2^n$.
- **Quantum QFT Complexity**: $O(n^2)$ gate operations, providing an exponential speedup in circuit complexity.

---

## Mathematical Formulation
For an $n$-qubit state, the QFT maps the basis state $|x\rangle$ (where $x \in \{0, 1, \dots, 2^n-1\}$) to the state:

$$\text{QFT}|x\rangle = \frac{1}{\sqrt{2^n}} \sum_{y=0}^{2^n-1} e^{2\pi i x y / 2^n} |y\rangle$$

Applying a product representation, this can be written as:

$$\text{QFT}|x_1 x_2 \dots x_n\rangle = \frac{1}{\sqrt{2^n}} \left(|0\rangle + e^{2\pi i 0.x_n}|1\rangle\right) \otimes \left(|0\rangle + e^{2\pi i 0.x_{n-1}x_n}|1\rangle\right) \otimes \dots \otimes \left(|0\rangle + e^{2\pi i 0.x_1 x_2 \dots x_n}|1\rangle\right)$$

where $0.x_1 x_2 \dots x_k = \sum_{j=1}^k x_j 2^{-j}$ represents binary fraction notation.

---

## Circuit Construction
The QFT circuit is constructed using two types of gates:
1.  **Hadamard Gates ($H$)**: Creates equal superposition and introduces basic phase terms.
2.  **Controlled-Phase Rotations ($R_k$)**: Introduces the precise phase shifts, where:
    $$R_k = \begin{pmatrix} 1 & 0 \\ 0 & e^{2\pi i / 2^k} \end{pmatrix}$$

### Step-by-Step Execution (Pedagogical)
For each qubit $i$ from $1$ to $n$:
1.  Apply $H$ to qubit $i$.
2.  For each subsequent qubit $j > i$, apply a controlled-$R_{j-i+1}$ gate with qubit $j$ as control and qubit $i$ as target.
3.  After processing all qubits, apply a series of SWAP gates to reverse the order of the qubits (since the product representation naturally outputs the binary fractions in reverse order).

---

## Qiskit v2.x & 3.0 Modern Implementation

In modern Qiskit (2.x / 3.0), the Quantum Fourier Transform is constructed using the `QFTGate` class inside the `qiskit.circuit.library` module.

### Construction Example
```python
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate

n_qubits = 4

# Create a circuit and append the standard QFT gate
qc = QuantumCircuit(n_qubits)
qft_gate = QFTGate(num_qubits=n_qubits)
qc.append(qft_gate, range(n_qubits))

print(qc.draw())
```

### Inverse QFT (IQFT)
To reverse the QFT (which is necessary in Shor's algorithm and QPE to map phase values back to the computational basis), call the `.inverse()` method of the `QFTGate` instance:
```python
from qiskit.circuit.library import QFTGate

iqft_gate = QFTGate(num_qubits=n_qubits).inverse()
```

---

## Implementation & Usage in this Project
*   **Integrated Usage**: The Inverse QFT is a core building block inside our Shor's Algorithm implementation to retrieve the period $r$, and in QPE to decode the phase $\phi$.
    *   **Shor Module**: [`src/algorithms/shor.py`](../../../src/algorithms/shor.py)
    *   **QPE Module**: [`src/algorithms/qpe.py`](../../../src/algorithms/qpe.py)
    *   **Specification**: [`docs/system/specs/08-shor_algorithm.md`](../../system/specs/08-shor_algorithm.md)

