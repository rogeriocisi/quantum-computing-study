import pytest
from src.algorithms.simon import (
    build_simon_oracle,
    create_simon_circuit,
    solve_simon,
    run_simulation,
)


@pytest.mark.parametrize("secret_s", ["11", "01", "101", "110"])
def test_simon_algorithm(secret_s):
    """Verifies that Simon's algorithm correctly retrieves the secret string."""
    n = len(secret_s)
    oracle = build_simon_oracle(secret_s)
    qc = create_simon_circuit(oracle)

    counts = run_simulation(qc)
    assert counts is not None

    found_s = solve_simon(counts, n)
    assert found_s == secret_s


def test_simon_zero_case():
    """Verifies behavior with s = '00' (one-to-one function)."""
    secret_s = "00"
    n = 2
    oracle = build_simon_oracle(secret_s)
    qc = create_simon_circuit(oracle)

    counts = run_simulation(qc)
    assert counts is not None

    found_s = solve_simon(counts, n)
    # For s=00, solve_simon should return 00
    assert found_s == "00"
