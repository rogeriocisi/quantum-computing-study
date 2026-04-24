import os
from typing import Dict
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Non-interactive backend for headless environments


def create_bell_state() -> QuantumCircuit:
    """Creates a 2-qubit Bell state (|00> + |11>) / sqrt(2).

    Returns:
        QuantumCircuit: The entangled circuit.
    """
    # 1. Create a quantum circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)

    # 2. Apply a Hadamard gate on qubit 0 to create superposition
    qc.h(0)

    # 3. Apply a CNOT gate with control on qubit 0 and target on qubit 1
    # This creates entanglement
    qc.cx(0, 1)

    # 4. Measure the qubits and store results in classical bits
    qc.measure([0, 1], [0, 1])
    return qc


def run_simulation(qc: QuantumCircuit) -> Dict[str, int]:
    """Runs the circuit on a local AerSimulator.

    Args:
        qc: The QuantumCircuit to simulate.

    Returns:
        Dict[str, int]: The measurement counts.
    """
    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)

    # 5. Visualize the circuit (saved as an image)
    print("Drawing the circuit...")
    qc.draw(output="mpl", filename="outputs/bell_circuit.png")

    # 6. Run the simulation using AerSimulator
    backend = AerSimulator()
    job = backend.run(qc, shots=1024)
    result = job.result()

    # 7. Get the counts of the results
    counts = result.get_counts(qc)
    print(f"Results (counts): {counts}")

    # 8. Visualize the histogram (saved as an image)
    plot_histogram(counts)
    plt.savefig("outputs/bell_histogram.png")
    print("Simulation complete. Images generated in 'outputs/'.")
    return counts


def main() -> None:
    """Main execution flow."""
    bell_circuit = create_bell_state()
    run_simulation(bell_circuit)


if __name__ == "__main__":
    main()
