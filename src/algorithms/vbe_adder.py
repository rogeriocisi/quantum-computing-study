"""
Quantum Ripple-Carry Adder — Vedral, Barenco & Ekert (1996)
============================================================
Reference: V. Vedral, A. Barenco, A. Ekert, "Quantum Networks for
Elementary Arithmetic Operations", Phys. Rev. A 54, 147 (1996).
arXiv: quant-ph/9511018

Circuit topology (n-bit adder)
-------------------------------
For each bit position i in 0..n-1 the register layout is:

    c[i]  — carry ancilla (initialised to |0⟩)
    a[i]  — first addend  (input)
    b[i]  — second addend / sum output (input, modified in place)

Plus one extra carry-out qubit  c[n]  that holds the most-significant
bit of the result after addition.

Building blocks (following the Quirk visualisation)
----------------------------------------------------
CARRY  gate  (C)    : (c_i, a_i, b_i, c_{i+1}) → propagates carry forward
SUM    gate  (S)    : (c_i, a_i, b_i)           → computes partial sum in place
CARRY† gate  (Cdag) : inverse of CARRY — uncomputes carry ancillae in
                      the backward pass

Full circuit structure (for n bits) — verified against the Quirk URL
----------------------------------------------------------------------
  1. Forward CARRY pass  : CARRY(0), CARRY(1), … , CARRY(n-1)  [n gates]
     → c[n] now holds the carry-out of the full n-bit addition.
  2. MSB step            : CX(a[n-1], b[n-1])
                           SUM(c[n-1], a[n-1], b[n-1])
     → b[n-1] gets the MSB of the sum; c[n] is untouched.
  3. Backward pass       : for i = n-2 downto 0:
                               CARRY†(c[i], a[i], b[i], c[i+1])
                               SUM   (c[i], a[i], b[i])
     → c[1..n-1] are uncomputed (restored to |0⟩); b[0..n-2] get
       the remaining sum bits.

After the circuit completes:
  • b[0..n-1]  holds the full n-bit sum   (LSB in b[0])
  • c[n]       holds the carry-out bit    (1 iff a + b ≥ 2ⁿ)
  • a[0..n-1]  is unchanged               (reversible computation)
  • c[0..n-1]  are restored to |0⟩        (ancillae cleaned up)

Total gate count: n×CARRY + 1×CNOT + 1×SUM + (n-1)×(CARRY†+SUM)
                = 2n Toffoli + 1 CNOT + (n-1) CNOT  [expanded]

"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile

try:
    from qiskit_aer import AerSimulator

    _HAS_AER = True
except ImportError:
    _HAS_AER = False


# ---------------------------------------------------------------------------
# Core building-block sub-circuits
# ---------------------------------------------------------------------------


def _carry_gate() -> QuantumCircuit:
    """Build the 4-qubit CARRY sub-circuit (gate C in VBE §II).

    Qubit order: (c_in, a, b, c_out)

    Truth table effect (on carry propagation):
        c_out ^= majority(c_in, a, b)
        b     ^= a  ⊕  c_in  (intermediate – undone by SUM)

    Gate sequence:
        Toffoli(a, b, c_out)
        CNOT(a, b)
        Toffoli(c_in, b, c_out)

    Matches the sub-circuit labelled 'C' in the Quirk visualisation:
        col 1: CCX(q1=a_ctrl, q2=b_ctrl, q3=c_out_tgt)  [col: 1,•,•,X]
        col 2: CX(q1=a_ctrl, q2=b_tgt)                  [col: 1,•,X]
        col 3: CCX(q0=c_in, q2=b_ctrl, q3=c_out_tgt)    [col: •,1,•,X]
    """
    qc = QuantumCircuit(4, name="CARRY")
    c_in, a, b, c_out = 0, 1, 2, 3
    qc.ccx(a, b, c_out)  # Toffoli: if a AND b → flip c_out
    qc.cx(a, b)  # CNOT: b ^= a  (partial XOR for majority)
    qc.ccx(c_in, b, c_out)  # Toffoli: if c_in AND (a⊕b) → flip c_out
    return qc


def _carry_dag_gate() -> QuantumCircuit:
    """Build the 4-qubit CARRY† (inverse CARRY) sub-circuit (gate C† in VBE §II).

    This is the exact reverse of CARRY: it uncomputes the carry ancilla
    while leaving a unchanged and restoring b to its pre-CARRY value.

    Gate sequence (reversed from CARRY):
        Toffoli(c_in, b, c_out)
        CNOT(a, b)
        Toffoli(a, b, c_out)

    Matches the sub-circuit labelled 'Cdag' in the Quirk visualisation:
        col 1: CCX(q0=c_in, q2=b_ctrl, q3=c_out_tgt)   [col: •,1,•,X]
        col 2: CX(q1=a_ctrl, q2=b_tgt)                  [col: 1,•,X]
        col 3: CCX(q1=a_ctrl, q2=b_ctrl, q3=c_out_tgt)  [col: 1,•,•,X]
    """
    qc = QuantumCircuit(4, name="CARRY†")
    c_in, a, b, c_out = 0, 1, 2, 3
    qc.ccx(c_in, b, c_out)  # reverse of last Toffoli in CARRY
    qc.cx(a, b)  # reverse of CNOT (self-inverse)
    qc.ccx(a, b, c_out)  # reverse of first Toffoli in CARRY
    return qc


def _sum_gate() -> QuantumCircuit:
    """Build the 3-qubit SUM sub-circuit (gate S in VBE §II).

    Qubit order: (c_in, a, b)

    Effect: b ^= c_in ⊕ a   →  b holds the partial sum bit

    Gate sequence:
        CNOT(a, b)
        CNOT(c_in, b)

    Matches the sub-circuit labelled 'S' in the Quirk visualisation:
        col 1: CX(q1=a_ctrl, q2=b_tgt)   [col: 1,•,X]
        col 2: CX(q0=c_in, q2=b_tgt)     [col: •,1,X]
    """
    qc = QuantumCircuit(3, name="SUM")
    c_in, a, b = 0, 1, 2
    qc.cx(a, b)  # b ^= a
    qc.cx(c_in, b)  # b ^= c_in  →  b = a ⊕ c_in ⊕ b_original
    return qc


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_vbe_adder(
    n: int,
    a_bits: Optional[List[int]] = None,
    b_bits: Optional[List[int]] = None,
) -> QuantumCircuit:
    """Construct the n-bit VBE ripple-carry quantum adder circuit.

    The circuit computes  b = a + b  (mod 2ⁿ⁺¹) in-place, leaving *a*
    unchanged and storing the full (n+1)-bit result across b[0..n-1]
    (LSB to MSB) and the carry-out qubit c[n].

    Register layout (3n + 1 qubits total)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    For each bit position i ∈ [0, n):
        c[i]  — carry ancilla qubit, always initialised to |0⟩
        a[i]  — i-th bit of operand A  (input, read-only after circuit)
        b[i]  — i-th bit of operand B  (input/output: holds sum after run)
    Extra:
        c[n]  — carry-out (most-significant bit of the sum)

    Classical register: n+1 bits for the result (b[0..n-1] + c[n]).

    Parameters
    ----------
    n:
        Number of bits in each operand.
    a_bits:
        Optional list of n integer values (0 or 1) encoding operand A.
        If provided, X gates are applied to initialise the a register.
    b_bits:
        Optional list of n integer values (0 or 1) encoding operand B.
        If provided, X gates are applied to initialise the b register.

    Returns
    -------
    QuantumCircuit
        The full VBE adder circuit with measurements on the result bits.

    Example
    -------
    >>> qc = build_vbe_adder(4, a_bits=[1,0,0,1], b_bits=[0,1,1,0])
    # Computes 9 + 6 = 15  (0b1111)

    Raises
    ------
    ValueError
        If a_bits or b_bits are provided but have the wrong length, or
        contain values other than 0/1.
    """
    if a_bits is not None:
        if len(a_bits) != n:
            raise ValueError(f"a_bits must have length n={n}, got {len(a_bits)}")
        if any(b not in (0, 1) for b in a_bits):
            raise ValueError("a_bits must contain only 0 or 1 values")
    if b_bits is not None:
        if len(b_bits) != n:
            raise ValueError(f"b_bits must have length n={n}, got {len(b_bits)}")
        if any(b not in (0, 1) for b in b_bits):
            raise ValueError("b_bits must contain only 0 or 1 values")

    # ------------------------------------------------------------------
    # Allocate registers
    # ------------------------------------------------------------------
    # c: carry ancillae c[0..n]  (n+1 qubits, all start in |0⟩)
    c = QuantumRegister(n + 1, name="c")
    # a: first addend a[0..n-1]
    a = QuantumRegister(n, name="a")
    # b: second addend / result b[0..n-1]
    b = QuantumRegister(n, name="b")
    # classical result: n+1 bits  (b[0..n-1] + c[n] as MSB)
    result = ClassicalRegister(n + 1, name="result")

    qc = QuantumCircuit(c, a, b, result, name=f"VBE_adder_{n}bit")

    # ------------------------------------------------------------------
    # Optional state initialisation
    # ------------------------------------------------------------------
    if a_bits is not None:
        for i, bit in enumerate(a_bits):
            if bit:
                qc.x(a[i])
    if b_bits is not None:
        for i, bit in enumerate(b_bits):
            if bit:
                qc.x(b[i])

    # ------------------------------------------------------------------
    # Build gate objects (reused for each carry/sum step)
    # ------------------------------------------------------------------
    carry_gate = _carry_gate().to_gate()
    carry_dag_gate = _carry_dag_gate().to_gate()
    sum_gate = _sum_gate().to_gate()

    # ------------------------------------------------------------------
    # Forward CARRY pass: propagate carries from bit 0 to n-1.
    # After this pass, c[n] holds the carry-out of the full addition.
    # ------------------------------------------------------------------
    for i in range(n):
        qc.append(carry_gate, [c[i], a[i], b[i], c[i + 1]])

    # ------------------------------------------------------------------
    # MSB step — as per Quirk circuit (cols 4 & 5 for n=4):
    #   Step 4: CX(a[n-1], b[n-1])
    #       b[n-1] ^= a[n-1]  (partial XOR — note b[n-1] was modified by
    #       the internal cx(a,b) inside CARRY(n-1), so this inverts that
    #       modification and then adds a[n-1] again, effectively computing
    #       the sum bit via the subsequent SUM gate)
    #   Step 5: SUM(c[n-1], a[n-1], b[n-1])
    #       b[n-1] ^= a[n-1] ^ c[n-1]   (completes the MSB sum)
    # The CARRY(n-1) is NOT inverted — c[n] keeps the final carry-out.
    # ------------------------------------------------------------------
    qc.cx(a[n - 1], b[n - 1])
    qc.append(sum_gate, [c[n - 1], a[n - 1], b[n - 1]])

    # ------------------------------------------------------------------
    # Backward CARRY† + SUM pass: for bits n-2 downto 0.
    # This uncomputes the intermediate carry ancillae c[1..n-1] and
    # computes the partial sum bits b[0..n-2].
    # Matches Quirk cols 6-11 for n=4:
    #   i = n-2: Cdag(c[n-2], a[n-2], b[n-2], c[n-1])
    #             SUM (c[n-2], a[n-2], b[n-2])
    #   ...
    #   i = 0:   Cdag(c[0], a[0], b[0], c[1])
    #             SUM (c[0], a[0], b[0])
    # After this loop, c[1..n-1] are restored to |0⟩.
    # ------------------------------------------------------------------
    for i in range(n - 2, -1, -1):
        qc.append(carry_dag_gate, [c[i], a[i], b[i], c[i + 1]])
        qc.append(sum_gate, [c[i], a[i], b[i]])

    # ------------------------------------------------------------------
    # Measurements
    # ------------------------------------------------------------------
    # result[0..n-1] ← b[0..n-1]  (LSB first)
    for i in range(n):
        qc.measure(b[i], result[i])
    # result[n] ← c[n]  (carry-out / MSB of sum)
    qc.measure(c[n], result[n])

    return qc


def run_simulation(
    qc: QuantumCircuit,
    shots: int = 1024,
) -> Dict[str, int]:
    """Simulate the VBE adder circuit using AerSimulator.

    Parameters
    ----------
    qc:
        The adder quantum circuit (as returned by ``build_vbe_adder``).
    shots:
        Number of simulation shots (default 1024).

    Returns
    -------
    Dict[str, int]
        Measurement counts keyed by bitstring (MSB first, Qiskit convention).

    Raises
    ------
    RuntimeError
        If ``qiskit-aer`` is not installed.
    """
    if not _HAS_AER:
        raise RuntimeError(
            "qiskit-aer is required for simulation. "
            "Install it with:  pip install qiskit-aer"
        )
    backend = AerSimulator()
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=shots).result()
    return result.get_counts()


def decode_result(counts: Dict[str, int], n: int) -> Tuple[int, Dict[str, int]]:
    """Decode simulation counts into the most-likely sum integer.

    Qiskit returns bitstrings in big-endian order (MSB first).  The VBE
    adder result register has layout  result[n] result[n-1] … result[0]
    where result[n] is the carry-out (MSB of the sum).

    Parameters
    ----------
    counts:
        Dictionary of measurement counts from ``run_simulation``.
    n:
        Number of bits in each operand (used for pretty-printing only).

    Returns
    -------
    (most_likely_value, counts)
        most_likely_value — integer value of the dominant measurement outcome.
        counts            — the raw counts dict (passed through for chaining).
    """
    dominant = max(counts, key=counts.get)
    # Qiskit bitstring order: leftmost character = highest-index classical bit
    # Our result register: result[n] is MSB, result[0] is LSB.
    # Qiskit prints result[n] on the LEFT → standard binary, read directly.
    value = int(dominant, 2)
    return value, counts


# ---------------------------------------------------------------------------
# Convenience wrapper
# ---------------------------------------------------------------------------


def add(a: int, b: int, n: int | None = None, shots: int = 2048) -> int:
    """Add two non-negative integers using the VBE quantum adder.

    Parameters
    ----------
    a, b:
        Non-negative integers to add.
    n:
        Bit-width.  Defaults to  max(a.bit_length(), b.bit_length(), 1).
    shots:
        Simulation shots.

    Returns
    -------
    int
        The integer result  a + b  as computed by the quantum circuit.

    Example
    -------
    >>> add(9, 6)
    15
    """
    if a < 0 or b < 0:
        raise ValueError("Operands must be non-negative integers.")

    if n is None:
        n = max(a.bit_length(), b.bit_length(), 1)

    # Encode operands as LSB-first bit lists
    a_bits = [(a >> i) & 1 for i in range(n)]
    b_bits = [(b >> i) & 1 for i in range(n)]

    qc = build_vbe_adder(n, a_bits=a_bits, b_bits=b_bits)
    counts = run_simulation(qc, shots=shots)
    value, _ = decode_result(counts, n)
    return value


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------


def main() -> None:
    """Demonstrate the VBE adder: compute 9 + 6 = 15 on 4 bits."""
    n = 4
    a_val, b_val = 9, 6  # binary: 1001 + 0110 = 1111 (15)

    print(f"VBE Quantum Ripple-Carry Adder — {n}-bit example")
    print(f"  a = {a_val}  ({a_val:0{n}b})")
    print(f"  b = {b_val}  ({b_val:0{n}b})")
    print(f"  Expected sum: {a_val + b_val}  ({a_val + b_val:0{n+1}b})\n")

    qc = build_vbe_adder(
        n,
        a_bits=[(a_val >> i) & 1 for i in range(n)],
        b_bits=[(b_val >> i) & 1 for i in range(n)],
    )
    print(qc.draw(output="text", fold=-1))
    print()

    counts = run_simulation(qc, shots=2048)
    value, _ = decode_result(counts, n)

    print(f"Measurement counts: {counts}")
    print(f"Quantum result: {value}  (expected {a_val + b_val})")
    assert value == a_val + b_val, "Mismatch — check circuit!"
    print("✓ Correct!")


if __name__ == "__main__":
    main()
