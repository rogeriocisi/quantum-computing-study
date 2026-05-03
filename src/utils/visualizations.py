"""
Visualization Utilities for Quantum States
==========================================
This module provides tools to format and display quantum states in a readable way,
including Dirac (Bra-Ket) notation and amplitude vectors.
"""

from qiskit.quantum_info import Statevector


def format_complex(c: complex) -> str:
    """Formats a complex number into a clean string representation.

    Args:
        c: The complex number to format.

    Returns:
        str: A human-readable string (e.g., "1", "i", "1+i").
    """
    r = round(c.real, 4)
    i = round(c.imag, 4)
    if abs(i) < 1e-4:
        return f"{int(r) if r.is_integer() else r}"
    if abs(r) < 1e-4:
        if i == 1:
            return "i"
        if i == -1:
            return "-i"
        return f"{int(i) if i.is_integer() else i}i"

    sign = "+" if i > 0 else "-"
    i_abs = abs(i)
    i_str = f"{int(i_abs) if i_abs.is_integer() else i_abs}i"
    if i_abs == 1:
        i_str = "i"

    r_str = f"{int(r) if r.is_integer() else r}"
    return f"{r_str}{sign}{i_str}"


def display_state(title: str, psi: Statevector) -> None:
    """Prints the quantum state in Dirac notation, vector form, and probabilities.

    Args:
        title: Title to display above the state info.
        psi: The Statevector object to visualize.
    """
    print(f"=== {title} ===")

    # Dirac Notation (Text)
    amplitude_dict = psi.to_dict()
    dirac_terms = []
    for basis, amp in amplitude_dict.items():
        r = round(amp.real, 4)
        i = round(amp.imag, 4)

        if abs(r) < 1e-4 and abs(i) < 1e-4:
            continue

        amp_str = format_complex(amp)
        if amp_str == "1":
            amp_str = ""
        elif amp_str == "-1":
            amp_str = "-"
        elif "+" in amp_str or ("-" in amp_str and not amp_str.startswith("-")):
            amp_str = f"({amp_str})"

        dirac_terms.append(f"{amp_str}|{basis}>")

    dirac_str = ""
    for term in dirac_terms:
        if not dirac_str:
            dirac_str = term
        else:
            if term.startswith("-"):
                dirac_str += f" - {term[1:]}"
            else:
                dirac_str += f" + {term}"

    if not dirac_str:
        dirac_str = "0"

    print(f"  Dirac:          {dirac_str}")

    # Vector Representation
    vector_str = "[" + ", ".join([format_complex(c) for c in psi.data]) + "]"
    print(f"  Vector:         {vector_str}")

    # Probabilities
    probs = psi.probabilities_dict()
    probs_str = ", ".join([f"P(|{k}>) = {v*100:.1f}%" for k, v in probs.items()])
    print(f"  Probabilities:  {probs_str}")

    # LaTeX Visualization (For Interactive Windows)
    try:
        from IPython.display import display

        display(psi.draw("latex"))
    except Exception:
        pass

    print()
