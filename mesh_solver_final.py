import sympy as sp

print("="*60)
print("MESH ANALYSIS WITH DEPENDENT CURRENT SOURCE")
print("="*60)

I1, I2 = sp.symbols('I1 I2', real=True)

print("\nCircuit Setup")
print("Mesh 1 (left) goes through 12 ohm and 24 ohm")
print("Mesh 2 (right) goes through 3 ohm, 36V source, 6 ohm")
print("Dependent source 3*Io between meshes (points UP)")
print("")

print("="*60)
print("SOLUTION 1 with supermesh equation")
print("KVL outer loop: 12*I1 + 9*I2 = 36")
print("Constraint: I2 - I1 = 3*I1, so I2 = 4*I1")
print("="*60)

eq1_sol1 = sp.Eq(12*I1 + 9*I2, 36)
constraint_sol1 = sp.Eq(I2 - I1, 3*I1)

sol1 = sp.solve([eq1_sol1, constraint_sol1], [I1, I2])
print(f"\nSolution")
print(f"I1 = {float(sol1[I1])} A")
print(f"I2 = {float(sol1[I2])} A")

Io_sol1 = sol1[I1]
I_6ohm_sol1 = sol1[I2]
P_6ohm_sol1 = I_6ohm_sol1**2 * 6

print(f"\nIo = {float(Io_sol1)} A")
print(f"Current through 6 ohm = {float(I_6ohm_sol1)} A")
print(f"Power in 6 ohm = {float(P_6ohm_sol1)} W")

print("\n" + "="*60)
print("SOLUTION 2 different supermesh")
print("KVL: 36*I1 - 15*I2 = 36")
print("Constraint: I2 = 4*I1")
print("="*60)

eq1_sol2 = sp.Eq(36*I1 - 15*I2, 36)
constraint_sol2 = sp.Eq(I2 - I1, 3*I1)

sol2 = sp.solve([eq1_sol2, constraint_sol2], [I1, I2])
print(f"\nSolution")
print(f"I1 = {float(sol2[I1])} A")
print(f"I2 = {float(sol2[I2])} A")

Io_sol2 = sol2[I1]
P_6ohm_sol2 = sol2[I2]**2 * 6

print(f"\nIo = {float(Io_sol2)} A")
print(f"Power in 6 ohm = {float(P_6ohm_sol2)} W")

print("\n" + "="*60)
print("CHECKING ANSWERS")
print("="*60)

answers = [
    (2.75, 253.5),
    (1, 253.5),
    (1, 6),
    (-2.75, 121.5),
    (5.5, 45.375),
    (-1, 45.375),
    (2.75, 6)
]

print("\nAnswer choices")
for i, (io, p) in enumerate(answers, 1):
    print(f"{i}. Io = {io} A, P = {p} W")

print(f"\nSolution 1: Io = {float(Io_sol1)} A, P = {float(P_6ohm_sol1)} W")
for i, (io, p) in enumerate(answers, 1):
    if abs(float(Io_sol1) - io) < 0.01 and abs(float(P_6ohm_sol1) - p) < 0.01:
        print(f"MATCH Answer {i}")

print(f"\nSolution 2: Io = {float(Io_sol2)} A, P = {float(P_6ohm_sol2)} W")
for i, (io, p) in enumerate(answers, 1):
    if abs(float(Io_sol2) - io) < 0.01 and abs(float(P_6ohm_sol2) - p) < 0.01:
        print(f"MATCH Answer {i}")

print("="*60)
