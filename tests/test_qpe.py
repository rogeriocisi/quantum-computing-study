"""
Tests for src/algorithms/qpe.py

Verifies:
- QPE circuit structure (correct count + target registers, correct measurements)
- Exact binary phase estimates for phi = 0.5, 0.25, 0.125, 0.75
- Approximate phase estimates for non-exact dízima fraction phases like 1/3
- Error margin conforms to QPE theoretical limits
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from qiskit import QuantumCircuit
from src.algorithms.qpe import (
    create_qpe_circuit,
    run_simulation,
    solve_qpe,
)


class TestQpeStructure:
    def test_qpe_circuit_dimensions(self):
        """create_qpe_circuit() must create a circuit with t + 1 qubits and t classical bits."""
        for t in [2, 3, 4]:
            qc = create_qpe_circuit(phi=0.25, n_counting=t)
            assert isinstance(qc, QuantumCircuit)
            assert qc.num_qubits == t + 1
            assert len(qc.clbits) == t


class TestQpeSimulation:
    def test_exact_phase_estimation(self):
        """QPE must estimate exact powers of two (0.5, 0.25, 0.125) with 100% precision."""
        exact_scenarios = [
            (0.5, 3, "100"),    # 0.5 * 8 = 4 -> binary 100
            (0.25, 3, "010"),   # 0.25 * 8 = 2 -> binary 010
            (0.125, 3, "001"),  # 0.125 * 8 = 1 -> binary 001
            (0.75, 4, "1100")   # 0.75 * 16 = 12 -> binary 1100
        ]

        for phi, t, expected_bitstring in exact_scenarios:
            qc = create_qpe_circuit(phi, t)
            counts = run_simulation(qc, shots=500)
            assert counts is not None

            est_phi, bin_str = solve_qpe(counts, t)
            
            # The most frequent measured bitstring must be the exact expected bitstring
            assert bin_str == expected_bitstring
            # The estimated phase must be exactly equal to the real phase
            assert est_phi == phi

    def test_approximate_phase_estimation(self):
        """QPE must find the closest binary approximation for non-exact fraction phases."""
        # phi = 1/3 = 0.3333...
        # Using t = 5 qubits of counting. The denominator is 2^5 = 32.
        # 1/3 * 32 = 10.666...
        # The two closest integers are 11 (binary "01011" -> 11/32 = 0.34375)
        # and 10 (binary "01010" -> 10/32 = 0.3125).
        # QPE must measure one of these two closest states as the top state.
        phi = 1 / 3
        t = 5
        
        qc = create_qpe_circuit(phi, t)
        counts = run_simulation(qc, shots=1000)
        assert counts is not None

        est_phi, bin_str = solve_qpe(counts, t)
        
        # Verify that the measured bitstring is either 10/32 or 11/32
        assert bin_str in ["01010", "01011"]
        
        # The estimated phase must be very close, with error <= 1 / 2^t = 1 / 32 = 0.03125
        error = abs(phi - est_phi)
        assert error <= (1 / (2**t))
