# Source Code Structure 📂

This directory follows a professional modular structure for Quantum Software Engineering.

## 📁 Directory Map

- **`algorithms/`**: Standard quantum algorithms (Deutsch-Jozsa, Simon, Grover, Shor).
- **`qml/`**: Quantum Machine Learning experiments using **PennyLane**.
- **`optimization/`**: Hybrid variational algorithms like **VQE** and **QAOA**.
- **`utils/`**: Helper functions for noise mitigation (NISQ), visualization, and data processing.
- **`capstone_demo.py`**: The main entry point for the hybrid pipeline demonstration.

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
