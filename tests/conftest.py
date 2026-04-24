"""
Shared pytest fixtures for the quantum-computing-study test suite.
"""

import pytest
import numpy as np


@pytest.fixture
def rng():
    """Seeded numpy random generator for reproducible tests."""
    return np.random.default_rng(seed=42)


@pytest.fixture
def mock_data():
    """Small synthetic dataset for QML tests."""
    X = [
        np.array([0.1, 0.2]),
        np.array([0.9, 0.8]),
        np.array([0.2, 0.1]),
        np.array([0.8, 0.9]),
    ]
    y = [1, -1, 1, -1]
    return X, y
