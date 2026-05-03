"""
Tests for src/algorithms/chsh_game.py

Verifies:
- Circuit construction for all (x, y) pairs
- Winning condition logic
- Violation of Bell's Inequality (>75% win rate)
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from qiskit import QuantumCircuit
from src.algorithms.chsh_game import (
    create_chsh_circuit,
    run_simulation,
    analyze_results,
)


class TestCHSHGame:
    @pytest.mark.parametrize("x, y", [(0, 0), (0, 1), (1, 0), (1, 1)])
    def test_create_circuit_valid_structure(self, x, y):
        """Circuit must be valid and have 2 qubits/bits."""
        qc = create_chsh_circuit(x, y)
        assert isinstance(qc, QuantumCircuit)
        assert qc.num_qubits == 2
        assert qc.num_clbits == 2

    def test_simulation_returns_all_configs(self):
        """Simulation must return results for all 4 (x, y) pairs."""
        results = run_simulation(trials_per_config=10)
        assert len(results) == 4
        for x in [0, 1]:
            for y in [0, 1]:
                assert (x, y) in results

    def test_win_rate_violates_bell_inequality(self):
        """Overall win rate must be significantly > 75% (using 1000 trials)."""
        results = run_simulation(trials_per_config=500)
        win_rate = analyze_results(results)

        # 75% is the classical limit. 80% is a safe threshold for a successful quantum test
        # even with small statistical fluctuations.
        assert win_rate > 0.80
        assert win_rate <= 1.0

    def test_analyze_results_output_type(self):
        """analyze_results should return a float."""
        results = {(0, 0): {"00": 100}}
        win_rate = analyze_results(results)
        assert isinstance(win_rate, float)
        assert win_rate == 1.0
