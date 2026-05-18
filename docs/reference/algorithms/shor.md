# Shor's Algorithm

## Overview
Shor's algorithm is a quantum algorithm for integer factorization that runs in polynomial time,
providing an exponential speedup over the best known classical algorithm. It reduces the problem
of factoring $N$ to **Order Finding**: given a co-prime $a$, find the smallest $r > 0$ such that
$a^r \equiv 1 \pmod{N}$. The order $r$ then exposes the prime factors of $N$ through a short
arithmetic computation.

- **Classical Complexity**: $O\!\left(e^{(\log N)^{1/3}(\log\log N)^{2/3}}\right)$ — sub-exponential (GNFS).
- **Quantum Complexity**: $O\!\left((\log N)^3\right)$ — polynomial.

The algorithm demonstrates that a quantum computer can break RSA-class public-key cryptography,
making it one of the most consequential results in quantum computing.

---

## Algorithm Logic

The algorithm combines a classical reduction with a quantum sub-routine for Order Finding.

### 1. Classical Pre-processing
1.  **Trivial checks**: if $N$ is even, return $2$; if $N = a^b$ for integers $a, b \ge 2$,
    return $a$.
2.  **Random base**: pick a random integer $a$ with $1 < a < N$.
3.  **GCD shortcut**: compute $\gcd(a, N)$. If $> 1$, a factor is found immediately without
    quantum processing.
4.  If $\gcd(a, N) = 1$, proceed to the quantum Order Finding sub-routine.

### 2. Quantum Order Finding (QPE Core)
Two registers are prepared:
- **Counting register** ($n = 2\lceil\log_2 N\rceil$ qubits): initialized in $|0\rangle^{\otimes n}$.
- **Target register** ($m = \lceil\log_2 N\rceil$ qubits): initialized in $|1\rangle$.

1.  **Superposition**: apply Hadamard gates to the counting register.
    $$|0\rangle^{\otimes n}|1\rangle \;\xrightarrow{H^{\otimes n}}\; \frac{1}{\sqrt{2^n}}\sum_{x=0}^{2^n-1}|x\rangle|1\rangle$$

2.  **Controlled modular exponentiation**: qubit $i$ of the counting register controls $U^{2^i}$,
    where $U|y\rangle = |ay \bmod N\rangle$:
    $$\frac{1}{\sqrt{2^n}}\sum_{x=0}^{2^n-1}|x\rangle|a^x \bmod N\rangle$$
    The eigenstates of $U$ are $|u_s\rangle = \frac{1}{\sqrt{r}}\sum_{k=0}^{r-1}e^{-2\pi i sk/r}|a^k \bmod N\rangle$
    with eigenvalue $e^{2\pi i s/r}$.

3.  **Inverse QFT (IQFT)**: applied to the counting register, it maps the phase $s/r$ into the
    computational basis.

4.  **Measurement**: the counting register collapses to an integer $m \approx 2^n \cdot s/r$.

### 3. Classical Post-processing
1.  **Phase extraction**: compute $\phi = m / 2^n$.
2.  **Continued fractions**: use `fractions.Fraction(phase).limit_denominator(N)` to find the
    best rational approximation $s/r$; $r$ is the candidate order.
3.  **Order verification**: check $a^r \equiv 1 \pmod{N}$.
4.  **Factor extraction**: if $r$ is even and $a^{r/2} \not\equiv -1 \pmod{N}$:
    $$p, q = \gcd\!\left(a^{r/2} \pm 1,\; N\right)$$
5.  If no non-trivial factor is found, choose a new $a$ and repeat.

---

## API Reference

The module `src.algorithms.shor` provides the implementation.

### `classical_preprocess(N: int) -> tuple[bool, int | None]`
Applies trivial reductions before quantum processing.
- **Parameters**:
  - `N`: the integer to factor.
- **Returns**: `(True, factor)` if a factor was found classically; `(False, None)` otherwise.

### `build_c_u_power(a: int, power: int, N: int) -> QuantumCircuit`
Constructs the hardcoded controlled-$U^{2^{\text{power}}}$ gate for small $N$.
- **Parameters**:
  - `a`: the base integer.
  - `power`: the exponent index $i$ such that the gate implements $U^{2^i}$.
  - `N`: the modulus.
- **Returns**: a `QuantumCircuit` on $1 + \lceil\log_2 N\rceil$ qubits (1 control + target).

### `create_shor_circuit(a: int, N: int) -> QuantumCircuit`
Assembles the full QPE circuit for Order Finding.
- **Parameters**:
  - `a`: the co-prime base chosen during pre-processing.
  - `N`: the integer to factor.
- **Returns**: a `QuantumCircuit` with $n + m$ qubits and $n$ classical bits.

### `run_simulation(qc: QuantumCircuit) -> dict[str, int]`
Executes the circuit on the Aer simulator using `SamplerV2`.
- **Parameters**:
  - `qc`: the circuit returned by `create_shor_circuit`.
- **Returns**: a counts dictionary mapping measured bitstrings to frequencies.

### `solve_shor(counts: dict[str, int], a: int, N: int) -> int | None`
Extracts the order $r$ from measurement results and returns a non-trivial factor.
- **Parameters**:
  - `counts`: output of `run_simulation`.
  - `a`: the base used to build the circuit.
  - `N`: the integer to factor.
- **Returns**: a non-trivial factor of $N$, or `None` if the measurement was inconclusive
  (caller should retry with a different $a$).

---

## Usage Example
```python
import math
from src.algorithms.shor import (
    classical_preprocess,
    create_shor_circuit,
    run_simulation,
    solve_shor,
)

N = 15

# 1. Classical pre-processing
done, factor = classical_preprocess(N)
if done:
    print(f"Classical factor: {factor}")
else:
    # 2. Pick a valid co-prime base
    a = 7  # gcd(7, 15) == 1
    assert math.gcd(a, N) == 1

    # 3. Build and run the QPE circuit
    qc = create_shor_circuit(a, N)
    counts = run_simulation(qc)

    # 4. Extract factor (retry with a different 'a' if None)
    factor = solve_shor(counts, a, N)
    print(f"Factors of {N}: {factor} and {N // factor}")
    # Expected: Factors of 15: 3 and 5  (or 5 and 3)
```

## Implementation Details
- **Module**: [`src/algorithms/shor.py`](../../../src/algorithms/shor.py)
- **Test Suite**: [`tests/test_shor.py`](../../../tests/test_shor.py)
- **Specification**: [`docs/system/specs/08-shor_algorithm.md`](../../system/specs/08-shor_algorithm.md)
