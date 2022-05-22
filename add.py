import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import SXdgGate

# Use Aer's qasm_simulator
simulator = QasmSimulator()

# Create a Quantum Circuit with 5 qubits and 3 classical registers
# Adder algorithm from https://www.researchgate.net/publication/262163558_Design_of_Efficient_Reversible_Logic-Based_Binary_and_BCD_Adder_Circuits
# Input:
# qubit_0 = a_0
# qubit_1 = a_1
# qubit_2 = b_0
# qubit_3 = b_1
# qubit_4 = 0
# Output:
# qubit_0 = a_0
# qubit_1 = a_1
# qubit_2 = sum_0
# qubit_3 = sum_1
# qubit_4 = sum_2
circuit = QuantumCircuit(5, 3)

# Define a controlled SX dagger gate as per https://quantumcomputing.stackexchange.com/questions/18107/how-to-construct-a-controlled-v-gate-in-qiskit
csxd = SXdgGate().control()

# Set initial state, by flipping bits using x()
# A = 2
#circuit.x(0) #a_0 = 1
circuit.x(1) #a_1 = 1
# B = 3
circuit.x(2) #b_0 = 1
circuit.x(3) #b_1 = 1

circuit.barrier()

# Perform the addition as per Thapliyal and Ranganathan's algorithm for
# a reversible ripple carry adder without input carry or ancilla inputs
# Step (1)
circuit.cx(1,3) # CNOT(a_1, b_1)
# Step (2)
circuit.cx(1,4) # CNOT(a_1, carry)
# Step (3)
circuit.ccx(0,2,1) # Toffoli(a_0, b_0, a_1)
# Step (4)
# Peres gate, A=1, B=3, C=4 == Peres(a_1, b_1, carry)
circuit.append(csxd, [1,4])
circuit.append(csxd, [3,4])
circuit.cx(1,3)
circuit.csx(3,4)
# Peres gate, A=0, B=2, C=1 == Peres (a_0, b_0, a_1)
circuit.append(csxd, [0,1])
circuit.append(csxd, [2,1])
circuit.cx(0,2)
circuit.csx(2,1)
# Step (5) - skipped
# Step (6)
circuit.cx(1,3) # CNOT(a_1, b_1)

circuit.barrier()

# Map the quantum measurement to the classical bits
circuit.measure([2,3,4],[0,1,2]) # Just measure the result

# Draw the circuit
print(circuit.draw())

# compile the circuit down to low-level QASM instructions
# supported by the backend (not needed for simple circuits)
compiled_circuit = transpile(circuit, simulator)

# Execute the circuit on the qasm simulator
job = simulator.run(compiled_circuit, shots=1000)

# Grab results from the job
result = job.result()

# Returns counts
counts = result.get_counts(compiled_circuit)
print("\nTotal counts are:",counts)
