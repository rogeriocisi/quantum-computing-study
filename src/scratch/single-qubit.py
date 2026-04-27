# %%
import os
import sys
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit

# Ensure Python finds the 'src' folder from the project root
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if root_path not in sys.path:
    sys.path.append(root_path)

from src.utils.visualizations import display_state

# 0. Clear screen (useful if running in terminal)
os.system("cls" if os.name == "nt" else "clear")


# %%
# ==============================================================================
# PART 1: Applying Gates to the Ground State |0>
# ==============================================================================
print("=" * 60)
print(" PART 1: EFFECT OF GATES ON THE INITIAL STATE |0> ")
print("=" * 60 + "\n")

# %%
# Initial State |0>
qc = QuantumCircuit(1)
psi = Statevector.from_instruction(qc)
display_state("Initial State |0>", psi)

# %%
# H Gate (Hadamard)
qc = QuantumCircuit(1)
qc.h(0)
psi = Statevector.from_instruction(qc)
display_state("After H Gate (Creates Superposition)", psi)

# %%
# X Gate (Quantum NOT)
qc = QuantumCircuit(1)
qc.x(0)
psi = Statevector.from_instruction(qc)
display_state("After X Gate (Inverts 0 <-> 1)", psi)

# %%
# Y Gate
qc = QuantumCircuit(1)
qc.y(0)
psi = Statevector.from_instruction(qc)
display_state("After Y Gate", psi)

# %%
# Z Gate
qc = QuantumCircuit(1)
qc.z(0)
psi = Statevector.from_instruction(qc)
display_state("After Z Gate (Does not alter |0>)", psi)

# %%
# S Gate (Phase Gate)
qc = QuantumCircuit(1)
qc.s(0)
psi = Statevector.from_instruction(qc)
display_state("After S Gate (Does not alter |0>)", psi)

# %%
# T Gate (T Gate)
qc = QuantumCircuit(1)
qc.t(0)
psi = Statevector.from_instruction(qc)
display_state("After T Gate (Does not alter |0>)", psi)

# %%
# ==============================================================================
# PART 2: Applying Gates to the State |+>
# ==============================================================================
print("=" * 60)
print(" PART 2: EFFECT OF GATES ON THE STATE |+> ")
print("=" * 60 + "\n")

# %%
# Initial State |+> (applying H first)
qc_plus = QuantumCircuit(1)
qc_plus.h(0)
psi_plus = Statevector.from_instruction(qc_plus)
display_state("Initial State |+> (Superposition)", psi_plus)

# %%
# H Gate on state |+>
qc_h = QuantumCircuit(1)
qc_h.h(0)
qc_h.h(0)
psi_h = Statevector.from_instruction(qc_h)
display_state("After H Gate on state |+> (Returns to |0>)", psi_h)

# %%
# X Gate on state |+>
qc_x = QuantumCircuit(1)
qc_x.h(0)
qc_x.x(0)
psi_x = Statevector.from_instruction(qc_x)
display_state("After X Gate on state |+> (Does not alter |+>)", psi_x)

# %%
# Y Gate on state |+>
qc_y = QuantumCircuit(1)
qc_y.h(0)
qc_y.y(0)
psi_y = Statevector.from_instruction(qc_y)
display_state("After Y Gate on state |+> (Phase and Inversion)", psi_y)

# %%
# Z Gate on state |+>
qc_z = QuantumCircuit(1)
qc_z.h(0)
qc_z.z(0)
psi_z = Statevector.from_instruction(qc_z)
display_state("After Z Gate on state |+> (Rotates 180 deg in Z -> |->)", psi_z)

# %%
# S Gate on state |+>
qc_s = QuantumCircuit(1)
qc_s.h(0)
qc_s.s(0)
psi_s = Statevector.from_instruction(qc_s)
display_state("After S Gate on state |+> (Rotates 90 deg in Z)", psi_s)

# %%
# T Gate on state |+>
qc_t = QuantumCircuit(1)
qc_t.h(0)
qc_t.t(0)
psi_t = Statevector.from_instruction(qc_t)
display_state("After T Gate on state |+> (Rotates 45 deg in Z)", psi_t)
