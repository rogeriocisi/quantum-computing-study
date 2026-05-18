# Source Code Structure 📂

This directory follows a professional modular structure for Quantum Software Engineering.

## 📁 Directory Map

- **`algorithms/`**: Quantum algorithms and submodules (Deutsch-Jozsa, Simon, Grover, Shor):
  - **`algorithms/optimization/`**: Hybrid variational algorithms like **VQE** and **QAOA**.
  - **`algorithms/qml/`**: Quantum Machine Learning experiments using **PennyLane**.
- **`utils/`**: Helper functions for noise mitigation (NISQ), visualization, and data processing.

> 📌 **Note**: Runnable entry point scripts (e.g., `capstone_demo.py`) live in `../scripts/`, not here. This folder contains only reusable, importable modules.

## 🚀 How to Run

1. Ensure your virtual environment is active:
   - Windows: `..\quantum_env\Scripts\activate`
   - Linux: `source ../quantum_env/bin/activate`
2. Run any module:
   ```bash
   python algorithms/algorithm_base.py
   ```

## 🧪 Testing

Unit tests are located in the `../tests/` directory. Run them using:
```bash
pytest ../tests/
```
