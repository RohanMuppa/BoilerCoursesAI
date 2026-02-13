import sympy as sp
import itertools

print("="*60)
print("BRUTE FORCE: TRYING DIFFERENT RESISTOR ARRANGEMENTS")
print("="*60)

I1, I2 = sp.symbols('I1 I2', real=True)

# Available resistors: 12, 24, 3, 6
# Voltage: 36V

answers = [
    (2.75, 253.5),
    (1, 253.5),
    (2.75, 6),
    (-2.75, 121.5),
    (5.5, 45.375),
    (-1, 45.375),
    (1, 6)
]

print("Target answers:")
for i, (io, p) in enumerate(answers, 1):
    I_6 = (p / 6) ** 0.5
    print(f"{i}. Io = {io} A, P = {p} W, I_6ohm = {I_6} A")

print("\n" + "="*60)
print("TESTING DIFFERENT RESISTOR COMBINATIONS")
print("="*60)

resistors = [12, 24, 3, 6]

# Try different ways to distribute resistors between meshes
# R1_only: resistors only in mesh 1
# R_shared: shared resistor between meshes
# R2_only: resistors only in mesh 2 (including the 6 ohm)

configurations = []

# Config 1: R1=12, shared=24, R2=3+6
# This is what we've been using
configurations.append(("Config 1", 12, 24, 9, 36))

# Config 2: R1=12+24, shared=0, R2=3+6
configurations.append(("Config 2", 36, 0, 9, 36))

# Config 3: R1=12, shared=24+3, R2=6
configurations.append(("Config 3", 12, 27, 6, 36))

# Config 4: R1=12, shared=3, R2=24+6
configurations.append(("Config 4", 12, 3, 30, 36))

# Config 5: R1=12+3, shared=24, R2=6
configurations.append(("Config 5", 15, 24, 6, 36))

# Config 6: R1=24, shared=12, R2=3+6
configurations.append(("Config 6", 24, 12, 9, 36))

# Config 7: Different voltage sign
configurations.append(("Config 7", 12, 24, 9, -36))

# Try each configuration with dependent source constraints
dependent_constraints = [
    ("I2 = 4*I1", sp.Eq(I2, 4*I1)),
    ("I2 = -2*I1", sp.Eq(I2, -2*I1)),
    ("I2 = 2*I1", sp.Eq(I2, 2*I1)),
    ("I1 = 4*I2", sp.Eq(I1, 4*I2)),
    ("I1 = 2*I2", sp.Eq(I1, 2*I2)),
    ("I1 = -2*I2", sp.Eq(I1, -2*I2)),
    ("I2 = I1/2", sp.Eq(I2, I1/2)),
    ("I1 = I2/2", sp.Eq(I1, I2/2)),
]

match_found = False

for config_name, R1, R_shared, R2, V in configurations:
    if R_shared == 0:
        # No shared resistor means independent meshes
        # This won't work with our circuit
        continue

    # Mesh equations:
    # Mesh 1: (R1 + R_shared)*I1 - R_shared*I2 = 0
    # Mesh 2: -R_shared*I1 + (R_shared + R2)*I2 = V

    a11 = R1 + R_shared
    a12 = -R_shared
    a21 = -R_shared
    a22 = R_shared + R2

    eq1 = sp.Eq(a11*I1 + a12*I2, 0)
    eq2 = sp.Eq(a21*I1 + a22*I2, V)

    for constraint_name, constraint_eq in dependent_constraints:
        try:
            sol = sp.solve([eq2, constraint_eq], [I1, I2])

            if not sol or sol[I1] is sp.nan or sol[I2] is sp.nan:
                continue

            # Try different Io definitions
            io_tests = [
                ("Io = I1", sol[I1]),
                ("Io = I2", sol[I2]),
                ("Io = I1-I2", sol[I1] - sol[I2]),
                ("Io = I2-I1", sol[I2] - sol[I1]),
            ]

            for io_desc, io_val in io_tests:
                P_val = sol[I2]**2 * 6

                for idx, (io_ans, p_ans) in enumerate(answers, 1):
                    if abs(float(io_val) - io_ans) < 0.01 and abs(float(P_val) - p_ans) < 0.01:
                        print(f"\n*** MATCH with answer {idx} ***")
                        print(f"{config_name}: R1={R1}, R_shared={R_shared}, R2={R2}, V={V}")
                        print(f"Constraint: {constraint_name}")
                        print(f"Solution: I1 = {float(sol[I1]):.4f} A, I2 = {float(sol[I2]):.4f} A")
                        print(f"{io_desc}: {float(io_val):.4f} A")
                        print(f"P = {float(P_val):.4f} W")
                        match_found = True
        except:
            pass

if not match_found:
    print("\nNo exact matches found")
    print("\nThis suggests the circuit description may be inaccurate")
    print("or the problem requires a different analysis approach")

print("\n" + "="*60)
print("ALTERNATIVE: What if 6 ohm is NOT the load resistor?")
print("What if the power is in a DIFFERENT resistor?")
print("="*60)

# Maybe power is in the 3 ohm, 12 ohm, or 24 ohm resistor instead?

print("\nChecking if power could be in 3 ohm resistor:")
print("For P = 253.5 W: I = sqrt(253.5/3) = 9.19 A")
print("For P = 45.375 W: I = sqrt(45.375/3) = 3.89 A")

print("\nChecking if power could be in 12 ohm resistor:")
print("For P = 253.5 W: I = sqrt(253.5/12) = 4.59 A")
print("For P = 45.375 W: I = sqrt(45.375/12) = 1.946 A")

print("\nChecking if power could be in 24 ohm resistor:")
for p_target in [253.5, 45.375, 6, 121.5]:
    I_calc = (p_target / 24) ** 0.5
    print(f"P = {p_target} W: I = {I_calc:.4f} A")

print("\n" + "="*60)
