import numpy as np
import matplotlib.pyplot as plt
from braket.circuits import Circuit
from braket.aws import AwsDevice

# Use AWS cloud simulator
device = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/dm1")
# Use quantum computer from IonQ - n.b. 1000 shots = about $10.30
#device = AwsDevice("arn:aws:braket:::device/qpu/ionq/ionQdevice")

#device_operations = device.properties.dict()['action']['braket.ir.jaqcd.program']['supportedOperations']
#print('Quantum Gates supported by {}:\n {}'.format(device.name, device_operations))

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
circuit = Circuit()

# Set initial state, by flipping bits using x()
# A = 2
#circuit.x(0) #a_0 = 1
circuit.x(1) #a_1 = 1
# B = 3
circuit.x(2) #b_0 = 1
circuit.x(3) #b_1 = 1

# Perform the addition as per Thapliyal and Ranganathan's algorithm for
# a reversible ripple carry adder without input carry or ancilla inputs
# Step (1)
circuit.cnot(1,3) # CNOT(a_1, b_1)
# Step (2)
circuit.cnot(1,4) # CNOT(a_1, carry)
# Step (3)
circuit.ccnot(0,2,1) # Toffoli(a_0, b_0, a_1)
# Step (4)
# Peres gate, A=1, B=3, C=4 == Peres(a_1, b_1, carry)
circuit.ccnot(1,3,4)
circuit.cnot(1,3)
# Peres gate, A=0, B=2, C=1 == Peres (a_0, b_0, a_1)
circuit.ccnot(0,2,1)
circuit.cnot(0,2)
# Step (5) - skipped
# Step (6)
circuit.cnot(1,3) # CNOT(a_1, b_1)

# Map the quantum measurement to the classical bits
#circuit.measure([2,3,4],[0,1,2]) # Just measure the result

# Draw the circuit
print(circuit)

# compile the circuit down to low-level QASM instructions
# supported by the backend (not needed for simple circuits)
#compiled_circuit = transpile(circuit, simulator)
print("Compiled circuit depth = ",circuit.depth)

# Execute the circuit on the qasm simulator
job = device.run(circuit, shots=1000)

# Grab results from the job
result = job.result()

# Returns counts
counts = result.measurement_counts

# Reverse and clean up counts for only the qubits we care about
clean_counts = {}
for key in counts:
  clean_key = key[2:][::-1]
  clean_counts[clean_key] = clean_counts.get(clean_key, 0) + counts[key]

print("\nTotal counts are:",clean_counts)

# Plot a histogram

plt.bar(clean_counts.keys(), list(map(lambda x: x/1000.0, clean_counts.values())))
plt.ylabel('Probabilities')
plt.show()
