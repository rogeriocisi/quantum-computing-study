# Variational Quantum Classifier (VQC)

## Overview
Quantum Machine Learning (QML) explores the use of quantum circuits as "Quantum Neural Networks". The **Variational Quantum Classifier (VQC)** is a supervised learning model that uses a parametrized circuit to map input features to predicted labels.

This implementation uses **PennyLane** for automatic differentiation and gradient-based optimization.

---

## Technical Details

### Model Components
1.  **Data Encoding (Embedding)**: Classical data (vectors) is mapped to quantum states. We use `AngleEmbedding`, which encodes features as rotation angles of gates.
2.  **Variational Ansatz**: A trainable layer (e.g., `StronglyEntanglingLayers`) that undergoes optimization.
3.  **Measurement**: The expectation value of an observable (like `PauliZ`) is measured to produce a prediction.

### Optimization Loop
We use the **Mean Squared Error (MSE)** as the loss function and update parameters using the **Gradient Descent Optimizer**.

---

## API Reference

The module `src.algorithms.qml.qml_vqc` manages the training and evaluation logic.

### `build_vqc(n_qubits: int = 2, n_layers: int = 2) -> (QNode, np.ndarray)`
Sets up the PennyLane device and QNode.
- **Parameters**:
  - `n_qubits`: Input feature dimension (qubits).
  - `n_layers`: Depth of the entangling layers.
- **Returns**: A tuple containing the `QNode` (circuit) and initial random parameters.

### `train_vqc(circuit, params, data, labels, steps=10) -> np.ndarray`
Performs the training loop.
- **Parameters**:
  - `data`: List of feature vectors.
  - `labels`: List of target values (e.g., 1 or -1).
  - `steps`: Number of optimization iterations.
- **Returns**: The optimized parameter array.

---

## Usage Example
```python
from src.algorithms.qml.qml_vqc import build_vqc, train_vqc
import numpy as np

# 1. Initialize circuit
circuit, init_params = build_vqc(n_qubits=2)

# 2. Mock data
data = [np.array([0.5, 0.1])]
labels = [1]

# 3. Train
final_params = train_vqc(circuit, init_params, data, labels, steps=5)
```

## Implementation Details
- **Module**: [`src/algorithms/qml/qml_vqc.py`](../../../../src/algorithms/qml/qml_vqc.py)
- **Test Suite**: [`tests/test_qml_vqc.py`](../../../../tests/test_qml_vqc.py)
