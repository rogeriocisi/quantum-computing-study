"""
Tests for src/utils/foundations.py

Verifies:
- apply_bell_pair: Correct gate application on target qubits
- create_bell_state: Circuit structure (qubits, gates, measurements)
- Simulation output: Bell state produces only |00> and |11>
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from qiskit import QuantumCircuit
from src.utils.foundations import apply_bell_pair, create_bell_state, run_simulation


class TestApplyBellPair:
    def test_applies_correct_gates(self):
        """apply_bell_pair must apply H and CX to the specified qubits."""
        qc = QuantumCircuit(3)
        apply_bell_pair(qc, 1, 2)

        # Filter for non-barrier instructions
        gate_names = [
            instr.operation.name
            for instr in qc.data
            if instr.operation.name != "barrier"
        ]
        assert gate_names == ["h", "cx"]

        # Check qubit indices
        assert qc.data[0].qubits[0]._index == 1  # H on q1
        assert qc.data[1].qubits[0]._index == 1  # CX control q1
        assert qc.data[1].qubits[1]._index == 2  # CX target q2


class TestCreateBellState:
    def test_returns_quantum_circuit(self):
        """create_bell_state() must return a QuantumCircuit."""
        qc = create_bell_state()
        assert isinstance(qc, QuantumCircuit)

    def test_circuit_has_two_qubits(self):
        """Bell state requires exactly 2 qubits."""
        qc = create_bell_state()
        assert qc.num_qubits == 2

    def test_circuit_has_two_classical_bits(self):
        """Bell state circuit must have 2 classical measurement bits."""
        qc = create_bell_state()
        assert qc.num_clbits == 2

    def test_circuit_contains_hadamard(self):
        """Circuit must contain a Hadamard gate for superposition."""
        qc = create_bell_state()
        gate_names = [instr.operation.name for instr in qc.data]
        assert "h" in gate_names

    def test_circuit_contains_cnot(self):
        """Circuit must contain a CNOT gate for entanglement."""
        qc = create_bell_state()
        gate_names = [instr.operation.name for instr in qc.data]
        assert "cx" in gate_names

    def test_circuit_has_measurements(self):
        """Circuit must contain measurement operations."""
        qc = create_bell_state()
        gate_names = [instr.operation.name for instr in qc.data]
        assert "measure" in gate_names


class TestRunSimulation:
    def test_returns_dict(self):
        """run_simulation() must return a counts dictionary."""
        qc = create_bell_state()
        counts = run_simulation(qc)
        assert isinstance(counts, dict)

    def test_only_bell_states_observed(self):
        """Bell state must only produce |00> and |11> — no |01> or |10>."""
        qc = create_bell_state()
        counts = run_simulation(qc)
        for key in counts:
            assert key in ("00", "11"), f"Unexpected state observed: |{key}>"

    def test_both_bell_states_observed(self):
        """With 1024 shots, both |00> and |11> must appear (high probability)."""
        qc = create_bell_state()
        counts = run_simulation(qc)
        assert "00" in counts
        assert "11" in counts

    def test_counts_sum_to_shots(self):
        """Total counts must equal the number of shots (1024)."""
        qc = create_bell_state()
        counts = run_simulation(qc)
        assert sum(counts.values()) == 1024

    def test_distribution_is_approximately_uniform(self):
        """Each Bell state should appear in roughly 40-60% of shots."""
        qc = create_bell_state()
        counts = run_simulation(qc)
        total = sum(counts.values())
        for state, count in counts.items():
            ratio = count / total
            assert (
                0.40 <= ratio <= 0.60
            ), f"|{state}> ratio {ratio:.2f} is outside the expected 40-60% range."
