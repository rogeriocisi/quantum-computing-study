"""
Tests for src/algorithms/grover.py

Verifies:
- Grover's optimal iterations calculation
- Oracle circuit structure (correct qubits, correct name)
- Diffuser circuit structure
- End-to-end simulation of Grover's search for 2, 3, and 4 qubits
- Success probability matches theoretical expectations (>90%)
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from qiskit import QuantumCircuit
from src.algorithms.grover import (
    build_grover_oracle,
    build_grover_diffuser,
    optimal_iterations,
    create_grover_circuit,
    run_simulation,
)


class TestGroverStructure:
    def test_optimal_iterations(self):
        """optimal_iterations() must return correct optimal steps R."""
        assert optimal_iterations(1) == 1
        assert optimal_iterations(2) == 1
        assert optimal_iterations(3) == 2
        assert optimal_iterations(4) == 3

    def test_oracle_structure(self):
        """build_grover_oracle() must return a circuit with len(target) qubits."""
        for target in ["10", "111", "0101"]:
            oracle = build_grover_oracle(target)
            assert isinstance(oracle, QuantumCircuit)
            assert oracle.num_qubits == len(target)
            assert oracle.name == "Oracle"

    def test_diffuser_structure(self):
        """build_grover_diffuser() must return a circuit with n qubits."""
        for n in [1, 2, 3, 4]:
            diffuser = build_grover_diffuser(n)
            assert isinstance(diffuser, QuantumCircuit)
            assert diffuser.num_qubits == n
            assert diffuser.name == "Diffuser"

    def test_create_grover_circuit(self):
        """create_grover_circuit() must assemble the correct register layout."""
        target = "10101"
        qc = create_grover_circuit(target)
        assert isinstance(qc, QuantumCircuit)
        assert qc.num_qubits == len(target)
        assert len(qc.clbits) == len(target)


class TestGroverSimulation:
    def test_end_to_end_2_qubits(self):
        """Grover's search on 2 qubits must find any target with 100% theoretical probability."""
        for target in ["00", "01", "10", "11"]:
            qc = create_grover_circuit(target)
            counts = run_simulation(qc, shots=500)
            assert counts is not None
            
            # Find the most frequent bitstring
            measured = max(counts, key=counts.get)
            assert measured == target
            
            # Theoretical success probability is 100% for 2 qubits (1 iteration)
            success_prob = counts[measured] / sum(counts.values())
            assert success_prob >= 0.98  # allowing tiny statistical noise if any

    def test_end_to_end_3_qubits(self):
        """Grover's search on 3 qubits must find target with >90% probability (R=2)."""
        target = "101"
        qc = create_grover_circuit(target)
        counts = run_simulation(qc, shots=1000)
        assert counts is not None

        measured = max(counts, key=counts.get)
        assert measured == target

        # Theoretical success probability is approx 94.5%
        success_prob = counts[measured] / sum(counts.values())
        assert success_prob >= 0.90

    def test_end_to_end_4_qubits(self):
        """Grover's search on 4 qubits must find target with >90% probability (R=3)."""
        target = "1100"
        qc = create_grover_circuit(target)
        counts = run_simulation(qc, shots=1000)
        assert counts is not None

        measured = max(counts, key=counts.get)
        assert measured == target

        # Theoretical success probability is approx 96.1%
        success_prob = counts[measured] / sum(counts.values())
        assert success_prob >= 0.90
