import sympy as sp

print("="*60)
print("FINDING MESH EQUATIONS FOR ANSWER 5")
print("Target: Io = 5.5 A, P = 45.375 W")
print("="*60)

I1, I2 = sp.symbols('I1 I2', real=True)

# From our analysis: I_6ohm = 2.75 A, and if I_6ohm = I2, then I2 = 2.75
# If Io = I1 = 5.5, then we have I1 = 5.5, I2 = 2.75
# Relationship: I2 = I1/2

print("\nTarget values:")
print("I1 = 5.5 A (= Io)")
print("I2 = 2.75 A (current through 6 ohm)")
print("Relationship: I2 = I1/2")
print("")

# What mesh equations would give I1 = 5.5, I2 = 2.75?
# Let's work backwards

# Standard form:
# a11*I1 + a12*I2 = b1
# a21*I1 + a22*I2 = b2

# Substituting I1 = 5.5, I2 = 2.75:
# a11*5.5 + a12*2.75 = b1
# a21*5.5 + a22*2.75 = b2

# From standard mesh analysis:
# Mesh 1: R1*I1 + R_shared*(I1-I2) = 0
# Mesh 2: R_shared*(I2-I1) + R2*I2 - V = 0

print("Standard mesh equations:")
print("Mesh 1: (R1 + R_shared)*I1 - R_shared*I2 = 0")
print("Mesh 2: -R_shared*I1 + (R_shared + R2)*I2 = V")
print("")

# Given: R1 = 12, R_shared = 24, R2 = 3+6 = 9, V = 36
# Mesh 1: (12+24)*I1 - 24*I2 = 0 => 36*I1 - 24*I2 = 0
# Mesh 2: -24*I1 + (24+9)*I2 = 36 => -24*I1 + 33*I2 = 36

# Check with I1=5.5, I2=2.75:
result1 = 36*5.5 - 24*2.75
result2 = -24*5.5 + 33*2.75

print(f"Check mesh 1: 36*5.5 - 24*2.75 = {result1} (should be 0)")
print(f"Check mesh 2: -24*5.5 + 33*2.75 = {result2} (should be 36)")
print("")

# These don't work. So the circuit must be different.

print("Standard mesh equations don't work")
print("The circuit topology must be different")
print("")

# What if R_shared is different?
# Or what if there's no shared resistor?
# Or what if the dependent source modifies the equations?

# Let's try: What R values would satisfy the equations?
# Mesh 1: a*I1 - b*I2 = 0
# Mesh 2: -c*I1 + d*I2 = 36

# For I1 = 5.5, I2 = 2.75:
# a*5.5 - b*2.75 = 0 => a*5.5 = b*2.75 => a/b = 2.75/5.5 = 0.5
# So a = 0.5*b

# -c*5.5 + d*2.75 = 36

print("="*60)
print("BACK-CALCULATING REQUIRED RESISTANCES")
print("="*60)

# Let's say a = 0.5*b (from mesh 1 constraint)
# Try b = 24 (our shared resistor): a = 12 ✓ (matches our R1!)

# For mesh 2: -c*5.5 + d*2.75 = 36
# If c = 24: -24*5.5 + d*2.75 = 36
# -132 + d*2.75 = 36
# d*2.75 = 168
# d = 61.09

print("If we use standard mesh 1: 12*I1 - 24*I2 = 0 (but should be 36*I1 - 24*I2 = 0)")
print("Wait, mesh 1 should have 36 coefficient for I1")
print("")

print("Let's recalculate:")
print("Mesh 1: 36*I1 - 24*I2 = c1")
print("For I1=5.5, I2=2.75: 36*5.5 - 24*2.75 = 198 - 66 = 132")
print(f"So c1 = 132")
print("")

# This means mesh 1 equation is: 36*I1 - 24*I2 = 132

# What would produce a non-zero RHS for mesh 1?
# A voltage source in mesh 1!

print("="*60)
print("HYPOTHESIS: There's a voltage source in mesh 1 too!")
print("="*60)

print("\nMesh 1 with voltage V1:")
print("12*I1 + 24*(I1-I2) = V1")
print("36*I1 - 24*I2 = V1")
print("")

print("For I1=5.5, I2=2.75:")
print("V1 = 132 V")
print("")

# Mesh 2 with voltage 36V:
print("Mesh 2:")
print("-24*I1 + 33*I2 = V2")
print("For I1=5.5, I2=2.75:")
V2_calc = -24*5.5 + 33*2.75
print(f"V2 = {V2_calc} V")
print("")

# So mesh 2 needs voltage = -41.25 V
# This means voltage source is -41.25 V (or 41.25 V in opposite direction)

print("="*60)
print("CONCLUSION FOR ANSWER 5:")
print("="*60)
print("The circuit would need:")
print("Mesh 1: 36*I1 - 24*I2 = 132 (requires 132V source in mesh 1)")
print("Mesh 2: -24*I1 + 33*I2 = -41.25 (requires -41.25V, not +36V)")
print("")
print("This doesn't match the given 36V source")
print("So answer 5 is likely INCORRECT for this circuit")

print("\n" + "="*60)
print("Let me try finding which answer DOES work with 36V")
print("="*60)

# Solve the standard equations and see what we get
eq1 = sp.Eq(36*I1 - 24*I2, 0)
eq2 = sp.Eq(-24*I1 + 33*I2, 36)

sol_std = sp.solve([eq1, eq2], [I1, I2])
print("\nStandard solution (no dependent source):")
print(f"I1 = {float(sol_std[I1]):.4f} A")
print(f"I2 = {float(sol_std[I2]):.4f} A")
print(f"P = {float(sol_std[I2]**2 * 6):.4f} W")

# Now with various dependent source constraints
print("\n" + "="*60)
print("WITH DEPENDENT SOURCE I2 - I1 = 3*Io")
print("="*60)

# If constraint is I2 - I1 = 3*I1 (Io = I1):
constraint1 = sp.Eq(I2 - I1, 3*I1)
sol1 = sp.solve([eq1, constraint1], [I1, I2])
print("\nCase: Io = I1, constraint I2 = 4*I1")
if sol1 and sol1[I1] != 0:
    print(f"I1 = {float(sol1[I1]):.4f} A (= Io)")
    print(f"I2 = {float(sol1[I2]):.4f} A")
    print(f"P = {float(sol1[I2]**2 * 6):.4f} W")
    # Check mesh 2
    check = -24*sol1[I1] + 33*sol1[I2]
    print(f"Mesh 2 check: -24*I1 + 33*I2 = {float(check)} (should be 36)")

sol2 = sp.solve([eq2, constraint1], [I1, I2])
print("\nUsing mesh 2 equation with constraint:")
if sol2:
    print(f"I1 = {float(sol2[I1]):.4f} A (= Io)")
    print(f"I2 = {float(sol2[I2]):.4f} A")
    print(f"P = {float(sol2[I2]**2 * 6):.4f} W")

# Check all answers against this solution
answers = [
    (2.75, 253.5),
    (1, 253.5),
    (2.75, 6),
    (-2.75, 121.5),
    (5.5, 45.375),
    (-1, 45.375),
    (1, 6)
]

if sol2:
    for i, (io, p) in enumerate(answers, 1):
        if abs(float(sol2[I1]) - io) < 0.01 and abs(float(sol2[I2]**2 * 6) - p) < 0.01:
            print(f"\n*** MATCHES ANSWER {i} ***")

print("="*60)
