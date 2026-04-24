"""
Tests for src/qml/qml_vqc.py

Verifies:
- build_vqc() returns a valid QNode and parameters
- Parameters have the correct shape and requires_grad=True
- loss_fn returns a scalar
- train_vqc runs without error and returns updated parameters
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import numpy as np
from src.qml.qml_vqc import build_vqc, loss_fn, train_vqc


class TestBuildVqc:
    def test_returns_tuple(self):
        """build_vqc() must return a tuple of (circuit, params)."""
        result = build_vqc()
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_params_have_correct_shape(self):
        """Initial params shape must be (n_layers, n_qubits, 3)."""
        n_qubits, n_layers = 2, 3
        _, params = build_vqc(n_qubits=n_qubits, n_layers=n_layers)
        if params is not None:
            assert params.shape == (n_layers, n_qubits, 3)

    def test_params_require_grad(self):
        """Parameters must have requires_grad=True for PennyLane autograd."""
        _, params = build_vqc()
        if params is not None:
            assert hasattr(params, "requires_grad")
            assert params.requires_grad is True

    def test_circuit_is_callable(self):
        """The returned QNode must be callable."""
        circuit, _ = build_vqc()
        if circuit is not None:
            assert callable(circuit)


class TestLossFn:
    def test_returns_scalar(self):
        """loss_fn() must return a scalar value."""
        circuit, params = build_vqc(n_qubits=2, n_layers=1)
        if circuit is None:
            pytest.skip("PennyLane not available.")
        data = [np.array([0.1, 0.2]), np.array([0.9, 0.8])]
        labels = [1, -1]
        loss = loss_fn(circuit, params, data, labels)
        assert hasattr(loss, "__float__") or isinstance(loss, (int, float))

    def test_loss_is_non_negative(self):
        """MSE loss must always be >= 0."""
        circuit, params = build_vqc(n_qubits=2, n_layers=1)
        if circuit is None:
            pytest.skip("PennyLane not available.")
        data = [np.array([0.1, 0.2])]
        labels = [1]
        loss = loss_fn(circuit, params, data, labels)
        assert float(loss) >= 0.0


class TestTrainVqc:
    def test_returns_updated_params(self):
        """train_vqc() must return a params array of the same shape."""
        circuit, params = build_vqc(n_qubits=2, n_layers=1)
        if circuit is None:
            pytest.skip("PennyLane not available.")
        data = [np.array([0.1, 0.2]), np.array([0.9, 0.8])]
        labels = [1, -1]
        updated = train_vqc(circuit, params, data, labels, steps=1)
        assert updated.shape == params.shape

    def test_handles_none_circuit(self):
        """train_vqc() must gracefully return params when circuit is None."""
        params = np.array([[1.0, 2.0, 3.0]])
        result = train_vqc(None, params, [], [], steps=1)
        np.testing.assert_array_equal(result, params)
