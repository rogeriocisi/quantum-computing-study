# Testing Strategy for Quantum Algorithms

## Overview
This project uses **[pytest](https://docs.pytest.org/)** as its primary testing framework. Testing quantum circuits requires a combination of structural checks (verifying the "blueprint") and functional verification via local simulation.

---

## How to Run the Tests

### 1. Activate the Environment
Always ensure your virtual environment is active before running tests:
```powershell
.\quantum_env\Scripts\activate
```

### 2. Execute all Tests
Run the entire suite from the project root:
```powershell
python -m pytest
```

### 3. Verbose Execution
For more details on which specific tests are running:
```powershell
python -m pytest -v
```

### 4. Target a Specific Module
To run tests only for a specific algorithm (e.g., the VBE Adder):
```powershell
python -m pytest tests/test_vbe_adder.py
```

---

## Test Architecture

### 1. Structural Verification
We verify that the `QuantumCircuit` objects have the correct:
- **Qubit Count**: Ensuring ancillas are correctly allocated.
- **Classical Bits**: Verifying measurement registers.
- **Gate Composition**: Checking if the required gates (e.g., Toffoli, Hadamard) are present in the circuit data.

### 2. Simulation & Correctness
We use `qiskit-aer` (`AerSimulator`) to execute circuits locally.
- **Deterministic Outcomes**: For algorithms like the VBE Adder, we assert that 100% of the shots yield the correct binary result.
- **Probabilistic Outcomes**: For states like the Bell State, we verify that the distribution of results is within a statistical range (e.g., 40-60% for a 50/50 state).

### 3. Reversibility
Since many quantum operations must be reversible, we test if applying a gate (like `CARRY`) followed by its inverse (`CARRY†`) results in an identity operation, restoring the qubits to their initial state.

---

## Structuring New Tests
When adding a new algorithm, create a file in `tests/test_<name>.py` following this structure:

```python
import pytest
from src.algorithms.my_new_algo import build_circuit

def test_circuit_structure():
    qc = build_circuit()
    assert qc.num_qubits == 2

def test_execution_correctness():
    # ... logic to run simulation and decode result
    assert result == expected_value
```

### Shared Fixtures
Common components like seeded random generators are stored in `tests/conftest.py`. You can use them in any test by adding the fixture name as an argument:
```python
def test_with_random_data(rng):
    data = rng.random(10)
    # ...
```

---

## Troubleshooting

### `_tkinter.TclError` (Headless Environments)
If tests fail because Matplotlib tries to open a GUI window, ensure the backend is set to `Agg` in the source file:
```python
import matplotlib
matplotlib.use('Agg')
```

### Performance
Quantum simulations are CPU and memory-intensive. For large circuits ($n > 25$), tests may run slowly or fail due to memory limits. Keep test cases within the 1-10 qubit range for local verification.
