"""
Tests for src/optimization/vqe_qaoa.py

Verifies:
- QAOA ansatz structure
- VQE workflow returns a valid numpy array of parameters
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
from qiskit import QuantumCircuit
from src.optimization.vqe_qaoa import build_qaoa_ansatz, vqe_workflow


class TestBuildQaoaAnsatz:
    def test_returns_quantum_circuit(self):
        """build_qaoa_ansatz() must return a QuantumCircuit."""
        qc = build_qaoa_ansatz()
        assert isinstance(qc, QuantumCircuit)

    def test_circuit_has_correct_qubit_count(self):
        """Ansatz must have the requested number of qubits."""
        for n in [2, 4, 6]:
            qc = build_qaoa_ansatz(n_qubits=n)
            assert qc.num_qubits == n

    def test_default_is_4_qubits(self):
        """Default n_qubits should be 4."""
        qc = build_qaoa_ansatz()
        assert qc.num_qubits == 4


class TestVqeWorkflow:
    def test_returns_numpy_array(self):
        """vqe_workflow() must return a numpy array of parameters."""
        qc = build_qaoa_ansatz()
        result = vqe_workflow(qc)
        assert isinstance(result, np.ndarray)

    def test_returns_correct_shape(self):
        """Returned parameter array must be non-empty."""
        qc = build_qaoa_ansatz()
        result = vqe_workflow(qc)
        assert result.shape[0] > 0

    def test_accepts_none_hamiltonian(self):
        """vqe_workflow() must handle a None hamiltonian without error."""
        qc = build_qaoa_ansatz()
        result = vqe_workflow(qc, hamiltonian=None)
        assert result is not None
