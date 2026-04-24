# Vedral, Barenco and Ekert (VBE) Quantum Adder

## Academic Reference
V. Vedral, A. Barenco, A. Ekert, "Quantum Networks for Elementary Arithmetic Operations", *Phys. Rev. A* 54, 147 (1996).  
[arXiv:quant-ph/9511018](https://arxiv.org/abs/quant-ph/9511018)

---

## Overview
The VBE adder is one of the classic implementations of quantum arithmetic. It uses a **ripple-carry** design to perform the addition of two $n$-bit integers reversibly.

### Key Features:
- **In-place**: The result of the sum $A + B$ is stored in register $B$ itself.
- **Reversible**: Register $A$ is preserved and all ancillas (auxiliary qubits) are cleaned (restored to $|0\rangle$) at the end.
- **Qubit Efficiency**: Uses $3n + 1$ qubits to add two $n$-bit numbers (including the carry-out bit).

---

## Technical Circuit Structure
The implementation strictly follows the original design, validated against visualizations in the [Quirk](https://algassert.com/quirk) simulator.

### Execution Flow:
1.  **Forward CARRY Pass (Propagation)**:
    Applies $n$ `CARRY` gates sequentially from position $0$ to $n-1$.
    - Qubits: `(c[i], a[i], b[i], c[i+1])`.
    - Result: Qubit `c[n]` stores the final carry-out.

2.  **MSB (Most Significant Bit) Sum Step**:
    - `CX(a[n-1], b[n-1])`: Prepares the most significant sum bit.
    - `SUM(c[n-1], a[n-1], b[n-1])`: Finalizes the sum for bit $n-1$.
    *Note: The CARRY(n-1) gate is NOT inverted to preserve the carry-out in c[n].*

3.  **Backward CARRY† + SUM Pass (Uncompute & Finalization)**:
    For each position $i$ from $n-2$ down to $0$:
    - `CARRY†(c[i], a[i], b[i], c[i+1])`: Reverses carry propagation to clear the $c[i+1]$ ancilla.
    - `SUM(c[i], a[i], b[i])`: Calculates the final sum bit for position $i$.

### Final State:
- `b[0..n-1]`: Contains the lower $n$ bits of the sum.
- `c[n]`: Contains the carry-out bit (MSB of the sum).
- `a[0..n-1]`: Keeps the original value (read-only).
- `c[0..n-1]`: Restored to $|0\rangle$.

---

## Repository Implementation
- **Main Module**: [`src/algorithms/vbe_adder.py`](../../../src/algorithms/vbe_adder.py)
- **Test Suite**: [`tests/test_vbe_adder.py`](../../../tests/test_vbe_adder.py)
  - Validates 55 test cases, including overflow sums, zero, and the original example from the paper.

## API Reference

The module `src.algorithms.vbe_adder` provides both high-level convenience functions and low-level circuit builders.

### `add(a: int, b: int, n: int = None) -> int`
The easiest way to use the adder. It handles bit encoding, circuit building, simulation, and decoding.
- **Parameters**:
  - `a`, `b`: Non-negative integers to add.
  - `n` (Optional): Bit-width of the registers. Defaults to the minimum required size.
- **Returns**: The integer result of $a + b$.

### `build_vbe_adder(n: int, a_bits: List[int] = None, b_bits: List[int] = None) -> QuantumCircuit`
Constructs the full VBE ripple-carry circuit.
- **Parameters**:
  - `n`: Number of bits for the input registers.
  - `a_bits`, `b_bits` (Optional): Lists of 0s and 1s to initialize the $A$ and $B$ registers.
- **Returns**: A `qiskit.QuantumCircuit` object containing the adder logic and measurements.

### `run_simulation(qc: QuantumCircuit, shots: int = 1024) -> Dict[str, int]`
Executes the circuit on the `AerSimulator`.
- **Returns**: A dictionary of measurement counts (e.g., `{'1111': 1024}`).

### `decode_result(counts: Dict[str, int], n: int) -> (int, Dict)`
Translates the raw bitstring counts from the simulator into a decimal integer.
- **Note**: It correctly interprets the Qiskit MSB-first bitstring convention for the $n+1$ result bits.

---

## Usage Example
```python
from src.algorithms.vbe_adder import add

# High-level API: Add 9 + 6
result = add(9, 6)
print(f"Result: {result}") # Output: 15

# Low-level API: Custom circuit building
from src.algorithms.vbe_adder import build_vbe_adder, run_simulation, decode_result
qc = build_vbe_adder(4, a_bits=[1,0,0,1], b_bits=[0,1,1,0])
counts = run_simulation(qc)
value, _ = decode_result(counts, 4)
print(f"Decoded: {value}")
```
