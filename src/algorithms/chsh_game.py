"""
CHSH Game (Bell's Inequality Test)
==================================
This module implements the CHSH game, a proof of Bell's Theorem.
Alice and Bob share an entangled pair and use specific measurement
bases to achieve a winning probability (~85%) that exceeds the
classical limit (75%).
"""

from typing import Dict, Tuple
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from src.utils.foundations import apply_bell_pair


def create_chsh_circuit(x: int, y: int) -> QuantumCircuit:
    """Creates a CHSH game circuit for inputs x and y.

    Args:
        x: Alice's input bit (0 or 1).
        y: Bob's input bit (0 or 1).

    Returns:
        QuantumCircuit: The circuit prepared for measurement.
    """
    # 2 qubits, 2 classical bits
    qc = QuantumCircuit(2, 2)

    # 1. Prepare entangled Bell state |Phi+> = (|00> + |11>) / sqrt(2)
    # Alice has qubit 0, Bob has qubit 1
    apply_bell_pair(qc, 0, 1)
    qc.barrier()

    # 2. Alice's measurement basis choice (based on x)
    # x=0: Z-basis (0 rad) -> no rotation needed
    # x=1: X-basis (pi/2 rad) -> Ry(pi/2)
    if x == 1:
        qc.ry(np.pi / 2, 0)

    # 3. Bob's measurement basis choice (based on y)
    # y=0: W-basis (pi/4 rad) -> Ry(pi/4)
    # y=1: V-basis (-pi/4 rad) -> Ry(-pi/4)
    if y == 0:
        qc.ry(np.pi / 4, 1)
    else:
        qc.ry(-np.pi / 4, 1)

    qc.barrier()

    # 4. Measure
    qc.measure([0, 1], [0, 1])

    return qc


def run_simulation(
    trials_per_config: int = 250,
) -> Dict[Tuple[int, int], Dict[str, int]]:
    """Simulates the CHSH game for all 4 input combinations (x, y).

    Args:
        trials_per_config: Number of shots for each (x, y) pair.

    Returns:
        Dict: A mapping of (x, y) to measurement counts.
    """
    simulator = AerSimulator()
    sampler = SamplerV2()
    results = {}

    for x in [0, 1]:
        for y in [0, 1]:
            qc = create_chsh_circuit(x, y)
            tqc = transpile(qc, simulator)
            job = sampler.run([(tqc, None, trials_per_config)])
            result = job.result()

            # Extract counts from first classical register
            creg_name = qc.cregs[0].name
            counts = result[0].data[creg_name].get_counts()
            results[(x, y)] = counts

    return results


def analyze_results(results: Dict[Tuple[int, int], Dict[str, int]]) -> float:
    """Calculates the overall winning probability and prints detailed stats.

    Winning condition: a ^ b == x * y

    Returns:
        float: Overall win rate.
    """
    total_wins = 0
    total_trials = 0

    print("\n--- CHSH Game Results ---")
    print(
        f"{'Inputs (x,y)':<12} | {'Winning Condition':<20} | {'Wins':<8} | {'Win Rate':<8}"
    )
    print("-" * 55)

    for (x, y), counts in results.items():
        wins_for_config = 0
        trials_for_config = sum(counts.values())
        target_xor = x * y

        for bitstring, count in counts.items():
            # bitstring is "ba" in Qiskit (b=q1, a=q0)
            a = int(bitstring[1])
            b = int(bitstring[0])

            if (a ^ b) == target_xor:
                wins_for_config += count

        win_rate = wins_for_config / trials_for_config
        total_wins += wins_for_config
        total_trials += trials_for_config

        print(
            f"({x}, {y}){' ':<8} | "
            f"a ^ b == {target_xor}{' ':<11} | "
            f"{wins_for_config:<8} | "
            f"{win_rate:.2%}"
        )

    overall_win_rate = total_wins / total_trials
    print("-" * 55)
    print(f"OVERALL WIN RATE: {overall_win_rate:.2%}")
    print("Classical Limit: 75.00%")
    print("Quantum Theoretical Bound: ~85.36%")

    return overall_win_rate


def main() -> None:
    """Main execution flow."""
    results = run_simulation(trials_per_config=1000)
    analyze_results(results)


if __name__ == "__main__":
    main()
