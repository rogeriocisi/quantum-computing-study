"""
Deutsch-Jozsa Algorithm
=======================
An implementation of the Deutsch-Jozsa algorithm, demonstrating quantum speedup
for determining if a black-box function (oracle) is constant or balanced.
"""

from typing import Dict, Optional
from qiskit import QuantumCircuit, transpile

try:
    from qiskit_aer import AerSimulator
except Exception:
    AerSimulator = None


def build_oracle(n_qubits: int, balanced: bool = True) -> QuantumCircuit:
    """
    Return an oracle circuit for D-J algorithm.
    Replace body to implement custom oracles.
    """
    qc = QuantumCircuit(n_qubits + 1)
    # Placeholder: prepare last qubit in |1> for phase kickback
    qc.x(n_qubits)
    return qc


def create_deutsch_jozsa_circuit(
    n_qubits: int = 2, balanced: bool = True
) -> QuantumCircuit:
    """Constructs a Deutsch-Jozsa circuit.

    Args:
        n_qubits: Number of input qubits.
        balanced: Whether the oracle is balanced or constant.

    Returns:
        QuantumCircuit: The constructed circuit.
    """
    qc = QuantumCircuit(n_qubits + 1, n_qubits)
    # Hadamard on input and ancilla
    qc.h(range(n_qubits + 1))
    oracle = build_oracle(n_qubits, balanced)
    qc.compose(oracle, inplace=True)
    qc.h(range(n_qubits))
    qc.measure(range(n_qubits), range(n_qubits))
    return qc


def run_simulation(qc: QuantumCircuit) -> Optional[Dict[str, int]]:
    """Runs the Deutsch-Jozsa circuit on a local AerSimulator.

    Args:
        qc: The QuantumCircuit to simulate.

    Returns:
        Optional[Dict[str, int]]: The measurement counts or None if Aer is missing.
    """
    if AerSimulator:
        sim = AerSimulator()
        tqc = transpile(qc, sim)
        result = sim.run(tqc).result()
        return result.get_counts()
    else:
        return None


def main() -> None:
    """Minimal runnable flow."""
    qc = create_deutsch_jozsa_circuit(n_qubits=3, balanced=False)
    counts = run_simulation(qc)
    print("Counts:", counts)


if __name__ == "__main__":
    main()
