"""
Simon's Algorithm
=================
Implementation of Simon's algorithm for finding a hidden period 's' in a 
two-to-one function. This algorithm provides an exponential speedup 
over classical algorithms and was a precursor to Shor's algorithm.
"""

import numpy as np
from typing import List, Dict, Optional
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2

def build_simon_oracle(s: str) -> QuantumCircuit:
    """
    A simple way to build such an oracle is to:
    1. Copy the input register to the output register: |x>|0> -> |x>|x>.
    2. Choose an index j where s[j] == 1.
    3. For every index i where s[i] == 1, apply CX(j_input, i_output).
    This implements the mapping f(x) = x ^ (x_j * s), which satisfies f(x) = f(x ^ s).
    """
    n = len(s)
    qc = QuantumCircuit(2 * n)
    
    # 1. Copy the input register to the output register
    for i in range(n):
        qc.cx(i, n + i)
    
    # 2. If s is non-zero, create the two-to-one mapping
    if '1' in s:
        # Qiskit bit 0 is the LAST character in the string usually, 
        # but let's just stick to a consistent mapping: bit i <-> s[n-1-i]
        s_bits = [int(b) for b in reversed(s)]
        j = s_bits.index(1)
        
        # Apply CX from input bit j to output bits where s_bits[i] == 1
        for i, val in enumerate(s_bits):
            if val == 1:
                qc.cx(j, n + i)
                
    return qc

def create_simon_circuit(oracle: QuantumCircuit) -> QuantumCircuit:
    """
    Constructs the quantum part of Simon's algorithm.
    """
    n = oracle.num_qubits // 2
    qc = QuantumCircuit(2 * n, n)
    
    # Apply Hadamards to the first register
    qc.h(range(n))
    
    # Apply Oracle
    qc.compose(oracle, inplace=True)
    
    # Apply Hadamards to the first register again
    qc.h(range(n))
    
    # Measure the first register
    qc.measure(range(n), range(n))
    
    return qc

def solve_simon(counts: Dict[str, int], n: int) -> str:
    """
    Classical post-processing for Simon's algorithm.
    Solves the system of linear equations y * s = 0 (mod 2).
    """
    # Get the unique measured bitstrings (y)
    # We only care about non-zero bitstrings usually, but all are valid
    bitstrings = list(counts.keys())
    
    # This is a simplified version of Gaussian elimination over GF(2)
    # to find a non-zero solution s.
    def get_null_space(M):
        rows, cols = M.shape
        pivot_row = 0
        for col in range(cols):
            if pivot_row >= rows: break
            # Find pivot
            pivot = np.argmax(M[pivot_row:, col]) + pivot_row
            if M[pivot, col] == 0: continue
            # Swap
            M[[pivot, pivot_row]] = M[[pivot_row, pivot]]
            # Eliminate
            for r in range(rows):
                if r != pivot_row and M[r, col] == 1:
                    M[r] = (M[r] + M[pivot_row]) % 2
            pivot_row += 1
        return M

    # Build matrix from measurements
    # Convert '010' -> [0, 1, 0]
    matrix = []
    for b in bitstrings:
        matrix.append([int(bit) for bit in b])
    
    M = np.array(matrix)
    if len(M) == 0:
        return '0' * n
        
    M_reduced = get_null_space(M)
    
    # Actually finding the exact 's' from the null space can be complex 
    # for large n. For a simple demonstration, we can iterate through 
    # all possible s (2^n) and check which one satisfies y * s = 0 (mod 2) 
    # for all measured y.
    
    for s_val in range(1, 1 << n):
        s_candidate = format(s_val, f'0{n}b')
        s_arr = np.array([int(bit) for bit in s_candidate])
        
        valid = True
        for b in bitstrings:
            y_arr = np.array([int(bit) for bit in b])
            if np.dot(y_arr, s_arr) % 2 != 0:
                valid = False
                break
        if valid:
            return s_candidate
            
    return '0' * n

def run_simulation(qc: QuantumCircuit) -> Optional[Dict[str, int]]:
    """Runs simulation on AerSimulator using SamplerV2.
    
    Args:
        qc: The quantum circuit to execute.
        
    Returns:
        A dictionary of counts if successful, None otherwise.
    """
    sim = AerSimulator()
    sampler = SamplerV2()
    tqc = transpile(qc, sim)
    job = sampler.run([(tqc, None, 1024)])
    result = job.result()
    
    # Extract counts from the first classical register
    if qc.cregs:
        creg_name = qc.cregs[0].name
        return result[0].data[creg_name].get_counts()
    return None

def main(secret_s: str = "110") -> None:
    n = len(secret_s)
    print(f"--- Simon's Algorithm ---")
    print(f"Secret string s: {secret_s}")
    
    oracle = build_simon_oracle(secret_s)
    qc = create_simon_circuit(oracle)
    
    counts = run_simulation(qc)
    if counts:
        print(f"Measurements: {counts}")
        found_s = solve_simon(counts, n)
        print(f"Found secret string s: {found_s}")
        if found_s == secret_s:
            print("Success!")
        else:
            print("Failed to find s (or s=000 case).")
    else:
        print("Simulator not available.")

if __name__ == "__main__":
    main("11")
    main("101")
