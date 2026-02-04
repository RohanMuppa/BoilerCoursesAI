import sympy as sp

print("="*60)
print("COMPREHENSIVE MESH ANALYSIS")
print("="*60)

I1, I2 = sp.symbols('I1 I2', real=True)

# Test all possible configurations systematically

configs = []

# Configuration 1: Standard mesh with I2 - I1 = 3*I1
print("\n" + "="*60)
print("CONFIG 1: Mesh 1 (12,24), Mesh 2 (3,6,36V)")
print("Constraint: I2 - I1 = 3*I1")
print("="*60)

# Mesh 1: 12*I1 + 24*(I1-I2) = 0
# 36*I1 - 24*I2 = 0
# Mesh 2: -36 + 3*I2 + 6*I2 + 24*(I2-I1) = 0
# -36 + 33*I2 - 24*I1 = 0

eq1 = sp.Eq(36*I1 - 24*I2, 0)
eq2 = sp.Eq(-36 + 33*I2 - 24*I1, 0)
constraint = sp.Eq(I2, 4*I1)

sol = sp.solve([eq2, constraint], [I1, I2])
print(f"Using eq2 and constraint:")
print(f"I1 = {float(sol[I1])} A, I2 = {float(sol[I2])} A")
print(f"Io = {float(sol[I1])} A, P = {float(sol[I2]**2 * 6)} W")
configs.append(("Config 1a", float(sol[I1]), float(sol[I2]**2 * 6)))

sol = sp.solve([eq1, constraint], [I1, I2])
print(f"Using eq1 and constraint:")
print(f"I1 = {float(sol[I1])} A, I2 = {float(sol[I2])} A")
print(f"Io = {float(sol[I1])} A, P = {float(sol[I2]**2 * 6)} W")
configs.append(("Config 1b", float(sol[I1]), float(sol[I2]**2 * 6)))

# Configuration 2: Try opposite sign
print("\n" + "="*60)
print("CONFIG 2: Same but I1 - I2 = 3*I1")
print("="*60)

constraint2 = sp.Eq(I1 - I2, 3*I1)
sol = sp.solve([eq2, constraint2], [I1, I2])
print(f"I1 = {float(sol[I1])} A, I2 = {float(sol[I2])} A")
print(f"Io = {float(sol[I1])} A, P = {float(sol[I2]**2 * 6)} W")
configs.append(("Config 2", float(sol[I1]), float(sol[I2]**2 * 6)))

# Configuration 3: Try Io = I2
print("\n" + "="*60)
print("CONFIG 3: Io = I2, constraint I2 - I1 = 3*I2")
print("="*60)

constraint3 = sp.Eq(I2 - I1, 3*I2)
sol = sp.solve([eq2, constraint3], [I1, I2])
print(f"I1 = {float(sol[I1])} A, I2 = {float(sol[I2])} A")
print(f"Io = {float(sol[I2])} A, P = {float(sol[I2]**2 * 6)} W")
configs.append(("Config 3", float(sol[I2]), float(sol[I2]**2 * 6)))

# Configuration 4: Try Io = I1-I2
print("\n" + "="*60)
print("CONFIG 4: Io = I1-I2, constraint I2-I1 = 3*(I1-I2)")
print("="*60)

constraint4 = sp.Eq(I2 - I1, -3*(I1-I2))
constraint4_simplified = sp.Eq(I2, 2*I1)
sol = sp.solve([eq2, constraint4_simplified], [I1, I2])
print(f"I1 = {float(sol[I1])} A, I2 = {float(sol[I2])} A")
Io4 = sol[I1] - sol[I2]
print(f"Io = I1-I2 = {float(Io4)} A, P = {float(sol[I2]**2 * 6)} W")
configs.append(("Config 4", float(Io4), float(sol[I2]**2 * 6)))

# Configuration 5: Different voltage polarity
print("\n" + "="*60)
print("CONFIG 5: Voltage opposite polarity")
print("="*60)

eq2_alt = sp.Eq(36 + 33*I2 - 24*I1, 0)
constraint_alt = sp.Eq(I2, 4*I1)

sol = sp.solve([eq2_alt, constraint_alt], [I1, I2])
print(f"I1 = {float(sol[I1])} A, I2 = {float(sol[I2])} A")
print(f"Io = {float(sol[I1])} A, P = {float(sol[I2]**2 * 6)} W")
configs.append(("Config 5", float(sol[I1]), float(sol[I2]**2 * 6)))

# Configuration 6: Different resistor arrangement
print("\n" + "="*60)
print("CONFIG 6: Alternative mesh definition")
print("Mesh 2: 3+6+24 = 33 ohm total")
print("="*60)

# What if the 6 ohm shares current with something else?
# -36 + (3+6)*I2 + 24*(I2-I1) = 0
eq2_v6 = sp.Eq(-36 + 9*I2 + 24*I2 - 24*I1, 0)
constraint_v6 = sp.Eq(I2, 4*I1)

sol = sp.solve([eq2_v6, constraint_v6], [I1, I2])
print(f"I1 = {float(sol[I1])} A, I2 = {float(sol[I2])} A")
print(f"Io = {float(sol[I1])} A, P = {float(sol[I2]**2 * 6)} W")
configs.append(("Config 6", float(sol[I1]), float(sol[I2]**2 * 6)))

# Configuration 7: What if 24 is not shared?
print("\n" + "="*60)
print("CONFIG 7: 24 ohm in mesh 1 only, other topology")
print("="*60)

# Mesh 1: (12+24)*I1 = 0 makes no sense
# Try: Mesh 2 has 3, 6, 24 and 36V
eq2_v7 = sp.Eq(-36 + 3*I2 + 6*I2 + 24*I2, 0)
print(f"Pure mesh 2: -36 + 33*I2 = 0, I2 = {36/33} A")
I2_v7 = 36/33
P_v7 = I2_v7**2 * 6
print(f"P = {P_v7} W")

print("\n" + "="*60)
print("CHECKING ALL CONFIGURATIONS")
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

print("\nAnswer choices")
for i, (io, p) in enumerate(answers, 1):
    print(f"{i}. Io = {io} A, P = {p} W")

print("\nAll tested configurations")
for name, io, p in configs:
    print(f"\n{name}: Io = {io:.3f} A, P = {p:.3f} W")
    for i, (io_ans, p_ans) in enumerate(answers, 1):
        if abs(io - io_ans) < 0.01 and abs(p - p_ans) < 0.01:
            print(f"  *** MATCH with Answer {i} ***")

print("="*60)
