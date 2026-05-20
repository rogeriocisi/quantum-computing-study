"""
Quantum Phase Estimation (QPE)
==============================
An implementation of the Quantum Phase Estimation algorithm to estimate the fractional
phase phi of an eigenvalue e^(2*pi*i*phi) associated with a unitary operator U.
Fully compliant with Qiskit 2.x / 3.0 standards and SamplerV2 primitives.
"""

import math
from typing import Dict, Optional, Tuple
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFTGate
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2


def create_qpe_circuit(phi: float, n_counting: int) -> QuantumCircuit:
    """Creates the Quantum Phase Estimation (QPE) circuit.

    Uses a single-qubit phase rotation gate P(2*pi*phi) as the unitary operator U,
    with the target qubit prepared in the eigenstate |1>.

    Args:
        phi: The real fractional phase to estimate (0 <= phi < 1).
        n_counting: The number of qubits in the counting register (determines precision).

    Returns:
        QuantumCircuit: The complete QPE circuit with measurements.
    """
    # QPE requires n_counting qubits in the counting register + 1 target qubit
    count_reg = QuantumRegister(n_counting, name="count")
    target_reg = QuantumRegister(1, name="target")
    class_reg = ClassicalRegister(n_counting, name="c")

    qc = QuantumCircuit(count_reg, target_reg, class_reg)

    # 1. Prepare target qubit in the eigenstate |1> (applying an X gate)
    qc.x(target_reg[0])

    # 2. Apply Hadamard gates to counting qubits to create an equal superposition
    qc.h(count_reg)

    # 3. Apply controlled-U^{2^j} phase rotation operations
    # Where U = P(2*pi*phi). Therefore U^{2^j} = P(2*pi*phi * 2^j).
    # The counting qubit 'j' controls the application of the operator on the target qubit.
    for j in range(n_counting):
        # The accumulated phase is theta = 2 * pi * phi * (2**j)
        theta = 2 * math.pi * phi * (2**j)
        qc.cp(theta, count_reg[j], target_reg[0])

    # 4. Apply Inverse Quantum Fourier Transform (IQFT) on the counting register
    iqft_gate = QFTGate(n_counting).inverse()
    qc.append(iqft_gate, list(range(n_counting)))

    # 5. Measure the counting register
    qc.measure(count_reg, class_reg)

    return qc


def run_simulation(qc: QuantumCircuit, shots: int = 2048) -> Optional[Dict[str, int]]:
    """Simulates the QPE circuit using AerSimulator and SamplerV2.

    Args:
        qc: The QPE quantum circuit to simulate.
        shots: The number of simulation executions.

    Returns:
        Optional[Dict[str, int]]: Dictionary mapping measured bitstrings to counts.
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
            return pub_result.data[creg_name].get_counts()
    except Exception as e:
        print(f"Error during Aer simulation for QPE: {e}")
    return None


def solve_qpe(counts: Dict[str, int], n_counting: int) -> Tuple[float, str]:
    """Interprets the measurement results to decode the estimated decimal phase phi.

    Finds the most frequent measured bitstring, and converts its fractional binary
    value to decimal: phi_est = int(b, 2) / (2**n_counting).

    Args:
        counts: The dictionary of measurement counts.
        n_counting: The number of counting qubits used in the circuit.

    Returns:
        Tuple[float, str]: The estimated decimal phase (phi_est) and the corresponding
        measured bitstring (b).
    """
    # Find the most frequent bitstring
    most_frequent_bitstring = max(counts, key=counts.get)

    # Convert fractional binary to decimal
    # e.g., "01" (n=2) -> int("01", 2) = 1 -> 1 / (2^2) = 0.25
    measured_int = int(most_frequent_bitstring, 2)
    estimated_phi = measured_int / (2**n_counting)

    return estimated_phi, most_frequent_bitstring


def main() -> None:
    """Main execution flow for demonstrating Quantum Phase Estimation (QPE)."""
    print("=== Quantum Phase Estimation (QPE) Demonstration ===")

    # Test scenarios: (real phase phi, number of counting qubits)
    scenarios = [
        (0.5, 3),    # Exact: phi = 0.5 -> 1/2 -> "100" with 3 qubits
        (0.25, 3),   # Exact: phi = 0.25 -> 1/4 -> "010" with 3 qubits
        (0.75, 4),   # Exact: phi = 0.75 -> 3/4 -> "1100" with 4 qubits
        (0.3333, 5)  # Non-exact: 1/3 (fraction) -> converges to nearest binary approximation in 5 qubits (11/32 or 10/32)
    ]

    for real_phi, t in scenarios:
        print(f"\n>> Scenario: Real phase phi = {real_phi:.4f} with t = {t} counting qubits")

        qc = create_qpe_circuit(real_phi, t)
        counts = run_simulation(qc)

        if counts:
            est_phi, bin_str = solve_qpe(counts, t)
            prob = counts[bin_str] / sum(counts.values()) * 100
            error = abs(real_phi - est_phi)

            print(f"   Most probable bitstring: |{bin_str}> (probability = {prob:.2f}%)")
            print(f"   Estimated Phase: phi_est = {est_phi:.5f}")
            print(f"   Absolute Error: {error:.5f}")
        else:
            print("   Local simulator not available.")


if __name__ == "__main__":
    main()
