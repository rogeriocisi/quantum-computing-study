# CHSH Game (Bell's Theorem Test)

## Overview
The CHSH (Clauser-Horne-Shimony-Holt) game is a physical experiment reformulated as a non-local game. It provides a definitive proof that quantum mechanics violates **Local Realism** (the idea that physical properties exist independently of measurement and that information cannot travel faster than light).

In this game, Alice and Bob collaborate to win against a referee, but they are prevented from communicating after receiving their inputs.

---

## Technical Details

### The Winning Condition
Given inputs $x, y \in \{0, 1\}$ and outputs $a, b \in \{0, 1\}$, the team wins if:
$$a \oplus b = x \cdot y$$

This means:
- If $(x,y)$ is $(0,0), (0,1),$ or $(1,0)$, they win if their outputs are the same ($a=b$).
- If $(x,y)$ is $(1,1)$, they win if their outputs are different ($a \neq b$).

### The Quantum Strategy
By sharing an entangled Bell pair $|\Phi^+\rangle$, Alice and Bob can correlate their measurement outcomes. The choice of rotation angles (measurement bases) is critical:

| Party | Input | Rotation | Basis |
| :--- | :--- | :--- | :--- |
| **Alice** | $x=0$ | $0$ | $Z$ |
| **Alice** | $x=1$ | $\pi/2$ | $X$ |
| **Bob** | $y=0$ | $\pi/4$ | $W$ |
| **Bob** | $y=1$ | $-\pi/4$ | $V$ |

---

## API Reference

The module `src.algorithms.chsh_game` provides functions to simulate and analyze the game.

### `create_chsh_circuit(x: int, y: int) -> QuantumCircuit`
Builds the quantum circuit for a specific input pair $(x, y)$.
- **Returns**: A `qiskit.QuantumCircuit` ready for execution.

### `run_simulation(trials_per_config: int = 250) -> Dict`
Executes the game for all four possible input combinations.
- **Returns**: A nested dictionary containing counts for each configuration.

### `analyze_results(results: Dict) -> float`
Processes the simulation counts, calculates the win rate for each configuration, and returns the overall probability.

---

## Usage Example

```python
from src.algorithms.chsh_game import run_simulation, analyze_results

# Run 1000 trials for each input combination
results = run_simulation(trials_per_config=1000)

# Print statistics and verify Bell inequality violation
win_rate = analyze_results(results)

if win_rate > 0.75:
    print("Success: Bell's Inequality violated!")
```

## Implementation Details
- **Module**: [`src/algorithms/chsh_game.py`](../../../src/algorithms/chsh_game.py)
- **Foundations Used**: `src.utils.foundations.apply_bell_pair`
- **Theory Phase**: Phase 2 (Quantum Mechanics & Algorithms I)
