# Project Setup & Developer Reminders

## 1. Virtual Environment Activation
Always activate the virtual environment before running scripts or installing dependencies.

### Windows PowerShell (Default in VS Code)
```powershell
.\quantum_env\Scripts\Activate.ps1
```
*Note: If you get an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` first.*

### Command Prompt (CMD)
```cmd
quantum_env\Scripts\activate.bat
```

### Git Bash
```bash
source quantum_env/Scripts/activate
```

### Rebuilding the Environment (If moved/broken)
If you move the project folder, executables like `pip` will break. Rebuild it using:
```powershell
Remove-Item -Recurse -Force .\quantum_env
python -m venv quantum_env
```

---

## 2. API Keys & Secrets
Never hardcode sensitive information like API tokens in your scripts.

* **Where to store:** In a `.env` file at the root of the repository.
* **Format:** `KEY=VALUE` (e.g., `IBM_QUANTUM_TOKEN=your_token_here`).
* **Template:** Use [.env.example](file:///c:/Antigravity/quantum-computing-study/.env.example) as a base.
* **Loading in Python:**
  ```python
  import os
  from dotenv import load_dotenv

  load_dotenv()
  api_token = os.getenv("IBM_QUANTUM_TOKEN")
  ```

---

## 3. Debugging & Quality Assurance

### Running Tests
Execute tests with coverage reporting:
```bash
pytest --cov=src
```

### Code Formatting & Linting
Keep the codebase clean:
```bash
# Format code
black .

# Check for style issues
flake8
```

### Qiskit Visualization Tips
* To draw quantum circuits in text mode: `print(circuit.draw())`
* To draw using Matplotlib (prettier): `circuit.draw('mpl')`
* If visualization fails, ensure `matplotlib` and `pylatexenc` are installed in your environment.
