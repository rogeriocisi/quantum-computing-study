# SPEC-08: Shor's Algorithm

## 1. Overview
Shor's algorithm is a quantum algorithm for integer factorization running in polynomial time
$O((\log N)^3)$, providing an exponential speedup over the best known classical algorithm (General
Number Field Sieve). It reduces factorization to **Order Finding**, a problem solved efficiently
by Quantum Phase Estimation (QPE) combined with the Quantum Fourier Transform (QFT).

## 2. Problem Statement
- **Input**: A composite integer $N$ (odd, not a perfect power).
- **Goal**: Find non-trivial factors $p, q$ such that $p \cdot q = N$.
- **Classical Complexity**: Sub-exponential $O(e^{(\log N)^{1/3}})$.
- **Quantum Complexity**: $O((\log N)^3)$ — polynomial.

## 3. Algorithm Flow

```mermaid
graph TD
    A[Input: Integer N] --> B{N even or N = a^b?}
    B -- Yes --> C[Trivial factor found]
    B -- No --> D[Pick random a, 1 < a < N]
    D --> E{GCD(a, N) > 1?}
    E -- Yes --> F[Factor found: GCD(a, N)]
    E -- No --> G[Quantum: Order Finding]

    subgraph Quantum Processing
    G --> H[Prepare: H^n on counting reg, |1> on target reg]
    H --> I[Controlled Modular Exponentiation: |x>|y> -> |x>|y·a^x mod N>]
    I --> J[IQFT on counting register]
    J --> K[Measure: obtain phase approx s/r]
    end

    K --> L[Classical Post-processing]

    subgraph Classical Post-processing
    L --> M[Continued fractions: extract r from s/r]
    M --> N{r even AND a^(r/2) != -1 mod N?}
    N -- No --> D
    N -- Yes --> O[Compute: GCD(a^(r/2) +/- 1, N)]
    O --> P[Success: factors of N found]
    end
```

## 4. Classical Subalgorithms

### 4.1. Trivial Reductions
Before invoking the quantum core, perform cheap classical checks:
- **Parity**: if $N$ is even, return $2$.
- **Perfect Power**: check if $N = a^b$ for $a \ge 2, b \ge 2$; if so, return $a$.

### 4.2. GCD Check
Choose random $a$ with $1 < a < N$ and compute $\gcd(a, N)$ via the Euclidean algorithm
(`math.gcd`). If $\gcd(a, N) > 1$, return the factor. Otherwise $a$ and $N$ are coprime;
proceed to Order Finding.

### 4.3. Factoring via Order Finding
Find the smallest $r > 0$ (the **order** of $a$ mod $N$) such that $a^r \equiv 1 \pmod{N}$.
Given an even $r$:
$$(a^{r/2} - 1)(a^{r/2} + 1) \equiv 0 \pmod{N}$$
If $a^{r/2} \not\equiv -1 \pmod{N}$, at least one prime factor of $N$ is shared with
$a^{r/2} \pm 1$:
$$p, q = \gcd(a^{r/2} \pm 1,\; N)$$

### 4.4. Continued Fractions
Measurement yields $m \approx 2^n \cdot \frac{s}{r}$, so the measured phase is:
$$\phi \approx \frac{s}{r}$$
Apply the continued fractions algorithm (`fractions.Fraction(phase).limit_denominator(N)`)
to recover $r$ as the denominator. Verify the candidate by testing $a^r \equiv 1 \pmod{N}$.

## 5. Quantum Subalgorithms

The circuit requires two registers:
1. **Counting register ($n$ qubits)**: controls modular operations; stores the phase after IQFT.
   Size: $n = 2\lceil\log_2 N\rceil$ (satisfies $N^2 \le 2^n < 2N^2$).
2. **Target register ($m$ qubits)**: holds the iterative modular multiplications.
   Size: $m = \lceil\log_2 N\rceil$.

### 5.1. Quantum Phase Estimation (QPE)
QPE extracts the phase (eigenvalue) of the unitary operator:
$$U|y\rangle = |ay \pmod{N}\rangle$$
The eigenstates of $U$ are:
$$|u_s\rangle = \frac{1}{\sqrt{r}} \sum_{k=0}^{r-1} e^{-\frac{2\pi i s k}{r}} |a^k \pmod{N}\rangle, \quad 0 \le s \le r-1$$
with eigenvalue $e^{2\pi i s/r}$. The computational state $|1\rangle$ decomposes as an equal
superposition of all eigenstates:
$$|1\rangle = \frac{1}{\sqrt{r}} \sum_{s=0}^{r-1} |u_s\rangle$$
Applying QPE to $|0\rangle^{\otimes n}|1\rangle$ produces, after measurement, a value $s/r$
with high probability.

### 5.2. Controlled Modular Exponentiation
With the counting register in uniform superposition, the controlled-$U^x$ action gives:
$$\frac{1}{\sqrt{2^n}} \sum_{x=0}^{2^n-1} |x\rangle |1\rangle
\;\xrightarrow{C\text{-}U^x}\;
\frac{1}{\sqrt{2^n}} \sum_{x=0}^{2^n-1} |x\rangle |a^x \pmod{N}\rangle$$
Each qubit $i$ in the counting register controls $U^{2^i}$, applied in sequence.

For small $N$ proof-of-concept (e.g. $N=15, 21$), use **hardcoded permutation gates**
(`UnitaryGate` on the target register) specific to each value of $a$. Avoid constructing
full unitary matrices for large $N$; the memory cost grows exponentially.

### 5.3. Inverse Quantum Fourier Transform (IQFT)
After controlled exponentiation, the counting register holds:
$$\frac{1}{\sqrt{r}} \sum_{s=0}^{r-1}
\left( \frac{1}{\sqrt{2^n}} \sum_{x=0}^{2^n-1} e^{\frac{2\pi i s x}{r}} |x\rangle \right) |u_s\rangle$$
Applying IQFT to the counting register maps each inner sum to $|\tilde{\phi}_s\rangle$, a
binary approximation of $s/r$. Measurement collapses to a single integer $m \approx 2^n \cdot s/r$.

Use `QFTGate(n_count).inverse()` from `qiskit.circuit.library`.

## 6. Implementation Guidelines

### 6.1. File Structure
- **Implementation**: `src/algorithms/shor.py`
- **Tests**: `tests/test_shor.py`

### 6.2. Key Functions
```
classical_preprocess(N: int) -> tuple[bool, int | None]
    Trivial checks (parity, perfect power, GCD). Returns (done, factor).

build_c_u_power(a: int, power: int, N: int) -> QuantumCircuit
    Hardcoded controlled-U^{2^power} gate for small N. Returns a 1+m qubit circuit.

create_shor_circuit(a: int, N: int) -> QuantumCircuit
    Assembles the full QPE circuit: H on counting reg, |1> on target,
    controlled-U applications, and IQFT.

run_simulation(qc: QuantumCircuit) -> dict[str, int]
    Executes via SamplerV2 and returns the counts dictionary.

solve_shor(counts: dict[str, int], a: int, N: int) -> int | None
    Extracts the measured phase, applies continued fractions, computes the order r,
    and returns a non-trivial factor or None (retry needed).
```

### 6.3. Qiskit Reference Implementation
```python
import math
from fractions import Fraction
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFTGate
from qiskit_aer.primitives import SamplerV2


def create_shor_circuit(a: int, N: int) -> QuantumCircuit:
    """Builds the Order Finding (QPE) circuit for Shor's algorithm."""
    n_count = 2 * math.ceil(math.log2(N))   # counting register size
    m = math.ceil(math.log2(N))              # target register size

    count_reg = QuantumRegister(n_count, name="count")
    target_reg = QuantumRegister(m, name="target")
    class_reg = ClassicalRegister(n_count, name="c")
    qc = QuantumCircuit(count_reg, target_reg, class_reg)

    # Initialise: counting in superposition, target in |1>
    qc.h(count_reg)
    qc.x(target_reg[0])

    # Controlled-U^{2^i} for each counting qubit
    for i in range(n_count):
        c_u = build_c_u_power(a, i, N)
        qc.append(c_u, [count_reg[i]] + list(target_reg))

    # Inverse QFT on counting register
    iqft_gate = QFTGate(n_count).inverse()
    qc.append(iqft_gate, count_reg)

    qc.measure(count_reg, class_reg)
    return qc
```


def run_simulation(qc: QuantumCircuit) -> dict[str, int]:
    """Executes the circuit using SamplerV2 and returns counts."""
    sampler = SamplerV2()
    job = sampler.run([qc], shots=2048)
    result = job.result()
    return result[0].data.c.get_counts()


def solve_shor(counts: dict[str, int], a: int, N: int) -> int | None:
    """Extracts order r from measurement counts and returns a factor or None."""
    n_count = 2 * math.ceil(math.log2(N))
    for bitstring, _ in sorted(counts.items(), key=lambda x: -x[1]):
        phase = int(bitstring, 2) / 2**n_count
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator
        if r == 0 or pow(a, r, N) != 1:
            continue
        if r % 2 == 0 and pow(a, r // 2, N) != N - 1:
            for offset in (1, -1):
                candidate = math.gcd(pow(a, r // 2, N) + offset, N)
                if 1 < candidate < N:
                    return candidate
    return None
```

### 6.4. Transpilation Notes
- Use `optimization_level=3` in `transpile` to reduce circuit depth from modular arithmetic.
- For noise-aware simulation (`GenericBackendV2`), enable SABRE routing to handle connectivity
  constraints. Hardcoded oracles for $N \in \{15, 21\}$ keep depth manageable.
- Avoid building full unitary matrices for the exponentiation gate; use structured permutation
  circuits instead.

## 7. Success Criteria
- Factor $N = 15$ correctly for all valid co-prime values of $a$ ($a \in \{2, 4, 7, 8, 11, 13\}$).
- Factor $N = 21$ correctly for at least one valid $a$.
- `solve_shor` returns `None` gracefully when measurement yields an unusable phase (retry logic
  in `main()` handles this).
- Full unit test coverage in `tests/test_shor.py`:
  - `test_classical_preprocess`: validates trivial reductions.
  - `test_build_c_u_power`: verifies gate action $|y\rangle \to |ay \bmod N\rangle$ on
    computational basis states.
  - `test_create_shor_circuit`: checks register sizes and circuit structure.
  - `test_solve_shor`: injects synthetic counts and verifies factor extraction.
  - `test_end_to_end_n15`: full simulation run for $N = 15$.
