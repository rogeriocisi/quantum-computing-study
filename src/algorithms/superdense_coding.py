import os
from typing import Dict
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for headless environments


def create_superdense_circuit(message: str) -> QuantumCircuit:
    """Creates a quantum superdense coding circuit.

    Args:
        message (str): The 2-bit classical message to send ('00', '01', '10', or '11').

    Returns:
        QuantumCircuit: The superdense coding circuit.
    """
    if message not in ["00", "01", "10", "11"]:
        raise ValueError("Message must be one of '00', '01', '10', '11'")

    qc = QuantumCircuit(2)

    # 1. Create Bell pair (shared between Alice and Bob)
    # This is the "pre-shared resource"
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    # 2. Alice's encoding
    # Alice applies gates to her qubit (0) based on the message
    # In Qiskit's bit ordering, for message "m1m0":
    # - If m0 == '1', Bob should measure q0=1. This requires Alice to apply Z.
    # - If m1 == '1', Bob should measure q1=1. This requires Alice to apply X.

    if message[1] == "1":  # m0
        qc.z(0)
    if message[0] == "1":  # m1
        qc.x(0)
    qc.barrier()

    # 3. Alice sends her qubit to Bob
    # (Simulated by Bob now having access to both qubits 0 and 1)

    # 4. Bob's decoding
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()

    # 5. Bob measures
    qc.measure_all()

    return qc


def run_simulation(qc: QuantumCircuit, message: str) -> Dict[str, int]:
    """Runs the superdense coding circuit on a local AerSimulator.

    Args:
        qc: The QuantumCircuit to simulate.
        message: The original message for display purposes.

    Returns:
        Dict[str, int]: The measurement counts.
    """
    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)

    # Visualize the circuit (saved as an image)
    print(f"Drawing the circuit for message '{message}'...")
    qc.draw(output="mpl", filename=f"outputs/superdense_circuit_{message}.png")

    # Run the simulation using SamplerV2
    sim = AerSimulator()
    sampler = SamplerV2()
    tqc = transpile(qc, sim)
    job = sampler.run([(tqc, None, 1024)])
    result = job.result()

    # Get the counts from the 'meas' register (added by measure_all)
    counts = result[0].data.meas.get_counts()
    print(f"Results for message '{message}': {counts}")

    # Visualize the histogram (saved as an image)
    plot_histogram(counts)
    plt.savefig(f"outputs/superdense_histogram_{message}.png")
    return counts


def main() -> None:
    """Main execution flow for all 4 possible messages."""
    messages = ["00", "01", "10", "11"]

    for msg in messages:
        print(f"\n--- Superdense Coding: Sending '{msg}' ---")
        qc = create_superdense_circuit(msg)
        run_simulation(qc, msg)

    print("\nSimulation complete. Images generated in 'outputs/'.")


if __name__ == "__main__":
    main()
