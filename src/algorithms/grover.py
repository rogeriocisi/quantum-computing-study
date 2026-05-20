"""
Grover's Search Algorithm
=========================
A complete implementation of Grover's Search algorithm to locate a specific target
binary state in an unstructured search space, providing a quadratic quantum speedup.
Fully compliant with Qiskit 2.x / 3.0 standards and SamplerV2 primitives.
"""

import math
from typing import Dict, Optional
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2


def build_grover_oracle(target: str) -> QuantumCircuit:
    """Creates a Grover oracle that flips the phase of the specified target state.

    For each '0' bit in the target string, an X gate is applied before and after
    the multi-controlled Z gate. This ensures only the target state undergoes
    the phase inversion.

    Args:
        target: The binary string representing the target state (e.g., "101").

    Returns:
        QuantumCircuit: The oracle circuit operating on len(target) qubits.
    """
    n = len(target)
    qc = QuantumCircuit(n, name="Oracle")

    # Reverse target to align with Qiskit's little-endian bit ordering
    # (qubit 0 corresponds to the rightmost bit)
    target_reversed = list(reversed(target))

    # 1. Apply X gates to qubits that should be '0' in the target state
    for i, bit in enumerate(target_reversed):
        if bit == "0":
            qc.x(i)

    # 2. Apply Multi-Controlled Z (MCZ)
    # In Qiskit, this is achieved by sandwiching an MCX gate with Hadamards on the target qubit
    if n == 1:
        qc.z(0)
    elif n == 2:
        qc.cz(0, 1)
    else:
        qc.h(n - 1)
        qc.mcx(list(range(n - 1)), n - 1)
        qc.h(n - 1)

    # 3. Undo X gates to restore the original computational basis
    for i, bit in enumerate(target_reversed):
        if bit == "0":
            qc.x(i)

    return qc


def build_grover_diffuser(n_qubits: int) -> QuantumCircuit:
    """Creates the Grover diffusion operator (amplitude amplification).

    The diffuser performs a reflection about the equal superposition state:
    H^n * (2|0><0| - I) * H^n

    Args:
        n_qubits: The number of qubits in the circuit.

    Returns:
        QuantumCircuit: The diffuser circuit.
    """
    qc = QuantumCircuit(n_qubits, name="Diffuser")

    # 1. Apply Hadamard gates to all qubits
    qc.h(range(n_qubits))

    # 2. Apply X gates to all qubits
    qc.x(range(n_qubits))

    # 3. Apply Multi-Controlled Z (MCZ)
    if n_qubits == 1:
        qc.z(0)
    elif n_qubits == 2:
        qc.cz(0, 1)
    else:
        qc.h(n_qubits - 1)
        qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
        qc.h(n_qubits - 1)

    # 4. Undo X gates
    qc.x(range(n_qubits))

    # 5. Apply Hadamard gates to all qubits
    qc.h(range(n_qubits))

    return qc


def optimal_iterations(n_qubits: int) -> int:
    """Calculates the theoretically optimal number of Grover iterations.

    The optimal formula is R = floor(pi/4 * sqrt(2^n)).

    Args:
        n_qubits: The number of qubits.

    Returns:
        int: The optimal number of iterations.
    """
    if n_qubits < 1:
        return 0
    return max(1, int(math.floor(math.pi / 4 * math.sqrt(2**n_qubits))))


def create_grover_circuit(target: str, iterations: Optional[int] = None) -> QuantumCircuit:
    """Orchestrates the assembly of the complete Grover's Search algorithm.

    Args:
        target: The target binary string to search for.
        iterations: Optional. Number of iterations. If None, the theoretical optimum is used.

    Returns:
        QuantumCircuit: The complete Grover circuit including measurements.
    """
    n = len(target)
    if iterations is None:
        iterations = optimal_iterations(n)

    qc = QuantumCircuit(n, n)

    # 1. Prepare equal superposition
    qc.h(range(n))

    # 2. Apply the (Oracle -> Diffuser) pair R times
    oracle = build_grover_oracle(target)
    diffuser = build_grover_diffuser(n)

    for _ in range(iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diffuser, inplace=True)

    # 3. Measure all qubits
    qc.measure(range(n), range(n))

    return qc


def run_simulation(qc: QuantumCircuit, shots: int = 1024) -> Optional[Dict[str, int]]:
    """Simulates the Grover circuit using AerSimulator and SamplerV2.

    Args:
        qc: The quantum circuit to simulate.
        shots: The number of simulation executions.

    Returns:
        Optional[Dict[str, int]]: Dictionary mapping measured bitstrings to counts,
        or None if the simulation fails.
    """
    try:
        sim = AerSimulator()
        sampler = SamplerV2()
        tqc = transpile(qc, sim)
        job = sampler.run([(tqc, None, shots)])
        result = job.result()
        pub_result = result[0]
        if qc.cregs:
            creg_name = qc.cregs[0].name
            counts = pub_result.data[creg_name].get_counts()
            return counts
    except Exception as e:
        print(f"Error during Aer simulation: {e}")
    return None


def main() -> None:
    """Main execution flow for demonstrating Grover's Search."""
    target_state = "101"
    n = len(target_state)
    r = optimal_iterations(n)

    print("=== Grover's Search Demonstration ===")
    print(f"Target state: |{target_state}> (size: {n} qubits)")
    print(f"Optimal iterations (theoretical): R = {r}")

    qc = create_grover_circuit(target_state, r)
    print(f"Grover circuit constructed. Total qubits: {qc.num_qubits}")

    counts = run_simulation(qc)
    if counts:
        print("\nSimulation Results (Top 3 frequencies):")
        sorted_counts = sorted(counts.items(), key=lambda x: -x[1])
        for state, count in sorted_counts[:3]:
            prob = count / sum(counts.values()) * 100
            print(f"  |{state}>: count = {count:4d} ({prob:.2f}%)")

        top_measured = sorted_counts[0][0]
        if top_measured == target_state:
            print("\nSUCCESS! The most frequently measured state matches the target!")
        else:
            print("\nFAILURE: The target state was not the most measured state.")
    else:
        print("Local simulator not available.")


if __name__ == "__main__":
    main()
