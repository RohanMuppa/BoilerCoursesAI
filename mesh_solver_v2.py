import sympy as sp

print("="*60)
print("MESH ANALYSIS PROBLEM SOLVER V2")
print("="*60)

# Define symbolic variables
I1, I2 = sp.symbols('I1 I2', real=True)

print("\nCircuit Description")
print("Left mesh: 12 ohm vertical, 24 ohm horizontal")
print("Right mesh: 3 ohm top, 6 ohm right, 36V source")
print("Middle: Io flows DOWN, 3*Io source points UP")
print("\n")

print("="*60)
print("APPROACH 1: Standard mesh with current source as constraint")
print("="*60)

# In a mesh with a dependent current source between two meshes,
# the constraint is: (I_mesh2 - I_mesh1) = current_source_value
# Here: I2 - I1 = 3*Io where Io is defined

# Case A: Io = I1 (current through 12 ohm resistor)
print("\nCase A: Io = I1")
print("Constraint: I2 - I1 = 3*I1, so I2 = 4*I1")

# Mesh 1: KVL around left mesh
# 12*I1 + 24*(I1 - I2) = 0
# 36*I1 - 24*I2 = 0
eq1a = sp.Eq(36*I1 - 24*I2, 0)
print(f"Mesh 1 KVL: 36*I1 - 24*I2 = 0")

# Mesh 2: KVL around right mesh  
# -36 + 3*I2 + 6*I2 + 24*(I2 - I1) = 0
# -36 + 33*I2 - 24*I1 = 0
eq2a = sp.Eq(-36 + 33*I2 - 24*I1, 0)
print(f"Mesh 2 KVL: -36 + 33*I2 - 24*I1 = 0")

# Constraint from dependent source
constraint_a = sp.Eq(I2, 4*I1)
print(f"Constraint: I2 = 4*I1")

# Solve
sol_a = sp.solve([eq1a, constraint_a], [I1, I2])
print(f"\nSolution:")
print(f"I1 = {sol_a[I1]} A = {float(sol_a[I1])} A")
print(f"I2 = {sol_a[I2]} A = {float(sol_a[I2])} A")

Io_a = sol_a[I1]
I_6ohm_a = sol_a[I2]
P_6ohm_a = I_6ohm_a**2 * 6

print(f"\nResults:")
print(f"Io = {float(Io_a)} A")
print(f"Current through 6 ohm = {float(I_6ohm_a)} A")
print(f"Power in 6 ohm = {float(P_6ohm_a)} W")

# Verify by checking mesh 2 equation
verify_a = -36 + 33*sol_a[I2] - 24*sol_a[I1]
print(f"Verify mesh 2: {float(verify_a)} (should be ~0)")

print("\n" + "="*60)
print("Case B: Io = I2 - I1 (branch current between meshes)")
print("Constraint: I2 - I1 = 3*(I2 - I1)")
print("This gives: I2 - I1 = 3*I2 - 3*I1")
print("Simplifying: 2*I1 = 2*I2, so I1 = I2")
print("This would mean no current, which is invalid.")

print("\n" + "="*60)
print("Case C: Io = I1 - I2 (branch current, opposite direction)")
print("Constraint: I2 - I1 = 3*(I1 - I2) = 3*I1 - 3*I2")
print("Simplifying: 4*I2 = 4*I1, so I1 = I2")
print("This also leads to no net current, invalid.")

print("\n" + "="*60)
print("APPROACH 2: Supermesh (ignoring current source constraint)")
print("="*60)

# Let's solve without the constraint first to see natural currents
print("\nWithout constraint:")
eq1_free = sp.Eq(36*I1 - 24*I2, 0)
eq2_free = sp.Eq(-36 + 33*I2 - 24*I1, 0)

sol_free = sp.solve([eq1_free, eq2_free], [I1, I2])
print(f"I1 = {sol_free[I1]} A = {float(sol_free[I1])} A")
print(f"I2 = {sol_free[I2]} A = {float(sol_free[I2])} A")

# Now check different Io definitions
Io_free1 = sol_free[I1]
Io_free2 = sol_free[I2] - sol_free[I1]
Io_free3 = sol_free[I1] - sol_free[I2]

print(f"\nIf Io = I1: {float(Io_free1)} A")
print(f"If Io = I2 - I1: {float(Io_free2)} A")
print(f"If Io = I1 - I2: {float(Io_free3)} A")

I_6ohm_free = sol_free[I2]
P_6ohm_free = I_6ohm_free**2 * 6
print(f"\nPower in 6 ohm = {float(P_6ohm_free)} W")

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
print("Case A Results:")
print(f"Io = {float(Io_a)} A, P = {float(P_6ohm_a)} W")
for i, (io, p) in enumerate(answers, 1):
    if abs(float(Io_a) - io) < 0.01 and abs(float(P_6ohm_a) - p) < 0.01:
        print(f"*** MATCH with Answer choice {i} ***")

print("\nApproach 2 (no constraint) Results:")
print(f"Io = I1 = {float(Io_free1)} A, P = {float(P_6ohm_free)} W")
for i, (io, p) in enumerate(answers, 1):
    if abs(float(Io_free1) - io) < 0.01 and abs(float(P_6ohm_free) - p) < 0.01:
        print(f"*** MATCH with Answer choice {i} ***")

print(f"\nIo = I2-I1 = {float(Io_free2)} A, P = {float(P_6ohm_free)} W")
for i, (io, p) in enumerate(answers, 1):
    if abs(float(Io_free2) - io) < 0.01 and abs(float(P_6ohm_free) - p) < 0.01:
        print(f"*** MATCH with Answer choice {i} ***")

print("="*60)
