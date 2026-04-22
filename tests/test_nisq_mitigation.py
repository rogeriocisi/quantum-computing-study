"""
Tests for src/utils/nisq_mitigation.py

Verifies:
- Circuit structure
- ZNE skeleton: correct keys, non-empty results
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from qiskit import QuantumCircuit
from src.utils.nisq_mitigation import build_test_circuit, apply_zne


class TestBuildTestCircuit:
    def test_returns_quantum_circuit(self):
        """build_test_circuit() must return a QuantumCircuit."""
        qc = build_test_circuit()
        assert isinstance(qc, QuantumCircuit)

    def test_circuit_has_two_qubits(self):
        qc = build_test_circuit()
        assert qc.num_qubits == 2

    def test_circuit_has_measurements(self):
        qc = build_test_circuit()
        gate_names = [instr.operation.name for instr in qc.data]
        assert 'measure' in gate_names


class TestApplyZne:
    def test_returns_dict_with_all_scale_factors(self):
        """apply_zne() must return a result for every scale factor."""
        qc = build_test_circuit()
        scale_factors = (1.0, 1.5, 2.0)
        results = apply_zne(qc, scale_factors=scale_factors)
        assert isinstance(results, dict)
        for s in scale_factors:
            assert s in results

    def test_custom_scale_factors(self):
        """apply_zne() must work with any tuple of scale factors."""
        qc = build_test_circuit()
        custom = (1.0, 2.0, 3.0, 4.0)
        results = apply_zne(qc, scale_factors=custom)
        assert len(results) == len(custom)

    def test_each_result_has_counts_key(self):
        """Each scale factor result must contain a 'counts' key."""
        qc = build_test_circuit()
        results = apply_zne(qc)
        for s, res in results.items():
            assert 'counts' in res, f"Missing 'counts' key for scale factor {s}"
