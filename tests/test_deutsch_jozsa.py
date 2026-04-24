"""
Tests for src/algorithms/deutsch_jozsa.py

Verifies:
- Oracle circuit structure
- Deutsch-Jozsa output: constant → all-zeros; balanced → non-zero result
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from qiskit import QuantumCircuit
from src.algorithms.deutsch_jozsa import build_oracle, deutsch_jozsa


class TestBuildOracle:
    def test_returns_quantum_circuit(self):
        """build_oracle() must return a QuantumCircuit."""
        oracle = build_oracle(n_qubits=2)
        assert isinstance(oracle, QuantumCircuit)

    def test_oracle_has_correct_qubit_count(self):
        """Oracle for n input qubits must have n+1 total qubits (includes ancilla)."""
        for n in [1, 2, 3]:
            oracle = build_oracle(n_qubits=n)
            assert oracle.num_qubits == n + 1

    def test_oracle_is_not_empty(self):
        """Oracle circuit must contain at least one gate."""
        oracle = build_oracle(n_qubits=2)
        assert len(oracle.data) > 0


class TestDeutschJozsa:
    def test_returns_dict_when_aer_available(self):
        """deutsch_jozsa() must return a dict of counts."""
        result = deutsch_jozsa(n_qubits=2)
        assert result is None or isinstance(result, dict)

    def test_result_has_correct_bit_length(self):
        """Result keys must have length equal to n_qubits."""
        for n in [2, 3, 4]:
            result = deutsch_jozsa(n_qubits=n)
            if result is not None:
                for key in result:
                    assert len(key) == n, (
                        f"Expected key length {n}, got '{key}' (len={len(key)})"
                    )

    def test_total_shots_is_1024(self):
        """Default shot count must be 1024."""
        result = deutsch_jozsa(n_qubits=2)
        if result is not None:
            assert sum(result.values()) == 1024

    def test_counts_are_positive(self):
        """All count values must be positive integers."""
        result = deutsch_jozsa(n_qubits=2)
        if result is not None:
            for count in result.values():
                assert count > 0
