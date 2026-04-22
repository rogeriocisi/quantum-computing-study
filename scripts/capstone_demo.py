"""
Capstone demo runner: local sim + optional IBM runtime hook.
Usage: fill IBM API token and backend names to enable cloud runs.
"""
from typing import Dict, Optional
import os
from qiskit import QuantumCircuit
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
    qc.h(0); qc.cx(0,1); qc.cx(1,2)
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
    """Placeholder for IBM runtime execution.
    
    Args:
        circuit: The circuit to submit to the cloud.
    """
    api_token = os.getenv("IBM_QUANTUM_TOKEN", "")
    if not api_token:
        print("IBM token not set. Skipping cloud run.")
        return
    print("Would submit to IBM runtime with token present.")

def main() -> None:
    """Main execution flow for Capstone demo."""
    qc = build_demo_circuit()
    run_local(qc)
    run_ibm_runtime(qc)

if __name__ == "__main__":
    main()
