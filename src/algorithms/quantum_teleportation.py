import os
from typing import Dict
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use("Agg")  # Non-interactive backend for headless environments


def create_teleportation_circuit(theta: float = np.pi / 3) -> QuantumCircuit:
    """Creates a quantum teleportation circuit.

    The circuit teleports a single qubit state prepared by an Rx rotation
    from Alice to Bob. Alice and Bob share a Bell pair.

    Args:
        theta (float): The angle for the initial Rx rotation to prepare
                       the state to be teleported. Defaults to pi/3.

    Returns:
        QuantumCircuit: The quantum circuit implementing teleportation.
    """
    # Create registers
    qr = QuantumRegister(3, name="q")
    crz = ClassicalRegister(
        1, name="crz"
    )  # Alice's measurement of q0 (determines Z gate)
    crx = ClassicalRegister(
        1, name="crx"
    )  # Alice's measurement of q1 (determines X gate)
    cr_result = ClassicalRegister(
        1, name="result"
    )  # Bob's measurement for verification

    qc = QuantumCircuit(qr, crz, crx, cr_result)

    # 1. State preparation (Alice's payload on q0)
    # We prepare a state to teleport by applying an Rx rotation
    qc.rx(theta, 0)
    qc.barrier()

    # 2. Create Bell pair (shared between Alice's q1 and Bob's q2)
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()

    # 3. Alice's operations on her qubits (q0, q1)
    qc.cx(0, 1)
    qc.h(0)
    qc.barrier()

    # 4. Alice measures her qubits
    qc.measure(0, crz)
    qc.measure(1, crx)
    qc.barrier()

    # 5. Bob's conditional operations based on Alice's classical bits
    with qc.if_test((crx, 1)):
        qc.x(2)
    with qc.if_test((crz, 1)):
        qc.z(2)
    qc.barrier()

    # 6. Verification
    # Bob applies the inverse of the state preparation to check if he gets |0>
    qc.rx(-theta, 2)

    # Bob measures his qubit
    qc.measure(2, cr_result)

    return qc


def run_simulation(qc: QuantumCircuit) -> Dict[str, int]:
    """Runs the teleportation circuit on a local AerSimulator.

    Args:
        qc: The QuantumCircuit to simulate.

    Returns:
        Dict[str, int]: The measurement counts.
    """
    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)

    # Visualize the circuit (saved as an image)
    print("Drawing the circuit...")
    qc.draw(output="mpl", filename="outputs/teleportation_circuit.png")

    # Run the simulation using SamplerV2
    sim = AerSimulator()
    sampler = SamplerV2()
    tqc = transpile(qc, sim)
    job = sampler.run([(tqc, None, 1024)])
    result = job.result()

    # Get the counts from the 'result' classical register
    # (Bob's verification qubit)
    counts = result[0].data.result.get_counts()
    print(f"Results (counts): {counts}")

    # Visualize the histogram (saved as an image)
    plot_histogram(counts)
    plt.savefig("outputs/teleportation_histogram.png")
    print("Simulation complete. Images generated in 'outputs/'.")
    return counts


def main() -> None:
    """Main execution flow."""
    # Create the teleportation circuit
    # The state prepared is Rx(pi/3)|0>
    teleport_circuit = create_teleportation_circuit(theta=np.pi / 3)

    # Run the simulation
    run_simulation(teleport_circuit)


if __name__ == "__main__":
    main()
