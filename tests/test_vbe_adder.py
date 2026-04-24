"""
Tests for src/algorithms/vbe_adder.py

Verifies the Vedral-Barenco-Ekert (VBE) quantum ripple-carry adder:
  - Circuit structure (qubits, classical bits, gate types)
  - Sub-circuit building blocks (CARRY, CARRY†, SUM)
  - Deterministic correctness: a + b == expected for multiple pairs
  - Edge cases: zero, max-value, single-bit
  - Convenience wrapper: add()
  - Input validation
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from qiskit import QuantumCircuit

from src.algorithms.vbe_adder import (
    _carry_gate,
    _carry_dag_gate,
    _sum_gate,
    build_vbe_adder,
    run_simulation,
    decode_result,
    add,
)

# ---------------------------------------------------------------------------
# Sub-circuit structure tests
# ---------------------------------------------------------------------------


class TestCarryGate:
    """The CARRY sub-circuit must have the expected shape."""

    def test_returns_quantum_circuit(self):
        qc = _carry_gate()
        assert isinstance(qc, QuantumCircuit)

    def test_has_four_qubits(self):
        assert _carry_gate().num_qubits == 4

    def test_has_no_classical_bits(self):
        assert _carry_gate().num_clbits == 0

    def test_contains_toffoli(self):
        names = {instr.operation.name for instr in _carry_gate().data}
        assert "ccx" in names, "CARRY must contain Toffoli (ccx) gates"

    def test_contains_cnot(self):
        names = {instr.operation.name for instr in _carry_gate().data}
        assert "cx" in names, "CARRY must contain a CNOT (cx) gate"

    def test_gate_count(self):
        """VBE CARRY = 2× Toffoli + 1× CNOT = 3 gates total."""
        data = _carry_gate().data
        assert len(data) == 3


class TestCarryDagGate:
    """CARRY† must be the exact inverse of CARRY."""

    def test_returns_quantum_circuit(self):
        assert isinstance(_carry_dag_gate(), QuantumCircuit)

    def test_has_four_qubits(self):
        assert _carry_dag_gate().num_qubits == 4

    def test_contains_toffoli(self):
        names = {instr.operation.name for instr in _carry_dag_gate().data}
        assert "ccx" in names

    def test_gate_count(self):
        """CARRY† = 2× Toffoli + 1× CNOT = 3 gates."""
        assert len(_carry_dag_gate().data) == 3

    def test_is_exact_reverse_of_carry(self):
        """Applying CARRY followed by CARRY† must be the identity."""
        from qiskit import transpile
        from qiskit_aer import AerSimulator

        qc = QuantumCircuit(4)
        # Start with a non-trivial state: flip qubits 1 and 2
        qc.x(1)
        qc.x(2)
        carry_gate = _carry_gate().to_gate()
        carry_dag_gate = _carry_dag_gate().to_gate()
        qc.append(carry_gate, [0, 1, 2, 3])
        qc.append(carry_dag_gate, [0, 1, 2, 3])
        qc.measure_all()

        backend = AerSimulator()
        result = backend.run(transpile(qc, backend), shots=256).result()
        counts = result.get_counts()
        # After carry + carry†, state must be restored to |0110⟩
        # Qiskit orders: qubit 3 (MSB) ... qubit 0 (LSB) → "0110"
        assert list(counts.keys()) == [
            "0110"
        ], f"CARRY · CARRY† is not identity: got {counts}"


class TestSumGate:
    """The SUM sub-circuit must have the expected shape."""

    def test_returns_quantum_circuit(self):
        assert isinstance(_sum_gate(), QuantumCircuit)

    def test_has_three_qubits(self):
        assert _sum_gate().num_qubits == 3

    def test_has_no_classical_bits(self):
        assert _sum_gate().num_clbits == 0

    def test_contains_cnot(self):
        names = {instr.operation.name for instr in _sum_gate().data}
        assert "cx" in names

    def test_gate_count(self):
        """VBE SUM = 2× CNOT."""
        assert len(_sum_gate().data) == 2


# ---------------------------------------------------------------------------
# Circuit structure tests
# ---------------------------------------------------------------------------


class TestBuildVbeAdder:
    """build_vbe_adder() must produce well-formed circuits."""

    def test_returns_quantum_circuit(self):
        assert isinstance(build_vbe_adder(2), QuantumCircuit)

    @pytest.mark.parametrize("n", [1, 2, 4, 8])
    def test_qubit_count(self, n):
        """Total qubits = (n+1) carry + n addend-a + n addend-b = 3n+1."""
        qc = build_vbe_adder(n)
        assert (
            qc.num_qubits == 3 * n + 1
        ), f"Expected {3*n+1} qubits for n={n}, got {qc.num_qubits}"

    @pytest.mark.parametrize("n", [1, 2, 4, 8])
    def test_classical_bit_count(self, n):
        """Result register width = n+1 (n sum bits + 1 carry-out)."""
        qc = build_vbe_adder(n)
        assert qc.num_clbits == n + 1

    def test_has_measurements(self):
        qc = build_vbe_adder(2)
        names = [instr.operation.name for instr in qc.data]
        assert "measure" in names

    def test_a_bits_initialisation(self):
        """X gates must be applied for set bits in a."""
        qc = build_vbe_adder(2, a_bits=[1, 0])
        # At least one X gate expected for the '1' bit
        names = [instr.operation.name for instr in qc.data]
        assert "x" in names

    def test_invalid_a_bits_length(self):
        with pytest.raises(ValueError, match="a_bits must have length"):
            build_vbe_adder(4, a_bits=[1, 0])  # wrong length

    def test_invalid_b_bits_length(self):
        with pytest.raises(ValueError, match="b_bits must have length"):
            build_vbe_adder(4, b_bits=[1, 0, 1])

    def test_invalid_a_bits_values(self):
        with pytest.raises(ValueError, match="only 0 or 1"):
            build_vbe_adder(2, a_bits=[0, 2])

    def test_invalid_b_bits_values(self):
        with pytest.raises(ValueError, match="only 0 or 1"):
            build_vbe_adder(2, b_bits=[-1, 1])


# ---------------------------------------------------------------------------
# Correctness tests (simulation-based)
# ---------------------------------------------------------------------------


class TestVbeAdderCorrectness:
    """The VBE adder must compute a + b correctly for all tested pairs."""

    SHOTS = 4096  # high shot count for deterministic results

    @pytest.mark.parametrize(
        "a_val, b_val, n",
        [
            # The Quirk example: init=[0,1,0,0,1,1,0,0,1,0,1,1] → 9 + 6 = 15
            (9, 6, 4),
            # Zero operands
            (0, 0, 1),
            (0, 5, 3),
            (5, 0, 3),
            # Single-bit cases
            (0, 1, 1),
            (1, 0, 1),
            (1, 1, 1),  # 1+1=2, carry-out = 1  → result = 10 in binary
            # Multi-bit cases
            (3, 4, 3),  # 011 + 100 = 111
            (7, 1, 3),  # 111 + 001 = 1000 (carry out)
            (15, 15, 4),  # max 4-bit + max 4-bit = 30
            (10, 5, 4),  # 1010 + 0101 = 1111
        ],
    )
    def test_addition(self, a_val, b_val, n):
        a_bits = [(a_val >> i) & 1 for i in range(n)]
        b_bits = [(b_val >> i) & 1 for i in range(n)]
        qc = build_vbe_adder(n, a_bits=a_bits, b_bits=b_bits)
        counts = run_simulation(qc, shots=self.SHOTS)
        value, _ = decode_result(counts, n)
        expected = a_val + b_val
        assert value == expected, (
            f"VBE adder: {a_val} + {b_val} in {n} bits → got {value}, "
            f"expected {expected}. counts={counts}"
        )

    def test_quirk_example(self):
        """Replicate the exact Quirk URL example: a=9 (1001), b=6 (0110)."""
        # Quirk init vector LSB first: a=[1,0,0,1], b=[0,1,1,0]
        qc = build_vbe_adder(4, a_bits=[1, 0, 0, 1], b_bits=[0, 1, 1, 0])
        counts = run_simulation(qc, shots=self.SHOTS)
        value, _ = decode_result(counts, 4)
        assert value == 15, f"Quirk example (9+6): expected 15, got {value}"

    def test_result_is_deterministic(self):
        """A fully specified input must yield exactly one outcome (counts has one key)."""
        qc = build_vbe_adder(3, a_bits=[1, 0, 1], b_bits=[0, 1, 0])
        counts = run_simulation(qc, shots=2048)
        assert (
            len(counts) == 1
        ), f"Deterministic circuit must yield exactly 1 outcome, got {counts}"

    def test_counts_sum_to_shots(self):
        qc = build_vbe_adder(2, a_bits=[1, 0], b_bits=[0, 1])
        shots = 512
        counts = run_simulation(qc, shots=shots)
        assert sum(counts.values()) == shots


# ---------------------------------------------------------------------------
# decode_result tests
# ---------------------------------------------------------------------------


class TestDecodeResult:
    def test_returns_dominant_value(self):
        counts = {"01111": 900, "00000": 1}
        val, returned_counts = decode_result(counts, 4)
        assert val == int("01111", 2)  # = 15
        assert returned_counts is counts

    def test_single_entry(self):
        counts = {"10000": 1024}
        val, _ = decode_result(counts, 4)
        assert val == 16  # 5-bit result: 1 carry-out + 0000 = 16


# ---------------------------------------------------------------------------
# Convenience wrapper tests
# ---------------------------------------------------------------------------


class TestAdd:
    def test_basic(self):
        assert add(9, 6) == 15

    def test_zero_plus_zero(self):
        assert add(0, 0) == 0

    def test_zero_plus_n(self):
        assert add(0, 7) == 7

    def test_n_plus_zero(self):
        assert add(5, 0) == 5

    def test_with_carry(self):
        assert add(7, 1, n=3) == 8

    def test_explicit_n(self):
        assert add(3, 3, n=4) == 6

    def test_negative_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            add(-1, 5)

    def test_both_negative_raises(self):
        with pytest.raises(ValueError, match="non-negative"):
            add(-3, -2)
