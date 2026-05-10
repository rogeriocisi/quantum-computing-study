"""
Deutsch-Jozsa Algorithm for solving query problems (Deutsch-Jozsa and Bernstein-Vazirani problems)
===============================================
Implementations of the Deutsch-Jozsa algorithm (Deutsch-Jozsa and Bernstein-Vazirani problems)
for solving query-based problems showing quantum speedup over classical algorithms.
"""

import random
from typing import Dict, Optional
from qiskit import QuantumCircuit, transpile

try:
    from qiskit_aer import AerSimulator
except Exception:
    AerSimulator = None


def build_dj_oracle(n_qubits: int, balanced: bool = True) -> QuantumCircuit:
    """Creates an oracle for the Deutsch-Jozsa algorithm."""
    qc = QuantumCircuit(n_qubits + 1)
    if balanced:
        # Simple balanced: CNOT from each input qubit to the ancilla
        for i in range(n_qubits):
            qc.cx(i, n_qubits)
    else:
        # Constant: either constant 0 (do nothing) or constant 1 (flip ancilla)
        if random.choice([True, False]):
            qc.x(n_qubits)
    return qc


def build_bv_oracle(s: str) -> QuantumCircuit:
    """Creates an oracle for the Bernstein-Vazirani problem."""
    n = len(s)
    qc = QuantumCircuit(n + 1)
    # Reverse string to match Qiskit's little-endian bit ordering
    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(i, n)
    return qc


def create_query_circuit(oracle: QuantumCircuit) -> QuantumCircuit:
    """
    Generic structure for query algorithms (DJ and BV).
    Sets up Hadamards, applies the oracle, and measures input qubits.
    """
    n_qubits = oracle.num_qubits - 1
    qc = QuantumCircuit(n_qubits + 1, n_qubits)

    # Phase kickback setup: Ancilla to |1> then H
    qc.x(n_qubits)
    qc.h(range(n_qubits + 1))

    # Apply the Oracle
    qc.compose(oracle, inplace=True)

    # Final Hadamards on input qubits
    qc.h(range(n_qubits))
    qc.measure(range(n_qubits), range(n_qubits))
    return qc


def run_simulation(qc: QuantumCircuit) -> Optional[Dict[str, int]]:
    """Runs the circuit on a local AerSimulator."""
    if AerSimulator:
        sim = AerSimulator()
        tqc = transpile(qc, sim)
        result = sim.run(tqc, shots=1024).result()
        return result.get_counts()
    return None


def main(mode: str = "DJ", n_qubits: int = 3, secret_s: str = "101") -> None:
    """
    Main flow with mode flexibility.

    Args:
        mode: "DJ" for Deutsch-Jozsa or "BV" for Bernstein-Vazirani.
        n_qubits: Number of qubits for DJ mode.
        secret_s: Hidden bitstring for BV mode.
    """
    print(f"\n--- Running Mode: {mode} ---")

    if mode == "DJ":
        is_balanced = random.choice([True, False])
        print(f"DJ Config: Oracle is {'Balanced' if is_balanced else 'Constant'}")
        oracle = build_dj_oracle(n_qubits, balanced=is_balanced)
    elif mode == "BV":
        print(f"BV Config: Expected secret string = '{secret_s}'")
        oracle = build_bv_oracle(secret_s)
    else:
        print("Invalid mode selected!")
        return

    qc = create_query_circuit(oracle)
    counts = run_simulation(qc)

    if counts:
        # Interpret the result
        # Since these are deterministic in simulation, we take the most frequent bitstring
        result_bits = max(counts, key=counts.get)
        print(f"Measured Result: {result_bits}")

        if mode == "DJ":
            is_constant = all(bit == "0" for bit in result_bits)
            print(f"Conclusion: Function is {'CONSTANT' if is_constant else 'BALANCED'}")
        else:
            print(f"Conclusion: Found secret string = '{result_bits}'")
    else:
        print("Error: AerSimulator not available.")


if __name__ == "__main__":
    # Test Deutsch-Jozsa
    main(mode="DJ", n_qubits=3)

    # Test Bernstein-Vazirani
    main(mode="BV", secret_s="1101")
