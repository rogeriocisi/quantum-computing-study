"""
Tests for src/algorithms/bell_state.py

Verifies:
- Circuit structure (qubits, gates, measurements)
- Simulation output: Bell state produces only |00> and |11>
- No |01> or |10> outcomes (entanglement contract)
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from qiskit import QuantumCircuit
from src.algorithms.bell_state import create_bell_state, run_simulation


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
        assert 'h' in gate_names

    def test_circuit_contains_cnot(self):
        """Circuit must contain a CNOT gate for entanglement."""
        qc = create_bell_state()
        gate_names = [instr.operation.name for instr in qc.data]
        assert 'cx' in gate_names

    def test_circuit_has_measurements(self):
        """Circuit must contain measurement operations."""
        qc = create_bell_state()
        gate_names = [instr.operation.name for instr in qc.data]
        assert 'measure' in gate_names


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
            assert key in ('00', '11'), f"Unexpected state observed: |{key}>"

    def test_both_bell_states_observed(self):
        """With 1024 shots, both |00> and |11> must appear (high probability)."""
        qc = create_bell_state()
        counts = run_simulation(qc)
        assert '00' in counts
        assert '11' in counts

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
            assert 0.40 <= ratio <= 0.60, (
                f"|{state}> ratio {ratio:.2f} is outside the expected 40-60% range."
            )
