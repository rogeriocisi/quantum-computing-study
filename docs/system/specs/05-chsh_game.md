# SPEC-05: CHSH Game (Bell's Inequality Test)

## 1. Overview
The CHSH (Clauser-Horne-Shimony-Holt) game is a experimental framework to test **Bell's Inequality**. It demonstrates that quantum mechanics allows for correlations between distant particles that cannot be explained by any local hidden variable theory.

It is often described as a game where two parties (Alice and Bob) cooperate to win, but are unable to communicate once the game starts.

## 2. Game Rules
1.  **Inputs**: A referee gives Alice a bit $x \in \{0, 1\}$ and Bob a bit $y \in \{0, 1\}$. These bits are chosen uniformly and at random.
2.  **Constraint**: Alice and Bob cannot communicate.
3.  **Outputs**: Alice outputs a bit $a \in \{0, 1\}$ and Bob outputs a bit $b \in \{0, 1\}$.
4.  **Winning Condition**: Alice and Bob win if:
    $$a \oplus b = x \cdot y$$
    - If $x=0, y=0 \implies a=b$
    - If $x=0, y=1 \implies a=b$
    - If $x=1, y=0 \implies a=b$
    - If $x=1, y=1 \implies a \neq b$

## 3. Theoretical Bounds
-   **Classical Limit (Local Realism)**: No classical strategy can win with a probability greater than **75%** ($3/4$).
-   **Quantum Limit (Tsirelson's Bound)**: By sharing an entangled Bell pair and choosing optimal measurement bases, Alice and Bob can win with a probability of **~85.4%** ($\cos^2(\pi/8)$).

## 4. Implementation Strategy

### 4.1. Quantum Strategy
1.  **Entanglement**: Alice and Bob share a Bell state $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$.
2.  **Alice's Measurement Bases**:
    - If $x=0$, measure in the $Z$ basis ($0$ rad).
    - If $x=1$, measure in the $X$ basis ($\pi/2$ rad).
3.  **Bob's Measurement Bases**:
    - If $y=0$, measure in the $W$ basis ($\pi/4$ rad).
    - If $y=1$, measure in the $V$ basis ($-\pi/4$ rad).

### 4.2. Code Structure
-   **File**: `src/algorithms/chsh_game.py`
-   **Functions**:
    - `create_chsh_circuit(x: int, y: int) -> QuantumCircuit`: Builds the circuit for a specific input pair.
    - `simulate_chsh_game(trials: int = 1000) -> Dict`: Runs multiple trials for all $(x, y)$ combinations.
    - `calculate_win_rate(results: Dict) -> float`: Computes the overall winning probability.

## 5. Success Criteria
-   The implementation must show a winning probability significantly exceeding 75% (ideally approaching 85%).
-   Full documentation in `docs/reference/algorithms/chsh_game.md`.
-   Integration into the `README.md`.
