import math
import pytest
from qiskit.quantum_info import Statevector

from src.algorithms.shor import (
    classical_preprocess,
    build_c_u_power,
    create_shor_circuit,
    run_simulation,
    solve_shor,
    factor,
)


def test_classical_preprocess():
    """Validates the classical preprocessing and trivial reductions."""
    # N is even
    done, f = classical_preprocess(12)
    assert done
    assert f == 2

    # N is prime or too small
    done, f = classical_preprocess(3)
    assert done
    assert f is None

    # N is a perfect power (e.g. 9 = 3^2, 8 = 2^3, 27 = 3^3)
    done, f = classical_preprocess(9)
    assert done
    assert f == 3

    done, f = classical_preprocess(8)
    assert done
    assert f == 2

    # N is composite but not trivial
    done, f = classical_preprocess(15)
    assert not done
    assert f is None


def test_build_c_u_power():
    """Verifies that build_c_u_power maps states |y> -> |(a * y) mod N> on basis states."""
    N = 15
    a = 7
    m = math.ceil(math.log2(N))  # 4 qubits for target register

    # We test y = 3. Expected: (3 * 7) % 15 = 21 % 15 = 6.
    # In Qiskit, bit 0 (rightmost) is the control qubit. We set it to 1.
    # The target register is qubits 1..m. We set it to 3 (binary '0011').
    # So the combined state label is: target_bin + control_bin = "0011" + "1" = "00111"
    initial_label = "00111"
    sv = Statevector.from_label(initial_label)

    # Build the U^{2^0} circuit
    circuit = build_c_u_power(a, 0, N)

    # Evolve the statevector through the circuit
    sv_out = sv.evolve(circuit)

    # Expected target output is 6 (binary '0110'). Control remains 1.
    # So expected output state label: "0110" + "1" = "01101"
    expected_label = "01101"
    sv_expected = Statevector.from_label(expected_label)

    assert sv_out.equiv(sv_expected)

    # Verify a state y >= N (e.g. y = 15, binary '1111').
    # It should map to itself (15).
    initial_label_out_of_bounds = "11111"
    sv_oob = Statevector.from_label(initial_label_out_of_bounds)
    sv_oob_out = sv_oob.evolve(circuit)
    assert sv_oob_out.equiv(sv_oob)


def test_create_shor_circuit():
    """Validates the register sizes and circuit structure of create_shor_circuit."""
    N = 15
    a = 7
    qc = create_shor_circuit(a, N)

    n_count = 2 * math.ceil(math.log2(N))  # 2 * 4 = 8
    m = math.ceil(math.log2(N))             # 4
    total_qubits = n_count + m              # 12

    assert qc.num_qubits == total_qubits
    assert len(qc.clbits) == n_count
    
    # Check that it contains the IQFT/QFT inverse operation
    iqft_found = False
    for instruction in qc.data:
        if instruction.operation.name in ["IQFT", "qft", "IQFT_gate"]:
            iqft_found = True
            break
    # In Qiskit, it could be appended as a gate with custom label or just QFT
    # Since we labeled it "IQFT" when creating, let's verify either label or QFT name
    assert any(
        "IQFT" in str(inst.operation.label) or "qft" in inst.operation.name
        for inst in qc.data
    )


def test_solve_shor():
    """Injects synthetic counts to verify continued fraction phase and factor extraction."""
    N = 15
    a = 7
    n_count = 8  # 2 * math.ceil(math.log2(15))

    # Phase s/r = 1/4 = 0.25
    # Measured value = 0.25 * 2**8 = 64
    # 64 in 8-bit binary is '01000000'
    counts = {"01000000": 1000}
    factor_found = solve_shor(counts, a, N)
    
    assert factor_found in [3, 5]

    # Phase s/r = 3/4 = 0.75
    # Measured value = 0.75 * 2**8 = 192
    # 192 in 8-bit binary is '11000000'
    counts_3_4 = {"11000000": 1000}
    factor_found_3_4 = solve_shor(counts_3_4, a, N)
    
    assert factor_found_3_4 in [3, 5]

    # Invalid phase (e.g. 0) which would lead to r=1
    counts_invalid = {"00000000": 1000}
    assert solve_shor(counts_invalid, a, N) is None


@pytest.mark.parametrize("a", [2, 4, 7, 8, 11, 13])
def test_end_to_end_n15(a):
    """Performs full simulation and factor extraction for N = 15 on all valid coprime bases."""
    N = 15
    qc = create_shor_circuit(a, N)
    counts = run_simulation(qc, shots=1024)
    
    factor_found = solve_shor(counts, a, N)
    assert factor_found in [3, 5]
    assert N % factor_found == 0


def test_factor_n21():
    """Validates the algorithm for N = 21 with at least one base."""
    N = 21
    # Coprimes: 2, 4, 5, 8, 10, 11, 13, 16, 17, 19, 20
    # Let's use a = 2. 2^6 = 64 = 3 * 21 + 1. So r = 6 (even).
    # 2^3 % 21 = 8 != 20. Non-trivial factor = gcd(8 +/- 1, 21) -> 7, 3.
    a = 2
    qc = create_shor_circuit(a, N)
    counts = run_simulation(qc, shots=2048)
    
    factor_found = solve_shor(counts, a, N)
    assert factor_found in [3, 7]
    assert N % factor_found == 0
