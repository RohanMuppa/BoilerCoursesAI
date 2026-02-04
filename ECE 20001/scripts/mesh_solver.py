import sympy as sp

print("="*60)
print("MESH ANALYSIS PROBLEM SOLVER")
print("="*60)

# Define symbolic variables
I1, I2, Io = sp.symbols('I1 I2 Io', real=True)

print("\nCircuit Components")
print("3 ohm resistor at top (horizontal)")
print("24 ohm and 6 ohm in middle (horizontal)")
print("12 ohm on far left (vertical)")
print("Io flows DOWN in the middle")
print("3*Io dependent current source points UP")
print("36V on right (+ at top)")

print("\n" + "="*60)
print("INTERPRETATION 1: Io = I1 (current through 12 ohm)")
print("="*60)

print("\nMesh equations")

# Mesh 1: Going clockwise
eq1_int1 = sp.Eq(12*I1 + 24*(I1 - I2), 0)
print(f"Mesh 1: 12*I1 + 24*(I1 - I2) = 0")

# Mesh 2
eq2_int1 = sp.Eq(-36 + 3*I2 + 6*I2 + 24*(I2 - I1), 0)
print(f"Mesh 2: -36 + 3*I2 + 6*I2 + 24*(I2 - I1) = 0")

# Current source constraint: I2 - I1 = 3*I1
eq3_int1 = sp.Eq(I2 - I1, 3*I1)
print(f"Current source constraint: I2 - I1 = 3*I1")

# Solve the system
solution_int1 = sp.solve([eq1_int1, eq3_int1], [I1, I2])
print(f"\nSolution:")
print(f"I1 = {solution_int1[I1]} A")
print(f"I2 = {solution_int1[I2]} A")

Io_int1 = solution_int1[I1]
print(f"Io = I1 = {Io_int1} A = {float(Io_int1)} A")

# Current through 6 ohm resistor is I2
I_6ohm_int1 = solution_int1[I2]
P_6ohm_int1 = I_6ohm_int1**2 * 6
print(f"\nCurrent through 6 ohm resistor = {float(I_6ohm_int1)} A")
print(f"Power in 6 ohm resistor = {float(P_6ohm_int1)} W")

print("\n" + "="*60)
print("INTERPRETATION 2: Io = I1 - I2 (middle branch current)")
print("="*60)

# Mesh 1
eq1_int2 = sp.Eq(12*I1 + 24*(I1 - I2), 0)
print(f"\nMesh 1: 12*I1 + 24*(I1 - I2) = 0")

# Mesh 2
eq2_int2 = sp.Eq(-36 + 3*I2 + 6*I2 + 24*(I2 - I1), 0)
print(f"Mesh 2: -36 + 3*I2 + 6*I2 + 24*(I2 - I1) = 0")

# Current source constraint: dependent source is 3*Io where Io = I1 - I2
eq3_int2 = sp.Eq(I2 - I1, 3*(I1 - I2))
print(f"Current source constraint: I2 - I1 = 3*(I1 - I2)")

# Solve the system
solution_int2 = sp.solve([eq1_int2, eq3_int2], [I1, I2])
print(f"\nSolution:")
print(f"I1 = {solution_int2[I1]} A")
print(f"I2 = {solution_int2[I2]} A")

Io_int2 = solution_int2[I1] - solution_int2[I2]
print(f"Io = I1 - I2 = {Io_int2} A = {float(Io_int2)} A")

I_6ohm_int2 = solution_int2[I2]
P_6ohm_int2 = I_6ohm_int2**2 * 6
print(f"\nCurrent through 6 ohm resistor = {float(I_6ohm_int2)} A")
print(f"Power in 6 ohm resistor = {float(P_6ohm_int2)} W")

print("\n" + "="*60)
print("CHECKING AGAINST GIVEN ANSWERS")
print("="*60)

answers = [
    (2.75, 253.5),
    (1, 253.5),
    (2.75, 6),
    (-2.75, 121.5),
    (5.5, 45.375),
    (-1, 45.375),
    (1, 6)
]

print("\nGiven answer choices:")
for i, (io, p) in enumerate(answers, 1):
    print(f"{i}. Io = {io} A, P = {p} W")

print("\n" + "="*60)
print("INTERPRETATION 1 RESULTS:")
print(f"Io = {float(Io_int1)} A, P = {float(P_6ohm_int1)} W")
for i, (io, p) in enumerate(answers, 1):
    if abs(float(Io_int1) - io) < 0.01 and abs(float(P_6ohm_int1) - p) < 0.01:
        print(f"*** MATCH with Answer choice {i} ***")

print("\nINTERPRETATION 2 RESULTS:")
print(f"Io = {float(Io_int2)} A, P = {float(P_6ohm_int2)} W")
for i, (io, p) in enumerate(answers, 1):
    if abs(float(Io_int2) - io) < 0.01 and abs(float(P_6ohm_int2) - p) < 0.01:
        print(f"*** MATCH with Answer choice {i} ***")

print("="*60)
