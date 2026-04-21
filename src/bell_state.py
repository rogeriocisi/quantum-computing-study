from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# 1. Criar o circuito quântico com 2 qubits e 2 bits clássicos
qc = QuantumCircuit(2, 2)

# 2. Aplicar uma porta Hadamard no qubit 0 para criar superposição
qc.h(0)

# 3. Aplicar uma porta CNOT (Control-NOT) com controle no qubit 0 e alvo no qubit 1
# Isso cria o entrelaçamento (entanglement)
qc.cx(0, 1)

# 4. Medir os qubits e armazenar os resultados nos bits clássicos
qc.measure([0, 1], [0, 1])

# 5. Visualizar o circuito (opcional, será salvo como imagem)
print("Desenhando o circuito...")
qc.draw(output='mpl', filename='outputs/bell_circuit.png')


# 6. Rodar a simulação usando o AerSimulator
backend = AerSimulator()
job = backend.run(qc, shots=1024)
result = job.result()

# 7. Obter as contagens dos resultados
counts = result.get_counts(qc)
print(f"Resultados (contagens): {counts}")

# 8. Visualizar o histograma (será salvo como imagem)
plot_histogram(counts)
plt.savefig('outputs/bell_histogram.png')
print("Simulação concluída. Imagens em 'outputs/' geradas.")

