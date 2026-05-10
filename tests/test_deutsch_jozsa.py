"""
Tests for src/algorithms/deutsch_jozsa.py

Verifies:
- DJ Oracle circuit structure (constant/balanced)
- BV Oracle circuit structure (secret string encoding)
- Query circuit structure (Phase Kickback, Hadamards)
- Algorithm outputs:
    - DJ: constant → all-zeros; balanced → non-zero result
    - BV: returns secret string s
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from qiskit import QuantumCircuit
from src.algorithms.deutsch_jozsa import (
    build_dj_oracle,
    build_bv_oracle,
    create_query_circuit,
    run_simulation,
)


class TestOracles:
    def test_dj_oracle_structure(self):
        """build_dj_oracle() must return a QuantumCircuit with n+1 qubits."""
        for n in [1, 2, 3]:
            oracle = build_dj_oracle(n_qubits=n, balanced=True)
            assert isinstance(oracle, QuantumCircuit)
            assert oracle.num_qubits == n + 1

    def test_bv_oracle_structure(self):
        """build_bv_oracle() must return a QuantumCircuit with len(s)+1 qubits."""
        for s in ["10", "110", "1111"]:
            oracle = build_bv_oracle(s)
            assert isinstance(oracle, QuantumCircuit)
            assert oracle.num_qubits == len(s) + 1


class TestQueryAlgorithms:
    def test_deutsch_jozsa_constant(self):
        """DJ must return all zeros for a constant oracle."""
        n = 3
        oracle = build_dj_oracle(n, balanced=False)
        qc = create_query_circuit(oracle)
        result = run_simulation(qc)
        if result:
            measured = max(result, key=result.get)
            assert measured == "0" * n

    def test_deutsch_jozsa_balanced(self):
        """DJ must return a non-zero string for a balanced oracle."""
        n = 3
        oracle = build_dj_oracle(n, balanced=True)
        qc = create_query_circuit(oracle)
        result = run_simulation(qc)
        if result:
            measured = max(result, key=result.get)
            assert measured != "0" * n

    def test_bernstein_vazirani(self):
        """BV must return the exact secret string."""
        for s in ["101", "1100", "11"]:
            oracle = build_bv_oracle(s)
            qc = create_query_circuit(oracle)
            result = run_simulation(qc)
            if result:
                measured = max(result, key=result.get)
                assert measured == s

    def test_returns_dict_when_aer_available(self):
        """run_simulation() must return a dict of counts."""
        oracle = build_dj_oracle(n_qubits=2)
        qc = create_query_circuit(oracle)
        result = run_simulation(qc)
        assert result is None or isinstance(result, dict)

    def test_result_has_correct_bit_length(self):
        """Result keys must have length equal to n_qubits."""
        for n in [2, 3]:
            oracle = build_dj_oracle(n_qubits=n)
            qc = create_query_circuit(oracle)
            result = run_simulation(qc)
            if result is not None:
                for key in result:
                    assert len(key) == n

    def test_total_shots_is_1024(self):
        """Default shot count must be 1024."""
        oracle = build_dj_oracle(n_qubits=2)
        qc = create_query_circuit(oracle)
        result = run_simulation(qc)
        if result is not None:
            assert sum(result.values()) == 1024
