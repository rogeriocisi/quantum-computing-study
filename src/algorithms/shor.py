"""
Shor's Algorithm
================
Implementation of Shor's algorithm for integer factorization.
This algorithm provides an exponential speedup over classical algorithms
by reducing factorization to the Order Finding problem, which is solved
efficiently using Quantum Phase Estimation (QPE) and the Quantum Fourier Transform (QFT).
"""

import math
from fractions import Fraction
from typing import Dict, Tuple, Optional
import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Operator
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2


def classical_preprocess(N: int) -> Tuple[bool, Optional[int]]:
    """Performs cheap classical checks to determine if N is prime or has trivial factors.

    Args:
        N: The composite integer to factor.

    Returns:
        A tuple (done, factor) where:
            done (bool): True if a factor was found or N is too small, False otherwise.
            factor (int or None): The non-trivial factor if found, else None.
    """
    if N <= 3:
        return True, None
    if N % 2 == 0:
        return True, 2

    # Perfect power check (N = a^b for integers a >= 2, b >= 2)
    for b in range(2, math.ceil(math.log2(N)) + 1):
        a = round(N ** (1.0 / b))
        if a**b == N:
            return True, a

    return False, None


def build_c_u_power(a: int, power: int, N: int) -> QuantumCircuit:
    """Builds a controlled-U^{2^power} gate for modular multiplication by a mod N.

    This function constructs the unitary operator for the mapping:
        |y> -> |(a^(2^power) * y) mod N>   for y < N
        |y> -> |y>                          for y >= N
    and wraps it in a controlled gate.

    Args:
        a: The coprime base.
        power: The exponent power index (i for 2^i).
        N: The modulus.

    Returns:
        QuantumCircuit: A circuit with 1 + m qubits (qubit 0 is control, qubits 1..m are target).
    """
    m = math.ceil(math.log2(N))
    qc = QuantumCircuit(1 + m, name=f"C-U^{2**power}")

    # Compute a^{2^power} mod N securely without overflow
    ap = a
    for _ in range(power):
        ap = (ap * ap) % N

    # Build the permutation matrix for U^{2^power}
    dim = 2**m
    matrix = np.zeros((dim, dim))
    for k in range(dim):
        if k < N:
            target = (k * ap) % N
        else:
            target = k
        matrix[target, k] = 1.0

    # Convert to Operator and create controlled gate
    u_op = Operator(matrix)
    controlled_u = u_op.to_instruction().control(1)

    # Append to circuit: qubit 0 is control, 1..m are target
    qc.append(controlled_u, [0] + list(range(1, 1 + m)))
    return qc


def create_shor_circuit(a: int, N: int) -> QuantumCircuit:
    """Assembles the full Order Finding (QPE) quantum circuit for Shor's algorithm.

    Args:
        a: The coprime base (1 < a < N, gcd(a, N) == 1).
        N: The composite integer to factor.

    Returns:
        QuantumCircuit: The complete quantum circuit.
    """
    n_count = 2 * math.ceil(math.log2(N))  # size of counting register
    m = math.ceil(math.log2(N))  # size of target register

    count_reg = QuantumRegister(n_count, name="count")
    target_reg = QuantumRegister(m, name="target")
    class_reg = ClassicalRegister(n_count, name="c")

    qc = QuantumCircuit(count_reg, target_reg, class_reg)

    # 1. Initialize counting register in superposition, target register in |1>
    qc.h(count_reg)
    qc.x(target_reg[0])

    # 2. Apply controlled modular exponentiation gates
    for i in range(n_count):
        c_u = build_c_u_power(a, i, N)
        qc.append(c_u, [count_reg[i]] + list(target_reg))

    # 3. Apply Inverse QFT on counting register
    qc.append(QFT(n_count, inverse=True).to_gate(label="IQFT"), count_reg)

    # 4. Measure counting register
    qc.measure(count_reg, class_reg)

    return qc


def run_simulation(qc: QuantumCircuit, shots: int = 2048) -> Dict[str, int]:
    """Simulates the Shor's circuit using AerSimulator and SamplerV2.

    Args:
        qc: The QuantumCircuit to execute.
        shots: The number of simulation shots.

    Returns:
        Dict[str, int]: The measurement counts dictionary.
    """
    sim = AerSimulator()
    sampler = SamplerV2()
    tqc = transpile(qc, sim)
    job = sampler.run([(tqc, None, shots)])
    result = job.result()

    if qc.cregs:
        creg_name = qc.cregs[0].name
        return result[0].data[creg_name].get_counts()
    return {}


def solve_shor(counts: Dict[str, int], a: int, N: int) -> Optional[int]:
    """Performs classical continued fractions post-processing to extract the order r

    and find a non-trivial factor of N.

    Args:
        counts: The measurement counts from the quantum circuit.
        a: The coprime base used in the circuit.
        N: The composite integer to factor.

    Returns:
        Optional[int]: A non-trivial factor of N if found, otherwise None.
    """
    n_count = 2 * math.ceil(math.log2(N))

    # Sort counts by frequency in descending order
    sorted_counts = sorted(counts.items(), key=lambda x: -x[1])

    for bitstring, _ in sorted_counts:
        # Convert binary measurement to integer
        measured_val = int(bitstring, 2)
        if measured_val == 0:
            continue

        # Convert to phase value in [0, 1)
        phase = measured_val / (2**n_count)

        # Use continued fractions to find approximation s/r
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator

        # Verify if r is indeed the order of a mod N
        if r == 0 or pow(a, r, N) != 1:
            continue

        # Condition for success: r is even and a^(r/2) != -1 mod N
        if r % 2 == 0 and pow(a, r // 2, N) != N - 1:
            for offset in (1, -1):
                candidate = math.gcd(pow(a, r // 2, N) + offset, N)
                if 1 < candidate < N:
                    return candidate

    return None


def factor(N: int) -> Optional[int]:
    """High-level orchestrator to factor N using Shor's algorithm.

    This function coordinates classical preprocessing, random coprime base selection,
    quantum order finding circuit simulation, and classical post-processing.

    Args:
        N: The composite integer to factor.

    Returns:
        Optional[int]: A non-trivial factor of N if found, otherwise None.
    """
    # 1. Classical pre-processing
    done, factor_val = classical_preprocess(N)
    if done:
        return factor_val

    # 2. Iterate or choose random bases coprime to N
    # For small demonstrations like 15 and 21, we can search or pick from coprime candidates.
    rng = np.random.default_rng(seed=42)
    max_attempts = 10

    for attempt in range(max_attempts):
        a = rng.integers(2, N)
        g = math.gcd(a, N)
        if g > 1:
            return g  # Lucky classical factor!

        # a is coprime to N, proceed with quantum simulation
        qc = create_shor_circuit(a, N)
        counts = run_simulation(qc)
        result_factor = solve_shor(counts, a, N)
        if result_factor is not None:
            return result_factor

    return None


def main() -> None:
    """Main execution flow for Shor's Algorithm demonstration."""
    N = 15
    print(f"--- Shor's Algorithm Demo: Factoring N = {N} ---")

    done, factor_val = classical_preprocess(N)
    if done:
        if factor_val:
            print(f"N = {N} has a trivial factor: {factor_val}")
        else:
            print(f"N = {N} is prime or too small.")
        return

    # Valid coprimes for N=15 are [2, 4, 7, 8, 11, 13]
    valid_coprimes = [2, 4, 7, 8, 11, 13]
    print(f"Valid coprime bases to try for N=15: {valid_coprimes}")

    for a in valid_coprimes:
        print(f"\n>> Trying base a = {a}...")
        qc = create_shor_circuit(a, N)
        print(f"   Circuit created with {qc.num_qubits} qubits.")

        counts = run_simulation(qc)
        print("   Simulation completed. Top 5 measurements:")
        for b, count in sorted(counts.items(), key=lambda x: -x[1])[:5]:
            val = int(b, 2)
            phase = val / (2 ** (2 * math.ceil(math.log2(N))))
            print(f"     |{b}> ({val:3d}): count={count:4d}, phase={phase:.4f}")

        found_factor = solve_shor(counts, a, N)
        if found_factor is not None:
            print(
                f"   SUCCESS! Found factor: {found_factor} "
                f"(meaning {found_factor} * {N // found_factor} = {N})"
            )
        else:
            print(f"   FAILED to factor N={N} with base a={a}.")


if __name__ == "__main__":
    main()
