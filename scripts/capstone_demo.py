"""
Capstone Demo Execution: Local Simulation & Cloud Validation.

This module validates the quantum development environment by executing three fundamental steps:
1. Create a Quantum Circuit: Builds a 3-qubit maximally entangled state (GHZ State).
2. Run a Local Simulation: Uses AerSimulator on the local processor.
3. Validate Cloud Connection: Submits to IBM Quantum real hardware (via Qiskit Runtime V2).

Usage:
    $ python scripts/capstone_demo.py          # Local simulation only (default)
    $ python scripts/capstone_demo.py --cloud  # Submit job to real IBM Quantum hardware
"""

import argparse
import os
from dotenv import load_dotenv
from qiskit import QuantumCircuit
from typing import Dict, Optional

# Load environment variables from .env file
load_dotenv()

try:
    from qiskit_aer import AerSimulator
except Exception:
    AerSimulator = None


def build_demo_circuit() -> QuantumCircuit:
    """Simple demo circuit used in capstone pipeline.

    Returns:
        QuantumCircuit: A 3-qubit entangled state.
    """
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)
    qc.measure_all()
    return qc


def run_local(circuit: QuantumCircuit) -> Optional[Dict[str, int]]:
    """Run on local AerSimulator if available.

    Args:
        circuit: The circuit to run.

    Returns:
        Optional[Dict[str, int]]: The measurement counts or None if Aer is missing.
    """
    if AerSimulator:
        sim = AerSimulator()
        result = sim.run(circuit).result()
        counts = result.get_counts()
        print("Local counts:", counts)
        return counts
    else:
        print("AerSimulator not available. Circuit built.")
        return None


def run_ibm_runtime(circuit: QuantumCircuit) -> None:
    """Submit the circuit to IBM Quantum real hardware or simulator.

    Args:
        circuit: The circuit to submit to the cloud.
    """
    api_token = os.getenv("IBM_QUANTUM_TOKEN", "")
    if not api_token:
        print("IBM token not set. Please check your .env file.")
        return

    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
    except ImportError:
        print("qiskit-ibm-runtime not installed. Run: pip install qiskit-ibm-runtime")
        return

    print("\nConnecting to IBM Quantum...")
    try:
        service = QiskitRuntimeService(channel="ibm_quantum", token=api_token)

        # Let's pick the least busy backend
        print("Finding the least busy operational backend...")
        backend = service.least_busy(simulator=False, operational=True)
        print(f"Submitting job to real hardware: {backend.name}")

        # Qiskit 1.x/2.x SamplerV2 execution
        sampler = SamplerV2(mode=backend)
        job = sampler.run([circuit])
        print(f"Job submitted successfully! Job ID: {job.job_id()}")
        print("Check progress at: https://quantum.ibm.com/jobs")

        print("Waiting for results (this may take time depending on queue)...")
        result = job.result()

        # SamplerV2 returns PubResult, extract counts
        pub_result = result[0]
        counts = pub_result.data.meas.get_counts()
        print("IBM Quantum Results:", counts)
    except Exception as e:
        print(f"Error connecting to or running on IBM Quantum: {e}")


def main() -> None:
    """Main execution flow for Capstone demo with CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Capstone demo runner: local simulation and optional cloud execution."
    )
    parser.add_argument(
        "--cloud",
        action="store_true",
        help="Execute the circuit on IBM Quantum cloud (real hardware).",
    )
    args = parser.parse_args()

    qc = build_demo_circuit()

    print("--- Running Local Simulation ---")
    run_local(qc)

    if args.cloud:
        print("\n--- Running on IBM Quantum Cloud ---")
        run_ibm_runtime(qc)
    else:
        print("\nCloud execution skipped. Run with '--cloud' to submit to IBM.")


if __name__ == "__main__":
    main()
